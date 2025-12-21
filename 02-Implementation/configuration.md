# Configuration Guide

This repo is public. **Do not commit real Telegram bot tokens or chat IDs.**

## Config Files
### Example (committed)
- `config/departments.example.json`  
  Used as a template to show structure and required fields.

### Real config (NOT committed)
Create one of the following on the server (recommended):
- `config/departments.json` (private on server)
  - Same structure as the example file
  - Contains real tokens/chat IDs
- or use `.env` + a private config approach (optional)

> If you create `config/departments.json`, ensure it is NOT committed.

## Recommended Steps (On Server)
1) Copy the example:
   - Copy `config/departments.example.json` → `config/departments.json`
2) Edit `config/departments.json` and replace placeholders:
   - `telegram_bot_token`
   - `chat_id`
   - `csv_path` to the real SMB path
3) Validate file permissions:
   - Only IT Admin + service account can read `config/departments.json`

## Fields (What they mean)
- `poll_interval_seconds`: how often to check the CSV file
- `csv_path`: SMB path to BioTime exported CSV
- `admin`: where to send daily summary / alerts to admin
- `departments[]`: list of departments to route notifications

## Security Notes
- Never store tokens in README or public docs
- Keep real secrets in server-only config
- Rotate Telegram bot tokens if exposure is suspected

## Quick Validation Checklist
- [ ] Service account can read the CSV share
- [ ] Server can reach Telegram API over HTTPS (443)
- [ ] `departments.json` is readable only by authorized accounts
- [ ] Example file remains unchanged (placeholders only)
