import json
import os
from datetime import datetime

CONFIG_PATH = os.path.join("config", "departments.json")
CONFIG_EXAMPLE_PATH = os.path.join("config", "departments.example.json")


def load_config():
    """
    Load runtime config from config/departments.json (NOT committed).
    If not found, print guidance and exit cleanly.
    """
    if os.path.exists(CONFIG_PATH):
        with open(CONFIG_PATH, "r", encoding="utf-8") as f:
            return json.load(f)

    print("❌ Missing config file:", CONFIG_PATH)
    print("✅ Create it by copying the example:")
    print(f"   {CONFIG_EXAMPLE_PATH}  ->  {CONFIG_PATH}")
    print("⚠️  Do NOT commit departments.json to GitHub (contains secrets).")
    return None


def main():
    cfg = load_config()
    if not cfg:
        return

    csv_path = cfg.get("csv_path")
    poll_interval = cfg.get("poll_interval_seconds", 2)

    print("=== BioTime Telegram Alert System ===")
    print("Start time:", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    print("CSV Path:", csv_path)
    print("Poll Interval (seconds):", poll_interval)

    if not csv_path:
        print("❌ csv_path is missing in config.")
        return

    # We only validate file existence at this step
    if os.path.exists(csv_path):
        print("✅ CSV file found.")
    else:
        print("⚠️  CSV file NOT found (path/permission/share?).")
        print("   Check SMB path, credentials, and share permissions.")


if __name__ == "__main__":
    main()
