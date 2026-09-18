from __future__ import annotations

import importlib.util
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CLI_PATH = ROOT / "scripts" / "clublabctl" / "clublabctl.py"
INVENTORY_PATH = ROOT / "infrastructure" / "teams" / "teams.json"

spec = importlib.util.spec_from_file_location("clublabctl", CLI_PATH)
assert spec and spec.loader
clublabctl = importlib.util.module_from_spec(spec)
spec.loader.exec_module(clublabctl)


class InventoryTests(unittest.TestCase):
    def setUp(self) -> None:
        self.raw = json.loads(INVENTORY_PATH.read_text(encoding="utf-8"))

    def test_inventory_is_valid(self) -> None:
        inv = clublabctl.Inventory(self.raw)
        self.assertEqual([], clublabctl.validate_inventory(inv))

    def test_expected_targets_exist(self) -> None:
        expected = {"team01", "team02", "team03", "team04", "team05", "team06", "spare"}
        self.assertEqual(expected, set(self.raw["teams"]))

    def test_ports_are_unique(self) -> None:
        ports = [team["access_port"] for team in self.raw["teams"].values()]
        self.assertEqual(len(ports), len(set(ports)))


if __name__ == "__main__":
    unittest.main()
