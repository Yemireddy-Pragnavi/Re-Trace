# Connected Supabase cloud mode

Preview: https://retrace-cloud.vvreddy1584.chatgpt.site (private to the owning ChatGPT account)

The supplied project is connected:
- Project: `noqdtxwvgqkgrkpsbhpi` (Re-Trace)
- URL: `https://noqdtxwvgqkgrkpsbhpi.supabase.co`
- Cloud API: `/functions/v1/retrace-api`
- Migration: `supabase/migrations/20260925140136_retrace_cloud_schema.sql`

The supplied `NEXT_PUBLIC_*` values were mapped to Vite's `VITE_*` variables. This application uses React/Vite, not Next.js. Only the publishable key is embedded in the frontend. The service key is supplied by Supabase to the Edge Function and is never sent to the browser or committed.

## Run the cloud-connected frontend in VS Code

```powershell
cd frontend
Copy-Item .env.example .env
npm ci
npm run dev
```

You do not need the local Python API when `VITE_RUNTIME=cloud`. To use the original local Python/SQLite version, remove `frontend/.env` or set `VITE_RUNTIME=local`, and follow the main README's two-terminal setup.

## First use

1. Create your account with your email and a password of at least 12 characters.
2. Confirm the Supabase verification email, then return to the Re-Trace preview and sign in. If the confirmation redirects to an unconfigured localhost page, return manually after confirmation; the project's Auth URL Configuration must list the desired live/local redirect URLs for automatic redirects.
3. New cloud accounts have INVESTIGATOR access to their own cases. They cannot view another user's cases or grant themselves administrator privileges.
4. Create a case, open File Carving & Recovery, generate the demo forensic image, select it and run recovery.
5. Inspect four artifacts, classification, confidence reasons, offsets and hashes. Download an artifact.
6. Open Secure Drive Eraser, select the image, preview the policy and type `ERASE SANDBOX COPY`. Run erasure and inspect read-back and residual-scan results.
7. For File & Folder Eraser, upload/select file targets. The cloud version removes only the temporary working object's content and entry; originals, provider backups and filesystem traces are not claimed erased.
8. Run Validation Lab, inspect the automatic timeline, verify Audit Integrity, then generate/download PDF and signed JSON reports.

Only existing database administrators can assign ADMIN, using the Supabase SQL editor or a trusted management tool. Do not choose an administrator by first public signup. No administrator email has been guessed or promoted.

## Database and security

Public tables: `profiles`, `cases`, `case_members`, `evidence_sources`, `jobs`, `recovered_files`, `audit_events`, `reports`. PostgreSQL RLS is enabled on all eight. Sessions and credentials are managed by Supabase Auth. Policies, verification outputs and performance metrics live with the relevant job; timelines are derived from audit events.

Buckets: `retrace-evidence`, `retrace-reports`, both private. The authorized Edge Function handles uploads/downloads and verifies hashes. Ordinary clients have SELECT access only to permitted database records; processing writes and trusted audit events are server-side.

`retrace_private.signing_keys` is service-only. Its RLS/no-public-policy advisory is intentional deny-by-default; authenticated/anonymous roles cannot read it or invoke key RPCs. Report signatures are tamper-evident, not independent certification; preserve an external key fingerprint and report checkpoint.

Every protected cloud API request validates the user with Supabase Auth and checks that its `session_id` still exists in `auth.sessions`. Roles are read from the server-managed profile. The Edge gateway JWT flag is disabled because validation happens explicitly in the handler, including with modern Supabase publishable keys. There is no unprotected processing endpoint.

## Cloud limits

8 MiB source/batch, 10 selected sources, 64 MiB retained source data per case, 128 carving candidates, 4-megapixel decoded image cap, 200 ZIP members / 8 MiB expanded ZIP data. PDF carving supports the first EOF/revision. Operations run synchronously under Edge Function execution limits. Interrupted requests can leave RUNNING records that need operational reconciliation; no durable queue or crash recovery is claimed. Reports/recovered outputs need further production quota/retention controls.

The original local version supports a larger 32 MiB source limit. Cloud erasure is an object-storage working-copy overwrite/read-back/removal, not the local filesystem xattr/timestamp/rename workflow.

## Validate or update

```powershell
npm ci --prefix supabase
npm run test:engines --prefix supabase
```

Function source is in `supabase/functions/retrace-api/`. Deployment uses Supabase's connected management tooling or the CLI after you authenticate and link this project. Never run the initial CREATE TABLE migration again manually on the existing database; it is already applied. Use a new migration for later changes.

Supabase email confirmation is enabled. No SMTP credentials were supplied or modified. Real-user email delivery and the full signed-in hosted workflow remain to be confirmed by the account holder.
