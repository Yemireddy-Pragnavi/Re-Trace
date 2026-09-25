import base64
import io
import json
from xml.sax.saxutils import escape
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
from cryptography.hazmat.primitives import serialization
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from . import store
from .engines import sha

def signing_key():
    path = store.ROOT / 'report-signing-key.pem'
    if not path.exists():
        key = Ed25519PrivateKey.generate()
        blob = key.private_bytes(serialization.Encoding.PEM,serialization.PrivateFormat.PKCS8,serialization.NoEncryption())
        try:
            with path.open('xb') as stream:
                stream.write(blob)
            path.chmod(0o600)
        except FileExistsError:
            pass
    return serialization.load_pem_private_key(path.read_bytes(),password=None)

def sign(payload):
    key = signing_key()
    public = key.public_key().public_bytes(serialization.Encoding.Raw,serialization.PublicFormat.Raw)
    message = store.canonical(payload).encode()
    return {'payload':payload,'algorithm':'Ed25519','signature':base64.b64encode(key.sign(message)).decode(),
            'public_key':base64.b64encode(public).decode(),'key_fingerprint':sha(public)}

def verify_envelope(envelope):
    from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey
    Ed25519PublicKey.from_public_bytes(base64.b64decode(envelope['public_key'],validate=True)).verify(
        base64.b64decode(envelope['signature'],validate=True),store.canonical(envelope['payload']).encode())
    return True

def pdf(payload):
    output = io.BytesIO()
    styles = getSampleStyleSheet()
    styles['Title'].textColor = colors.HexColor('#12485c')
    story = [Paragraph('Re-Trace | Forensic & Sanitization Report',styles['Title']),Spacer(1,16)]
    for label in ('id','case','operator','created','scope','audit'):
        story.append(Paragraph(escape(label.upper()+': '+str(payload[label])),styles['BodyText']))
        story.append(Spacer(1,8))
    for label in ('sources','jobs','evidence','timeline'):
        story.append(Paragraph(label.title(),styles['Heading2']))
        for item in payload[label]:
            # Escape user-supplied titles and filenames before ReportLab's XML parser.
            text = json.dumps(item,ensure_ascii=True)
            story.append(Paragraph(escape(text),styles['BodyText']))
            story.append(Spacer(1,8))
    SimpleDocTemplate(output,title='Re-Trace evidence report').build(story)
    return output.getvalue()
