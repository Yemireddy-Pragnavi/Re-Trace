# RE:TRACE

### Integrated Secure Data Erasure + Advanced File Recovery

**Smart India Hackathon 2026 · Problem Statement SIH26149 · Team Cryptic Crew**

[![Live Prototype](https://img.shields.io/badge/Live%20Prototype-Vercel-000000?style=for-the-badge&logo=vercel&logoColor=white)](https://re-trace-phi.vercel.app/)
![React](https://img.shields.io/badge/Frontend-React-149ECA?style=for-the-badge&logo=react&logoColor=white)
![TypeScript](https://img.shields.io/badge/TypeScript-3178C6?style=for-the-badge&logo=typescript&logoColor=white)
![Python](https://img.shields.io/badge/Backend-Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/API-FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![Supabase](https://img.shields.io/badge/Cloud-Supabase-3FCF8E?style=for-the-badge&logo=supabase&logoColor=white)
![SQLite](https://img.shields.io/badge/Local%20DB-SQLite-003B57?style=for-the-badge&logo=sqlite&logoColor=white)
![SHA-256](https://img.shields.io/badge/Integrity-SHA--256-1D3557?style=for-the-badge)
![SIH](https://img.shields.io/badge/Smart%20India%20Hackathon-2026-F97316?style=for-the-badge)
![NIST Guidance](https://img.shields.io/badge/Guidance-NIST%20SP%20800--88%20Rev.2-2E7D32?style=for-the-badge)

---

> **RE:TRACE combines secure data sanitization, forensic file recovery, independent validation, activity provenance, tamper-evident auditing, and forensic reporting in one case-based workflow.**

Most tools solve only one side of the problem: they either **erase data** or **recover data**.

RE:TRACE connects both sides and adds a third layer: **assurance**.

The platform is designed to answer five important questions:

- Can sensitive data be securely sanitized?
- Can deleted evidence still be recovered?
- Can the result of sanitization be independently challenged?
- Can we track **who performed what action and when**?
- Can the entire process be converted into a verifiable forensic record?

### RE:TRACE in One Line

> **Recover what matters. Erase what must never return. Verify both with trusted proof.**

---

# 🚀 Live Prototype

### [Open RE:TRACE](https://re-trace-phi.vercel.app/)

The deployed prototype demonstrates the complete user workflow through a controlled cloud environment.

> **Safety Note:** The hosted version performs destructive operations only on controlled uploads, generated test media, and disposable working copies. It does not directly erase a visitor's physical HDD, SSD, or NVMe device.

---

# 🎯 Why RE:TRACE?

Digital-forensics and sanitization workflows are commonly separated across multiple utilities.

A recovery tool may recover evidence but does not necessarily provide secure sanitization.

A sanitization tool may erase data but does not normally attempt forensic recovery afterward to challenge the result.

An investigator may also need separate tools for:

- User authentication
- Case tracking
- Evidence registration
- Forensic recovery
- Secure sanitization
- Sanitization verification
- Activity logging
- Timeline preparation
- Audit integrity
- Forensic reporting

RE:TRACE brings these capabilities into **one accountable workflow**.

---

# 🏗️ System Architecture

```text
                    RE:TRACE SECURE MEDIA ASSURANCE PLATFORM

┌─────────────────────────────────────────────────────────────────────┐
│                    1. IDENTITY & ACCESS CONTROL                     │
│                                                                     │
│     Authentication → Session Management → Role-Based Access         │
│                  Admin / Investigator / Viewer                      │
└────────────────────────────────┬────────────────────────────────────┘
                                 │
                                 ▼
┌─────────────────────────────────────────────────────────────────────┐
│                        2. CASE MANAGEMENT                           │
│                                                                     │
│     Create Case → Assign Investigator → Register Evidence Source    │
│                  → Store Case Metadata                              │
└────────────────────────────────┬────────────────────────────────────┘
                                 │
                                 ▼
┌─────────────────────────────────────────────────────────────────────┐
│                    3. SOURCE / EVIDENCE INSPECTION                  │
│                                                                     │
│     Disk Image / Files / Folders                                    │
│            ↓                                                        │
│     Media Profile + Filesystem Information + SHA-256                │
└────────────────────────────────┬────────────────────────────────────┘
                                 │
                                 ▼
                        ┌───────────────────┐
                        │ CHOOSE OPERATION  │
                        └─────────┬─────────┘
                                 │
             ┌───────────────────┼───────────────────┐
             │                   │                   │
             ▼                   ▼                   ▼

┌───────────────────┐  ┌────────────────────┐  ┌─────────────────────┐
│ SECURE DRIVE      │  │ FILE / FOLDER      │  │ ADVANCED FILE       │
│ ERASURE           │  │ ERASURE            │  │ RECOVERY            │
│                   │  │                    │  │                     │
│ Media profile     │  │ Select targets     │  │ Read-only source    │
│ Policy decision   │  │ Batch processing   │  │ Raw byte scanning   │
│ Working copy      │  │ Overwrite copy     │  │ Signature carving   │
│ Sanitization      │  │ Rename / unlink    │  │ Structure checks    │
│ Read-back verify  │  │ Metadata handling  │  │ Classification      │
│ Before/after hash │  │ Verify deletion    │  │ Confidence score    │
│                   │  │                    │  │ SHA-256             │
└─────────┬─────────┘  └─────────┬──────────┘  └──────────┬──────────┘
          │                      │                        │
          └──────────────────────┼────────────────────────┘
                                 │
                                 ▼
┌─────────────────────────────────────────────────────────────────────┐
│                  4. INDEPENDENT SANITIZATION VALIDATION             │
│                                                                     │
│ Sanitized Copy → Recovery Challenge → Artifact Scan                 │
│                                                                     │
│                PASS / WARNING / INCONCLUSIVE                        │
└────────────────────────────────┬────────────────────────────────────┘
                                 │
                                 ▼
┌─────────────────────────────────────────────────────────────────────┐
│                     5. ACTIVITY PROVENANCE                          │
│                                                                     │
│ User + Case + Source + Operation + Timestamp + Result               │
│                                                                     │
│                       AUTOMATIC TIMELINE                            │
└────────────────────────────────┬────────────────────────────────────┘
                                 │
                                 ▼
┌─────────────────────────────────────────────────────────────────────┐
│                     6. TAMPER-EVIDENT AUDIT                         │
│                                                                     │
│           Event 1 → Event 2 → Event 3 → Event N                     │
│                    SHA-256 Hash Chain                               │
└────────────────────────────────┬────────────────────────────────────┘
                                 │
                                 ▼
┌─────────────────────────────────────────────────────────────────────┐
│                       7. REPORT GENERATION                          │
│                                                                     │
│        Recovery Report | Sanitization Certificate                   │
│              Timeline | Hashes | Audit Status                       │
│                        PDF + JSON                                   │
└─────────────────────────────────────────────────────────────────────┘
```

---

# 🔍 Architecture Explained

RE:TRACE is divided into seven main layers.

## 1. Identity and Access Control

Before performing forensic or sanitization operations, a user must authenticate.

The system maintains:

- Authenticated user identity
- User role
- Active session
- Access permissions
- Login/logout activity

### Supported Roles

| Role | Access |
|---|---|
| **Admin** | Administrative and case-wide access |
| **Investigator** | Creates cases and performs forensic operations |
| **Viewer** | Read-only access to assigned information |

Authentication activity also becomes part of the audit trail.

---

## 2. Case Management

Every investigation or sanitization task is connected to a **case**.

A case contains information such as:

- Case ID
- Title
- Description
- Department
- Investigator
- Priority
- Status
- Evidence sources
- Jobs
- Timeline
- Reports

This prevents evidence and operations from existing without investigation context.

---

## 3. Evidence Source Registration and Inspection

The investigator registers the source before an operation begins.

### Supported Prototype Inputs

- Raw disk images
- Uploaded files
- Folders / batch files
- Generated forensic test media

For every source, RE:TRACE stores or calculates:

- Source name
- Source type
- Media profile
- Size
- Filesystem information where available
- SHA-256 fingerprint
- Associated case

The original forensic source is preserved during recovery operations.

---

# 🧹 Core Module 1 — Secure Drive Erasure

RE:TRACE provides a controlled sanitization workflow for forensic test images and disposable working copies.

The workflow considers:

- Media profile
- Sanitization purpose
- Data sensitivity
- Requested scope

It then determines a suitable sanitization direction.

### Example Workflow

```text
Media Profile: HDD
        +
Purpose: External Transfer
        +
Sensitivity: Sensitive
        ↓
Smart Policy Decision
        ↓
Controlled Sanitization
        ↓
Read-Back Verification
        ↓
Post-Sanitization Recovery Challenge
        ↓
Sanitization Certificate
```

The system records:

- Sanitization method
- Bytes processed
- Duration
- Before/after hashes
- Verification result
- Validation result

---

# 📁 Core Module 2 — Secure File & Folder Erasure

Investigators can select:

- A single file
- Multiple files
- Folders
- Batch targets

The controlled workflow performs supported operations such as:

```text
Select Targets
      ↓
Calculate Metadata / Hash
      ↓
Create Safe Working Copy
      ↓
Overwrite
      ↓
Rename
      ↓
Unlink
      ↓
Supported Metadata Cleanup
      ↓
Verify Absence
      ↓
Record Result
```

## File & Folder Erasure — Input

![File and Folder Eraser Input](screenshots/01-file-folder-eraser-input.png)

## File & Folder Erasure — Output

![File and Folder Eraser Output](screenshots/02-file-folder-eraser-output.png)

---

# 🔬 Core Module 3 — Advanced File Carving & Recovery

RE:TRACE performs recovery from raw forensic/test images without depending only on normal filesystem metadata.

### Current MVP Recovery Formats

| Category | Supported Type |
|---|---|
| Image | JPEG |
| Image | PNG |
| Document | PDF |
| Archive | ZIP |

### Recovery Pipeline

```text
Read-Only Source
       ↓
Raw Byte Scan
       ↓
Signature Detection
       ↓
Candidate Extraction
       ↓
Structure Validation
       ↓
Automatic Classification
       ↓
Confidence Scoring
       ↓
SHA-256
       ↓
Recovered Evidence
```

## Recovery Input

![File Carving Recovery Input](screenshots/03-file-carving-recovery-input.png)

## Recovered Evidence

![File Carving Recovery Output](screenshots/04-file-carving-recovery-output.png)

---

# 🧠 Explainable Recovery Confidence

A recovered file is not automatically treated as valid simply because its header was found.

RE:TRACE checks characteristics such as:

- Expected file header
- Expected footer where applicable
- Structural validity
- Parser/readability result
- Plausible file boundaries
- Format-specific consistency checks

The resulting confidence assessment gives investigators additional context when reviewing recovered artifacts.

---

# 💡 Key Innovation 1 — Smart Sanitization Policy

Different storage media cannot always be treated using exactly the same sanitization approach.

RE:TRACE therefore considers:

```text
MEDIA TYPE
     +
OPERATION SCOPE
     +
PURPOSE
     +
DATA SENSITIVITY
     ↓
SANITIZATION POLICY
     ↓
RECOMMENDED APPROACH
```

### Media-Aware Sanitization Direction

| Media | Recommended Direction |
|---|---|
| HDD | Overwrite-based workflow |
| SSD | Secure erase / cryptographic erase where supported |
| NVMe | NVMe sanitize / secure format where supported |
| USB Flash | Logical sanitization with flash-storage limitation warning |
| File / Folder | Controlled selective erasure |

For the hosted prototype, these decisions are safely demonstrated using controlled working copies rather than direct hardware commands.

---

# 🛡️ Key Innovation 2 — Independent Sanitization Validation

A traditional erase workflow may stop after the erase command reports success.

RE:TRACE adds another assurance layer.

```text
SANITIZE
    ↓
READ-BACK VERIFY
    ↓
RUN RECOVERY ENGINE
    ↓
SCAN FOR SUPPORTED ARTIFACTS
    ↓
RESULT
```

### Validation Results

| Result | Meaning |
|---|---|
| **PASS** | No supported recoverable artifacts detected |
| **WARNING** | One or more supported artifacts remain recoverable |
| **INCONCLUSIVE** | The result could not be determined reliably |

RE:TRACE intentionally avoids claiming that a successful logical scan proves absolute physical irrecoverability.

---

# 👤 Key Innovation 3 — Activity Provenance

RE:TRACE tracks important actions performed throughout an investigation.

Examples include:

- User login
- Case creation
- Evidence registration
- Source hashing
- Sanitization start
- Sanitization completion
- Recovery start
- Recovered artifact creation
- Validation
- Report generation
- Evidence export

Each recorded event can contain:

```text
User
Role
Session
Case
Source
Job
Operation
Timestamp
Parameters
Result
```

This creates accountability throughout the workflow.

---

# ⏱️ Key Innovation 4 — Automatic Timeline Construction

Recorded activity is automatically arranged into a chronological case timeline.

### Example

```text
09:31:08  Investigator authenticated
09:31:19  CASE-001 opened
09:32:05  Disk image registered
09:32:06  SHA-256 generated
09:33:14  Recovery started
09:37:41  Artifact recovery completed
09:38:12  Evidence hashes generated
09:39:02  Forensic report generated
```

This allows investigators and reviewers to understand the sequence of an investigation without manually reconstructing events from separate logs.

---

# 🔗 Key Innovation 5 — Tamper-Evident Audit Chain

Audit events are linked using SHA-256.

```text
EVENT 01
   │
   │ Hash A
   ▼
EVENT 02
Previous Hash = A
   │
   │ Hash B
   ▼
EVENT 03
Previous Hash = B
```

If an earlier copied event is modified during validation:

```text
Original Hash ≠ Recalculated Hash
               ↓
       TAMPERING DETECTED
```

The system therefore provides **tamper evidence**, rather than simply maintaining ordinary application logs.

---

# 📄 Forensic Reporting

RE:TRACE generates structured recovery and sanitization reports.

Reports can include:

- Case ID
- Investigator
- Evidence source
- SHA-256 values
- Operation details
- Recovered evidence
- Confidence results
- Sanitization result
- Validation result
- Activity timeline
- Audit integrity result

### Supported Formats

- **PDF**
- **JSON**

## Generated Forensic Report

![Generated Forensic Report](screenshots/05-forensic-report-generated.png)

---

# 🖥️ Platform Screens

## Landing Page

![RE:TRACE Landing Page](screenshots/01-landing-page.png)

The landing page introduces the problem, platform capabilities, and key assurance features before authentication.

---

## Investigator Dashboard

![RE:TRACE Dashboard Overview](screenshots/02-dashboard-overview.png)

The dashboard gives investigators one place to access:

- Cases
- Recovery
- Sanitization
- Validation
- Activity timeline
- Audit records
- Forensic reports

---

# 🔄 Data Flow

```text
INPUT
│
├── Authenticated User
├── Case Details
├── Disk Image
├── Files / Folders
└── Selected Operation

        ↓

PROCESS
│
├── Session + Case Mapping
├── Source Inspection
├── SHA-256 Fingerprinting
├── Sanitization / Recovery
├── Validation
├── Activity Tracking
├── Automatic Timeline
├── Audit Hash Chaining
└── Report Generation

        ↓

OUTPUT
│
├── Recovered Evidence
├── Sanitization Result
├── Sanitization Certificate
├── Forensic Recovery Report
├── Activity Timeline
└── Verified Audit Record
```

---

# 🛠️ Technology Stack

## Frontend

| Technology | Purpose |
|---|---|
| **React** | User interface |
| **TypeScript** | Type-safe frontend development |
| **Vite** | Development and production build tooling |

---

## Backend

| Technology | Purpose |
|---|---|
| **Python** | Core local processing |
| **FastAPI** | Local REST API |
| **Python Processing Engines** | Sanitization, recovery, verification, and fixture logic |

---

## Database & Storage

| Technology | Purpose |
|---|---|
| **SQLite** | Local metadata database |
| **Supabase PostgreSQL** | Cloud metadata persistence |
| **Supabase Storage** | Private cloud evidence/file storage |
| **Local Filesystem** | Controlled local evidence storage |

---

## Cloud Services

| Technology | Purpose |
|---|---|
| **Supabase Auth** | Cloud authentication |
| **Supabase RLS** | Database access isolation |
| **Supabase Edge Functions** | Cloud backend operations |
| **Vercel** | Web frontend deployment |

---

## Security & Integrity

| Technology | Purpose |
|---|---|
| **SHA-256** | Evidence and audit hashing |
| **Hash Chaining** | Tamper-evident event records |
| **Role-Based Access Control** | User authorization |
| **Supabase RLS** | Cloud database isolation |
| **Private Object Storage** | Evidence access control |

---

# 🧪 Reproducible Demo Dataset

RE:TRACE includes a deterministic forensic test image.

The fixture contains:

| Artifact | Quantity |
|---|---:|
| JPEG | 3 |
| PNG | 2 |
| PDF | 2 |
| ZIP | 1 |
| **Total** | **8** |

This gives the team and evaluators a repeatable recovery experiment with known ground truth.

---

# 🎬 Suggested Evaluation Demo

A complete RE:TRACE demonstration can be performed as follows.

## Step 1 — Authenticate

Sign in as an investigator.

## Step 2 — Create a Case

Create a new investigation case.

## Step 3 — Add Evidence

Generate or upload a demo forensic image.

The system generates its SHA-256 fingerprint.

## Step 4 — Recover Evidence

Run **File Carving & Recovery**.

Recover supported formats:

- JPEG
- PNG
- PDF
- ZIP

Review:

- Classification
- Structure validation
- Confidence
- SHA-256 hash

## Step 5 — Generate Recovery Report

Create a PDF or JSON forensic output.

## Step 6 — Sanitize

Use a disposable working copy and start the secure erasure workflow.

## Step 7 — Verify

Perform read-back verification.

## Step 8 — Challenge the Result

Run the recovery engine against the sanitized copy.

Display one of the following:

```text
PASS
WARNING
INCONCLUSIVE
```

## Step 9 — Review Timeline

Open the automatically generated chronological activity timeline.

## Step 10 — Verify Audit Integrity

Validate the SHA-256 hash chain.

## Step 11 — Generate Final Report

Generate the sanitization certificate and forensic report.

---

# 📚 Standards & Technical Guidance

The project references recognized sanitization and evidence-handling guidance, including:

- **NIST SP 800-88 Rev. 2**
- **IEEE 2883**
- Digital evidence integrity and chain-of-custody principles
- **DoD 5220.22-M** as a legacy/reference overwrite approach

These are used as engineering references while designing the prototype.

> **Important:** RE:TRACE does not claim formal certification or independently validated standards conformance.

---

# ✅ What Is Currently Implemented

| Capability | Current Prototype Status |
|---|---|
| Case-based workflow | ✅ Implemented |
| User authentication | ✅ Implemented |
| Role-based access | ✅ Implemented |
| Raw image processing | ✅ Implemented |
| Secure working-copy erasure | ✅ Implemented |
| File/folder batch erasure | ✅ Implemented |
| JPEG recovery | ✅ Implemented |
| PNG recovery | ✅ Implemented |
| PDF recovery | ✅ Implemented |
| ZIP recovery | ✅ Implemented |
| Structure validation | ✅ Implemented |
| Explainable recovery confidence | ✅ Implemented |
| SHA-256 evidence hashing | ✅ Implemented |
| Independent sanitization validation | ✅ Implemented |
| Activity tracking | ✅ Implemented |
| Automatic case timeline | ✅ Implemented |
| SHA-256 audit chain | ✅ Implemented |
| PDF / JSON reports | ✅ Implemented |
| Physical HDD/SSD/NVMe sanitization | 🔄 Local hardware integration / future deployment |
| Fragmented-file reconstruction | 🛣️ Roadmap |

---

# ⚠️ Honest Prototype Boundaries

RE:TRACE is currently a **hackathon prototype**, not a certified production forensic suite.

Current limitations include:

- The hosted version does not directly execute ATA/NVMe commands on a visitor's physical storage device.
- Hosted media types are controlled/declarative profiles.
- Physical-drive support requires a local privileged hardware agent.
- Fragmented-file reconstruction remains future work.
- Metadata cleanup is limited by the controlled prototype environment.
- Recovery currently focuses on JPEG, PNG, PDF, and ZIP.
- Hash chaining is tamper-evident rather than absolutely immutable against a fully privileged database or host administrator.
- Hostile or untrusted forensic images should receive stronger isolation before production deployment.

These limitations are documented intentionally so that the prototype demonstrates **real working capability without overstating implementation**.

---

# 💻 Run Locally

## Requirements

Install:

- Python **3.12**
- Node.js **22.12+**
- Git

---

## 1. Clone the Repository

```bash
git clone https://github.com/Yemireddy-Pragnavi/Re-Trace.git
cd Re-Trace
```

---

# 🪟 Windows Setup

## 2. Create Python Virtual Environment

```powershell
py -3.12 -m venv .venv
```

## 3. Install Backend Dependencies

```powershell
.\.venv\Scripts\python.exe -m pip install -r backend\requirements.txt
```

## 4. Create Backend Environment File

```powershell
Copy-Item backend\.env.example backend\.env
```

Configure the required environment variables inside:

```text
backend/.env
```

Do not commit private credentials or production secrets to GitHub.

## 5. Start Backend

```powershell
cd backend
..\.venv\Scripts\python.exe -m uvicorn app.main:app --host 127.0.0.1 --port 8000
```

Backend API:

```text
http://127.0.0.1:8000
```

FastAPI documentation:

```text
http://127.0.0.1:8000/docs
```

---

## 6. Start Frontend

Open another terminal:

```powershell
cd frontend
npm ci
npm run dev
```

Frontend:

```text
http://localhost:5173
```

---

# 🍎 macOS / Linux Setup

## Create Virtual Environment

```bash
python3.12 -m venv .venv
```

## Install Backend Dependencies

```bash
.venv/bin/python -m pip install -r backend/requirements.txt
```

## Create Environment File

```bash
cp backend/.env.example backend/.env
```

## Start Backend

```bash
cd backend
../.venv/bin/python -m uvicorn app.main:app --host 127.0.0.1 --port 8000
```

Then open another terminal:

```bash
cd frontend
npm ci
npm run dev
```

---

# 🧪 Testing

## Backend Tests

```bash
cd backend
pytest -q
```

## Frontend Production Build

```bash
cd frontend
npm run build
```

---

# 📂 Repository Structure

```text
Re-Trace/
│
├── backend/
│   ├── app/
│   │   ├── auth.py
│   │   ├── engines.py
│   │   ├── main.py
│   │   ├── native_adapter.py
│   │   ├── reports.py
│   │   └── store.py
│   │
│   └── tests/
│
├── frontend/
│   └── src/
│
├── docs/
│
├── screenshots/
│   ├── 01-landing-page.png
│   ├── 01-file-folder-eraser-input.png
│   ├── 02-dashboard-overview.png
│   ├── 02-file-folder-eraser-output.png
│   ├── 03-file-carving-recovery-input.png
│   ├── 04-file-carving-recovery-output.png
│   └── 05-forensic-report-generated.png
│
├── scripts/
│
└── README.md
```

---

# 🧩 Important Source Files

| File | Purpose |
|---|---|
| `backend/app/auth.py` | Authentication and session handling |
| `backend/app/engines.py` | Sanitization, carving, validation, and demo fixtures |
| `backend/app/main.py` | API routes and application control |
| `backend/app/store.py` | Persistence, timeline, and audit records |
| `backend/app/reports.py` | PDF/JSON forensic reporting |
| `backend/app/native_adapter.py` | Local/native integration abstraction |
| `frontend/src/` | Public landing page and investigator workspace |

---

# 🔐 Security Design Principles

RE:TRACE is designed around several core security principles:

### Evidence Integrity

Evidence and important outputs are fingerprinted using **SHA-256** so investigators can detect unexpected modification.

### Read-Only Recovery

Recovery operations are designed to avoid modifying the original forensic source.

### Controlled Sanitization

Hosted sanitization operations are performed against disposable working copies instead of directly targeting a visitor's physical storage device.

### Least-Privilege Access

User actions are restricted according to assigned roles.

### Accountability

Important actions are connected to:

```text
User
+
Session
+
Case
+
Source
+
Operation
+
Timestamp
+
Result
```

### Tamper Evidence

Audit records are linked through cryptographic hashes, making unexpected historical modification detectable during validation.

---

# 🌟 What Makes RE:TRACE Different?

The primary idea behind RE:TRACE is not simply:

```text
ERASE DATA
```

or:

```text
RECOVER DATA
```

Instead, the complete lifecycle is:

```text
IDENTIFY
   ↓
REGISTER
   ↓
HASH
   ↓
RECOVER / SANITIZE
   ↓
VERIFY
   ↓
CHALLENGE
   ↓
TRACK
   ↓
AUDIT
   ↓
REPORT
```

This creates a workflow where technical actions produce evidence that can be reviewed later.

---

# 💭 Why We Built RE:TRACE

The goal was not to create another tool with an **Erase** button.

It was also not to build another utility that only says **Recover**.

We wanted every important action to have context.

A recovered file should have:

- A source
- A hash
- A confidence result
- A case

A sanitization operation should have:

- A method
- Verification
- A validation result
- An audit record

Every investigator action should have:

- An identity
- A timestamp
- A case
- A result

That is the idea behind **RE:TRACE**.

---

# 🗺️ Roadmap

Future development can extend RE:TRACE with:

- Physical HDD sanitization through a privileged local agent
- ATA Secure Erase integration
- NVMe sanitize / secure-format integration
- SSD cryptographic erase support
- Additional recovery formats
- Fragmented-file reconstruction
- Filesystem-aware recovery
- Stronger forensic sandboxing
- External verification exports
- Signed forensic reports
- Advanced chain-of-custody workflows
- Scalable case collaboration

---

# 👥 Team

## Cryptic Crew

**Smart India Hackathon 2026**

**Problem Statement ID:** `SIH26149`

### RE:TRACE

> **Recover what matters.**  
> **Erase what must never return.**  
> **Verify with trusted proof.**

---

## 🔗 Project Links

**Live Prototype:**  
https://re-trace-phi.vercel.app/

**GitHub Repository:**  
https://github.com/Yemireddy-Pragnavi/Re-Trace

---

<div align="center">

### RE:TRACE

**Integrated Secure Data Erasure + Advanced File Recovery**

Built by **Team Cryptic Crew** for **Smart India Hackathon 2026**

</div>
