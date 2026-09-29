import subprocess
from .security import SecurityMonitor

class CommandExecutor:
    def __init__(self):
        self.security = SecurityMonitor()

    def execute(self, command: str, allow_dangerous: bool = False) -> str:
        if self.security.is_blocked(command) and not allow_dangerous:
            self.security.log_blocked_command(command)
            raise PermissionError("Blocked dangerous command")

        try:
            completed = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                check=False,
                timeout=60,
            )
            output = completed.stdout + completed.stderr
            self.security.log_command(command, completed.returncode, output)
            return output.strip()
        except subprocess.TimeoutExpired:
            return "Command timed out after 60 seconds."
