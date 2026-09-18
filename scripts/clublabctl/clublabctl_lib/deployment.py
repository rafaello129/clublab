from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

from .audit import AuditLogger
from .inventory import Inventory
from .operations import (
    CHECK_FAILED,
    CONFIG,
    OK,
    OPERATION_FAILED,
    STATE_CONFLICT,
    OperationResult,
    aggregate,
)
from .preflight import PreflightRunner, has_critical_failure
from .state import StateStore


@dataclass(frozen=True)
class SmokeCheck:
    name: str
    ok: bool
    detail: str


class DeploymentManager:
    """Deploy and validate ClubLab team stacks.

    Deployment is intentionally fail-closed:
    - preflight must pass;
    - an already deployed team must already be READY/normal;
    - no deployment command resets or destroys existing data.
    """

    def __init__(
        self,
        inventory: Inventory,
        runtime,
        state: StateStore,
        preflight: PreflightRunner,
        audit: AuditLogger | None = None,
    ) -> None:
        self.inventory = inventory
        self.runtime = runtime
        self.state = state
        self.preflight = preflight
        self.audit = audit

    def targets(self, target: str) -> list[str]:
        if target != "all":
            if target not in self.inventory.teams:
                raise ValueError(f"Unknown target: {target}")
            return [target]

        return [
            name
            for name, cfg in self.inventory.teams.items()
            if cfg.get("enabled_by_default")
        ]

    def _audit(
        self,
        action: str,
        team: str,
        result: str,
        *,
        code: int,
    ) -> None:
        if self.audit:
            self.audit.write(
                action=action,
                result=result,
                team=team,
                meta={"code": code},
            )

    def smoke_one(self, team: str) -> list[SmokeCheck]:
        if team not in self.inventory.teams:
            raise ValueError(f"Unknown target: {team}")

        raw = self.runtime.smoke_checks(team)
        checks = [
            SmokeCheck(
                name=str(item["name"]),
                ok=bool(item["ok"]),
                detail=str(item["detail"]),
            )
            for item in raw
        ]

        if not checks:
            return [
                SmokeCheck(
                    "smoke",
                    False,
                    "runtime returned no checks",
                )
            ]

        return checks

    def smoke_result(self, team: str) -> OperationResult:
        try:
            checks = self.smoke_one(team)
        except Exception as exc:
            self._audit(
                "smoke",
                team,
                "failure",
                code=CHECK_FAILED,
            )
            return OperationResult(
                team,
                False,
                str(exc),
                CHECK_FAILED,
            )

        failed = [
            item
            for item in checks
            if not item.ok
        ]

        if failed:
            detail = "; ".join(
                f"{item.name}: {item.detail}"
                for item in failed
            )
            self._audit(
                "smoke",
                team,
                "failure",
                code=CHECK_FAILED,
            )
            return OperationResult(
                team,
                False,
                detail,
                CHECK_FAILED,
            )

        self._audit(
            "smoke",
            team,
            "success",
            code=OK,
        )
        return OperationResult(
            team,
            True,
            f"{len(checks)} smoke checks passed",
        )

    def deploy_one(self, team: str) -> OperationResult:
        if team not in self.inventory.teams:
            raise ValueError(f"Unknown target: {team}")

        if self.runtime.is_deployed(team):
            try:
                observed = self.runtime.get_app_scenario(team)
            except Exception as exc:
                self._audit(
                    "deploy",
                    team,
                    "failure",
                    code=STATE_CONFLICT,
                )
                return OperationResult(
                    team,
                    False,
                    "team is partially deployed or unreadable: "
                    f"{exc}",
                    STATE_CONFLICT,
                )

            if observed != "normal":
                self._audit(
                    "deploy",
                    team,
                    "failure",
                    code=STATE_CONFLICT,
                )
                return OperationResult(
                    team,
                    False,
                    "team already deployed with scenario "
                    f"{observed}; clear/recover it first",
                    STATE_CONFLICT,
                )

            smoke = self.smoke_result(team)
            if smoke.ok:
                self.state.write(
                    team,
                    infra_state="READY",
                    expected_scenario="normal",
                )
                self._audit(
                    "deploy",
                    team,
                    "success",
                    code=OK,
                )
                return OperationResult(
                    team,
                    True,
                    "already deployed and healthy",
                )

            self._audit(
                "deploy",
                team,
                "failure",
                code=STATE_CONFLICT,
            )
            return OperationResult(
                team,
                False,
                "team already exists but is not healthy: "
                f"{smoke.detail}. Recover or reset explicitly.",
                STATE_CONFLICT,
            )

        checks = self.preflight.run(team)
        if has_critical_failure(checks):
            failed = [
                f"{item.category}/{item.name}: {item.detail}"
                for item in checks
                if item.status == "FAIL" and item.critical
            ]
            self._audit(
                "deploy",
                team,
                "failure",
                code=CHECK_FAILED,
            )
            return OperationResult(
                team,
                False,
                "preflight failed: " + "; ".join(failed),
                CHECK_FAILED,
            )

        self.state.write(
            team,
            infra_state="STARTING",
            expected_scenario="normal",
        )

        try:
            self.runtime.deploy_team(team)
            self.runtime.ensure_gateway()
            self.runtime.attach_gateway_to_team(team)

            smoke = self.smoke_result(team)
            if not smoke.ok:
                raise RuntimeError(
                    f"post-deploy smoke failed: {smoke.detail}"
                )

            self.state.write(
                team,
                infra_state="READY",
                expected_scenario="normal",
            )
            self._audit(
                "deploy",
                team,
                "success",
                code=OK,
            )
            return OperationResult(
                team,
                True,
                "READY",
            )
        except Exception as exc:
            self.state.write(
                team,
                infra_state="FAILED",
                expected_scenario="normal",
            )
            self._audit(
                "deploy",
                team,
                "failure",
                code=OPERATION_FAILED,
            )
            return OperationResult(
                team,
                False,
                str(exc),
                OPERATION_FAILED,
            )

    def deploy(self, target: str) -> tuple[list[OperationResult], int]:
        results = [
            self.deploy_one(team)
            for team in self.targets(target)
        ]
        return results, aggregate(results)

    def smoke(self, target: str) -> tuple[list[OperationResult], int]:
        results = [
            self.smoke_result(team)
            for team in self.targets(target)
            if self.runtime.is_deployed(team)
        ]
        if not results:
            return (
                [
                    OperationResult(
                        target,
                        False,
                        "no deployed targets selected",
                        CONFIG,
                    )
                ],
                CONFIG,
            )
        return results, aggregate(results)
