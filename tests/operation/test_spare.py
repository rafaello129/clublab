from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CLI_DIR = ROOT / "scripts" / "clublabctl"
sys.path.insert(0, str(CLI_DIR))

from clublabctl_lib.inventory import Inventory
from clublabctl_lib.monitor import TeamStatus
from clublabctl_lib.spare import SpareManager


class FakeMonitor:
    def __init__(self) -> None:
        self.ready = True

    def status_one(
        self,
        team: str,
    ) -> TeamStatus:
        if self.ready:
            return TeamStatus(
                team=team,
                frontend="OK",
                api="OK",
                database="OK",
                toolbox="OK",
                scenario="normal",
                infra_state="READY",
            )
        return TeamStatus(
            team=team,
            frontend="DOWN",
            api="DOWN",
            database="OK",
            toolbox="OK",
            scenario="unknown",
            infra_state="DEGRADED",
        )


def inventory() -> Inventory:
    return Inventory(
        {
            "teams": {
                "team01": {
                    "access_port": 8211,
                },
                "team02": {
                    "access_port": 8212,
                },
                "spare": {
                    "access_port": 8219,
                },
            }
        }
    )


class SpareTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.monitor = FakeMonitor()
        self.manager = SpareManager(
            inventory(),
            self.monitor,
            Path(self.tmp.name),
        )

    def tearDown(self) -> None:
        self.tmp.cleanup()

    def test_assign_and_release(self) -> None:
        value = self.manager.assign(
            "team01"
        )
        self.assertEqual(
            "team01",
            value["assigned_team"],
        )
        self.assertEqual(
            8219,
            value["access_port"],
        )
        self.assertTrue(
            self.manager.release()
        )
        self.assertIsNone(
            self.manager.read_assignment()
        )

    def test_assignment_is_idempotent_for_same_team(self) -> None:
        first = self.manager.assign(
            "team01"
        )
        second = self.manager.assign(
            "team01"
        )
        self.assertEqual(
            first["assigned_team"],
            second["assigned_team"],
        )

    def test_cannot_reassign_without_release(self) -> None:
        self.manager.assign(
            "team01"
        )
        with self.assertRaises(
            RuntimeError
        ):
            self.manager.assign(
                "team02"
            )

    def test_spare_must_be_ready(self) -> None:
        self.monitor.ready = False
        with self.assertRaises(
            RuntimeError
        ):
            self.manager.assign(
                "team01"
            )


if __name__ == "__main__":
    unittest.main()
