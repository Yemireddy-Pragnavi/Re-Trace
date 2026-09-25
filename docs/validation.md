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
