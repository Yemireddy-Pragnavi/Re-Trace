# Re-Trace — Product requirements

Re-Trace brings two opposing responsibilities into one accountable workflow: removing sensitive information and recovering evidence that needs to be preserved. The value is in the record around each operation—who performed it, which source was used, how the result was checked, and what the result can actually prove.

This document describes the repository as reviewed on 29 September 2026, against commit `b1825fa`. It is a working software prototype, not a certified physical-media sanitization product. The requirements below come from the project brief; they are not a fresh independent verification of the competition portal.

## Who it is for

An investigator needs to recover supported artifacts from a raw image without relying on filesystem metadata. An authorized operator needs to sanitize a controlled working copy and inspect verification results. An administrator needs to approve access, assign cases and review activity across the project. An evaluator needs a short, repeatable demonstration with visible evidence behind each claim.

A realistic future use case is a forensic laboratory: the administrator approves the department’s email domain and individual investigators, assigns cases, and reviews recorded operations. Physical-device access would require a separately deployed privileged local agent; the browser prototype does not supply that capability.

## The three core modules

| Module | Required behavior | Current boundary |
|---|---|---|
| Secure Drive Eraser | Select a source image, review the media policy, explicitly confirm erasure, overwrite a disposable copy, verify read-back and record the result. | Works on image copies. No direct HDD, SSD or NVMe controller commands. |
| Secure File & Folder Eraser | Select files or a folder, process multiple targets, verify each result and describe metadata/residual handling. | Local copies support timestamp/xattr handling and rename/unlink. Cloud handles working-object removal. Uploaded originals, journals, snapshots and provider backups are not cleansed. |
| Advanced File Carving & Recovery | Scan raw bytes by signature, validate boundaries and internal structure, classify recovered artifacts, explain confidence and preserve evidence hashes. | Supports contiguous JPEG, PNG, PDF and ZIP artifacts. Fragmented reconstruction remains roadmap work. |

These modules stay separate in navigation and demonstrations. Identity assurance, the policy engine, activity tracking, automatic timelines and recovery-based erasure challenges strengthen the core workflows; they do not replace them.

## Shared requirements

Every operation belongs to an authorized case. The interface must show source integrity, job outcome, relevant verification, elapsed time and throughput when measured. Media profiles include HDD, SSD, NVMe, USB, SD, optical and image workflows; those profiles are declared by the operator, not automatically detected hardware support.

Audit records must retain actor, timestamp, action and relevant source/job context. Reports combine case evidence, results and a timeline with a signed JSON envelope containing the PDF hash. Hash chains and signatures make changes detectable within their stated scope; an externally preserved fingerprint/report is needed for stronger protection against wholesale replacement or rollback.

## Access and administration

Cloud access requires verified email, an active session, an approved account, an approved exact domain or explicitly authorized account exception, and authenticator MFA. ADMIN can oversee all project cases; INVESTIGATOR operates owned/assigned cases; VIEWER inspects accessible cases without write permission.

The public access-request form asks only for an email address. It prepares a message in the visitor’s email app, where the visitor must press Send. It does not create an account or notify the admin automatically. Account setup is currently a separate administrator-managed step. Password and MFA remain part of sign-in.

## Acceptance criteria

1. An unauthorized visitor cannot read case data through either the API or direct database queries.
2. Approving a domain alone does not approve every account. Suspension or domain disable blocks subsequent protected requests.
3. Recovery extracts eight hash-matching artifacts from the deterministic demo fixture: three JPEGs, two PNGs, two PDFs and one ZIP.
4. Sanitization targets only disposable copies; source hashes remain unchanged. Verification states its actual scope.
5. Completed and failed operations produce recorded outcomes and timeline events. Reports can be checked independently.
6. Dashboard counts come from saved data. Confidence is labelled as a heuristic, not statistical accuracy.
7. Mobile, keyboard, email confirmation, MFA, approval and report-download journeys receive browser acceptance testing before a production-readiness claim.

## Success and non-goals

Success means an evaluator can follow a case from source intake through processing, verification and reporting, and understand both the result and its limitations. Do not substitute an attractive dashboard for a working backend.

The current release does not promise physical irrecoverability, universal recovery, identity-document verification, operating-system-wide monitoring, independent standards certification or production-scale concurrency. See [tasks.md](tasks.md) for the next acceptance gates and [memory.md](memory.md) for evidence-based presentation wording.
