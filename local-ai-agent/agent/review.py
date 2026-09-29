import json
import os
import threading
import uuid
from datetime import datetime

DEFAULT_STORAGE = os.path.join(os.path.dirname(__file__), '..', 'review_queue.json')

class ReviewManager:
    def __init__(self, storage_path: str | None = None):
        self.storage_path = os.path.abspath(storage_path or DEFAULT_STORAGE)
        self.lock = threading.Lock()
        self.pending = self._load()

    def _load(self) -> dict:
        if os.path.exists(self.storage_path):
            try:
                with open(self.storage_path, 'r', encoding='utf-8') as handle:
                    return json.load(handle)
            except Exception:
                return {}
        return {}

    def _save(self) -> None:
        os.makedirs(os.path.dirname(self.storage_path), exist_ok=True)
        with open(self.storage_path, 'w', encoding='utf-8') as handle:
            json.dump(self.pending, handle, indent=2)

    def add_request(self, action: dict) -> dict:
        request_id = uuid.uuid4().hex
        record = {
            'id': request_id,
            'created_at': datetime.utcnow().isoformat() + 'Z',
            'status': 'pending',
            'action': action,
        }
        with self.lock:
            self.pending[request_id] = record
            self._save()
        return record

    def list_requests(self) -> list:
        with self.lock:
            return list(self.pending.values())

    def get_request(self, request_id: str) -> dict | None:
        return self.pending.get(request_id)

    def confirm_request(self, request_id: str) -> dict:
        with self.lock:
            request = self.pending.get(request_id)
            if request is None:
                raise KeyError('request not found')
            request['status'] = 'confirmed'
            request['confirmed_at'] = datetime.utcnow().isoformat() + 'Z'
            self._save()
            return request

    def cancel_request(self, request_id: str) -> dict:
        with self.lock:
            request = self.pending.get(request_id)
            if request is None:
                raise KeyError('request not found')
            request['status'] = 'cancelled'
            request['cancelled_at'] = datetime.utcnow().isoformat() + 'Z'
            self._save()
            return request

    def complete_request(self, request_id: str, result: dict) -> dict:
        with self.lock:
            request = self.pending.get(request_id)
            if request is None:
                raise KeyError('request not found')
            request['status'] = 'completed'
            request['completed_at'] = datetime.utcnow().isoformat() + 'Z'
            request['result'] = result
            self._save()
            return request
