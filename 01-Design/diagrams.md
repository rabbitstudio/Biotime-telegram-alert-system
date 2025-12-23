# Diagrams — BioTime → Telegram Alert System

All diagrams are **sanitized** (placeholders only).  
Use these for portfolio / recruiters / ops handover.

---

## 1) High-level Architecture (System Context)

```mermaid
flowchart LR
  subgraph OnPrem["On-Prem Network (LAN)"]
    BT["BioTime Server\n(ZK BioTime)"]
    SHARE["File Share (SMB)\n\\\\FILE-SRV\\Biotime\\Export\\...csv"]
    MON["Monitor Host\nPython Service / Task Scheduler"]
    CFG["Runtime Config (server-only)\nconfig/departments.json\n(dry_run, tokens, chat_ids)"]
    LOGS["Logs + State\nlogs/*.log\nlogs/last_seen.json"]
  end

  subgraph Internet["Internet"]
    TG["Telegram Bot API\napi.telegram.org (HTTPS 443)"]
  end

  subgraph Chats["Telegram Chats"]
    HR["HR Chat Room"]
    IT["IT Chat Room"]
    ADMIN["Admin Chat\n(daily summary)"]
  end

  BT -->|CSV Export Job| SHARE
  SHARE -->|Read CSV| MON
  CFG -->|Load Config| MON
  MON -->|Write| LOGS
  MON -->|Send HTTPS 443| TG
  TG --> HR
  TG --> IT
  TG --> ADMIN
```

## 2) Flowchart — Monitoring Logic (Polling / Routing / DRY RUN)

```mermaid
   flowchart TD
  A([Start monitor]) --> B[Load config departments.json]
  B --> C{Config found}
  C -- No --> C1[Log missing config<br/>Exit]
  C -- Yes --> D[Init logger and load last_seen state]
  D --> E{CSV exists}
  E -- No --> E1[Log CSV not found<br/>Sleep poll interval] --> E
  E -- Yes --> F[Read CSV safely]
  F --> G{New rows}
  G -- No --> G1[Sleep poll interval] --> E
  G -- Yes --> H[Parse new rows]
  H --> I[For each row get Dept]
  I --> J{Dept mapped}
  J -- No --> J1[Log unknown dept<br/>Skip row] --> I
  J -- Yes --> K{Dry run enabled}
  K -- Yes --> K1[Log DRY RUN would notify dept] --> L[Update last_seen state]
  K -- No --> K2[Send Telegram message to dept chat] --> L
  L --> M[Write last_seen.json and logs]
  M --> G1
```

## 3) Sequence Diagram — “New row detected → Telegram notify”

```mermaid
   sequenceDiagram
  autonumber
  participant S as Scheduler/Service
  participant M as monitor_biotime.py
  participant F as SMB Share (CSV)
  participant C as departments.json (runtime)
  participant T as Telegram API

  S->>M: Start process / run loop
  M->>C: Load config (dry_run, dept tokens/chat_ids)
  M->>F: Check CSV exists
  F-->>M: Exists
  M->>F: Read CSV + determine last_seen
  F-->>M: Rows (N)
  M->>M: Compare with last_seen → detect +Δ rows
  alt dry_run=true
    M->>M: Log "[DRY RUN] Would notify dept=IT"
  else dry_run=false
    M->>T: POST message (HTTPS 443)
    T-->>M: 200 OK (message_id)
  end
  M->>M: Update last_seen.json + write logs
  M->>M: Sleep poll_interval → next loop
```
## 4) State Diagram — Runtime behavior (safe + ops-friendly)

```mermaid
   stateDiagram-v2
  [*] --> Starting
  Starting --> LoadConfig
  LoadConfig --> MissingConfig: config not found
  MissingConfig --> [*]

  LoadConfig --> WaitingForCSV
  WaitingForCSV --> WaitingForCSV: CSV missing (sleep)
  WaitingForCSV --> ReadingCSV: CSV found

  ReadingCSV --> NoChanges: no new rows
  ReadingCSV --> Processing: new rows detected
  NoChanges --> WaitingForCSV: sleep

  Processing --> Routing
  Routing --> SkipUnknownDept: dept not mapped
  SkipUnknownDept --> Processing: next row

  Routing --> DryRun: dry_run=true
  Routing --> Sending: dry_run=false

  DryRun --> PersistState
  Sending --> PersistState: send ok
  Sending --> ErrorBackoff: send failed

  ErrorBackoff --> WaitingForCSV: sleep/backoff
  PersistState --> WaitingForCSV: next loop
```

## Notes (Sanitization)
- Use placeholders only (FILE-SRV / sample paths / no real tokens)
- Real tokens/chat IDs must live only in config/departments.json (not committed)

