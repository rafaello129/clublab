from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CLI_DIR = ROOT / "scripts" / "clublabctl"
sys.path.insert(0, str(CLI_DIR))

from clublabctl_lib.audit import AuditLogger
from clublabctl_lib.deployment import DeploymentManager
from clublabctl_lib.inventory import Inventory
from clublabctl_lib.preflight import CheckResult, FAIL, PASS
from clublabctl_lib.state import StateStore


class FakePreflight:
    def __init__(self) -> None:
        self.fail = False

    def run(self, target: str):
        if self.fail:
            return [
                CheckResult(
                    "CONFIG",
                    "compose",
                    FAIL,
                    "missing",
                )
            ]
        return [
            CheckResult(
                "CONFIG",
                "compose",
                PASS,
                "ok",
            )
        ]


class FakeRuntime:
    def __init__(self) -> None:
        self.deployed: set[str] = set()
        self.scenario: dict[str, str] = {}
        self.smoke_ok = True
        self.deploy_count = 0
        self.gateway_count = 0
        self.attach_count = 0

    def is_deployed(
        self,
        team: str,
    ) -> bool:
        return team in self.deployed

    def get_app_scenario(
        self,
        team: str,
    ) -> str:
        return self.scenario.get(
            team,
            "normal",
        )

    def deploy_team(
        self,
        team: str,
    ) -> None:
        self.deploy_count += 1
        self.deployed.add(team)
        self.scenario[team] = "normal"

    def ensure_gateway(self) -> None:
        self.gateway_count += 1

    def attach_gateway_to_team(
        self,
        team: str,
    ) -> None:
        self.attach_count += 1

    def smoke_checks(
        self,
        team: str,
    ):
        return [
            {
                "name": "api",
                "ok": self.smoke_ok,
                "detail": (
                    "HTTP 200"
                    if self.smoke_ok
                    else "HTTP 500"
                ),
            }
        ]


def inventory() -> Inventory:
    return Inventory(
        {
            "teams": {
                "team01": {
                    "enabled_by_default": True,
                },
                "team02": {
                    "enabled_by_default": False,
                },
                "spare": {
                    "enabled_by_default": True,
                },
            }
        }
    )


class DeploymentTests(
    unittest.TestCase
):
    def setUp(self) -> None:
        self.tmp = (
            tempfile.TemporaryDirectory()
        )
        self.runtime = FakeRuntime()
        self.preflight = FakePreflight()
        runtime_dir = Path(
            self.tmp.name
        )

        self.manager = DeploymentManager(
            inventory(),
            self.runtime,
            StateStore(runtime_dir),
            self.preflight,
            AuditLogger(runtime_dir),
        )

    def tearDown(self) -> None:
        self.tmp.cleanup()

    def test_deploy_absent_team(
        self,
    ) -> None:
        result = self.manager.deploy_one(
            "team01"
        )
        self.assertTrue(result.ok)
        self.assertEqual(
            1,
            self.runtime.deploy_count,
        )
        self.assertEqual(
            1,
            self.runtime.gateway_count,
        )
        self.assertEqual(
            1,
            self.runtime.attach_count,
        )

    def test_deploy_is_idempotent_when_healthy(
        self,
    ) -> None:
        self.runtime.deployed.add(
            "team01"
        )
        self.runtime.scenario[
            "team01"
        ] = "normal"

        result = self.manager.deploy_one(
            "team01"
        )

        self.assertTrue(result.ok)
        self.assertEqual(
            0,
            self.runtime.deploy_count,
        )

    def test_deploy_refuses_active_scenario(
        self,
    ) -> None:
        self.runtime.deployed.add(
            "team01"
        )
        self.runtime.scenario[
            "team01"
        ] = "api-down"

        result = self.manager.deploy_one(
            "team01"
        )

        self.assertFalse(result.ok)
        self.assertIn(
            "clear/recover",
            result.detail,
        )

    def test_preflight_failure_stops_deploy(
        self,
    ) -> None:
        self.preflight.fail = True

        result = self.manager.deploy_one(
            "team01"
        )

        self.assertFalse(result.ok)
        self.assertEqual(
            0,
            self.runtime.deploy_count,
        )

    def test_smoke_failure_marks_deploy_failed(
        self,
    ) -> None:
        self.runtime.smoke_ok = False

        result = self.manager.deploy_one(
            "team01"
        )

        self.assertFalse(result.ok)

    def test_all_uses_enabled_defaults(
        self,
    ) -> None:
        self.assertEqual(
            ["team01", "spare"],
            self.manager.targets(
                "all"
            ),
        )


if __name__ == "__main__":
    unittest.main()
