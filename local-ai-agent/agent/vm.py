import shutil
import subprocess
from typing import Any

class VMManager:
    def __init__(self):
        self.vboxmanage = shutil.which('VBoxManage')
        self.simulate = not bool(self.vboxmanage)
        self.simulated_commands: list[str] = []

    def _run(self, args: list[str]) -> dict[str, Any]:
        cmd = [self.vboxmanage] + args if self.vboxmanage else ['VBoxManage'] + args
        if self.simulate:
            self.simulated_commands.append(' '.join(cmd))
            return {'simulated': True, 'cmd': ' '.join(cmd)}
        try:
            completed = subprocess.run(
                [self.vboxmanage] + args,
                capture_output=True,
                text=True,
                check=False,
                timeout=60,
            )
            return {
                'returncode': completed.returncode,
                'stdout': completed.stdout.strip(),
                'stderr': completed.stderr.strip(),
            }
        except subprocess.TimeoutExpired:
            return {'error': 'VBoxManage timed out'}

    def list_vms(self) -> dict[str, Any]:
        result = self._run(['list', 'vms'])
        if result.get('returncode') != 0:
            return result
        vms = []
        for line in result['stdout'].splitlines():
            if line.strip():
                name = line.split('"')[1]
                vms.append(name)
        return {'vms': vms}

    def start_vm(self, name: str) -> dict[str, Any]:
        return self._run(['startvm', name, '--type', 'headless'])

    def stop_vm(self, name: str) -> dict[str, Any]:
        return self._run(['controlvm', name, 'acpipowerbutton'])

    def get_vm_info(self, name: str) -> dict[str, Any]:
        return self._run(['showvminfo', name, '--machinereadable'])

    def create_vm(self, name: str, iso_path: str | None = None) -> dict[str, Any]:
        if not iso_path:
            return {'error': 'ISO path required to create a VM.'}
        # proceed with commands (they will be simulated if VBoxManage is not available)
        create_result = self._run([
            'createvm', '--name', name, '--register'
        ])
        if not create_result.get('simulated') and create_result.get('returncode') != 0:
            return create_result
        storage_result = self._run([
            'storagectl', name, '--name', 'SATA Controller', '--add', 'sata', '--controller', 'IntelAhci'
        ])
        if not storage_result.get('simulated') and storage_result.get('returncode') != 0:
            return storage_result
        self._run([
            'createhd', '--filename', f'{name}.vdi', '--size', '32768'
        ])
        self._run([
            'storageattach', name, '--storagectl', 'SATA Controller', '--port', '0', '--device', '0', '--type', 'hdd', '--medium', f'{name}.vdi'
        ])
        self._run([
            'storageattach', name, '--storagectl', 'SATA Controller', '--port', '1', '--device', '0', '--type', 'dvddrive', '--medium', iso_path
        ])
        if self.simulate:
            return {
                'status': 'simulated',
                'vm': name,
                'iso': iso_path,
                'commands': self.simulated_commands,
            }
        return {'status': 'created', 'vm': name, 'iso': iso_path}

    def create_kali_vm(self, name: str, iso_path: str | None = None) -> dict[str, Any]:
        return self.create_vm(name, iso_path)
