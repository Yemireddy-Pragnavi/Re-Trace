# Optional Supabase Auth integration

This path is included for later configuration; no Supabase project was created or modified and no live cloud-auth test was performed. App persistence remains SQLite/private local files. No Supabase database/RLS/storage integration is claimed.

1. Use a separate private data directory for cloud mode. Existing local accounts are never automatically linked to Supabase accounts by email.
2. Configure a Supabase project with confirmed email required, appropriate site/redirect URLs, production SMTP and your organization's account policies.
3. Set `AUTH_MODE=supabase`, `SUPABASE_URL` and `SUPABASE_PUBLISHABLE_KEY` in `backend/.env`.
4. Set the matching `VITE_SUPABASE_URL` and `VITE_SUPABASE_PUBLISHABLE_KEY` in `frontend/.env`. Never put a service-role/secret key in frontend variables.
5. Restart the backend and frontend. Register, confirm email, then log in.
6. The API validates the cloud access token against `/auth/v1/user` and requires `email_confirmed_at`. It does not trust client role values or user metadata. New cloud accounts are local VIEWERs.
7. From a trusted local shell in `backend`, run `../.venv/bin/python manage.py promote investigator@example.com` (Windows: `..\.venv\Scripts\python.exe manage.py promote investigator@example.com`). Sign in again.

The cloud token is exchanged for a 30-minute opaque local application session. The frontend signs out of its transient Supabase session after exchange. Local revocation endpoints revoke application sessions immediately; upstream Supabase revocation does not automatically revoke an already-issued local session. Strict upstream session checks, MFA, passkeys, password-reset UI and lifecycle integration remain future work.

Primary implementation references:
- https://supabase.com/docs/guides/auth/passwords
- https://supabase.com/docs/reference/javascript/auth-signinwithpassword
- https://supabase.com/docs/reference/javascript/auth-getuser

The changelog was checked during implementation. This integration targets hosted Supabase, not the changed self-hosted gateway configuration.
