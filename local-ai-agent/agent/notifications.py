import os
import httpx
from typing import Any

class NotificationClient:
    def __init__(self):
        self.backend = os.getenv("ALERT_BACKEND", "custom").lower()
        self.alert_url = os.getenv("ALERT_URL")
        self.alert_token = os.getenv("ALERT_TOKEN")
        self.pushover_user = os.getenv("PUSHOVER_USER")
        self.pushover_token = os.getenv("PUSHOVER_TOKEN")

    def send(self, title: str, message: str, data: dict[str, Any] | None = None) -> bool:
        if self.backend == "pushover":
            return self._send_pushover(title, message)
        return self._send_custom(title, message, data)

    def _send_custom(self, title: str, message: str, data: dict[str, Any] | None = None) -> bool:
        if not self.alert_url or not self.alert_token:
            print("[NOTIFICATION] Missing ALERT_URL or ALERT_TOKEN for custom webhook.")
            return False
        payload = {
            "token": self.alert_token,
            "title": title,
            "message": message,
            "data": data or {},
        }
        try:
            response = httpx.post(self.alert_url, json=payload, timeout=10)
            if response.status_code == 200:
                return True
            print(f"[NOTIFICATION] Custom webhook failure: {response.status_code} {response.text}")
        except Exception as exc:
            print(f"[NOTIFICATION] Custom webhook error: {exc}")
        return False

    def _send_pushover(self, title: str, message: str) -> bool:
        if not self.pushover_user or not self.pushover_token:
            print("[NOTIFICATION] Missing PUSHOVER_USER or PUSHOVER_TOKEN.")
            return False
        payload = {
            "token": self.pushover_token,
            "user": self.pushover_user,
            "title": title,
            "message": message,
        }
        try:
            response = httpx.post("https://api.pushover.net/1/messages.json", data=payload, timeout=10)
            if response.status_code == 200:
                return True
            print(f"[NOTIFICATION] Pushover failure: {response.status_code} {response.text}")
        except Exception as exc:
            print(f"[NOTIFICATION] Pushover error: {exc}")
        return False
