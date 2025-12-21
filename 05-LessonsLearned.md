# Lessons Learned — BioTime → Telegram Alert System

This section documents technical and operational lessons learned while designing and implementing a department-based Telegram alert system based on BioTime CSV exports.

---

## What went well
- **Clear separation of responsibilities**: configuration, monitoring logic, logging, and docs are organized into a predictable structure.
- **Safe testing workflow**: DRY RUN mode allowed validation without risking message spam.
- **Ops-first mindset**: test cases, evidence, and rollback plan were documented early for maintainability.
- **Lightweight integration**: using CSV exports avoided touching BioTime database or vendor internals.

---

## Challenges encountered
- **CSV variability**: CSV exports can change format/encoding between versions and environments.
- **Shared folder reliability**: SMB availability and permissions can cause intermittent read failures.
- **Duplicate notification risk**: file resets/rotations and reorder scenarios can lead to re-processing if state handling is not robust.
- **Security constraints**: public portfolio required strict secret redaction and safe example configs.

---

## How we addressed them
- Implemented **DRY RUN** as default for safe validation.
- Added **retry-friendly behavior** (no crash on missing CSV / read failure).
- Introduced **evidence and test documentation** to confirm behavior with real logs (sanitized).
- Defined rollback options:
  - Stop monitoring immediately
  - Switch to DRY RUN
  - Revert to known-good version
  - Disable export only if required

---

## What I would improve next (Roadmap)
### Reliability / correctness
- **Dedup by fingerprint** (hash per row) instead of row count only
- **Robust CSV parsing** with schema validation + fallback column mapping
- Add structured error categories and clearer operator messages

### Operations
- Run as a Windows Service / Scheduled Task with health checks
- Add alerting for “CSV not updated for N minutes” (export pipeline failure)
- Log rotation + retention policy documentation

### Security
- Use `.env` + secret manager approach (or DPAPI/Windows Credential Manager) on server
- Add explicit “redaction checklist” before publishing portfolio updates

---

## Key takeaway
This project was designed not only to “work once,” but to be **operated**: documented, testable, safe to roll back, and secure for public sharing as a portfolio.

---

## Credits / Role
- Designed and implemented monitoring + notification workflow
- Produced documentation (design, tests, evidence, rollback, lessons learned)
- Focused on on-prem operational constraints and security-by-default
