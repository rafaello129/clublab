from __future__ import annotations

import getpass
import json
import os
from collections import deque
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


class AuditLogger:
    """Structured instructor-side audit log.

    Only known operational metadata is accepted. Secrets, env dumps and
    arbitrary subprocess output must never be written here.
    """

    def __init__(self, runtime_dir: Path) -> None:
        self.root = runtime_dir / "audit"
        self.path = self.root / "clublabctl.jsonl"

    def write(
        self,
        *,
        action: str,
        result: str,
        team: str | None = None,
        scenario: str | None = None,
        meta: dict[str, Any] | None = None,
    ) -> None:
        self.root.mkdir(parents=True, exist_ok=True)
        try:
            os.chmod(self.root, 0o700)
        except OSError:
            pass

        event: dict[str, Any] = {
            "ts": datetime.now(timezone.utc).isoformat(),
            "actor": getpass.getuser(),
            "action": action,
            "result": result,
        }
        if team is not None:
            event["team"] = team
        if scenario is not None:
            event["scenario"] = scenario
        if meta:
            safe_meta = {
                key: value
                for key, value in meta.items()
                if key
                in {
                    "code",
                    "generation_id",
                    "source_team",
                    "assigned_team",
                    "check",
                }
            }
            if safe_meta:
                event["meta"] = safe_meta

        with self.path.open("a", encoding="utf-8") as handle:
            handle.write(
                json.dumps(
                    event,
                    sort_keys=True,
                    separators=(",", ":"),
                )
                + "\n"
            )

        try:
            os.chmod(self.path, 0o600)
        except OSError:
            pass

    def tail(self, lines: int = 30) -> list[dict[str, Any]]:
        if lines < 1 or lines > 500:
            raise ValueError("Audit lines must be between 1 and 500")
        if not self.path.exists():
            return []

        raw_lines: deque[str] = deque(maxlen=lines)
        with self.path.open("r", encoding="utf-8") as handle:
            for line in handle:
                raw_lines.append(line)

        events: list[dict[str, Any]] = []
        for raw in raw_lines:
            try:
                value = json.loads(raw)
            except json.JSONDecodeError:
                continue
            if isinstance(value, dict):
                events.append(value)
        return events
