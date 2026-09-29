import os
import re
import httpx
from dotenv import load_dotenv
from datetime import datetime
from .notifications import NotificationClient

load_dotenv()

SAFE_COMMAND_PATTERNS = [
    r"^dir( /[A-Za-z]+)?$",
    r"^echo .+",
    r"^type .+",
    r"^ping .+",
    r"^whoami$",
    r"^ipconfig( /all)?$",
]

DANGEROUS_COMMAND_PATTERNS = [
    r"(^|\s)(del|erase)\s+.+",
    r"(^|\s)(format|diskpart|shutdown|reboot|restart|taskkill|rmdir|rd)\b",
    r"(^|\s)(powershell|pwsh)\b.*-Command",
    r"(^|\s)(curl|wget)\s+.*https?://",
    r"(^|\s)net\s+user\b",
    r"(^|\s)whoami\s+/all",
]

class SecurityMonitor:
    def __init__(self):
        self.alert_url = os.getenv("ALERT_URL")
        self.alert_token = os.getenv("ALERT_TOKEN")
        self.notifications = NotificationClient()

    def is_dangerous(self, command: str) -> bool:
        normalized = command.strip().lower()
        for pattern in DANGEROUS_COMMAND_PATTERNS:
            if re.search(pattern, normalized):
                return True
        return False

    def requires_confirmation(self, command: str) -> bool:
        return self.is_dangerous(command)

    def is_blocked(self, command: str) -> bool:
        return self.is_dangerous(command)

    def log_command(self, command: str, returncode: int, output: str) -> None:
        timestamp = datetime.utcnow().isoformat() + "Z"
        entry = {
            "timestamp": timestamp,
            "command": command,
            "returncode": returncode,
            "output": output,
            "dangerous": self.is_dangerous(command),
        }
        print("[SECURITY LOG]", entry)
        if entry["dangerous"]:
            self.send_alert(entry)

    def log_blocked_command(self, command: str) -> None:
        timestamp = datetime.utcnow().isoformat() + "Z"
        entry = {
            "timestamp": timestamp,
            "command": command,
            "status": "blocked",
            "dangerous": True,
        }
        print("[SECURITY LOG]", entry)
        self.send_alert(entry)

    def send_alert(self, entry: dict) -> None:
        title = "Security Alert: Dangerous command"
        message = f"Command: {entry.get('command')}\nStatus: {entry.get('status', 'executed')}"
        self.notifications.send(title, message, data=entry)
