# RE:TRACE

### Integrated Secure Data Erasure + Advanced File Recovery
**Smart India Hackathon 2026 · Problem Statement SIH26149 · Team Cryptic Crew**

RE:TRACE is a secure media assurance prototype that brings **data sanitization, forensic recovery, verification, accountability, and reporting into one case-based workflow**.

Most tools solve only one side of the problem: they either erase data or recover it. RE:TRACE connects both sides and keeps a verifiable record of **who performed an action, on which source, when it happened, what method was used, and what result was produced**.

> **Core idea:** Recover what matters. Erase what must never return. Verify both with trusted proof.

---

## Try the Prototype

**Cloud Prototype:**  
https://retrace-cloud.vvreddy1584.chatgpt.site

- Public landing page: `/`
- Sign in: `/login`
- Investigator workspace: `/app/*`

The hosted version is a **safe sandbox prototype**. Sanitization runs on disposable working copies and test media images. It does **not** directly erase a visitor's physical HDD, SSD, or NVMe device.

---

## The Problem We Are Solving

Digital-forensics teams often have to switch between separate tools for recovery, sanitization, verification, reporting, and audit logging.

That creates fragmented workflows and makes it harder to answer important questions such as:

- Was the data actually erased?
- Can deleted evidence still be recovered?
- Who performed the operation?
- When did each action happen?
- Can the final evidence and report be trusted?

RE:TRACE brings these operations into **one controlled and auditable platform**.

---

# Core Modules

## 1. Secure Drive Erasure

RE:TRACE provides a media-aware sanitization workflow for controlled disk images and disposable working copies.

The workflow records:

- Media profile
- Sanitization purpose
- Data sensitivity
- Recommended sanitization method
- Before/after SHA-256 hashes
- Bytes processed
- Processing duration
- Read-back verification
- Independent post-erasure validation
- Sanitization certificate

The original uploaded evidence is preserved.

---

## 2. Secure File & Folder Erasure

Investigators can securely process:

- A single file
- Multiple files
- Folders
- Batch selections

The current prototype performs supported operations such as:

- Overwriting disposable copies
- Rename before deletion
- File unlinking
- Supported metadata cleanup
- Logical absence verification
- Operation logging
- Timeline updates

### Input

![File and Folder Eraser Input](screenshots/01-file-folder-eraser-input.png)

### Output

![File and Folder Eraser Output](screenshots/02-file-folder-eraser-output.png)

---

## 3. Advanced File Carving & Recovery

RE:TRACE can recover supported deleted files directly from raw forensic images without depending only on normal filesystem metadata.

Current MVP formats:

- JPEG
- PNG
- PDF
- ZIP

The recovery workflow performs:

1. Read-only source handling
2. Raw byte scanning
3. Signature detection
4. Candidate extraction
5. Structure validation
6. Automatic classification
7. Confidence scoring
8. SHA-256 hashing
9. Secure recovered-file storage

### Recovery Input

![File Carving Recovery Input](screenshots/03-file-carving-recovery-input.png)

### Recovery Output

![File Carving Recovery Output](screenshots/04-file-carving-recovery-output.png)

---

# What Makes RE:TRACE Different

RE:TRACE is not simply an eraser placed next to a recovery tool.

The main difference is that **sanitization, forensic recovery, verification, timeline construction, and audit integrity work together inside the same case workflow**.

---

## Smart Sanitization Policy

The sanitization workflow considers:

- Media type
- Operation scope
- Purpose
- Data sensitivity

It then recommends an appropriate sanitization approach instead of applying the same method to every device type.

Example:

```text
HDD
  ↓
Overwrite-based sanitization

SSD / NVMe
  ↓
Secure erase / sanitize recommendation where supported

File / Folder
  ↓
Filesystem-aware selective erasure
