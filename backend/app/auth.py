import hashlib
import hmac
import os
import secrets
import time
from collections import defaultdict, deque
from threading import Lock
import httpx
from fastapi import Depends, HTTPException, Request
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from pydantic import BaseModel, Field
from . import store

bearer = HTTPBearer(auto_error=False)
limits = defaultdict(deque)
limit_lock = Lock()
AUTH_MODE = os.getenv('AUTH_MODE', 'local')

def password_hash(password, salt=None):
    salt = salt or secrets.token_hex(16)
    digest = hashlib.scrypt(password.encode(), salt=bytes.fromhex(salt), n=16384, r=8, p=1).hex()
    return salt + ':' + digest

def check_password(password, encoded):
    if ':' not in encoded:
        password_hash(password, '0' * 32)
        return False
    return hmac.compare_digest(password_hash(password, encoded.split(':')[0]), encoded)

class Credentials(BaseModel):
    email: str = Field(min_length=3, max_length=254, pattern=r'^[^\s@]+@[^\s@]+\.[^\s@]+$')
    password: str = Field(min_length=12, max_length=128)

def throttle(request):
    key = request.client.host if request.client else 'unknown'
    stamp = time.time()
    with limit_lock:
        bucket = limits[key]
        while bucket and bucket[0] < stamp - 60:
            bucket.popleft()
        if len(bucket) >= 10:
            raise HTTPException(429, 'Too many authentication attempts. Wait one minute.')
        bucket.append(stamp)

def authenticate(credentials: HTTPAuthorizationCredentials = Depends(bearer)):
    if not credentials:
        raise HTTPException(401, 'Sign in required')
    digest = hashlib.sha256(credentials.credentials.encode()).hexdigest()
    with store.connection() as db:
        row = db.execute('SELECT users.*,sessions.id AS session_id FROM sessions JOIN users ON users.id=sessions.user_id WHERE token_hash=? AND expires>? AND revoked=0', (digest, time.time())).fetchone()
    if not row:
        raise HTTPException(401, 'Session expired or revoked')
    return dict(row)

def session(user, method):
    token = secrets.token_urlsafe(48)
    sid = store.uid()
    with store.connection() as db:
        db.execute('INSERT INTO sessions(id,user_id,token_hash,expires,created) VALUES(?,?,?,?,?)', (sid,user['id'],hashlib.sha256(token.encode()).hexdigest(),time.time()+1800,store.now()))
    actor = {**user, 'session_id': sid}
    store.record(actor, 'SESSION_STARTED', details={'method':method})
    return {'token': token, 'expires_in': 1800, 'user': {k:actor[k] for k in ('id','email','role','session_id')}}

def signup(data, request):
    throttle(request)
    if AUTH_MODE != 'local':
        raise HTTPException(409, 'Use configured Supabase registration')
    email = data.email.strip().lower()
    with store.connection() as db:
        db.execute('BEGIN IMMEDIATE')
        if db.execute('SELECT 1 FROM users WHERE email=?',(email,)).fetchone():
            raise HTTPException(409,'Account unavailable')
        # Explicit local-only first-run bootstrap; cloud accounts always start VIEWER.
        role = 'ADMIN' if not db.execute('SELECT 1 FROM users').fetchone() else 'VIEWER'
        user = {'id':store.uid(),'email':email,'password':password_hash(data.password),'role':role,'created':store.now()}
        db.execute('INSERT INTO users VALUES(:id,:email,:password,:role,:created)',user)
    store.record(user, 'ACCOUNT_CREATED', details={'mode':'local','email_verified':False})
    return session(user, 'Local password (email not verified)')

def login(data, request):
    throttle(request)
    if AUTH_MODE != 'local':
        raise HTTPException(409, 'Use configured Supabase authentication')
    with store.connection() as db:
        row = db.execute('SELECT * FROM users WHERE email=?',(data.email.strip().lower(),)).fetchone()
    if not check_password(data.password, row['password'] if row else ''):
        raise HTTPException(401,'Invalid credentials')
    return session(dict(row), 'Local password')

class CloudToken(BaseModel):
    access_token: str = Field(min_length=20, max_length=10000)

def cloud_exchange(data, request):
    throttle(request)
    if AUTH_MODE != 'supabase':
        raise HTTPException(409,'Cloud authentication not configured')
    url = os.environ.get('SUPABASE_URL','').rstrip('/')
    key = os.environ.get('SUPABASE_PUBLISHABLE_KEY','')
    if not url.startswith('https://') or not key:
        raise HTTPException(503,'Supabase configuration missing')
    try:
        response = httpx.get(url+'/auth/v1/user',headers={'apikey':key,'Authorization':'Bearer '+data.access_token},timeout=10)
        response.raise_for_status()
        verified = response.json()
    except Exception:
        raise HTTPException(401,'Supabase could not verify the supplied token')
    if not verified.get('email_confirmed_at'):
        raise HTTPException(403,'Verify your email first')
    email = verified['email'].lower()
    identity = 'supabase:' + verified['id']
    with store.connection() as db:
        # Never link cloud identities to local accounts based only on email.
        row = db.execute('SELECT * FROM users WHERE id=?',(identity,)).fetchone()
        if not row:
            if db.execute('SELECT 1 FROM users WHERE email=?',(email,)).fetchone():
                raise HTTPException(409,'Use a separate data directory for cloud authentication')
            db.execute('INSERT INTO users VALUES(?,?,?,?,?)',(identity,email,'external','VIEWER',store.now()))
            row = db.execute('SELECT * FROM users WHERE id=?',(identity,)).fetchone()
    return session(dict(row), 'Supabase verified email session')
