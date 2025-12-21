import json
import os
from datetime import datetime

from utils.logger import setup_logger

CONFIG_PATH = os.path.join("config", "departments.json")
CONFIG_EXAMPLE_PATH = os.path.join("config", "departments.example.json")

logger = setup_logger()


def load_config():
    if os.path.exists(CONFIG_PATH):
        with open(CONFIG_PATH, "r", encoding="utf-8") as f:
            return json.load(f)

    logger.error("Missing config file: %s", CONFIG_PATH)
    logger.info("Create it by copying the example:")
    logger.info("  %s  ->  %s", CONFIG_EXAMPLE_PATH, CONFIG_PATH)
    logger.warning("Do NOT commit departments.json to GitHub (contains secrets).")
    return None


def main():
    cfg = load_config()
    if not cfg:
        return

    csv_path = cfg.get("csv_path")
    poll_interval = cfg.get("poll_interval_seconds", 2)

    logger.info("=== BioTime Telegram Alert System ===")
    logger.info("Start time: %s", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    logger.info("CSV Path: %s", csv_path)
    logger.info("Poll Interval (seconds): %s", poll_interval)

    if not csv_path:
        logger.error("csv_path is missing in config.")
        return

    if os.path.exists(csv_path):
        logger.info("CSV file found.")
    else:
        logger.warning("CSV file NOT found (path/permission/share?).")
        logger.warning("Check SMB path, credentials, and share permissions.")


if __name__ == "__main__":
    main()
