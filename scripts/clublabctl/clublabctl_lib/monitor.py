from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from .inventory import Inventory
from .state import StateStore


TEAM_ROLES = (
    "frontend",
    "api",
    "database",
    "toolbox",
)


@dataclass(frozen=True)
class TeamStatus:
    team: str
    frontend: str
    api: str
    database: str
    toolbox: str
    scenario: str
    infra_state: str


class OperationalMonitor:
    def __init__(
        self,
        inventory: Inventory,
        runtime,
        state: StateStore,
    ) -> None:
        self.inventory = inventory
        self.runtime = runtime
        self.state = state

    def targets(self, target: str) -> list[str]:
        if target == "all":
            return list(self.inventory.teams)
        if target not in self.inventory.teams:
            raise ValueError(f"Unknown target: {target}")
        return [target]

    def status_one(self, team: str) -> TeamStatus:
        expected = self.state.read(team).get(
            "expected_scenario",
            "normal",
        )

        if not self.runtime.is_deployed(team):
            return TeamStatus(
                team=team,
                frontend="ABSENT",
                api="ABSENT",
                database="ABSENT",
                toolbox="ABSENT",
                scenario="absent",
                infra_state="ABSENT",
            )

        statuses: dict[str, str] = {}
        for role in TEAM_ROLES:
            try:
                statuses[role] = self.runtime.service_status(
                    team,
                    role,
                )
            except Exception:
                statuses[role] = "ERROR"

        if statuses["api"] == "DOWN":
            observed = "api-down"
        else:
            try:
                observed = self.runtime.get_app_scenario(team)
            except Exception:
                observed = "unknown"

        bad = any(
            value in {"DOWN", "ERROR", "ABSENT"}
            for value in statuses.values()
        )

        if bad and observed != "api-down":
            infra_state = "DEGRADED"
        elif observed != "normal":
            infra_state = "SCENARIO"
        elif all(value == "OK" for value in statuses.values()):
            infra_state = "READY"
        else:
            infra_state = "DEGRADED"

        # Expected scenario is intentionally not used to hide an observed
        # degradation. It remains in the state store for instructor context.
        _ = expected

        return TeamStatus(
            team=team,
            frontend=statuses["frontend"],
            api=statuses["api"],
            database=statuses["database"],
            toolbox=statuses["toolbox"],
            scenario=observed,
            infra_state=infra_state,
        )

    def resources(self, target: str) -> list[dict[str, Any]]:
        rows: list[dict[str, Any]] = []
        for team in self.targets(target):
            if not self.runtime.is_deployed(team):
                continue
            rows.extend(
                self.runtime.resource_rows(team)
            )
        return rows

    def logs(
        self,
        team: str,
        role: str,
        *,
        lines: int,
    ) -> str:
        if team not in self.inventory.teams:
            raise ValueError(f"Unknown target: {team}")
        if role not in TEAM_ROLES:
            raise ValueError(
                "Technical logs support only "
                + ", ".join(TEAM_ROLES)
            )
        if not 1 <= lines <= 500:
            raise ValueError("Log lines must be between 1 and 500")
        return self.runtime.technical_logs(
            team,
            role,
            lines=lines,
        )
