# SIH26149 requirement coverage

Baseline: the user's priority instruction and attached master prompt. The priority instruction supersedes the master prompt's emphasis on enhancements. This matrix is an implementation assessment, not an independently verified quotation of the SIH portal.

| Priority | Requirement | Visible location | Backend evidence | Status / acceptance limit |
|---|---|---|---|---|
| Core 1 | Secure Drive Eraser | Separate navigation entry and image workflow | `engines.sanitize`, `POST /cases/{id}/jobs` | Working sandbox image overwrite; native hardware pending |
| Core 2 | Secure File & Folder Eraser | Separate entry, file/folder picker, multi-selection | `module=files`, per-file verification | Working flattened batch workflow; no OS filesystem-aware delete |
| Core 2 | Metadata and residual cleansing | Recorded metadata result and scope statement | xattr removal, timestamp reset, rename/unlink, zero read-back and carving challenge | Partial: working-copy metadata only; retained originals and host traces explicitly excluded |
| Core 3 | Signature-based carving | Recovery format filters | Raw byte signatures for PNG/JPEG/PDF/ZIP | Working on contiguous supported formats |
| Core 3 | Structure-based validation/carving | Confidence reasons and rejected candidates | PNG chunks/CRC, image parser/decode, PDF xref/page tree, ZIP directory/CRCs | Working boundary/structure checks; not general filesystem reconstruction |
| Core 3 | Automatic classification | Recovered evidence table | Image, Document, Archive classification | Working |
| Core 3 | Confidence scoring | Expandable 95/100 score | Header +25, boundary +30, successful parser +40 | Working heuristic; not probability, no calibrated accuracy claim |
| Core 3 | Without filesystem metadata | Raw fixture generation and image upload | Direct bytes and offsets; no filesystem library needed | Working |
| Core 3 | Evidential integrity | SHA-256 hashes, downloads and reports | Before/after source hash checks and export rehash | Working logical integrity, not hardware write-blocking |
| Core 3 | Fragmented-file reconstruction | Roadmap notice in Recovery and Identity | Documented future strategy | Roadmap only; no reconstruction claim |
| Shared | Multiple storage/media | Declared media selector | Media policy branches | Raw-image/file support; physical profiles simulated |
| Shared | Erasure verification | Recorded erasure result | Whole logical content read-back and size check | Working within sandbox |
| Shared | Audit management | Audit Integrity and admin security events | Server events, per-case chain, append-only triggers | Working; no external immutable storage |
| Shared | Tamper-resistant reporting | Forensic Reports, signature verification | Ed25519 envelope containing PDF hash | Tamper-evident; trusted external fingerprint required |
| Shared | GUI dashboard | Overview, three module cards | Real per-case counts | Working; no fabricated statistics |
| Shared | Forensic reporting | PDF/JSON downloads | Case, operator, source, artifacts, metrics and event snapshot | Working combined report; not certified certificate |
| Shared | Validation/testing | Validation Lab | Ground-truth hashes, malformed PNG, erase/recover challenge | Working synthetic suite; independent validation pending |
| Shared | Performance metrics | Operation results | Wall-clock seconds, bytes and MiB/s | Working; not physical-device benchmark |
| Enhancement | Identity assurance | Sign-in, Identity & Access | scrypt local auth; optional Supabase verified-email exchange | Partial; MFA/passkeys/ID verification absent |
| Enhancement | Activity tracking | Timeline and admin security events | Server-generated application events | Working application scope; no OS monitoring |
| Enhancement | Automatic timeline | Timeline filters and expandable detail | Query persistent ordered audit events | Working; grouped event context by job ID, no separate grouping view |
| Enhancement | Smart policy | Erasure policy preview | Media/purpose/sensitivity decision | Working recommendation; hardware execution unavailable |
| Enhancement | Adversarial validation | Erasure result and Validation Lab | Real carver scan of overwritten bytes | Working supported-format challenge, not absolute erasure proof |

## Master-prompt differences

The repository prioritizes a clone-and-run local prototype. The requested full Supabase PostgreSQL/RLS schema, hosted link, passkeys/MFA, password reset, separate device/session management pages, organization-level admin controls, durable background queue, cloud storage and native agent are not delivered. They must be implemented and independently tested before representing this as a fully complete or production-ready build.
