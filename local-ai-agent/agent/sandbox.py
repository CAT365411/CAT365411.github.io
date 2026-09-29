import json
import os
from pathlib import Path

STATE_FILE = Path(__file__).resolve().parent.parent / 'sandbox_state.json'

class SandboxManager:
    def __init__(self):
        self.state = {'enabled': False}
        self._load()

    def _load(self):
        try:
            if STATE_FILE.exists():
                with open(STATE_FILE, 'r', encoding='utf-8') as handle:
                    self.state = json.load(handle)
        except Exception:
            self.state = {'enabled': False}

    def _save(self):
        try:
            with open(STATE_FILE, 'w', encoding='utf-8') as handle:
                json.dump(self.state, handle, indent=2)
        except Exception:
            pass

    def is_enabled(self) -> bool:
        return bool(self.state.get('enabled', False))

    def enable(self) -> dict:
        self.state['enabled'] = True
        self._save()
        return {'enabled': True}

    def disable(self) -> dict:
        self.state['enabled'] = False
        self._save()
        return {'enabled': False}

    def toggle(self) -> dict:
        self.state['enabled'] = not self.is_enabled()
        self._save()
        return {'enabled': self.is_enabled()}

    def status(self) -> dict:
        return {'enabled': self.is_enabled()}
