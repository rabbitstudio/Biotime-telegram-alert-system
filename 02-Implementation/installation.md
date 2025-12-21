# Installation Guide (On-Prem / Windows Server)

> This is a sanitized guide. Do not store real tokens or chat IDs in a public repo.

## Prerequisites
- Windows Server (or Windows 10/11) with access to the BioTime CSV shared folder
- Python 3.x installed and added to PATH
- Network access:
  - SMB to file server (TCP 445) for CSV read
  - Outbound HTTPS (TCP 443) to Telegram API

## Folder Structure (recommended)
Create a working directory on the monitor host, e.g.
- `C:\biotime-telegram-alert-system\`

Place project files under that folder (src, config, docs, etc.)

## Python Dependencies
Create and use a virtual environment (recommended):

1) Open PowerShell as Administrator
2) Run:
   - `cd C:\biotime-telegram-alert-system`
   - `python -m venv .venv`
   - `.\.venv\Scripts\activate`

Install dependencies:
- `pip install -r requirements.txt`

## Configuration (secure)
- Store secrets outside the repo (recommended):
  - `.env` on the server (NOT committed)
  - or `config/departments.json` stored privately on the server

Example (placeholders only):
- Telegram Bot Token: `123456:REPLACE_ME`
- Dept Chat ID: `-100XXXXXXXXXX`

## Run (manual test)
Run the monitor script manually first (example):
- `python src\monitor_biotime.py`

Expected:
- Script starts, reads CSV, and writes logs
- When a new row appears in CSV, it sends Telegram message to mapped department

## Run as Scheduled Task (recommended)
1) Open **Task Scheduler**
2) Create Task (not Basic Task)
3) Run whether user is logged on or not
4) Use a dedicated service account (recommended)
5) Trigger:
   - At startup OR Daily + repeat every 1 minute (depending on your design)
6) Action:
   - Program/script: `C:\biotime-telegram-alert-system\.venv\Scripts\python.exe`
   - Arguments: `C:\biotime-telegram-alert-system\src\monitor_biotime.py`
   - Start in: `C:\biotime-telegram-alert-system\`

## Logs & Troubleshooting
- Check logs under `logs/`
- Common issues:
  - No access to SMB share (permission/firewall)
  - CSV locked/encoding issues
  - Telegram token/chat ID invalid
  - Proxy or outbound 443 blocked
