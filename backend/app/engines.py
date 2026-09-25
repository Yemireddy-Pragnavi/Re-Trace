"""Bounded, metadata-independent contiguous carving and sandbox sanitization."""
import hashlib
import io
import os
import struct
import time
import zipfile
import zlib
from pathlib import Path
from PIL import Image
from pypdf import PdfReader, PdfWriter

MAX_BYTES = 32 * 1024 * 1024
MAX_CANDIDATES = 256
SIGNATURES = {'png': b'\x89PNG\r\n\x1a\n', 'jpeg': b'\xff\xd8\xff', 'pdf': b'%PDF-', 'zip': b'PK\x03\x04'}
CLASSIFICATION = {'png': 'Image', 'jpeg': 'Image', 'pdf': 'Document', 'zip': 'Archive'}

def sha(data):
    return hashlib.sha256(data).hexdigest()

def parse_end(data, start, kind):
    """Locate boundaries using PNG chunks, JPEG EOI, PDF EOF or ZIP directory."""
    if kind == 'png':
        pos = start + 8
        chunks = 0
        while pos + 12 <= len(data) and chunks < 10000:
            n = int.from_bytes(data[pos:pos+4], 'big')
            end = pos + 12 + n
            if end > len(data) or n > MAX_BYTES:
                raise ValueError('Truncated PNG chunk')
            ctype = data[pos+4:pos+8]
            if zlib.crc32(data[pos+4:pos+8+n]) & 0xffffffff != int.from_bytes(data[pos+8+n:end], 'big'):
                raise ValueError('PNG CRC mismatch')
            if chunks == 0 and ctype != b'IHDR':
                raise ValueError('Missing IHDR')
            pos, chunks = end, chunks + 1
            if ctype == b'IEND':
                return end, 'PNG chunk lengths, CRCs and IEND verified'
    elif kind == 'jpeg':
        end = data.find(b'\xff\xd9', start + 3)
        if end >= 0:
            return end + 2, 'JPEG SOI/EOI boundaries'
    elif kind == 'pdf':
        end = data.find(b'%%EOF', start + 5)
        if end >= 0:
            return end + 5, 'PDF EOF boundary; first revision only'
    elif kind == 'zip':
        end = data.find(b'PK\x05\x06', start + 4)
        if end >= 0 and end + 22 <= len(data):
            comment_size = int.from_bytes(data[end+20:end+22], 'little')
            if end + 22 + comment_size <= len(data):
                return end + 22 + comment_size, 'ZIP end-of-central-directory structure'
    raise ValueError('No complete supported boundary')

def validate_payload(blob, kind):
    if kind in ('png', 'jpeg'):
        with Image.open(io.BytesIO(blob)) as im:
            if im.width * im.height > 20_000_000:
                raise ValueError('Image pixel budget exceeded')
            im.verify()
        with Image.open(io.BytesIO(blob)) as im:
            im.load()
        return 'Image parser and pixel decode succeeded'
    if kind == 'pdf':
        pdf = PdfReader(io.BytesIO(blob), strict=True)
        if pdf.is_encrypted:
            raise ValueError('Encrypted PDF cannot be validated')
        if len(pdf.pages) > 1000:
            raise ValueError('PDF page budget exceeded')
        return 'PDF cross-reference and page tree parsed'
    with zipfile.ZipFile(io.BytesIO(blob)) as archive:
        infos = archive.infolist()
        if len(infos) > 1000 or sum(i.file_size for i in infos) > MAX_BYTES:
            raise ValueError('ZIP expansion budget exceeded')
        if any(i.flag_bits & 1 for i in infos):
            raise ValueError('Encrypted ZIP cannot be validated')
        if archive.testzip() is not None:
            raise ValueError('ZIP CRC failure')
    return 'ZIP directory and member CRCs validated; never extracted'

