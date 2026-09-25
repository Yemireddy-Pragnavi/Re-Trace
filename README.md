# Re-Trace

**SIH26149 · Integrated Secure Data Erasure + Advanced File Recovery**

A runnable local and cloud SIH prototype with three separate modules, real sandbox processing, persistent cases, role checks, automatic event timelines, hash-chained audits and signed forensic reports.

**Status: functional local and connected cloud sandbox prototype, not a complete implementation of every master-prompt requirement.** It is not a physical-drive eraser or a certified forensic tool. Original uploaded evidence is retained; erase operations affect disposable working copies only.

## Connected cloud version (v0.2)

[Open the private website preview](https://retrace-cloud.vvreddy1584.chatgpt.site)

The Supabase project `noqdtxwvgqkgrkpsbhpi` now has the cloud schema, RLS, private storage, and the deployed `retrace-api` function. See [cloud setup and use](docs/cloud-auth.md). The original Python/SQLite mode remains available.

Cloud features: verified-email Auth with live session checks, isolated cases, real PNG/JPEG/PDF/ZIP carving, Storage working-copy overwrite/read-back/removal, automatic timelines, hash-chained audits, Ed25519-signed reports, and synthetic validation. The cloud limit is 8 MiB per operation batch. Physical-media cleansing, MFA/passkeys and fragmented reconstruction remain out of scope.

Latest delivery and exact demo steps: [DELIVERY-STATUS.md](docs/DELIVERY-STATUS.md).

The public landing is at `/`; sign-in is at `/login`; existing workspaces are under `/app/*`. The fixture now contains **eight** actual artifacts (3 JPEG, 2 PNG, 2 PDF, 1 ZIP).

## Download or clone into VS Code

- [Download ZIP](https://github.com/tevi87637-ship-it/Re-Trace/archive/refs/heads/main.zip), extract it, and open the extracted folder in VS Code.
- Or install Git and run:

```powershell
git clone https://github.com/tevi87637-ship-it/Re-Trace.git
cd Re-Trace
code .
```

The entire application source is included. You do not need ChatGPT to edit or run it.

## Windows quick start

Install **Python 3.12**, **Node.js 22.12+** and VS Code. Open two VS Code terminals in the cloned folder.

**Terminal 1 — API**

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r backend\requirements.txt
Copy-Item backend\.env.example backend\.env
cd backend
..\.venv\Scripts\python.exe -m uvicorn app.main:app --host 127.0.0.1 --port 8000
```

**Terminal 2 — frontend**

```powershell
cd frontend
npm ci
npm run dev
```

Open **http://localhost:5173**. API documentation: **http://127.0.0.1:8000/docs**.

No PowerShell execution-policy change is needed: the commands invoke the virtual environment's Python directly. If PowerShell blocks `npm.ps1`, use `npm.cmd ci` and `npm.cmd run dev`.

Create your account in the UI. In local mode the **first account becomes ADMIN**; subsequent accounts start as VIEWER. The administrator can promote users and assign them to cases in **Identity & Access**. There are no seeded passwords. Keep local mode bound to loopback; it has no email verification, password reset, MFA or passkeys.

## macOS / Linux

```bash
python3.12 -m venv .venv
.venv/bin/python -m pip install -r backend/requirements.txt
cp backend/.env.example backend/.env
cd backend
../.venv/bin/python -m uvicorn app.main:app --host 127.0.0.1 --port 8000
```

In another terminal, `cd frontend`, `npm ci`, then `npm run dev`.

## Demonstrate the three official modules

1. Create a case.
2. **File Carving & Recovery:** generate a demo forensic image, select it, and run recovery. Inspect all four formats, structural evidence, confidence reasons, hashes and offsets. Downloaded evidence is hash-checked.
3. **Secure Drive Eraser:** select the test image, preview the media policy, type `ERASE SANDBOX COPY`, and run erasure. Inspect full read-back verification, source preservation and the post-erasure artifact challenge.
4. **File & Folder Eraser:** upload files or select a folder, select the uploaded targets, preview the policy and confirm. This performs a real batch overwrite, logical read-back, extended-attribute removal where supported, timestamp reset, rename, unlink and absence check on copies.
5. **Validation Lab:** run the reproducible synthetic test suite and view measured duration/throughput and pass/fail checks.
6. **Activity Timeline:** inspect actors, source/job IDs, parameters, UTC timestamps and hashes; filter by action, actor, source/job and dates.
7. **Audit Integrity:** verify the case hash chain; as admin, demonstrate tampering on an in-memory copy.
8. **Forensic Reports:** generate and download PDF plus signed JSON. The JSON includes the PDF hash and the report's audit/timeline snapshot.

## What is implemented

| Required area | Implementation |
|---|---|
| Secure Drive Eraser | Full raw-image working-copy zero overwrite and full read-back |
| Secure File & Folder Eraser | Multi-file/folder upload, batch erasure, limited copy metadata cleansing, rename/unlink verification |
| Advanced carving & recovery | Metadata-independent raw-byte scanning; PNG CRC/chunk validation, JPEG parser/decode, PDF page/xref parsing, ZIP directory/CRC validation |
| Classification and confidence | Image / Document / Archive; explainable 95/100 heuristic for fully validated candidates; invalid candidates reported separately |
| Media support | Raw `.img`, `.raw`, `.dd`, `.bin`, file/folder copies; operator-declared HDD/SSD/NVMe/USB/SD/Optical profiles |
| Verification and validation | Logical read-back, source hash checks, residual scanning and reproducible ground-truth fixture |
| Audit and reporting | Append-only database triggers, per-case SHA-256 chains, Ed25519-signed JSON and PDF hash, authenticated exports |
| GUI and metrics | Responsive dashboard, three module pages, per-operation bytes/duration/MiB/s |
| Enhancements | Policy recommendations, server-enforced roles, 30-minute revocable sessions, activity events and automatically constructed case timeline |

## Explicit limits and unfinished requirements

- **Local mode uses SQLite. Cloud mode uses Supabase PostgreSQL/RLS, Edge Functions and private Storage.** The Python API remains the local implementation; the deployed cloud API is TypeScript/Deno.
- **Supabase Auth** is configured for confirmed email. A real-user email delivery/confirmation walkthrough still needs the account holder. No MFA or passkeys are claimed. See [cloud-auth.md](docs/cloud-auth.md).
- **Passkeys, MFA, ID verification, local email verification and password reset are not implemented.** Never describe local login as biometric or verified identity.
- **Native physical-drive erasure is not implemented.** Media types are selected profiles, not hardware detection. ATA/NVMe sanitize and crypto-erase are recommendations only.
- **Fragmented-file reconstruction is roadmap only.** See [fragmented-reconstruction.md](docs/fragmented-reconstruction.md). PDF extraction currently handles the first EOF/revision; split ZIPs, ZIP64, encrypted files, E01/AFF and filesystem reconstruction are unsupported.
- File metadata cleansing covers the working-copy directory entry, timestamps and available xattrs. It does not cleanse source uploads, audit records, host journals, caches, thumbnails, swap, snapshots, backups or flash remapped cells. Folder hierarchy is flattened into independent safe upload IDs.
- Activity tracking covers this application's operations, not all activity on the user's computer. Session/admin events are shown separately from case events.
- Local jobs run synchronously under a single-process lock; cloud jobs run within Edge Function request limits. The UI shows an indeterminate busy indicator, not a fabricated progress percentage. Interrupted jobs are marked on API restart; automatic resume/cancellation is not implemented.
- Hash chains are tamper-evident, not immutable. A host/database administrator can replace data. External trusted report fingerprints/checkpoints are needed to detect whole-chain replacement or truncation. Local signing keys reside on the host; cloud report keys are stored in a private service-only database table.
- Limits: 32 MiB per source, 256 MiB retained source quota, 256 signature candidates per scan, 1,000 ZIP entries / 32 MiB expansion, bounded image pixels. Repeated recovered outputs and reports still need production retention quotas. Treat untrusted hostile forensic images as requiring isolated worker processes before deployment.
- Standards names are guidance references, not certification or a validated standards-conformance mapping. The supplied requirements are the project baseline; the live official SIH portal wording was not independently retrieved.

See [requirements.md](docs/requirements.md) and [validation.md](docs/validation.md) for acceptance coverage and test results.

## Edit in VS Code

- `frontend/src/main.tsx`: pages, forms and workflows.
- `frontend/src/style.css`: dark navy/cyan design system and responsive layout.
- `frontend/src/api.ts`: authenticated API client and optional cloud auth.
- `backend/app/main.py`: API routes, authorization, operations, reports.
- `backend/app/engines.py`: binary carving, validation, erasure and fixtures.
- `backend/app/store.py`: SQLite schema, persistence and audit chain.
- `backend/app/auth.py`: local credentials, sessions and cloud token exchange.
- `backend/app/reports.py`: PDF creation and Ed25519 report signatures.
- `backend/tests/test_system.py`: meaningful API/engine/security tests.

Select `.venv` as the VS Code Python interpreter. The repository includes an API debugger configuration and frontend tasks. Frontend changes reload automatically; restart the API after backend changes, or add `--reload` during development.

## Test and build

```powershell
cd backend
..\.venv\Scripts\python.exe -m pytest -q
cd ..\frontend
npm run build
```

On Linux use `../.venv/bin/python` instead. CI repeats backend tests and the frontend production build. CI success must be checked on GitHub after upload.

## Verify a report offline

Keep the report signing-key fingerprint somewhere trusted when the report is generated. Do not trust a replacement key shipped with an unknown report.

```powershell
.\.venv\Scripts\python.exe scripts\verify_report.py report.json --trusted-fingerprint YOUR_SAVED_FINGERPRINT --pdf report.pdf
```

## Save your updates to GitHub

```bash
git add .
git commit -m "Describe your changes"
git push origin main
```

`.env`, virtual environments, runtime data, signing keys and build outputs are ignored. Do not commit sensitive forensic evidence or credentials. Runtime files persist in `backend/data/` by default. Back up that directory and the signing key securely if the case records matter.
