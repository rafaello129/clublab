from __future__ import annotations

import json
import os
import stat
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CLI_DIR = ROOT / "scripts" / "clublabctl"
sys.path.insert(0, str(CLI_DIR))

from clublabctl_lib.audit import AuditLogger


class AuditTests(unittest.TestCase):
    def test_write_and_tail(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            logger = AuditLogger(Path(tmp))
            logger.write(
                action="scenario.load",
                result="success",
                team="team01",
                scenario="ranking-db-failure",
                meta={"code": 0},
            )

            events = logger.tail(10)
            self.assertEqual(1, len(events))
            self.assertEqual(
                "scenario.load",
                events[0]["action"],
            )
            self.assertEqual(
                "team01",
                events[0]["team"],
            )

            mode = stat.S_IMODE(
                logger.path.stat().st_mode
            )
            self.assertEqual(0o600, mode)

    def test_unknown_meta_is_not_logged(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            logger = AuditLogger(Path(tmp))
            logger.write(
                action="test",
                result="success",
                meta={
                    "password": "never-log-me",
                    "code": 0,
                },
            )
            raw = logger.path.read_text(
                encoding="utf-8"
            )
            self.assertNotIn(
                "never-log-me",
                raw,
            )
            event = json.loads(raw)
            self.assertEqual(
                {"code": 0},
                event["meta"],
            )


if __name__ == "__main__":
    unittest.main()
