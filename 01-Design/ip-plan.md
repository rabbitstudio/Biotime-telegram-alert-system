# IP Plan (Sanitized / Example)

> This document uses placeholders. Real IPs, hostnames, and tokens are not stored in this public repository.

## Network Zones (example)
- **VLAN-Server**: Servers / VM / shared services
- **VLAN-User**: End-user clients (HR/IT)
- **VLAN-CCTV**: Cameras/NVR (if applicable)

## Key Nodes (placeholders)
| Component | Hostname (example) | IP (example) | Port | Notes |
|---|---|---:|---:|---|
| BioTime Export Share | `FILE-SRV` | `10.0.0.10` | 445 | SMB share for CSV export |
| Python Monitor Host | `MON-SRV` | `10.0.0.20` | - | Runs scheduled task/service |
| Telegram API | `api.telegram.org` | Internet | 443 | Outbound HTTPS only |

## Shared Folder Path (example)
- `\\FILE-SRV\Biotime\Export\Telegram report.csv`

## Firewall / Access Requirements
- Monitor host → File server: **SMB 445/TCP**
- Monitor host → Internet: **HTTPS 443/TCP** (Telegram API)
- No inbound ports required to Monitor host (recommended)

## Service Account & Permissions (recommended)
- Create a dedicated service account (e.g. `svc_biotime_monitor`)
- Permissions:
  - Read-only to the BioTime export folder
  - Write access to local `logs/` on monitor host
- Restrict SMB share access to minimum required users/services
