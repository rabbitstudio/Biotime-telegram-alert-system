# Test Cases — BioTime → Telegram Alert System

This document lists test cases used to validate the BioTime CSV monitoring and department-based Telegram notification workflow.

> Notes:
> - Public repo uses placeholders only.
> - Run initial tests with `"dry_run": true` to avoid sending real messages.

---

## Test Environment (example / sanitized)
- OS: Windows Server / Windows 10/11 (on-prem)
- Python: 3.x
- Dependencies: `pandas`, `requests`
- Data source: BioTime exported CSV on SMB share (or `sample-data/sample.csv` for local test)
- Network: Outbound HTTPS (443) to Telegram API
- Config: `config/departments.json` (NOT committed)

---

## Test Cases Table

| TC ID | Scenario | Preconditions | Steps | Expected Result | Pass/Fail | Notes |
|---|---|---|---|---|---|---|
| TC-01 | Start without config file | `config/departments.json` does not exist | Run `python src/monitor_biotime.py` | App logs **Missing config file** and shows how to create it from example |  |  |
| TC-02 | Start with config (DRY RUN) | `departments.json` exists, `"dry_run": true` | Run app | App starts successfully, prints config summary, creates `logs/` |  |  |
| TC-03 | CSV path not found | `csv_path` incorrect or share unreachable | Run app | App logs **CSV not found** and keeps retrying (no crash) |  |  |
| TC-04 | CSV readable with supported encoding | Valid CSV exists | Run app | App reads CSV successfully; logs encoding used (if applicable) |  |  |
| TC-05 | First run does not spam old rows | CSV has existing rows | Start app (fresh state) | App initializes `last_row_count` to current rows; **does not** process old rows |  |  |
| TC-06 | Detect new row appended | App running, CSV exists | Append 1 new row to CSV | App logs `New rows detected: +1` |  |  |
| TC-07 | DRY RUN output format | `"dry_run": true` | Append new row | App logs `[DRY RUN] Would notify dept=...` with message content |  |  |
| TC-08 | Department mapping found | Dept exists in config (`departments[]`) | Append row with matching dept value | App selects correct dept target; prepares message for that dept |  |  |
| TC-09 | Unknown department handling | Dept not in config | Append row with dept not configured | App logs warning **No target config** and skips sending (no crash) |  |  |
| TC-10 | CSV reset / rotation | App running; state exists | Replace CSV with smaller file / clear rows | App detects row_count decreased and resets state safely (no spam) |  |  |
| TC-11 | Network blocked to Telegram (send mode) | `"dry_run": false`, Telegram blocked | Append row | App logs send failure error; continues running (no crash) |  |  |
| TC-12 | Invalid Telegram token/chat_id | `"dry_run": false`, invalid token or chat_id | Append row | App logs error from Telegram API; continues running |  |  |
| TC-13 | Permission issue on SMB share | Service account lacks read permission | Run app | App cannot read CSV; logs error; continues retrying |  |  |
| TC-14 | Stability (long run) | Normal config | Run for 1–2 hours | No memory leak symptoms; logs rotate by date; continues polling |  |  |
| TC-15 | Stop gracefully | App running | Press `Ctrl+C` | App logs stopped message and exits cleanly |  |  |

---

## Acceptance Criteria
- App does not crash on missing config / missing CSV / unreadable CSV / network failure.
- New rows are detected reliably and processed exactly once per append (normal case).
- DRY RUN mode allows safe validation without sending messages.
- No secrets are committed to the public repository.

---

## Evidence Location
See: `03-Test/evidence.md` (screenshots / logs / sample outputs)
