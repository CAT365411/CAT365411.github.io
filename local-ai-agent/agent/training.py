from .executor import CommandExecutor

class TrainingMode:
    TASKS = {
        'local_user': {
            'id': 'local_user',
            'title': 'Inspect current user',
            'description': 'Run a command to show the current Windows user account.',
            'command': 'whoami',
        },
        'network_info': {
            'id': 'network_info',
            'title': 'Inspect network configuration',
            'description': 'Review local network interfaces and IP settings.',
            'command': 'ipconfig /all',
        },
        'open_notepad': {
            'id': 'open_notepad',
            'title': 'Open Notepad',
            'description': 'Launch Notepad so you can practice typing or review a local file.',
            'command': 'start notepad',
        },
        'list_ports': {
            'id': 'list_ports',
            'title': 'List active network ports',
            'description': 'See active local ports and listening services with a safe system command.',
            'command': 'netstat -an',
        },
        'read_hosts': {
            'id': 'read_hosts',
            'title': 'View hosts file',
            'description': 'Open the Windows hosts file to learn how name resolution entries are configured.',
            'command': 'type C:\\Windows\\System32\\drivers\\etc\\hosts',
        },
    }

    def __init__(self):
        self.executor = CommandExecutor()

    def list_tasks(self) -> list[dict]:
        return list(self.TASKS.values())

    def get_task(self, task_id: str) -> dict | None:
        return self.TASKS.get(task_id)

    def execute_task(self, task_id: str) -> dict:
        task = self.get_task(task_id)
        if not task:
            raise KeyError('Task not found')
        output = self.executor.execute(task['command'])
        return {'task': task, 'output': output}
