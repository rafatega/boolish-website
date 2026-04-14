from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime, timedelta
from threading import Lock
from typing import Dict
from uuid import uuid4


@dataclass(frozen=True)
class StoredRunArtifacts:
    created_at: datetime
    map_html: str
    excel_bytes: bytes


class ExpiringRunStore:
    def __init__(self, ttl: timedelta) -> None:
        self._ttl = ttl
        self._items: Dict[str, StoredRunArtifacts] = {}
        self._lock = Lock()

    def save(self, map_html: str, excel_bytes: bytes) -> str:
        with self._lock:
            self._cleanup_locked()
            run_id = str(uuid4())
            self._items[run_id] = StoredRunArtifacts(
                created_at=datetime.now(UTC),
                map_html=map_html,
                excel_bytes=excel_bytes,
            )
            return run_id

    def get(self, run_id: str) -> StoredRunArtifacts | None:
        with self._lock:
            self._cleanup_locked()
            return self._items.get(run_id)

    def _cleanup_locked(self) -> None:
        now = datetime.now(UTC)
        expired_ids = [
            run_id
            for run_id, item in self._items.items()
            if now - item.created_at > self._ttl
        ]
        for run_id in expired_ids:
            del self._items[run_id]
