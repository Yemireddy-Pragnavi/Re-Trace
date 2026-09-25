"""Local operator CLI. No credentials are committed or printed."""
import argparse
from pathlib import Path
from dotenv import load_dotenv
load_dotenv(Path(__file__).parent / '.env')
from app import store
parser=argparse.ArgumentParser()
parser.add_argument('command',choices=['promote'])
parser.add_argument('email')
args=parser.parse_args()
store.initialize()
with store.connection() as db:
    row=db.execute('SELECT * FROM users WHERE email=?',(args.email.lower(),)).fetchone()
    if not row:
        parser.error('User must sign in once before promotion')
    db.execute("UPDATE users SET role='ADMIN' WHERE id=?",(row['id'],))
    db.execute('UPDATE sessions SET revoked=1 WHERE user_id=?',(row['id'],))
store.record({'id':'local-operator','email':'local-cli','role':'ADMIN'},'CLI_ADMIN_PROMOTION',details={'user_id':row['id']})
print('Admin role assigned. Sign in again.')
