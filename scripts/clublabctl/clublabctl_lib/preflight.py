from __future__ import annotations

import ipaddress
import os
import shutil
import socket
import stat
from dataclasses import dataclass
from pathlib import Path

from .inventory import Inventory, validate_inventory


PASS = "PASS"
WARN = "WARN"
FAIL = "FAIL"


@dataclass(frozen=True)
class CheckResult:
    category: str
    name: str
    status: str
    detail: str
    critical: bool = True


def mode_string(path: Path) -> str:
    return oct(stat.S_IMODE(path.stat().st_mode))


def mem_available_bytes(
    path: Path = Path("/proc/meminfo"),
) -> int:
    values: dict[str, int] = {}
    for line in path.read_text(
        encoding="utf-8"
    ).splitlines():
        key, value = line.split(":", 1)
        parts = value.strip().split()
        if (
            parts
            and parts[0].isdigit()
        ):
            values[key] = (
                int(parts[0]) * 1024
            )
    return values.get(
        "MemAvailable",
        0,
    )


class PreflightRunner:
    def __init__(
        self,
        inventory: Inventory,
        runtime,
        runner,
        repo_root: Path,
        runtime_dir: Path,
    ) -> None:
        self.inventory = inventory
        self.runtime = runtime
        self.runner = runner
        self.repo_root = repo_root
        self.runtime_dir = runtime_dir

    def _targets(
        self,
        target: str,
    ) -> list[str]:
        if target == "all":
            return [
                name
                for name, cfg
                in self.inventory.teams.items()
                if cfg.get(
                    "enabled_by_default"
                )
            ]
        if target not in self.inventory.teams:
            raise ValueError(
                f"Unknown target: {target}"
            )
        return [target]

    def _port_free(
        self,
        bind_ip: str,
        port: int,
    ) -> bool:
        family = (
            socket.AF_INET6
            if ":" in bind_ip
            else socket.AF_INET
        )
        sock = socket.socket(
            family,
            socket.SOCK_STREAM,
        )
        try:
            sock.setsockopt(
                socket.SOL_SOCKET,
                socket.SO_REUSEADDR,
                1,
            )
            sock.bind(
                (bind_ip, port)
            )
            return True
        except OSError:
            return False
        finally:
            sock.close()

    def run(
        self,
        target: str,
    ) -> list[CheckResult]:
        results: list[CheckResult] = []
        teams = self._targets(
            target
        )

        inv_errors = validate_inventory(
            self.inventory
        )
        if inv_errors:
            results.append(
                CheckResult(
                    "CONFIG",
                    "inventory",
                    FAIL,
                    "; ".join(
                        inv_errors
                    ),
                )
            )
            return results

        results.append(
            CheckResult(
                "CONFIG",
                "inventory",
                PASS,
                f"{len(self.inventory.teams)} targets valid",
            )
        )

        try:
            self.runtime.ensure_docker()
            results.append(
                CheckResult(
                    "HOST",
                    "docker",
                    PASS,
                    "daemon available",
                )
            )
        except Exception as exc:
            results.append(
                CheckResult(
                    "HOST",
                    "docker",
                    FAIL,
                    str(exc),
                )
            )
            return results

        compose = (
            self.repo_root
            / "infrastructure"
            / "compose"
            / "team.compose.yml"
        )
        results.append(
            CheckResult(
                "CONFIG",
                "team.compose.yml",
                (
                    PASS
                    if compose.is_file()
                    else FAIL
                ),
                str(compose),
            )
        )

        bind_env = (
            self.inventory.raw
            .get(
                "gateway",
                {},
            )
            .get(
                "bind_ip_env",
                "CLUBLAB_BIND_IP",
            )
        )
        bind_ip = os.getenv(
            bind_env,
            "",
        ).strip()

        try:
            ipaddress.ip_address(
                bind_ip
            )
            bind_valid = True
        except ValueError:
            bind_valid = False

        results.append(
            CheckResult(
                "NETWORK",
                bind_env,
                (
                    PASS
                    if bind_valid
                    else FAIL
                ),
                bind_ip or "not set",
            )
        )

        capacity = (
            self.inventory.raw
            .get(
                "preflight",
                {},
            )
        )
        memory_per_team_mib = int(
            capacity.get(
                "memory_per_absent_team_mib",
                1536,
            )
        )
        memory_reserve_mib = int(
            capacity.get(
                "memory_host_reserve_mib",
                4096,
            )
        )
        disk_per_team_gib = int(
            capacity.get(
                "disk_per_absent_team_gib",
                2,
            )
        )
        disk_reserve_gib = int(
            capacity.get(
                "disk_host_reserve_gib",
                5,
            )
        )

        try:
            available = (
                mem_available_bytes()
            )
        except OSError as exc:
            available = 0
            results.append(
                CheckResult(
                    "HOST",
                    "memory probe",
                    WARN,
                    str(exc),
                    False,
                )
            )

        absent = sum(
            1
            for team in teams
            if not self.runtime.is_deployed(
                team
            )
        )

        required = (
            (
                absent
                * memory_per_team_mib
                + memory_reserve_mib
            )
            * 1024**2
        )

        results.append(
            CheckResult(
                "HOST",
                "memory",
                (
                    PASS
                    if available
                    >= required
                    else FAIL
                ),
                (
                    f"available="
                    f"{available // 1024**2}MiB "
                    f"required>="
                    f"{required // 1024**2}MiB"
                ),
            )
        )

        disk_root = (
            Path("/home")
            if Path("/home").exists()
            else self.runtime_dir.parent
        )
        usage = shutil.disk_usage(
            disk_root
        )
        disk_required = (
            (
                absent
                * disk_per_team_gib
                + disk_reserve_gib
            )
            * 1024**3
        )

        results.append(
            CheckResult(
                "HOST",
                "disk",
                (
                    PASS
                    if usage.free
                    >= disk_required
                    else FAIL
                ),
                (
                    f"free="
                    f"{usage.free // 1024**3}GiB "
                    f"required>="
                    f"{disk_required // 1024**3}GiB"
                ),
            )
        )

        teams_dir = (
            self.runtime_dir
            / "teams"
        )
        secrets_dir = (
            self.runtime_dir
            / "secrets"
        )

        for directory, name in (
            (
                teams_dir,
                "runtime teams dir",
            ),
            (
                secrets_dir,
                "runtime secrets dir",
            ),
        ):
            if not directory.exists():
                results.append(
                    CheckResult(
                        "SECRETS",
                        name,
                        FAIL,
                        f"missing {directory}",
                    )
                )
            else:
                mode = mode_string(
                    directory
                )
                results.append(
                    CheckResult(
                        "SECRETS",
                        name,
                        (
                            PASS
                            if mode == "0o700"
                            else FAIL
                        ),
                        (
                            f"{directory} "
                            f"mode={mode}"
                        ),
                    )
                )

        for team in teams:
            env_file = (
                teams_dir
                / f"{team}.env"
            )

            if not env_file.is_file():
                results.append(
                    CheckResult(
                        "SECRETS",
                        f"{team} runtime env",
                        FAIL,
                        f"missing {env_file}",
                    )
                )
            else:
                mode = mode_string(
                    env_file
                )
                results.append(
                    CheckResult(
                        "SECRETS",
                        f"{team} runtime env",
                        (
                            PASS
                            if mode == "0o600"
                            else FAIL
                        ),
                        f"mode={mode}",
                    )
                )

            if bind_valid:
                port = int(
                    self.inventory.teams[
                        team
                    ][
                        "access_port"
                    ]
                )
                deployed = (
                    self.runtime.is_deployed(
                        team
                    )
                )
                free = self._port_free(
                    bind_ip,
                    port,
                )

                if deployed:
                    status = PASS
                    detail = (
                        "team already deployed; "
                        "runtime owns expected access"
                    )
                else:
                    status = (
                        PASS
                        if free
                        else FAIL
                    )
                    detail = (
                        "free"
                        if free
                        else "already in use"
                    )

                results.append(
                    CheckResult(
                        "PORTS",
                        f"{bind_ip}:{port}",
                        status,
                        detail,
                    )
                )

            try:
                conflicts = (
                    self.runtime
                    .network_conflicts(
                        team
                    )
                )
                results.append(
                    CheckResult(
                        "NETWORK",
                        f"{team} IPAM",
                        (
                            FAIL
                            if conflicts
                            else PASS
                        ),
                        (
                            "; ".join(
                                conflicts
                            )
                            if conflicts
                            else "no foreign overlap"
                        ),
                    )
                )
            except Exception as exc:
                results.append(
                    CheckResult(
                        "NETWORK",
                        f"{team} IPAM",
                        FAIL,
                        str(exc),
                    )
                )

            if self.runtime.is_deployed(
                team
            ):
                try:
                    issues = (
                        self.runtime
                        .security_issues(
                            team
                        )
                    )
                    results.append(
                        CheckResult(
                            "SECURITY",
                            f"{team} containers",
                            (
                                FAIL
                                if issues
                                else PASS
                            ),
                            (
                                "; ".join(
                                    issues
                                )
                                if issues
                                else "guard rails satisfied"
                            ),
                        )
                    )
                except Exception as exc:
                    results.append(
                        CheckResult(
                            "SECURITY",
                            f"{team} containers",
                            FAIL,
                            str(exc),
                        )
                    )

        try:
            spare_deployed = (
                self.runtime
                .is_deployed(
                    "spare"
                )
            )
            results.append(
                CheckResult(
                    "SPARE",
                    "spare deployed",
                    (
                        PASS
                        if spare_deployed
                        else WARN
                    ),
                    (
                        "available"
                        if spare_deployed
                        else "not deployed"
                    ),
                    False,
                )
            )
        except Exception as exc:
            results.append(
                CheckResult(
                    "SPARE",
                    "spare deployed",
                    WARN,
                    str(exc),
                    False,
                )
            )

        return results


def has_critical_failure(
    results: list[CheckResult],
) -> bool:
    return any(
        item.status == FAIL
        and item.critical
        for item in results
    )
