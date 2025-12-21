# Rollback Plan — BioTime → Telegram Alert System

This rollback plan ensures the alert system can be safely disabled or reverted without impacting BioTime data, HR operations, or existing infrastructure.

---

## Rollback Triggers (when to rollback)
- Telegram notifications spam / incorrect routing
- Unexpected high CPU/RAM usage on the server
- CSV export format changed causing parsing failures
- Network/security policy changes (egress blocked)
- Operational request from HR/IT (maintenance window)

---

## Scope
Rollback affects only:
- Python monitoring process/service
- Local config & logs on the monitoring host

Rollback does NOT affect:
- BioTime database
- BioTime export jobs (unless explicitly disabled)
- HR data entry processes
- Network share content (CSV files remain intact)

---

## Pre-Rollback Checklist
- [ ] Confirm current version/commit running (if known)
- [ ] Capture last 50 lines of logs (for incident record)
- [ ] Notify HR/IT stakeholders (brief impact statement)
- [ ] Verify no secrets are stored in the repo (public safety)

---

## Rollback Option A — Disable Monitoring (fastest)
**Goal:** Stop sending alerts immediately.

1) Stop the running process  
- If running in terminal: press `Ctrl + C`
- If running as scheduled task/service: stop the task/service

2) Ensure no auto-restart is active  
- Disable Task Scheduler job / service restart policy (if configured)

3) Validate
- No new logs are generated after stop
- No Telegram messages are sent after stop

---

## Rollback Option B — Revert to DRY RUN (safe mode)
**Goal:** Keep monitoring logic running without sending messages.

1) Edit `config/departments.json` (server-only)  
Set:
```json
"dry_run": true
