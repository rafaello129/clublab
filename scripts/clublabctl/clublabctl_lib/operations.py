from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

from .inventory import Inventory
from .state import StateStore


OK = 0
CONFIG = 3
CHECK_FAILED = 4
OPERATION_FAILED = 5
STATE_CONFLICT = 6
PARTIAL_SUCCESS = 7
DEPENDENCY_UNAVAILABLE = 8
SECURITY_GUARD = 9
NOT_IMPLEMENTED = 10


@dataclass
class OperationResult:
    team: str
    ok: bool
    detail: str
    code: int = OK


class ScenarioManager:
    def __init__(
        self,
        inventory: Inventory,
        runtime,
        state: StateStore,
        audit=None,
    ) -> None:
        self.inventory = inventory
        self.runtime = runtime
        self.state = state
        self.audit = audit

    def _audit(
        self,
        action: str,
        team: str,
        result: str,
        *,
        scenario: str | None = None,
        code: int | None = None,
    ) -> None:
        if not self.audit:
            return
        meta = {"code": code} if code is not None else None
        self.audit.write(
            action=action,
            result=result,
            team=team,
            scenario=scenario,
            meta=meta,
        )

    def expand_target(
        self,
        target: str,
        *,
        include_spare: bool = False,
    ) -> list[str]:
        if target != "all":
            if target not in self.inventory.teams:
                raise ValueError(f"Unknown target: {target}")
            return [target]

        deployed: list[str] = []
        for team in self.inventory.teams:
            if team == "spare" and not include_spare:
                continue
            try:
                if self.runtime.is_deployed(team):
                    deployed.append(team)
            except Exception:
                continue

        if not deployed:
            raise RuntimeError(
                "No deployed ClubLab teams were found"
            )
        return deployed

    def status_one(self, team: str) -> dict:
        expected = self.state.read(team).get(
            "expected_scenario",
            "normal",
        )
        if not self.runtime.is_deployed(team):
            return {
                "team": team,
                "infra_state": "ABSENT",
                "expected_scenario": expected,
                "observed_scenario": "absent",
            }

        observed = self.runtime.get_app_scenario(team)
        infra = (
            "SCENARIO"
            if observed != "normal"
            else "READY"
        )
        return {
            "team": team,
            "infra_state": infra,
            "expected_scenario": expected,
            "observed_scenario": observed,
        }

    def load_one(
        self,
        team: str,
        scenario: str,
    ) -> OperationResult:
        if scenario not in self.inventory.scenarios:
            raise ValueError(
                f"Unknown scenario: {scenario}"
            )
        if scenario == "normal":
            return self.clear_one(team)

        self.state.write(
            team,
            infra_state="SCENARIO",
            expected_scenario=scenario,
        )

        try:
            if scenario == "ranking-db-failure":
                self.runtime.start_api(team)
                self.runtime.set_app_scenario(
                    team,
                    "ranking-db-failure",
                )
            elif scenario == "api-down":
                try:
                    if (
                        self.runtime.get_app_scenario(team)
                        != "normal"
                    ):
                        self.runtime.set_app_scenario(
                            team,
                            "normal",
                        )
                except Exception:
                    pass
                self.runtime.stop_api(team)
            else:
                raise ValueError(
                    f"Unsupported scenario: {scenario}"
                )

            self.runtime.validate_scenario(
                team,
                scenario,
            )
            self._audit(
                "scenario.load",
                team,
                "success",
                scenario=scenario,
                code=OK,
            )
            return OperationResult(
                team,
                True,
                f"scenario={scenario}",
            )
        except Exception as exc:
            self.state.write(
                team,
                infra_state="FAILED",
                expected_scenario=scenario,
            )
            self._audit(
                "scenario.load",
                team,
                "failure",
                scenario=scenario,
                code=OPERATION_FAILED,
            )
            return OperationResult(
                team,
                False,
                str(exc),
                OPERATION_FAILED,
            )

    def clear_one(
        self,
        team: str,
    ) -> OperationResult:
        self.state.write(
            team,
            infra_state="RECOVERING",
            expected_scenario="normal",
        )

        try:
            if not self.runtime.is_deployed(team):
                raise RuntimeError(
                    "team is not deployed"
                )

            observed = self.runtime.get_app_scenario(
                team
            )
            if observed == "api-down":
                self.runtime.start_api(team)

            self.runtime.set_app_scenario(
                team,
                "normal",
            )
            self.runtime.validate_scenario(
                team,
                "normal",
            )
            self.state.write(
                team,
                infra_state="READY",
                expected_scenario="normal",
            )
            self._audit(
                "scenario.clear",
                team,
                "success",
                scenario="normal",
                code=OK,
            )
            return OperationResult(
                team,
                True,
                "scenario=normal",
            )
        except Exception as exc:
            self.state.write(
                team,
                infra_state="FAILED",
                expected_scenario="normal",
            )
            self._audit(
                "scenario.clear",
                team,
                "failure",
                scenario="normal",
                code=OPERATION_FAILED,
            )
            return OperationResult(
                team,
                False,
                str(exc),
                OPERATION_FAILED,
            )

    def recover_one(
        self,
        team: str,
    ) -> OperationResult:
        """Non-destructive instructor recovery.

        R1 clears the scenario.
        R2 restarts the API and clears the scenario.
        Reset is never automatic.
        """

        self.state.write(
            team,
            infra_state="RECOVERING",
            expected_scenario="normal",
        )

        first = self.clear_one(team)
        if first.ok:
            self._audit(
                "recover",
                team,
                "success",
                scenario="normal",
                code=OK,
            )
            return OperationResult(
                team,
                True,
                "R1 scenario clear succeeded",
            )

        try:
            self.runtime.restart_api(team)
            self.runtime.set_app_scenario(
                team,
                "normal",
            )
            self.runtime.validate_scenario(
                team,
                "normal",
            )
            self.state.write(
                team,
                infra_state="READY",
                expected_scenario="normal",
            )
            self._audit(
                "recover",
                team,
                "success",
                scenario="normal",
                code=OK,
            )
            return OperationResult(
                team,
                True,
                "R2 API restart succeeded",
            )
        except Exception as exc:
            self.state.write(
                team,
                infra_state="FAILED",
                expected_scenario="normal",
            )
            self._audit(
                "recover",
                team,
                "failure",
                scenario="normal",
                code=STATE_CONFLICT,
            )
            return OperationResult(
                team,
                False,
                "R1 failed: "
                f"{first.detail}; "
                f"R2 failed: {exc}. "
                "Explicit reset required.",
                STATE_CONFLICT,
            )

    def reset_one(
        self,
        team: str,
        *,
        confirmed: bool,
    ) -> OperationResult:
        if not confirmed:
            return OperationResult(
                team,
                False,
                "Reset requires --yes.",
                SECURITY_GUARD,
            )

        self.state.write(
            team,
            infra_state="RESETTING",
            expected_scenario="normal",
        )

        try:
            self.runtime.reset_team(team)
            self.state.write(
                team,
                infra_state="READY",
                expected_scenario="normal",
            )
            self._audit(
                "reset",
                team,
                "success",
                scenario="normal",
                code=OK,
            )
            return OperationResult(
                team,
                True,
                "reset complete",
            )
        except Exception as exc:
            self.state.write(
                team,
                infra_state="FAILED",
                expected_scenario="normal",
            )
            self._audit(
                "reset",
                team,
                "failure",
                scenario="normal",
                code=OPERATION_FAILED,
            )
            return OperationResult(
                team,
                False,
                str(exc),
                OPERATION_FAILED,
            )


def aggregate(
    results: Iterable[OperationResult],
) -> int:
    items = list(results)
    if not items:
        return CONFIG

    success = sum(
        1
        for item in items
        if item.ok
    )
    if success == len(items):
        return OK
    if success:
        return PARTIAL_SUCCESS
    return max(
        (
            item.code
            for item in items
        ),
        default=OPERATION_FAILED,
    )
