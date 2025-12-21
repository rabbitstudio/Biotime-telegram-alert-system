# Policy Matrix (Access & Operations)

> Sanitized example. This matrix documents **who can access what** and **why** (least privilege).

## Roles
- **HR User**: HR staff who need alerts and summary
- **IT Admin**: Maintains server, share permissions, and monitor runtime
- **Service Account**: Runs the monitor job/service with minimum required access

## Access Matrix
| Area | Resource | HR User | IT Admin | Service Account | Notes / Rationale |
|---|---|---:|---:|---:|---|
| BioTime CSV Share | `\\FILE-SRV\Biotime\Export\` | Read (optional) | Full | **Read-only** | Service account should only read CSV exports |
| Monitor Host (OS) | `MON-SRV` | None | Full | Logon as service only | HR should not access server |
| Local Logs | `MON-SRV:\app\logs\` | None | Read (optional) | Write | Logs are written by service; IT can review |
| Config Files | `MON-SRV:\app\config\` | None | Full | Read | Secrets stored outside repo (env/config) |
| Telegram Bot Token | Secret store / `.env` | None | Full | Read | Never committed to GitHub |
| Telegram Chat IDs | Config (sanitized in repo) | None | Full | Read | Keep examples in repo; real IDs in private config |
| Scheduled Task / Service | Windows Task Scheduler / Service | None | Full | Execute | IT maintains runtime and recovery |
| Network (Outbound) | HTTPS to Telegram API | N/A | Allow | Allow | Only 443 outbound required |
| Network (Inbound) | Inbound to monitor host | N/A | Block | Block | No inbound ports required (recommended) |

## Operational Policies
### Least Privilege
- Service account: **read share + write local logs only**
- HR: receives alerts only (no server access)

### Change Management
- Any change to alert rules/config should be tracked via Git commit
- Production secrets are updated outside repo (env/config)

### Incident Response (basic)
- If Telegram API unreachable: log error + retry with backoff
- If CSV missing/locked: log warning + continue polling

## Audit Trail
- Logs should include timestamp, event type, department, and delivery status
- Backup/archival retained per org policy (e.g., 30/90 days)
