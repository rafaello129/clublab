from __future__ import annotations

import ipaddress
import json
from typing import Any

from .docker_runtime import DockerRuntime


TEAM_ROLES = (
    "frontend",
    "api",
    "database",
    "toolbox",
)

DANGEROUS_CAPS = {
    "SYS_ADMIN",
    "NET_ADMIN",
    "SYS_PTRACE",
    "SYS_MODULE",
}

SENSITIVE_HOST_PATHS = (
    "/var/run/docker.sock",
    "/home/docker-data",
    "/var/www/pelican",
)


class OperationalRuntime(DockerRuntime):
    """DockerRuntime plus read-only operational observations."""

    def service_status(
        self,
        team: str,
        role: str,
    ) -> str:
        ref = self.find_one(
            team,
            role,
        )
        if not self.container_running(
            ref
        ):
            return "DOWN"

        if role == "api":
            status = self.public_status(
                team,
                "/api/health",
            )
            return (
                "OK"
                if status == 200
                else f"HTTP{status or 'DOWN'}"
            )

        state = self.container_health(
            ref
        )
        if state in {
            "healthy",
            "running",
        }:
            return "OK"
        return (
            state.upper()
            or "UNKNOWN"
        )

    def resource_rows(
        self,
        team: str,
    ) -> list[dict[str, Any]]:
        rows: list[dict[str, Any]] = []

        for role in TEAM_ROLES:
            ref = self.find_one(
                team,
                role,
            )
            result = self.runner.run(
                [
                    "docker",
                    "stats",
                    "--no-stream",
                    "--format",
                    "{{json .}}",
                    ref.id,
                ],
                timeout=15,
            )

            if result.returncode != 0:
                raise RuntimeError(
                    f"docker stats failed for {ref.name}: "
                    f"{result.stderr.strip()}"
                )

            lines = [
                line
                for line in result.stdout.splitlines()
                if line.strip()
            ]

            if not lines:
                raise RuntimeError(
                    f"docker stats returned no data for {ref.name}"
                )

            try:
                stats = json.loads(
                    lines[-1]
                )
            except json.JSONDecodeError as exc:
                raise RuntimeError(
                    f"Invalid docker stats JSON for {ref.name}"
                ) from exc

            rows.append(
                {
                    "team": team,
                    "role": role,
                    "cpu": stats.get(
                        "CPUPerc",
                        "?",
                    ),
                    "memory": stats.get(
                        "MemUsage",
                        "?",
                    ),
                    "pids": stats.get(
                        "PIDs",
                        "?",
                    ),
                    "net_io": stats.get(
                        "NetIO",
                        "?",
                    ),
                }
            )

        return rows

    def technical_logs(
        self,
        team: str,
        role: str,
        *,
        lines: int,
    ) -> str:
        ref = self.find_one(
            team,
            role,
        )
        result = self.runner.run(
            [
                "docker",
                "logs",
                "--tail",
                str(lines),
                ref.id,
            ],
            timeout=15,
        )

        if result.returncode != 0:
            raise RuntimeError(
                f"Unable to read logs for {ref.name}: "
                f"{result.stderr.strip()}"
            )

        if (
            result.stdout
            and result.stderr
        ):
            return (
                result.stdout.rstrip()
                + "\n"
                + result.stderr.rstrip()
            )

        return (
            result.stdout
            or result.stderr
        ).rstrip()

    def access_port_owned_by_gateway(
        self,
        bind_ip: str,
        port: int,
    ) -> bool:
        result = self.runner.run(
            [
                "docker",
                "ps",
                "--filter",
                f"publish={port}",
                "--format",
                "{{.ID}}",
            ],
            timeout=10,
        )

        if result.returncode != 0:
            raise RuntimeError(
                "Unable to inspect published ports: "
                f"{result.stderr.strip()}"
            )

        ids = [
            line.strip()
            for line in result.stdout.splitlines()
            if line.strip()
        ]

        if len(ids) != 1:
            return False

        inspect = self.runner.run(
            [
                "docker",
                "inspect",
                ids[0],
            ],
            timeout=10,
        )

        if inspect.returncode != 0:
            return False

        data = json.loads(
            inspect.stdout
        )
        if len(data) != 1:
            return False

        obj = data[0]
        labels = (
            (obj.get("Config") or {})
            .get(
                "Labels"
            )
            or {}
        )
        name = str(
            obj.get("Name")
            or ""
        ).lstrip("/")

        if labels.get(
            "com.clublab.project"
        ) != "clublab":
            return False

        if labels.get(
            "com.clublab.role"
        ) != "gateway":
            return False

        if labels.get(
            "com.clublab.managed-by"
        ) != "clublab":
            return False

        if not name.startswith(
            "clublab-gateway"
        ):
            return False

        ports = (
            (obj.get("NetworkSettings") or {})
            .get(
                "Ports"
            )
            or {}
        )

        for bindings in ports.values():
            for binding in (
                bindings
                or []
            ):
                if (
                    str(
                        binding.get(
                            "HostPort"
                        )
                    )
                    == str(port)
                    and str(
                        binding.get(
                            "HostIp"
                        )
                    )
                    == bind_ip
                ):
                    return True

        return False

    def network_conflicts(
        self,
        team: str,
    ) -> list[str]:
        planned = [
            ipaddress.ip_network(
                self.inventory.teams[
                    team
                ][
                    "app_subnet"
                ],
                strict=True,
            ),
            ipaddress.ip_network(
                self.inventory.teams[
                    team
                ][
                    "data_subnet"
                ],
                strict=True,
            ),
        ]

        ids = self.runner.run(
            [
                "docker",
                "network",
                "ls",
                "--format",
                "{{.ID}}",
            ],
            timeout=10,
        )

        if ids.returncode != 0:
            raise RuntimeError(
                "Unable to list Docker networks: "
                f"{ids.stderr.strip()}"
            )

        conflicts: list[str] = []

        for network_id in [
            line.strip()
            for line in ids.stdout.splitlines()
            if line.strip()
        ]:
            result = self.runner.run(
                [
                    "docker",
                    "network",
                    "inspect",
                    network_id,
                ],
                timeout=10,
            )

            if result.returncode != 0:
                raise RuntimeError(
                    f"Unable to inspect network {network_id}"
                )

            data = json.loads(
                result.stdout
            )
            if not data:
                continue

            obj = data[0]
            labels = (
                obj.get(
                    "Labels"
                )
                or {}
            )

            own_network = (
                labels.get(
                    "com.clublab.project"
                )
                == "clublab"
                and labels.get(
                    "com.clublab.team"
                )
                == team
            )

            if own_network:
                continue

            configs = (
                (obj.get("IPAM") or {})
                .get(
                    "Config"
                )
                or []
            )

            for cfg in configs:
                subnet = cfg.get(
                    "Subnet"
                )
                if not subnet:
                    continue

                try:
                    existing = (
                        ipaddress.ip_network(
                            subnet,
                            strict=False,
                        )
                    )
                except ValueError:
                    continue

                for candidate in planned:
                    if candidate.overlaps(
                        existing
                    ):
                        conflicts.append(
                            f"{candidate} overlaps "
                            f"{obj.get('Name', network_id)}:"
                            f"{existing}"
                        )

        return conflicts

    def security_issues(
        self,
        team: str,
    ) -> list[str]:
        issues: list[str] = []

        for role in TEAM_ROLES:
            ref = self.find_one(
                team,
                role,
            )

            result = self.runner.run(
                [
                    "docker",
                    "inspect",
                    ref.id,
                ],
                timeout=10,
            )

            if result.returncode != 0:
                raise RuntimeError(
                    f"Unable to inspect {ref.name}: "
                    f"{result.stderr.strip()}"
                )

            data = json.loads(
                result.stdout
            )
            obj = data[0]
            host = (
                obj.get(
                    "HostConfig"
                )
                or {}
            )
            config = (
                obj.get(
                    "Config"
                )
                or {}
            )

            if host.get(
                "Privileged"
            ):
                issues.append(
                    f"{role}: privileged=true"
                )

            if host.get(
                "NetworkMode"
            ) == "host":
                issues.append(
                    f"{role}: host network"
                )

            if host.get(
                "PidMode"
            ) == "host":
                issues.append(
                    f"{role}: host PID namespace"
                )

            if host.get(
                "IpcMode"
            ) == "host":
                issues.append(
                    f"{role}: host IPC namespace"
                )

            for cap in (
                host.get(
                    "CapAdd"
                )
                or []
            ):
                if (
                    str(cap).upper()
                    in DANGEROUS_CAPS
                ):
                    issues.append(
                        f"{role}: dangerous capability {cap}"
                    )

            if role in {
                "frontend",
                "api",
                "toolbox",
            }:
                user = str(
                    config.get(
                        "User"
                    )
                    or ""
                ).strip()

                if user in {
                    "",
                    "0",
                    "root",
                    "0:0",
                }:
                    issues.append(
                        f"{role}: runtime user appears root/default"
                    )

                opts = [
                    str(value)
                    for value in (
                        host.get(
                            "SecurityOpt"
                        )
                        or []
                    )
                ]

                if not any(
                    "no-new-privileges"
                    in value
                    for value in opts
                ):
                    issues.append(
                        f"{role}: no-new-privileges missing"
                    )

            if role in {
                "frontend",
                "api",
            } and not host.get(
                "ReadonlyRootfs"
            ):
                issues.append(
                    f"{role}: root filesystem not read-only"
                )

            memory = int(
                host.get(
                    "Memory"
                )
                or 0
            )
            pids = int(
                host.get(
                    "PidsLimit"
                )
                or 0
            )
            nano_cpus = int(
                host.get(
                    "NanoCpus"
                )
                or 0
            )
            cpu_quota = int(
                host.get(
                    "CpuQuota"
                )
                or 0
            )

            if memory <= 0:
                issues.append(
                    f"{role}: memory limit missing"
                )

            if pids <= 0:
                issues.append(
                    f"{role}: PIDs limit missing"
                )

            if (
                nano_cpus <= 0
                and cpu_quota <= 0
            ):
                issues.append(
                    f"{role}: CPU limit missing"
                )

            for mount in (
                obj.get(
                    "Mounts"
                )
                or []
            ):
                source = str(
                    mount.get(
                        "Source"
                    )
                    or ""
                )

                if source in (
                    SENSITIVE_HOST_PATHS
                ):
                    issues.append(
                        f"{role}: sensitive mount {source}"
                    )

                if (
                    source == "/home/tulum"
                    or source.startswith(
                        "/home/tulum/apps/"
                    )
                ):
                    issues.append(
                        f"{role}: host app mount {source}"
                    )

            ports = (
                (obj.get("NetworkSettings") or {})
                .get(
                    "Ports"
                )
                or {}
            )

            for (
                container_port,
                bindings,
            ) in ports.items():
                if bindings:
                    issues.append(
                        f"{role}: directly published {container_port}"
                    )

        return issues
