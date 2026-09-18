from __future__ import annotations

import json
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .audit import AuditLogger
from .inventory import Inventory
from .monitor import OperationalMonitor


class SpareManager:
    def __init__(
        self,
        inventory: Inventory,
        monitor: OperationalMonitor,
        runtime_dir: Path,
        audit: AuditLogger | None = None,
    ) -> None:
        self.inventory = inventory
        self.monitor = monitor
        self.path = runtime_dir / "state" / "spare.json"
        self.audit = audit

    def read_assignment(self) -> dict[str, Any] | None:
        if not self.path.exists():
            return None
        raw = json.loads(self.path.read_text(encoding="utf-8"))
        if not isinstance(raw, dict):
            raise ValueError("Invalid spare assignment state")
        return raw

    def _write_assignment(self, value: dict[str, Any]) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        try:
            os.chmod(self.path.parent, 0o700)
        except OSError:
            pass

        tmp = self.path.with_suffix(".tmp")
        tmp.write_text(
            json.dumps(value, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
        try:
            os.chmod(tmp, 0o600)
        except OSError:
            pass
        tmp.replace(self.path)

    def status(self) -> dict[str, Any]:
        status = self.monitor.status_one("spare")
        return {
            "team": "spare",
            "infra_state": status.infra_state,
            "frontend": status.frontend,
            "api": status.api,
            "database": status.database,
            "toolbox": status.toolbox,
            "scenario": status.scenario,
            "assignment": self.read_assignment(),
            "access_port": self.inventory.teams["spare"]["access_port"],
        }

    def assign(self, team: str) -> dict[str, Any]:
        if team == "spare" or team not in self.inventory.teams:
            raise ValueError(f"Invalid spare assignment target: {team}")

        spare = self.monitor.status_one("spare")
        if (
            spare.infra_state != "READY"
            or spare.scenario != "normal"
        ):
            raise RuntimeError(
                "Spare is not READY in normal scenario"
            )

        existing = self.read_assignment()
        if existing:
            if existing.get("assigned_team") == team:
                return existing
            raise RuntimeError(
                "Spare is already assigned to "
                f"{existing.get('assigned_team')}"
            )

        value = {
            "schema": 1,
            "assigned_team": team,
            "assigned_at": datetime.now(timezone.utc).isoformat(),
            "access_port": self.inventory.teams["spare"]["access_port"],
        }
        self._write_assignment(value)

        if self.audit:
            self.audit.write(
                action="spare.assign",
                result="success",
                team="spare",
                meta={"assigned_team": team},
            )
        return value

    def release(self) -> bool:
        existing = self.read_assignment()
        if not existing:
            return False

        assigned_team = str(existing.get("assigned_team") or "")
        self.path.unlink(missing_ok=True)

        if self.audit:
            self.audit.write(
                action="spare.release",
                result="success",
                team="spare",
                meta={"assigned_team": assigned_team},
            )
        return True
