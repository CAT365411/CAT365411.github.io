import subprocess
import shutil
from typing import Any

class GuestCommandManager:
    def __init__(self):
        self.ssh_cmd = shutil.which('ssh')
        self.powershell_cmd = shutil.which('powershell') or shutil.which('pwsh')

    def _run(self, args: list[str]) -> dict[str, Any]:
        try:
            completed = subprocess.run(
                args,
                capture_output=True,
                text=True,
                check=False,
                timeout=120,
            )
            return {
                'returncode': completed.returncode,
                'stdout': completed.stdout.strip(),
                'stderr': completed.stderr.strip(),
                'command': ' '.join(args),
            }
        except subprocess.TimeoutExpired:
            return {'error': 'timeout'}

    def run_ssh(self, host: str, user: str, command: str, port: int = 22, identity_file: str | None = None) -> dict[str, Any]:
        if not self.ssh_cmd:
            return {'error': 'ssh client not found on PATH'}
        args = [self.ssh_cmd, '-o', 'StrictHostKeyChecking=no', '-p', str(port)]
        if identity_file:
            args.extend(['-i', identity_file])
        args.append(f"{user}@{host}")
        args.append(command)
        return self._run(args)

    def run_winrm(self, host: str, user: str, password: str, command: str) -> dict[str, Any]:
        if not self.powershell_cmd:
            return {'error': 'PowerShell not found on PATH'}
        escaped_password = password.replace("'", "''")
        escaped_command = command.replace("'", "''")
        ps_script = (
            f"$pass = ConvertTo-SecureString '{escaped_password}' -AsPlainText -Force; "
            f"$cred = New-Object System.Management.Automation.PSCredential('{user}',$pass); "
            f"Invoke-Command -ComputerName '{host}' -Credential $cred -ScriptBlock {{ {escaped_command} }}"
        )
        args = [self.powershell_cmd, '-NoProfile', '-NonInteractive', '-Command', ps_script]
        return self._run(args)
