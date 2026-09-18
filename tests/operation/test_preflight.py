from __future__ import annotations

import os
import stat
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CLI_DIR = ROOT / "scripts" / "clublabctl"
sys.path.insert(0, str(CLI_DIR))

from clublabctl_lib.preflight import (
    CheckResult,
    FAIL,
    PASS,
    has_critical_failure,
    mode_string,
)


class PreflightHelpersTests(
    unittest.TestCase
):
    def test_critical_failure(self) -> None:
        self.assertTrue(
            has_critical_failure(
                [
                    CheckResult(
                        "HOST",
                        "docker",
                        FAIL,
                        "down",
                        True,
                    )
                ]
            )
        )
        self.assertFalse(
            has_critical_failure(
                [
                    CheckResult(
                        "SPARE",
                        "spare",
                        FAIL,
                        "absent",
                        False,
                    )
                ]
            )
        )

    def test_mode_string(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "secret.env"
            path.write_text(
                "x",
                encoding="utf-8",
            )
            os.chmod(path, 0o600)
            self.assertEqual(
                "0o600",
                mode_string(path),
            )

    def test_pass_is_not_failure(self) -> None:
        self.assertFalse(
            has_critical_failure(
                [
                    CheckResult(
                        "CONFIG",
                        "inventory",
                        PASS,
                        "valid",
                    )
                ]
            )
        )


if __name__ == "__main__":
    unittest.main()
