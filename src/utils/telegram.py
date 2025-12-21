import time
from typing import Optional

import requests


def send_telegram_message(
    bot_token: str,
    chat_id: str,
    text: str,
    timeout_sec: int = 10,
    retries: int = 3,
    retry_delay_sec: float = 1.5,
) -> Optional[str]:
    """
    Send a Telegram message. Returns Telegram message_id (as str) if available.
    Retries on transient failures.
    """
    if not bot_token or not chat_id:
        raise ValueError("bot_token/chat_id is missing")

    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": text,
        "disable_web_page_preview": True,
    }

    last_err = None
    for attempt in range(1, retries + 1):
        try:
            resp = requests.post(url, json=payload, timeout=timeout_sec)
            if resp.status_code == 200:
                data = resp.json()
                # Telegram returns {"ok":true,"result":{"message_id":...}}
                if isinstance(data, dict) and data.get("ok") and "result" in data:
                    return str(data["result"].get("message_id", ""))
                return ""
            else:
                last_err = RuntimeError(f"HTTP {resp.status_code}: {resp.text[:200]}")
        except Exception as e:
            last_err = e

        if attempt < retries:
            time.sleep(retry_delay_sec)

    # If all retries failed:
    raise RuntimeError(f"Telegram send failed after {retries} retries: {last_err}")
