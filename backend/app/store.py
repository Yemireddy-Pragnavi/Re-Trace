import json
import os
import sqlite3
from contextlib import contextmanager
from datetime import datetime, timezone
from pathlib import Path
from uuid import uuid4
from .engines import sha

ROOT = Path(os.getenv('RETRACE_DATA_DIR', str(Path(__file__).resolve().parents[1] / 'data'))).resolve()
ROOT.mkdir(parents=True, exist_ok=True)
DB = ROOT / 'retrace.db'

def now():
    return datetime.now(timezone.utc).isoformat()

def uid():
    return str(uuid4())

def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(',', ':'), ensure_ascii=True)

@contextmanager
def connection():
    db = sqlite3.connect(DB, timeout=30)
    db.row_factory = sqlite3.Row
    db.execute('PRAGMA foreign_keys=ON')
    try:
        yield db
        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()

def initialize():
    with connection() as db:
        db.executescript('''
        PRAGMA journal_mode=WAL;
        CREATE TABLE IF NOT EXISTS users(id TEXT PRIMARY KEY,email TEXT UNIQUE NOT NULL,password TEXT NOT NULL,role TEXT NOT NULL CHECK(role IN ('ADMIN','INVESTIGATOR','VIEWER')),created TEXT NOT NULL);
        CREATE TABLE IF NOT EXISTS sessions(id TEXT PRIMARY KEY,user_id TEXT NOT NULL REFERENCES users(id),token_hash TEXT UNIQUE NOT NULL,expires REAL NOT NULL,created TEXT NOT NULL,revoked INTEGER NOT NULL DEFAULT 0);
        CREATE TABLE IF NOT EXISTS cases(id TEXT PRIMARY KEY,title TEXT NOT NULL,description TEXT NOT NULL,owner TEXT NOT NULL REFERENCES users(id),created TEXT NOT NULL);
        CREATE TABLE IF NOT EXISTS members(case_id TEXT REFERENCES cases(id),user_id TEXT REFERENCES users(id),PRIMARY KEY(case_id,user_id));
        CREATE TABLE IF NOT EXISTS sources(id TEXT PRIMARY KEY,case_id TEXT NOT NULL REFERENCES cases(id),name TEXT NOT NULL,media TEXT NOT NULL,kind TEXT NOT NULL,size INTEGER NOT NULL,hash TEXT NOT NULL,created TEXT NOT NULL);
        CREATE TABLE IF NOT EXISTS jobs(id TEXT PRIMARY KEY,case_id TEXT NOT NULL REFERENCES cases(id),module TEXT NOT NULL,status TEXT NOT NULL,created TEXT NOT NULL,result TEXT NOT NULL);
        CREATE TABLE IF NOT EXISTS evidence(id TEXT PRIMARY KEY,case_id TEXT NOT NULL REFERENCES cases(id),job_id TEXT NOT NULL REFERENCES jobs(id),details TEXT NOT NULL);
        CREATE TABLE IF NOT EXISTS events(seq INTEGER PRIMARY KEY AUTOINCREMENT,id TEXT UNIQUE NOT NULL,case_id TEXT,body TEXT NOT NULL,previous_hash TEXT NOT NULL,hash TEXT NOT NULL);
        CREATE TABLE IF NOT EXISTS reports(id TEXT PRIMARY KEY,case_id TEXT NOT NULL REFERENCES cases(id),created TEXT NOT NULL,envelope TEXT NOT NULL,pdf_hash TEXT NOT NULL);
        CREATE INDEX IF NOT EXISTS event_case ON events(case_id,seq);
        CREATE INDEX IF NOT EXISTS source_case ON sources(case_id);
        CREATE TRIGGER IF NOT EXISTS event_no_update BEFORE UPDATE ON events BEGIN SELECT RAISE(ABORT,'Audit events are append-only'); END;
        CREATE TRIGGER IF NOT EXISTS event_no_delete BEFORE DELETE ON events BEGIN SELECT RAISE(ABORT,'Audit events are append-only'); END;
        PRAGMA user_version=1;
        ''')
        db.execute("UPDATE jobs SET status='INTERRUPTED' WHERE status='RUNNING'")

def record(actor, action, case_id=None, details=None):
    body = {'id': uid(), 'case_id': case_id, 'user_id': actor['id'], 'user': actor['email'],
            'role': actor['role'], 'session_id': actor.get('session_id'), 'action': action,
            'timestamp': now(), 'details': details or {}}
    with connection() as db:
        db.execute('BEGIN IMMEDIATE')
        prior = db.execute('SELECT hash FROM events WHERE case_id IS ? ORDER BY seq DESC LIMIT 1', (case_id,)).fetchone()
        previous = prior['hash'] if prior else '0' * 64
        digest = sha((previous + canonical(body)).encode())
        db.execute('INSERT INTO events(id,case_id,body,previous_hash,hash) VALUES(?,?,?,?,?)', (body['id'], case_id, canonical(body), previous, digest))
    return body

def events(case_id):
    with connection() as db:
        return [{**json.loads(r['body']), 'sequence': r['seq'], 'previous_hash': r['previous_hash'], 'hash': r['hash']}
                for r in db.execute('SELECT * FROM events WHERE case_id IS ? ORDER BY seq', (case_id,))]

def verify(rows):
    previous = '0' * 64
    for row in rows:
        body = {k: v for k, v in row.items() if k not in ('sequence', 'previous_hash', 'hash')}
        if row['previous_hash'] != previous or sha((previous + canonical(body)).encode()) != row['hash']:
            return {'status': 'BROKEN', 'first_invalid_event': row['id'], 'checked': len(rows)}
        previous = row['hash']
    return {'status': 'VALID', 'checked': len(rows), 'head': previous,
            'scope': 'Internal chain consistency; use an externally saved signed report to detect rollback or truncation'}


def case_timeline(case_id):
    rows = events(case_id)
    sessions = {r.get('session_id') for r in rows if r.get('session_id')}
    identity = [dict(r, chain_scope='identity') for r in events(None)
                if r.get('session_id') in sessions and r['action'] in ('SESSION_STARTED','SESSION_ENDED','ALL_SESSIONS_REVOKED')]
    return sorted([dict(r, chain_scope='case') for r in rows] + identity, key=lambda r: (r['timestamp'], r['sequence']))
