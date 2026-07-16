from __future__ import annotations

import json
import os
import time
import uuid
from collections import OrderedDict
from pathlib import Path

from backend.app.core.logging import get_logger

logger = get_logger(__name__)

_MemoryEntry = list[dict[str, str]]


class ConversationMemory:
    def __init__(
        self,
        window_size: int = 10,
        session_ttl: int = 3600,
        persist_path: str | None = None,
    ) -> None:
        self._window_size = window_size
        self._session_ttl = session_ttl
        self._sessions: dict[str, _MemoryEntry] = OrderedDict()
        self._session_timestamps: dict[str, float] = {}
        self._persist_path = Path(persist_path) if persist_path else None
        self._load_from_disk()

    def _load_from_disk(self) -> None:
        if self._persist_path and self._persist_path.exists():
            try:
                data = json.loads(self._persist_path.read_text())
                self._sessions = OrderedDict(
                    (k, v) for k, v in data.get("sessions", {}).items()
                )
                self._session_timestamps = data.get("timestamps", {})
                logger.info(f"Loaded {len(self._sessions)} session(s) from disk")
            except Exception as e:
                logger.warning(f"Failed to load persisted sessions: {e}")

    def _save_to_disk(self) -> None:
        if self._persist_path:
            try:
                self._persist_path.parent.mkdir(parents=True, exist_ok=True)
                data = {
                    "sessions": dict(self._sessions),
                    "timestamps": self._session_timestamps,
                }
                self._persist_path.write_text(json.dumps(data, indent=2))
            except Exception as e:
                logger.warning(f"Failed to persist sessions: {e}")

    def get_or_create_session(self, session_id: str | None = None) -> str:
        sid = session_id or uuid.uuid4().hex
        if sid not in self._sessions:
            self._sessions[sid] = []
            self._session_timestamps[sid] = time.time()
            logger.debug(f"Created new session: {sid}")
        self._session_timestamps[sid] = time.time()
        return sid

    def add_message(self, session_id: str, role: str, content: str) -> None:
        self._evict_stale()
        if session_id not in self._sessions:
            self._sessions[session_id] = []
        history = self._sessions[session_id]
        history.append({"role": role, "content": content})
        if len(history) > self._window_size:
            self._sessions[session_id] = history[-self._window_size :]
        self._save_to_disk()

    def get_history(self, session_id: str) -> _MemoryEntry:
        self._evict_stale()
        return list(self._sessions.get(session_id, []))

    def clear_session(self, session_id: str) -> None:
        if session_id in self._sessions:
            del self._sessions[session_id]
            del self._session_timestamps[session_id]
            self._save_to_disk()

    def _evict_stale(self) -> None:
        now = time.time()
        stale = [
            sid
            for sid, ts in self._session_timestamps.items()
            if now - ts > self._session_ttl
        ]
        for sid in stale:
            del self._sessions[sid]
            del self._session_timestamps[sid]
        if stale:
            logger.debug(f"Evicted {len(stale)} stale session(s)")
            self._save_to_disk()
