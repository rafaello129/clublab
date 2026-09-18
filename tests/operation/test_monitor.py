from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CLI_DIR = ROOT / "scripts" / "clublabctl"
sys.path.insert(0, str(CLI_DIR))

from clublabctl_lib.inventory import Inventory
from clublabctl_lib.monitor import OperationalMonitor
from clublabctl_lib.state import StateStore


class FakeRuntime:
    def __init__(self) -> None:
        self.deployed = True
        self.scenario = "normal"
        self.services = {
            "frontend": "OK",
            "api": "OK",
            "database": "OK",
            "toolbox": "OK",
        }

    def is_deployed(self, team: str) -> bool:
        return self.deployed

    def service_status(
        self,
        team: str,
        role: str,
    ) -> str:
        return self.services[role]

    def get_app_scenario(
        self,
        team: str,
    ) -> str:
        return self.scenario

    def resource_rows(self, team: str):
        return [
            {
                "team": team,
                "role": "api",
                "cpu": "0.1%",
                "memory": "10MiB / 512MiB",
                "pids": "5",
                "net_io": "1kB / 1kB",
            }
        ]

    def technical_logs(
        self,
        team: str,
        role: str,
        *,
        lines: int,
    ) -> str:
        return f"{team}:{role}:{lines}"


def inventory() -> Inventory:
    return Inventory(
        {
            "teams": {
                "team01": {},
                "spare": {},
            }
        }
    )


class MonitorTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.runtime = FakeRuntime()
        self.monitor = OperationalMonitor(
            inventory(),
            self.runtime,
            StateStore(Path(self.tmp.name)),
        )

    def tearDown(self) -> None:
        self.tmp.cleanup()

    def test_ready(self) -> None:
        status = self.monitor.status_one(
            "team01"
        )
        self.assertEqual(
            "READY",
            status.infra_state,
        )

    def test_api_down_is_scenario(self) -> None:
        self.runtime.services["api"] = "DOWN"
        self.runtime.scenario = "api-down"
        status = self.monitor.status_one(
            "team01"
        )
        self.assertEqual(
            "SCENARIO",
            status.infra_state,
        )
        self.assertEqual(
            "api-down",
            status.scenario,
        )

    def test_absent(self) -> None:
        self.runtime.deployed = False
        status = self.monitor.status_one(
            "team01"
        )
        self.assertEqual(
            "ABSENT",
            status.infra_state,
        )

    def test_logs_are_scoped(self) -> None:
        self.assertEqual(
            "team01:api:20",
            self.monitor.logs(
                "team01",
                "api",
                lines=20,
            ),
        )
        with self.assertRaises(ValueError):
            self.monitor.logs(
                "team01",
                "gateway",
                lines=20,
            )


if __name__ == "__main__":
    unittest.main()
