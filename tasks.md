# Re-Trace — Tasks and progress

Last reviewed: 29 September 2026. Code baseline: `b1825fa`. This is a status record, not a claim that every deployed journey has been tested. Historical results below come from the development records; no tests were rerun for this documentation-only update.

## Implemented in the repository

- [x] Three separate workflows for drive-image erasure, file/folder batch erasure and advanced contiguous-file recovery.
- [x] Signature scans and structural checks for JPEG, PNG, PDF and ZIP; classification, confidence reasons and artifact hashes.
- [x] Working-copy overwrite verification and a recovery scan that challenges supported residual artifacts.
- [x] Persistent cloud cases, private object storage, hash-linked application events and signed PDF/JSON reporting.
- [x] Cloud domain/account approval, verified-email checks, active-session checks and authenticator MFA enforcement.
- [x] Admin oversight for users, domains, case assignments, cross-case activity, recent jobs and available auth/session records.
- [x] Email-only access requests through the visitor’s email application; separate secure sign-in.
- [x] Consistent charcoal/orange theme, Home navigation, animated access notice and evaluator-oriented landing content.
- [x] Vercel SPA routing configuration and production defaults for the existing cloud backend.

## Verification evidence already recorded

| Evidence | Recorded outcome | What it does not establish |
|---|---|---|
| Local backend suite, 25 September | Nine tests passed | Complete hosted/browser acceptance |
| Cloud engine Node harness | Eight fixture hashes matched; no misses or false positives in that fixture; malformed PNG rejected | General forensic recovery accuracy |
| Rollback-only authorization tests, 26 September | Pending, AAL1, suspended, revoked and domain-denied access blocked; case isolation and RPC grants checked | Every real-account enrollment or recovery path |
| Admin change/audit checks | Transactional change event and valid security chain verified | External immutable anchoring |
| Frontend builds, through 27 September | TypeScript and Vite production builds passed | Responsive visual QA or current Vercel deployment health |
| Live Edge smoke check | Health responded; unauthenticated admin request returned 401 | Full signed-in operation flow |

See [validation history](docs/validation.md), [access policy tests](supabase/tests/access-policy.sql) and [institutional access notes](docs/INSTITUTIONAL-ACCESS.md). Earlier sections of older documents contain historical limitations superseded by their later updates.

## Next: complete release acceptance

- [ ] Run a real two-user cloud journey: admin MFA enrollment, approved organization, operator account setup, individual approval, case assignment, denied unrelated case, suspension and sign-out. Save observations without secrets.
- [ ] Test account setup/invitation, confirmation and password reset against the actual deployment URL and redirect allowlist. Verify the access request works when an email application is configured; plan a fallback for visitors without one.
- [ ] Confirm which commit Vercel serves, then test direct/reloaded `/login`, `/app/admin` and reset routes. Do not infer deployment success from a push.
- [ ] Check mobile layout, keyboard focus, dialog dismissal, contrast and reduced-motion behavior in a browser.
- [ ] Run the complete cloud case demonstration: fixture, recovery, copy erasure, validation, timeline, PDF/JSON download and independent verification.
- [ ] Review Supabase leaked-password protection. It was disabled at the last recorded advisor check; recheck current settings before changing or claiming it is enabled.

## Next: robustness and evidence quality

- [ ] Add durable job execution, cancellation, timeout handling and recovery/cleanup of interrupted jobs. Acceptance: an interrupted operation has an unambiguous outcome and does not silently leave uncontrolled work objects.
- [ ] Expand the corpus with malformed, truncated, overlapping and diverse real-world samples. Publish format-specific measurements and rejected/incomplete cases.
- [ ] Isolate parsers and measure memory/runtime behavior under hostile inputs.
- [ ] Add external audit anchoring, documented key rotation and explicit retention/recovery procedures.
- [ ] Design evaluator-specific, limited-duration account exceptions without approving entire public email domains. Existing public request handling does not grant such exceptions automatically.

## Longer-term research

- [ ] Design and independently test a privileged local device agent for supported physical media.
- [ ] Research fragmented-file reconstruction with labelled fragments and measurable false-assembly rates.
- [ ] Assess passkeys, institutional SSO and identity verification only when there is a concrete deployment need.

Mark work complete only when the behavior exists and its acceptance check has evidence. Keep implementation status separate from deployment and validation status.
