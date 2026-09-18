from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CLI_DIR = ROOT / "scripts" / "clublabctl"
sys.path.insert(0, str(CLI_DIR))

from clublabctl_lib.inventory import Inventory
from clublabctl_lib.operations import (
    SECURITY_GUARD,
    ScenarioManager,
)
from clublabctl_lib.state import StateStore


class FakeRuntime:
    def __init__(self) -> None:
        self.deployed = {
            "team01": True,
            "team02": True,
            "spare": True,
        }
        self.scenarios = {
            "team01": "normal",
            "team02": "normal",
            "spare": "normal",
        }
        self.restart_count = 0
        self.fail_clear_once = False

    def is_deployed(self, team: str) -> bool:
        return self.deployed.get(
            team,
            False,
        )

    def get_app_scenario(
        self,
        team: str,
    ) -> str:
        return self.scenarios[team]

    def set_app_scenario(
        self,
        team: str,
        scenario: str,
    ) -> None:
        if (
            self.fail_clear_once
            and scenario == "normal"
        ):
            self.fail_clear_once = False
            raise RuntimeError(
                "simulated clear failure"
            )
        self.scenarios[team] = scenario

    def start_api(self, team: str) -> None:
        if (
            self.scenarios[team]
            == "api-down"
        ):
            self.scenarios[team] = "normal"

    def stop_api(self, team: str) -> None:
        self.scenarios[team] = "api-down"

    def restart_api(
        self,
        team: str,
    ) -> None:
        self.restart_count += 1
        self.scenarios[team] = "normal"

    def validate_scenario(
        self,
        team: str,
        scenario: str,
    ) -> None:
        if self.scenarios[team] != scenario:
            raise RuntimeError(
                f"expected {scenario}, "
                f"got {self.scenarios[team]}"
            )

    def reset_team(self, team: str) -> None:
        self.scenarios[team] = "normal"


def inventory() -> Inventory:
    return Inventory(
        {
            "scenarios": [
                "normal",
                "ranking-db-failure",
                "api-down",
            ],
            "teams": {
                "team01": {
                    "enabled_by_default": True,
                },
                "team02": {
                    "enabled_by_default": True,
                },
                "spare": {
                    "enabled_by_default": True,
                },
            },
        }
    )


class ScenarioManagerTests(
    unittest.TestCase
):
    def setUp(self) -> None:
        self.tmp = (
            tempfile.TemporaryDirectory()
        )
        self.runtime = FakeRuntime()
        self.manager = ScenarioManager(
            inventory(),
            self.runtime,
            StateStore(
                Path(self.tmp.name)
            ),
        )

    def tearDown(self) -> None:
        self.tmp.cleanup()

    def test_load_ranking_failure(
        self,
    ) -> None:
        result = self.manager.load_one(
            "team01",
            "ranking-db-failure",
        )
        self.assertTrue(result.ok)
        self.assertEqual(
            "ranking-db-failure",
            self.runtime.scenarios["team01"],
        )

    def test_load_api_down(
        self,
    ) -> None:
        result = self.manager.load_one(
            "team01",
            "api-down",
        )
        self.assertTrue(result.ok)
        self.assertEqual(
            "api-down",
            self.runtime.scenarios["team01"],
        )

    def test_clear_api_down(
        self,
    ) -> None:
        self.runtime.scenarios["team01"] = (
            "api-down"
        )
        result = self.manager.clear_one(
            "team01"
        )
        self.assertTrue(result.ok)
        self.assertEqual(
            "normal",
            self.runtime.scenarios["team01"],
        )

    def test_recover_uses_restart_as_r2(
        self,
    ) -> None:
        self.runtime.scenarios["team01"] = (
            "ranking-db-failure"
        )
        self.runtime.fail_clear_once = True

        result = self.manager.recover_one(
            "team01"
        )

        self.assertTrue(result.ok)
        self.assertEqual(
            1,
            self.runtime.restart_count,
        )
        self.assertEqual(
            "normal",
            self.runtime.scenarios["team01"],
        )

    def test_reset_requires_confirmation(
        self,
    ) -> None:
        result = self.manager.reset_one(
            "team01",
            confirmed=False,
        )
        self.assertFalse(result.ok)
        self.assertEqual(
            SECURITY_GUARD,
            result.code,
        )

    def test_all_excludes_spare(
        self,
    ) -> None:
        self.assertEqual(
            ["team01", "team02"],
            self.manager.expand_target(
                "all"
            ),
        )


if __name__ == "__main__":
    unittest.main()
