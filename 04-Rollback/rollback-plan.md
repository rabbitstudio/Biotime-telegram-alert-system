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
```

2) Restart the monitor process/service

3) Validate
- Logs show `DRY RUN=True`
- App logs `[DRY RUN] Would notify ...` instead of sending Telegram

## Rollback Option C — Revert to Previous Known-Good Version

### Goal: Restore behavior to last stable commit/tag.

1) Identify a previous stable commit or release tag
Example:
```bash
git log --oneline --max-count=20
```

2) Checkout the stable version
```bash
git checkout <stable_commit_or_tag>
```

3) Reinstall dependencies if needed
```bash
pip install -r requirements.txt
```

4) Restart the monitor

5) Validate using `03-Test/test-cases.md` basic tests

## Rollback Option D — Disable BioTime Export (only if required)

### Goal: Stop file changes at the source (rare case).

Use only if continuous exports create operational risk. This may affect HR workflows.

1) Disable BioTime CSV export schedule/job (per BioTime configuration)
2) Confirm no new CSV files are generated
3) Re-enable once system is fixed

## Post-Rollback Actions
- [ ] Save incident notes in `05-LessonsLearned.md`
- [ ] Collect evidence logs (redacted) in `03-Test/evidence.md`
- [ ] Open a change request for fixes (CSV format, mapping, retry, dedup)
- [ ] Re-test before re-enabling send mode
 
## Recovery Criteria (when rollback is complete)
- Monitoring is stopped OR confirmed in DRY RUN mode
- HR/IT confirms no incorrect notifications are being sent
- Root cause identified and documented
- Fix plan created with an owner and timeline
