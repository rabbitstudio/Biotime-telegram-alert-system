# System Architecture

BioTime → CSV Export (shared folder) → Python Monitor → Telegram Bot API → Dept Chat Rooms

## Components
- BioTime CSV export (source)
- Python monitor (polling + parse + dedup + routing)
- Telegram bot (send to dept chats + admin summary)
- Logs/backup for audit trail

## Notes
- Use placeholders for tokens/chat IDs in public repo
- Keep secrets in .env or private config