def carve(data, selected=None):
    if len(data) > MAX_BYTES:
        raise ValueError('Image exceeds 32 MiB limit')
    chosen = selected or list(SIGNATURES)
    if set(chosen) - set(SIGNATURES):
        raise ValueError('Unsupported file type')
    found, rejected, scanned = [], [], 0
    started = time.perf_counter()
    for kind in chosen:
        cursor = 0
        while (start := data.find(SIGNATURES[kind], cursor)) >= 0:
            cursor = start + len(SIGNATURES[kind])
            scanned += 1
            if scanned > MAX_CANDIDATES:
                return {'files': found, 'rejected': rejected, 'complete': False, 'reason': 'Candidate budget exceeded'}
            try:
                end, boundary = parse_end(data, start, kind)
                blob = data[start:end]
                parsed = validate_payload(blob, kind)
                found.append({'type': kind, 'classification': CLASSIFICATION[kind], 'offset': start,
                              'end_offset': end, 'size': len(blob), 'sha256': sha(blob), 'confidence': 95,
                              'reasons': ['Known signature (+25)', boundary + ' (+30)', parsed + ' (+40)'],
                              'confidence_note': 'Heuristic evidence score, not a statistical probability', 'data': blob})
            except Exception as exc:
                rejected.append({'type': kind, 'offset': start, 'reason': str(exc)[:200]})
    return {'files': sorted(found, key=lambda f: f['offset']), 'rejected': rejected, 'complete': True,
            'duration_seconds': time.perf_counter() - started}

def sanitize(path: Path, unlink=False):
    """Only called with backend-generated paths within a job directory."""
    start = time.perf_counter()
    size = path.stat().st_size
    before = sha(path.read_bytes())
    removed_xattrs = []
    if hasattr(os, 'listxattr'):
        for key in os.listxattr(path):
            os.removexattr(path, key)
            removed_xattrs.append(key)
    with path.open('r+b') as stream:
        remaining = size
        while remaining:
            count = min(1024 * 1024, remaining)
            stream.write(b'\0' * count)
            remaining -= count
        stream.flush()
        os.fsync(stream.fileno())
    after = path.read_bytes()
    verified = len(after) == size and not any(after)
    after_hash = sha(after)
    challenge = carve(after)
    validation = 'WARNING' if challenge['files'] else ('PASS' if challenge['complete'] else 'INCONCLUSIVE')
    os.utime(path, (0, 0))
    if unlink:
        renamed = path.with_name('cleansed-' + os.urandom(8).hex())
        path.rename(renamed)
        renamed.unlink()
        absence = not path.exists() and not renamed.exists()
    else:
        absence = None
    elapsed = time.perf_counter() - start
    return {'before_sha256': before, 'after_sha256': after_hash, 'bytes_processed': size,
            'duration_seconds': elapsed, 'throughput_mib_s': size / 1048576 / max(elapsed, 1e-9),
            'readback_verified': verified, 'absence_verified': absence, 'validation': validation,
            'residual_artifacts': len(challenge['files']), 'metadata': {'extended_attributes_removed': removed_xattrs,
            'timestamps_reset': True, 'work_copy_name_removed': bool(unlink),
            'scope': 'Sandbox working copy only; source evidence, audit metadata, host journals, snapshots and SSD remapped cells are not cleansed'},
            'method': 'Single zero overwrite with full logical read-back',
            'assurance': 'Logical sandbox verification only; not physical-media sanitization certification'}

def fixture():
    """Generate genuine small files embedded without a filesystem in a raw image."""
    payloads = []
    for kind in ('PNG', 'JPEG'):
        stream = io.BytesIO()
        Image.new('RGB', (24, 24), (36, 170, 190)).save(stream, format=kind)
        payloads.append(stream.getvalue())
    pdf = io.BytesIO()
    writer = PdfWriter()
    writer.add_blank_page(width=200, height=200)
    writer.write(pdf)
    payloads.append(pdf.getvalue().rstrip())
    archive = io.BytesIO()
    with zipfile.ZipFile(archive, 'w', zipfile.ZIP_DEFLATED) as z:
        z.writestr('evidence.txt', 'Re-Trace reproducible forensic test fixture')
    payloads.append(archive.getvalue())
    image = b'RETRACE TEST IMAGE\0' + b'\0' * 4096
    for blob in payloads:
        image += blob + b'\0' * 4096
    return image, payloads
