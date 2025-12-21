# BioTime → Telegram Alert System (Department-based)

Real-time attendance alert system integrating **ZK BioTime** CSV exports with **Telegram** notifications.  
Designed for **on-premise** environments where HR/IT need instant visibility without manual checks.

## What it does
- Monitors BioTime exported CSV (polling-based)
- Sends Telegram notifications **by department**
- Supports **DRY RUN** mode (safe testing without sending messages)
- Logging + audit-friendly trail
- Ops-ready docs (install/config/test/rollback)

## High-level flow
BioTime → CSV Export (shared folder) → Python Monitor → Telegram Bot API → Dept Chat Rooms

### Quick start (safe demo / DRY RUN)
> This repo is public. Use sample data + DRY RUN first.

```bash
pip install -r requirements.txt
python src/monitor_biotime.py
```
## Config required
- Create config/departments.json on your runtime machine (NOT committed)
- Copy structure from config/departments.example.json
- Keep "dry_run": true during testing

## Simulate new events locally
- Append a new row to your CSV and watch logs for New rows detected

## Why this matters (business value)
- Reduces manual attendance checking for HR/Operations
- Improves response time (late/absent patterns)
- Adds a lightweight audit trail without modifying BioTime

## Tech stack
- Python 3.x
- pandas, requests
- Telegram Bot API
- Windows Server / On-Prem file share (SMB)

## Security notes (important)
- Never commit real Bot Tokens / Chat IDs to this repo.
- Use placeholders in examples and keep real secrets in config/departments.json or .env (server-only).
- Rotate tokens immediately if exposure is suspected.

## Repository structure
```text
00-Overview.md
01-Design/
02-Implementation/
03-Test/
04-Rollback/
05-LessonsLearned.md
src/
config/
docs/
```
## Documentation
- Design docs: 01-Design/
- Implementation guides: 02-Implementation/
- Test cases & evidence: 03-Test/
- Rollback plan: 04-Rollback/
- Portfolio PDF (recruiters): docs/portfolio.pdf

## Author
System & Network Engineer
