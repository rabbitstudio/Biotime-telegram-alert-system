# Evidence — BioTime → Telegram Alert System

This page contains **sanitized** evidence that the system works end-to-end.
All secrets (tokens/chat IDs) and sensitive infrastructure details are removed.

---

## Evidence Checklist (what to include)
- [ ] App starts successfully (DRY RUN)
- [ ] CSV not found handling (retry, no crash)
- [ ] New row detection (+N)
- [ ] Department routing decision
- [ ] (Optional) Real Telegram delivery proof (with redactions)

---

## 1) DRY RUN — App startup + config loaded
> Paste a short log snippet (5–20 lines). Remove sensitive paths if needed.

```text
=== BioTime Telegram Alert System (DRY RUN=True) ===
Start time: 2025-12-21 13:00:00
CSV Path: sample-data/sample.csv
Poll Interval (seconds): 2
Departments configured: ['IT', 'HR']
Initialized state at row_count=1 (encoding=utf-8)
```
## 2) CSV Not Found — retry without crashing

```text
CSV not found. Waiting... (\\FILE-SRV\Biotime\Export\Telegram report.csv)
CSV not found. Waiting... (\\FILE-SRV\Biotime\Export\Telegram report.csv)
```

## 3) New Row Detected — DRY RUN message preview

```text
New rows detected: +1 (encoding=utf-8)
[DRY RUN] Would notify dept=IT
📣 BioTime Alert
🏢 Dept: IT
- EmployeeID: 1002
- EmployeeName: Another User
- DateTime: 2025-12-21 13:05:00
- Event: Check-in
```
## 4) Unknown Department — safe skip

```text
New rows detected: +1 (encoding=utf-8)
No target config for dept=SALES. Skipping send.
```

## 5) (Optional) Real Telegram Delivery — redacted proof
If you include screenshots, blur token/chat_id/employee personal data.
Add images into this repo under 03-Test/screenshots/ and link them here.

Example (redacted log):

```text
✅ Sent Telegram to dept=IT message_id=**** (redacted)
```

### Screenshots (optional)
- 03-Test/screenshots/telegram-alert-redacted.png
- 03-Test/screenshots/log-new-rows-redacted.png

### Redaction Rules (must follow)
- Remove/blur: bot tokens, chat IDs, real employee names/IDs, internal hostnames, private IPs, share paths if sensitive.
- Keep: timestamps, event flow, dept routing result, “dry_run” behavior, success/failure handling.

## Notes
- DRY RUN mode demonstrates logic safely without sending messages.
- Real delivery evidence is optional for a public repo, but helpful if properly redacted.






