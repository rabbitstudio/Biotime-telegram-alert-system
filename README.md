# BioTime → Telegram Alert System (Department-based)

Real-time attendance alert system integrating **ZK BioTime** CSV exports with **Telegram** notifications.
Designed for **on-premise** environments where HR/IT need instant visibility without manual checks.

## What it does
- Monitors BioTime exported CSV (polling-based)
- Sends Telegram notifications **by department**
- Sends daily summary report to admin
- Weekly reset / housekeeping
- Logging + backup trail (audit-friendly)

## High-level flow
BioTime → CSV Export (shared folder) → Python Monitor → Telegram Bot API → Dept Chat Rooms

## Why this matters (business value)
- Reduces manual attendance checking for HR/Operations
- Improves incident response (late/absent patterns)
- Creates a lightweight audit trail without changing BioTime

## Tech stack
- Python 3.x
- pandas, requests
- Telegram Bot API
- Windows Server / On-Prem file share

## Security notes (important)
- **Do not commit real Bot Tokens / Chat IDs** to this repo.
- Use placeholders in examples and keep real secrets in `.env` or external config.

## Documentation
- Portfolio PDF (for recruiters): `docs/portfolio.pdf`
- Design docs: `01-Design/`
- Implementation notes: `02-Implementation/`
- Test cases & evidence: `03-Test/`

## Author
System & Network Engineer
