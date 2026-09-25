# Re-Trace delivery status — landing and backend update

Preview: https://retrace-cloud.vvreddy1584.chatgpt.site

## Working — executed and verified

- Local backend: nine tests passed. Tests execute authorization, case operations, true file carving/downloads, working-copy overwrite/read-back, batch removal, signed PDF/JSON report verification, safe copied-chain tampering, session revocation, source integrity and cross-case isolation.
- Deterministic fixture: 3 JPEG + 2 PNG + 2 PDF + 1 ZIP. Both engine implementations recovered all eight expected hashes. Ground-truth results: eight matches, zero missed artifacts, zero false positives, 100% recovery on this synthetic fixture.
- Cloud engine source: executed through the Node test harness, including malformed-PNG rejection, candidate limits, zero-buffer artifact checks and PDF creation.
- Supabase schema migration and rollback-only RLS/audit tests passed in the prior cloud setup. Anonymous protected API access was rejected.
- React/TypeScript production build passed. Existing authenticated screens are preserved; landing styles are scoped separately.

## Implemented / partially verified

- Public landing `/`: reference-inspired black/orange hero, connected architecture nodes, alternating rounded light panels, provenance network, timeline explanation, media selector, recovery flow, use cases, standards, capability cards and final glow CTA. The 46.5-second reference was sampled across its duration and every decoded frame was processed for scene changes; this is not a claim of pixel-identical reproduction.
- `/login`, `/app/*`, `/forgot-password`, `/reset-password`: route selection and auth gating are implemented. Active-case selection is retained per user. Email-password reset UI and a protected password-change audit event are implemented.
- Cloud operations, private Storage, signed reports, audit and timeline are deployed. Identity session events are joined into case timelines using actual session IDs and remain labelled as a separate audit-chain scope.
- Browser visual checks at desktop/tablet/mobile and the full signed-in cloud acceptance sequence have NOT been executed. Deno's standalone type-check remained blocked by local npm type resolution; the cloud engine ran under Node and the frontend type-check passed.
- Real confirmation/reset emails have NOT been sent or tested. The Supabase Auth redirect allowlist must contain the live site's `/login` and `/reset-password` URLs (and localhost equivalents for local frontend work). Custom SMTP/delivery has not been configured by this update.
- The live Site remains owner-private. Changing it into a public SIH submission link is a separate sharing change; the public landing is outside app authentication within the Site, not a claim that Site-level access restrictions were removed.

## Local-agent only / not implemented

- Physical ATA/NVMe sanitize, crypto-erase and direct hardware access: local privileged agent roadmap. No physical commands are simulated as successful execution.
- Hosted file erasure is cloud-object working-copy overwrite/read-back/removal. Local filesystem mode implements xattr removal, timestamp reset, rename and unlink. Neither claims to erase retained originals, journals, snapshots, backups or remapped flash cells.
- Passkeys, biometric/ID verification and MFA are not implemented. No raw biometric data is stored.
- Fragmented-file reconstruction, durable background queue/crash recovery, independent certification and production-scale validation are not implemented.

## Exact demo steps

1. Open the preview. Inspect the landing sections and the interactive HDD/SSD/NVMe/USB policy examples.
2. Select **Launch Platform**, register, confirm email, and sign in. New cloud users are investigators limited to their own cases. Administrator access is not assigned to the first public signup.
3. Create a case. In **File Carving & Recovery**, select **Generate demo forensic image**, select the resulting image, and run recovery.
4. Confirm eight artifacts: three JPEG, two PNG, two PDF, one ZIP. Expand confidence reasons, inspect ground-truth metrics, and download an artifact.
5. Generate a recovery report under **Forensic Reports**; download both PDF and signed JSON.
6. In **Secure Drive Eraser**, select the image, preview its policy, enter `ERASE SANDBOX COPY`, and run. Inspect hashes, bytes, duration, read-back and residual challenge.
7. In **File & Folder Eraser**, select file/folder inputs, select uploaded file targets, preview policy and confirm. The original uploads remain preserved.
8. Run **Validation Lab** to execute a fresh measured ground-truth benchmark.
9. Inspect **Activity Timeline** and verify **Audit Integrity**. Administrators can run the copied-chain tamper demonstration. A normal investigator cannot grant themself this role.
10. Generate another report after sanitization. Log out, log in again, and confirm your case and saved results remain.

No result on the marketing page is presented as a live case measurement. The illustrated timeline is labelled; the authenticated timeline uses persisted events.
