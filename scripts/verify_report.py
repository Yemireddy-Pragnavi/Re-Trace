"""Verify a report against an independently trusted signing-key fingerprint."""
import argparse
import base64
import hashlib
import json
from pathlib import Path
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey
parser=argparse.ArgumentParser()
parser.add_argument('json_report',type=Path)
parser.add_argument('--trusted-fingerprint',required=True)
parser.add_argument('--pdf',type=Path)
args=parser.parse_args()
envelope=json.loads(args.json_report.read_text())
key=base64.b64decode(envelope['public_key'],validate=True)
if hashlib.sha256(key).hexdigest()!=args.trusted_fingerprint:
    raise SystemExit('FAIL: public key does not match trusted fingerprint')
payload=json.dumps(envelope['payload'],sort_keys=True,separators=(',',':'),ensure_ascii=True).encode()
try:
    Ed25519PublicKey.from_public_bytes(key).verify(base64.b64decode(envelope['signature'],validate=True),payload)
except Exception:
    raise SystemExit('FAIL: signature invalid')
if args.pdf and hashlib.sha256(args.pdf.read_bytes()).hexdigest()!=envelope['payload']['pdf_sha256']:
    raise SystemExit('FAIL: PDF hash mismatch')
print('PASS: trusted signature verified'+(' and PDF hash matched' if args.pdf else ''))
