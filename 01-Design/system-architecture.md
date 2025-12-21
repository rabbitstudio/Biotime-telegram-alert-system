# System Architecture

## Overview
This system monitors BioTime exported CSV files from an on-prem shared folder and sends Telegram alerts.
Alerts are routed **by department**, plus a daily summary is sent to an admin channel.

## Architecture (logical flow)
```mermaid
flowchart LR
  A[ZK BioTime] --> B[CSV Export<br/>Shared Folder]
  B --> C[Python Monitor<br/>Polling + Parse]
  C --> D{Event detected?}
  D -- No --> C
  D -- Yes --> E[Dedup / Rules<br/>per dept]
  E --> F[Telegram Bot API]
  F --> G[Dept Chat Room(s)]
  E --> H[Admin Summary]
