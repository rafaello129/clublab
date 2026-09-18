from __future__ import annotations

import json
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


VALID_INFRA_STATES = {
    "ABSENT",
    "STARTING",
    "READY",
    "SCENARIO",
    "RECOVERING",
    "RESETTING",
    "DEGRADED",
    "FAILED",
}


class StateStore:
    def __init__(self, runtime_dir: Path) -> None:
        self.root = runtime_dir / "state"

    def path_for(self, team: str) -> Path:
        return self.root / f"{team}.json"

    def read(self, team: str) -> dict[str, Any]:
        path = self.path_for(team)
        if not path.exists():
            return {
                "schema": 1,
                "team": team,
                "infra_state": "ABSENT",
                "expected_scenario": "normal",
            }

        raw = json.loads(path.read_text(encoding="utf-8"))
        if raw.get("team") != team:
            raise ValueError(f"State file team mismatch for {team}")
        return raw

    def write(
        self,
        team: str,
        *,
        infra_state: str | None = None,
        expected_scenario: str | None = None,
        extra: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        if infra_state is not None and infra_state not in VALID_INFRA_STATES:
            raise ValueError(f"Invalid infra state: {infra_state}")

        current = self.read(team)
        if infra_state is not None:
            current["infra_state"] = infra_state
        if expected_scenario is not None:
            current["expected_scenario"] = expected_scenario
        if extra:
            current.update(extra)

        current["schema"] = 1
        current["team"] = team
        current["updated_at"] = datetime.now(timezone.utc).isoformat()

        self.root.mkdir(parents=True, exist_ok=True)
        try:
            os.chmod(self.root, 0o700)
        except OSError:
            pass

        path = self.path_for(team)
        tmp = path.with_suffix(".tmp")
        tmp.write_text(
            json.dumps(current, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
        try:
            os.chmod(tmp, 0o600)
        except OSError:
            pass
        tmp.replace(path)
        return current
