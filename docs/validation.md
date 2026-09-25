# Validation record

Executed in the development environment on 2026-09-25. These are observed results, not independent certification.

| Check | Result |
|---|---|
| Backend `python -m pytest -q` | 8 passed in 0.67 seconds |
| Genuine PNG/JPEG/PDF/ZIP recovery | All four output hashes matched generated source-file hashes |
| Malformed/truncated candidate handling | Corrupted PNG rejected; incomplete PDF not reported recovered; candidate budget enforced |
| API authorization | Unauthenticated access denied; unassigned case access denied; viewer writes denied |
| Cross-case source injection | Rejected |
| Erasure | Sandbox read-back zero check, original-source preservation and batch unlink verified |
| Audit | Primary chain valid; altered copy detected; ordinary database updates blocked |
| Reports | Ed25519 signature valid; PDF hash matched; modified payload rejected |
| Session lifecycle | Logout and role changes revoke affected local sessions |
| Frontend | TypeScript check and Vite production build passed |
| npm dependency audit | Vite updated from 7.1.7 to 7.3.6 to resolve reported advisories; final audit: 0 vulnerabilities |
| Browser workflow / visual QA | Not completed: Playwright browser binary download returned an invalid archive in this environment |
| Live Supabase | Not configured or tested |
| Physical hardware / fragmented reconstruction | Not implemented or tested |

The test run emitted one upstream Starlette TestClient deprecation warning about its httpx transport. There were no backend test failures.

## Reproduce and extend

Run the commands in the README. Tests generate their own temporary data directory and never modify your normal `backend/data` cases. The in-app Validation Lab runs a real generated-fixture benchmark on your machine and saves the result to the current case.

The synthetic fixture has four contiguous supported files. It is not a representative forensic corpus and does not support general recovery-accuracy, scalability or physical-erasure claims. Browser testing, parser isolation and independent corpus validation remain required before a public-facing deployment.

## Cloud update

- Applied the cloud schema migration to the specified Supabase project.
- Ran rollback-only SQL assertions: another user cannot read an owned case; the owner can read it; authenticated clients cannot insert job results; audit append and verification work. Temporary test rows were rolled back.
- Checked that authenticated clients cannot call the trusted audit append RPC and anonymous clients cannot read report signing keys.
- Deployed the Edge Function; `/health` returned HTTP 200 with cloud mode, and unauthenticated `/cases` returned HTTP 401.
- Tested the actual cloud engine source through the Node harness: all four ground-truth hashes matched, sources remained unchanged, corrupted PNG was rejected, the candidate limit worked, zeroed bytes contained no supported artifacts, and PDF generation succeeded.
- Frontend cloud-mode TypeScript/build passed.
- No real-user confirmation email was sent. Signed-in hosted end-to-end/browser verification remains pending.

## Latest eight-artifact update
Nine local backend tests passed in 0.69 seconds. The actual cloud engine source passed its Node harness with eight matched hashes, 0 misses, 0 false positives, deterministic image generation, corrupt-PNG rejection and valid PDF output. Full cloud browser acceptance remains unverified. See DELIVERY-STATUS.md.
