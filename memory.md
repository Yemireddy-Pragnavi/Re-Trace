# Re-Trace — Project context

This file preserves durable decisions for the next developer or AI assistant. It is project context, not permission to perform unrelated account, data or deployment changes.

Last reviewed on 29 September 2026 against GitHub commit `b1825fa`. Read current source and [tasks.md](tasks.md) before assuming a historical result is still current.

## The story we are building

Re-Trace explores a practical question: after recovering evidence or sanitizing a working copy, can we explain exactly what happened and support the result with records? The prototype connects raw-file processing with case authorization, integrity checks, automatic timelines and signed reports.

The strongest demonstration is a complete case, not a collection of dashboard screenshots. Start with a deterministic image, inspect the recovered artifacts, sanitize a disposable copy, challenge the result with recovery, and export the record.

## Decisions to preserve

- The original repository URL, `tevi87637-ship-it/Re-Trace`, now resolves through GitHub to `Yemireddy-Pragnavi/Re-Trace`, with the same latest project commit verified on 29 September 2026. Use this existing repository; do not create a separate project copy or assume an older proposed destination is current.
- Keep the existing configured Supabase project. Do not reset or replace it to solve a frontend issue.
- Keep the existing authorized cloud administrator, with its specifically authorized account exception. That does not approve other accounts from the same email provider. Never infer an administrator change from a UI contact edit.
- The three core modules remain distinct. The official brief takes priority over enhancements, even though competition labels have been removed from the product UI.
- Preserve the charcoal/orange palette, accessible motion, clear Home navigation and professional access notice.
- Access requests ask only for email and use a mailto handoff. The user must press Send in their email app. The admin address is not printed in the popup; email recipients are naturally visible in the composed message.
- Sign-in still requires the configured approval checks and MFA. Requests do not create or approve accounts automatically.
- Sanitization affects disposable copies. Uploaded originals are retained. Fragment reconstruction and native hardware erasure remain future work.

## Deployment context

The currently deployed Vercel commit has not been verified in this documentation task. The older Sites preview was owner-private; do not assume it is a public evaluator link or that it tracks later GitHub commits.

Vercel’s project root should be `frontend`. Production builds use cloud defaults unless explicitly overridden. An older cyan “Local development workspace” screen indicated outdated source and/or local-mode configuration. Fix the source/environment/build selection rather than removing security checks.

## Communicate results accurately

Use “implemented,” “tested,” “deployed” and “independently validated” carefully. The repository contains functioning sandbox engines and access controls, but full cloud browser acceptance remains an open task. Confidence values are explained heuristics. The eight-artifact synthetic fixture is useful regression evidence, not a real-world accuracy study.

Do not claim government adoption, certification, biometric verification, AI-based recovery or physical irrecoverability. Keep secrets and real case material out of prompts and public documentation.

## Evaluator-ready description

“Re-Trace combines controlled data erasure and raw-image recovery in a case-based workspace. Each operation is linked to an authorized operator, checked for integrity and added to a timeline that can be exported in a signed report. The prototype demonstrates these workflows on files and image copies, with physical-device support and fragmented reconstruction identified as future work.”

## Resume-ready wording

Use only the bullets that describe your own contribution. For shared work, say “contributed to” or identify the component you owned; do not imply sole authorship of the entire system.

- Built a React/TypeScript forensic workspace with separate erasure and recovery modules, backed by Supabase case storage, role-based access and administrator oversight.
- Implemented signature scanning and structural validation for JPEG, PNG, PDF and ZIP artifacts, with source-integrity checks, classification and explainable confidence scores.
- Connected verified-email authentication, account/domain approval and authenticator MFA to API authorization and database row-level security.
- Developed hash-linked case timelines and Ed25519-signed report envelopes that include PDF hashes for independent integrity verification.
- Validated the recovery workflow against an eight-artifact synthetic image, matching all expected hashes in the recorded test run; report this as fixture coverage, not universal recovery accuracy.

For an interview, explain a trade-off: keeping uploaded originals intact makes the prototype safer to demonstrate, while limiting what its erasure result can claim. Another is the difference between having a valid login session and being authorized to read a specific case.

## Reading order and source of truth

Start with [prd.md](prd.md), then [architecture.md](architecture.md), [rules.md](rules.md), [design.md](design.md) and [tasks.md](tasks.md). Use the source and newest scoped evidence to resolve discrepancies in older notes. Update this file when a lasting product decision changes; do not turn it into an unfiltered transcript.
