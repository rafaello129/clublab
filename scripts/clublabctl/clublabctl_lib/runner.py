from __future__ import annotations

import subprocess
from dataclasses import dataclass
from typing import Sequence


@dataclass
class CommandResult:
    args: list[str]
    returncode: int
    stdout: str
    stderr: str


class CommandRunner:
    def run(self, args: Sequence[str], *, timeout: int = 30) -> CommandResult:
        argv = [str(x) for x in args]
        completed = subprocess.run(
            argv,
            capture_output=True,
            text=True,
            timeout=timeout,
            check=False,
        )
        return CommandResult(
            argv,
            completed.returncode,
            completed.stdout,
            completed.stderr,
        )
