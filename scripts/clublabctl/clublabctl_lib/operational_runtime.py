from __future__ import annotations

import ipaddress
import json
import os
import time
import urllib.error
import urllib.request
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
    """DockerRuntime plus deployment and operational observations."""

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
                    "cpu": stats.get("CPUPerc", "?"),
                    "memory": stats.get("MemUsage", "?"),
                    "pids": stats.get("PIDs", "?"),
                    "net_io": stats.get("NetIO", "?"),
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

    def _gateway_ids(self) -> list[str]:
        result = self.runner.run(
            [
                "docker",
                "ps",
                "-a",
                "--filter",
                "label=com.clublab.project=clublab",
                "--filter",
                "label=com.clublab.role=gateway",
                "--filter",
                "label=com.clublab.managed-by=clublab",
                "--format",
                "{{.ID}}",
            ],
            timeout=10,
        )
        if result.returncode != 0:
            raise RuntimeError(
                "Unable to query ClubLab gateway: "
                f"{result.stderr.strip()}"
            )
        return [
            line.strip()
            for line in result.stdout.splitlines()
            if line.strip()
        ]

    def find_gateway(self):
        ids = self._gateway_ids()
        if len(ids) != 1:
            raise RuntimeError(
                "Expected exactly one ClubLab gateway; "
                f"found {len(ids)}"
            )

        result = self.runner.run(
            [
                "docker",
                "inspect",
                ids[0],
            ],
            timeout=10,
        )
        if result.returncode != 0:
            raise RuntimeError(
                "Unable to inspect ClubLab gateway"
            )

        obj = json.loads(
            result.stdout
        )[0]
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

        if not name.startswith(
            "clublab-gateway"
        ):
            raise RuntimeError(
                "Security guard: invalid gateway name"
            )
        if labels.get(
            "com.clublab.project"
        ) != "clublab":
            raise RuntimeError(
                "Security guard: invalid gateway project label"
            )
        if labels.get(
            "com.clublab.role"
        ) != "gateway":
            raise RuntimeError(
                "Security guard: invalid gateway role label"
            )
        if labels.get(
            "com.clublab.managed-by"
        ) != "clublab":
            raise RuntimeError(
                "Security guard: invalid gateway ownership label"
            )

        return ids[0], name, obj

    def ensure_gateway(self) -> None:
        ids = self._gateway_ids()
        if ids:
            gateway_id, _, _ = self.find_gateway()
            result = self.runner.run(
                [
                    "docker",
                    "inspect",
                    "--format",
                    "{{.State.Running}}",
                    gateway_id,
                ],
                timeout=10,
            )
            if (
                result.returncode == 0
                and result.stdout.strip().lower()
                == "true"
            ):
                return

        manifest = (
            self.repo_root
            / "infrastructure"
            / "compose"
            / "gateway.compose.yml"
        )
        env_file = (
            self.runtime_dir
            / "gateway.env"
        )

        if not manifest.is_file():
            raise RuntimeError(
                f"Gateway compose manifest not found: {manifest}"
            )
        if not env_file.is_file():
            raise RuntimeError(
                f"Gateway runtime env not found: {env_file}"
            )

        result = self.runner.run(
            [
                "docker",
                "compose",
                "--project-name",
                "clublab-gateway",
                "--env-file",
                str(env_file),
                "-f",
                str(manifest),
                "up",
                "-d",
                "gateway",
            ],
            timeout=90,
        )

        if result.returncode != 0:
            raise RuntimeError(
                "Unable to deploy ClubLab gateway: "
                f"{result.stderr.strip()}"
            )

        gateway_id, _, _ = self.find_gateway()
        deadline = time.monotonic() + 30

        while time.monotonic() < deadline:
            state = self.runner.run(
                [
                    "docker",
                    "inspect",
                    "--format",
                    "{{if .State.Health}}{{.State.Health.Status}}"
                    "{{else}}{{.State.Status}}{{end}}",
                    gateway_id,
                ],
                timeout=10,
            )

            if (
                state.returncode == 0
                and state.stdout.strip()
                in {"healthy", "running"}
            ):
                return

            time.sleep(1)

        raise RuntimeError(
            "ClubLab gateway did not become ready"
        )

    def _find_team_app_network(
        self,
        team: str,
    ) -> str:
        result = self.runner.run(
            [
                "docker",
                "network",
                "ls",
                "--filter",
                "label=com.clublab.project=clublab",
                "--filter",
                f"label=com.clublab.team={team}",
                "--filter",
                "label=com.clublab.network-role=app",
                "--format",
                "{{.ID}}",
            ],
            timeout=10,
        )

        if result.returncode != 0:
            raise RuntimeError(
                "Unable to query team APP network: "
                f"{result.stderr.strip()}"
            )

        ids = [
            line.strip()
            for line in result.stdout.splitlines()
            if line.strip()
        ]

        if len(ids) != 1:
            raise RuntimeError(
                f"Expected one APP network for {team}; "
                f"found {len(ids)}"
            )

        inspect = self.runner.run(
            [
                "docker",
                "network",
                "inspect",
                ids[0],
            ],
            timeout=10,
        )

        if inspect.returncode != 0:
            raise RuntimeError(
                "Unable to inspect team APP network"
            )

        obj = json.loads(
            inspect.stdout
        )[0]
        labels = obj.get(
            "Labels"
        ) or {}

        required = {
            "com.clublab.project": "clublab",
            "com.clublab.team": team,
            "com.clublab.network-role": "app",
            "com.clublab.managed-by": "clublab",
        }

        for key, expected in required.items():
            if labels.get(key) != expected:
                raise RuntimeError(
                    "Security guard: invalid APP network label "
                    f"{key}"
                )

        return str(
            obj.get("Name")
            or ids[0]
        )

    def attach_gateway_to_team(
        self,
        team: str,
    ) -> None:
        gateway_id, _, gateway = self.find_gateway()
        network_name = self._find_team_app_network(
            team
        )

        connected = (
            (gateway.get("NetworkSettings") or {})
            .get(
                "Networks"
            )
            or {}
        )

        if network_name in connected:
            return

        result = self.runner.run(
            [
                "docker",
                "network",
                "connect",
                network_name,
                gateway_id,
            ],
            timeout=20,
        )

        if result.returncode != 0:
            raise RuntimeError(
                f"Unable to connect gateway to {network_name}: "
                f"{result.stderr.strip()}"
            )

    def _host_http_status(
        self,
        url: str,
        *,
        timeout: float = 5.0,
    ) -> int:
        try:
            request = urllib.request.Request(
                url,
                method="GET",
            )
            with urllib.request.urlopen(
                request,
                timeout=timeout,
            ) as response:
                return int(
                    response.status
                )
        except urllib.error.HTTPError as exc:
            return int(exc.code)
        except Exception:
            return 0

    def gateway_status(
        self,
        team: str,
        path: str,
    ) -> int:
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
        if not bind_ip:
            raise RuntimeError(
                f"{bind_env} is not set"
            )

        port = int(
            self.inventory.teams[
                team
            ][
                "access_port"
            ]
        )

        return self._host_http_status(
            f"http://{bind_ip}:{port}{path}"
        )

    def deploy_team(
        self,
        team: str,
    ) -> None:
        base = self._compose_base(
            team
        )

        up_db = self.runner.run(
            base
            + [
                "up",
                "-d",
                "database",
            ],
            timeout=90,
        )

        if up_db.returncode != 0:
            raise RuntimeError(
                f"Unable to start database for {team}: "
                f"{up_db.stderr.strip()}"
            )

        db = self.find_one(
            team,
            "database",
        )
        deadline = (
            time.monotonic()
            + 45
        )

        while (
            time.monotonic()
            < deadline
        ):
            if self.container_health(
                db
            ) in {
                "healthy",
                "running",
            }:
                break
            time.sleep(1)
        else:
            raise RuntimeError(
                f"Database for {team} did not become ready"
            )

        bootstrap = self.runner.run(
            base
            + [
                "run",
                "--rm",
                "bootstrap",
            ],
            timeout=120,
        )

        if bootstrap.returncode != 0:
            raise RuntimeError(
                f"Bootstrap failed for {team}: "
                f"{bootstrap.stderr.strip()}"
            )

        up = self.runner.run(
            base
            + [
                "up",
                "-d",
                "frontend",
                "api",
                "toolbox",
            ],
            timeout=120,
        )

        if up.returncode != 0:
            raise RuntimeError(
                f"Unable to start team services for {team}: "
                f"{up.stderr.strip()}"
            )

        self.wait_api(
            team,
            timeout=45,
        )
        self.set_app_scenario(
            team,
            "normal",
        )
        self.validate_scenario(
            team,
            "normal",
        )

    def smoke_checks(
        self,
        team: str,
    ) -> list[dict[str, Any]]:
        checks: list[dict[str, Any]] = []

        if not self.is_deployed(
            team
        ):
            return [
                {
                    "name": "deployment",
                    "ok": False,
                    "detail": "team is not deployed",
                }
            ]

        for role in TEAM_ROLES:
            try:
                status = self.service_status(
                    team,
                    role,
                )
                checks.append(
                    {
                        "name": f"service:{role}",
                        "ok": status == "OK",
                        "detail": status,
                    }
                )
            except Exception as exc:
                checks.append(
                    {
                        "name": f"service:{role}",
                        "ok": False,
                        "detail": str(exc),
                    }
                )

        try:
            api = self.find_one(
                team,
                "api",
            )
            ready_status, _ = self._node_fetch(
                api,
                path="/internal/health/ready",
                method="GET",
                control=False,
            )
            checks.append(
                {
                    "name": "api:readiness",
                    "ok": ready_status == 200,
                    "detail": f"HTTP {ready_status}",
                }
            )
        except Exception as exc:
            checks.append(
                {
                    "name": "api:readiness",
                    "ok": False,
                    "detail": str(exc),
                }
            )

        try:
            ranking = self.public_status(
                team,
                "/api/ranking",
            )
            checks.append(
                {
                    "name": "api:ranking",
                    "ok": ranking == 200,
                    "detail": f"HTTP {ranking}",
                }
            )
        except Exception as exc:
            checks.append(
                {
                    "name": "api:ranking",
                    "ok": False,
                    "detail": str(exc),
                }
            )

        try:
            scenario = self.get_app_scenario(
                team
            )
            checks.append(
                {
                    "name": "scenario",
                    "ok": scenario == "normal",
                    "detail": scenario,
                }
            )
        except Exception as exc:
            checks.append(
                {
                    "name": "scenario",
                    "ok": False,
                    "detail": str(exc),
                }
            )

        try:
            frontend = self.gateway_status(
                team,
                "/",
            )
            checks.append(
                {
                    "name": "gateway:frontend",
                    "ok": frontend == 200,
                    "detail": f"HTTP {frontend}",
                }
            )

            api_status = self.gateway_status(
                team,
                "/api/health",
            )
            checks.append(
                {
                    "name": "gateway:api",
                    "ok": api_status == 200,
                    "detail": f"HTTP {api_status}",
                }
            )
        except Exception as exc:
            checks.append(
                {
                    "name": "gateway",
                    "ok": False,
                    "detail": str(exc),
                }
            )

        return checks

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
