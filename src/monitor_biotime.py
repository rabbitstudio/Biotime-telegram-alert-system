import json
import os
import time
from datetime import datetime
from typing import Any, Dict, Optional, Tuple

import pandas as pd

from utils.logger import setup_logger
from utils.telegram import send_telegram_message

CONFIG_PATH = os.path.join("config", "departments.json")
CONFIG_EXAMPLE_PATH = os.path.join("config", "departments.example.json")
STATE_PATH_DEFAULT = os.path.join("logs", "last_seen.json")

logger = setup_logger()


def load_config() -> Optional[Dict[str, Any]]:
    if os.path.exists(CONFIG_PATH):
        with open(CONFIG_PATH, "r", encoding="utf-8") as f:
            return json.load(f)

    logger.error("Missing config file: %s", CONFIG_PATH)
    logger.info("Create it by copying the example:")
    logger.info("  %s  ->  %s", CONFIG_EXAMPLE_PATH, CONFIG_PATH)
    logger.warning("Do NOT commit departments.json to GitHub (contains secrets).")
    return None


def read_csv_with_fallback(path: str) -> Tuple[Optional[pd.DataFrame], Optional[str]]:
    encodings = ["utf-8-sig", "utf-8", "cp874", "tis-620", "latin1"]
    last_err = None

    for enc in encodings:
        try:
            df = pd.read_csv(
                path,
                dtype=str,
                keep_default_na=False,
                encoding=enc,
                engine="python",
            )
            return df, enc
        except Exception as e:
            last_err = e

    logger.error("Failed to read CSV with all encodings. Last error: %s", last_err)
    return None, None


def load_state(state_path: str) -> Dict[str, Any]:
    os.makedirs(os.path.dirname(state_path), exist_ok=True)
    if not os.path.exists(state_path):
        return {"last_row_count": None}

    try:
        with open(state_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        logger.warning("State file corrupted/unreadable (%s). Resetting state. Error: %s", state_path, e)
        return {"last_row_count": None}


def save_state(state_path: str, state: Dict[str, Any]) -> None:
    os.makedirs(os.path.dirname(state_path), exist_ok=True)
    with open(state_path, "w", encoding="utf-8") as f:
        json.dump(state, f, ensure_ascii=False, indent=2)


def pick_department(row: Dict[str, str], dept_col: str) -> str:
    candidates = [dept_col, "Department", "DEPARTMENT", "dept", "Dept"]
    for c in candidates:
        v = (row.get(c) or "").strip()
        if v:
            return v
    return "UNKNOWN"


def format_message(row: Dict[str, str], dept: str) -> str:
    lines = [f"📣 BioTime Alert", f"🏢 Dept: {dept}"]
    shown = 0
    for k, v in row.items():
        if not v:
            continue
        if k.lower() in ["department", "dept"]:
            continue
        lines.append(f"- {k}: {v}")
        shown += 1
        if shown >= 8:
            break
    return "\n".join(lines)


def build_dept_map(cfg: Dict[str, Any]) -> Dict[str, Dict[str, str]]:
    """
    Returns dict: dept_name -> {"telegram_bot_token": "...", "chat_id": "..."}
    """
    dept_map: Dict[str, Dict[str, str]] = {}
    for d in cfg.get("departments", []):
        name = (d.get("name") or "").strip()
        if not name:
            continue
        dept_map[name] = {
            "telegram_bot_token": (d.get("telegram_bot_token") or "").strip(),
            "chat_id": str(d.get("chat_id") or "").strip(),
        }
    return dept_map


def get_admin_target(cfg: Dict[str, Any]) -> Dict[str, str]:
    admin = cfg.get("admin", {}) or {}
    return {
        "telegram_bot_token": (admin.get("telegram_bot_token") or "").strip(),
        "chat_id": str(admin.get("chat_id") or "").strip(),
    }


def main():
    cfg = load_config()
    if not cfg:
        return

    csv_path = cfg.get("csv_path")
    poll_interval = int(cfg.get("poll_interval_seconds", 2))
    dept_col = cfg.get("department_column", "Department")
    dry_run = bool(cfg.get("dry_run", True))
    state_path = cfg.get("state_path", STATE_PATH_DEFAULT)

    dept_map = build_dept_map(cfg)
    admin_target = get_admin_target(cfg)

    logger.info("=== BioTime Telegram Alert System (DRY RUN=%s) ===", dry_run)
    logger.info("Start time: %s", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    logger.info("CSV Path: %s", csv_path)
    logger.info("Poll Interval (seconds): %s", poll_interval)
    logger.info("Departments configured: %s", list(dept_map.keys()))

    if not csv_path:
        logger.error("csv_path is missing in config.")
        return

    state = load_state(state_path)
    last_row_count = state.get("last_row_count")

    while True:
        try:
            if not os.path.exists(csv_path):
                logger.warning("CSV not found. Waiting... (%s)", csv_path)
                time.sleep(poll_interval)
                continue

            df, enc = read_csv_with_fallback(csv_path)
            if df is None:
                time.sleep(poll_interval)
                continue

            row_count = len(df)

            # First run: initialize without spamming old rows
            if last_row_count is None:
                last_row_count = row_count
                state["last_row_count"] = last_row_count
                save_state(state_path, state)
                logger.info("Initialized state at row_count=%s (encoding=%s)", row_count, enc)
                time.sleep(poll_interval)
                continue

            # CSV reset/rotated
            if row_count < last_row_count:
                logger.warning("CSV row_count decreased (%s -> %s). Treat as reset.", last_row_count, row_count)
                last_row_count = row_count
                state["last_row_count"] = last_row_count
                save_state(state_path, state)
                time.sleep(poll_interval)
                continue

            # New rows appended
            if row_count > last_row_count:
                new_df = df.iloc[last_row_count:row_count]
                logger.info("New rows detected: +%s (encoding=%s)", row_count - last_row_count, enc)

                for _, r in new_df.iterrows():
                    row_dict = {k: str(v).strip() for k, v in r.to_dict().items()}
                    dept = pick_department(row_dict, dept_col)
                    msg = format_message(row_dict, dept)

                    target = dept_map.get(dept)
                    if not target:
                        logger.warning("No target config for dept=%s. Skipping send.", dept)
                        logger.info("[DRY RUN] Message would be:\n%s", msg)
                        continue

                    if dry_run:
                        logger.info("[DRY RUN] Would notify dept=%s\n%s", dept, msg)
                    else:
                        try:
                            mid = send_telegram_message(
                                bot_token=target["telegram_bot_token"],
                                chat_id=target["chat_id"],
                                text=msg,
                            )
                            logger.info("✅ Sent Telegram to dept=%s message_id=%s", dept, mid)
                        except Exception as e:
                            logger.error("❌ Telegram send failed dept=%s error=%s", dept, e)

                # Update state after processing new rows
                last_row_count = row_count
                state["last_row_count"] = last_row_count
                save_state(state_path, state)

            time.sleep(poll_interval)

        except KeyboardInterrupt:
            logger.info("Stopped by user (Ctrl+C).")
            break
        except Exception as e:
            logger.exception("Unexpected error: %s", e)
            time.sleep(poll_interval)


if __name__ == "__main__":
    main()
