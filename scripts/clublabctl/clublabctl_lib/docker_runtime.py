from __future__ import annotations

import json
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .inventory import Inventory
from .runner import CommandRunner


PROJECT_LABEL = "com.clublab.project"
TEAM_LABEL = "com.clublab.team"
ROLE_LABEL = "com.clublab.role"
MANAGED_LABEL = "com.clublab.managed-by"
DISPOSABLE_LABEL = "com.clublab.disposable"


@dataclass(frozen=True)
class ContainerRef:
    id: str
    name: str
    team: str
    role: str
    labels: dict[str, str]


class DockerRuntime:
    """Safe Docker adapter for ClubLab resources only."""

    def __init__(
        self,
        inventory: Inventory,
        runner: CommandRunner,
        repo_root: Path,
        runtime_dir: Path,
    ) -> None:
        self.inventory = inventory
        self.runner = runner
        self.repo_root = repo_root
        self.runtime_dir = runtime_dir
        self.compose_file = (
            repo_root / "infrastructure" / "compose" / "team.compose.yml"
        )

    def ensure_docker(self) -> None:
        result = self.runner.run(
            ["docker", "version", "--format", "{{.Server.Version}}"],
            timeout=10,
        )
        if result.returncode != 0:
            raise RuntimeError(
                f"Docker is unavailable: {result.stderr.strip()}"
            )

    def _list_container_ids(
        self,
        team: str,
        role: str | None = None,
    ) -> list[str]:
        args = [
            "docker",
            "ps",
            "-a",
            "--filter",
            f"label={PROJECT_LABEL}=clublab",
            "--filter",
            f"label={TEAM_LABEL}={team}",
        ]
        if role:
            args += ["--filter", f"label={ROLE_LABEL}={role}"]
        args += ["--format", "{{.ID}}"]

        result = self.runner.run(args, timeout=10)
        if result.returncode != 0:
            raise RuntimeError(
                f"Unable to query Docker containers: {result.stderr.strip()}"
            )
        return [
            line.strip()
            for line in result.stdout.splitlines()
            if line.strip()
        ]

    def is_deployed(self, team: str) -> bool:
        return bool(self._list_container_ids(team))

    def find_one(self, team: str, role: str) -> ContainerRef:
        ids = self._list_container_ids(team, role)
        if len(ids) != 1:
            raise RuntimeError(
                f"Expected exactly one {role} container for {team}; "
                f"found {len(ids)}"
            )

        result = self.runner.run(
            ["docker", "inspect", ids[0]],
            timeout=10,
        )
        if result.returncode != 0:
            raise RuntimeError(
                f"Unable to inspect container {ids[0]}: "
                f"{result.stderr.strip()}"
            )

        data = json.loads(result.stdout)
        if len(data) != 1:
            raise RuntimeError("Unexpected docker inspect result")

        obj = data[0]
        labels = (obj.get("Config") or {}).get("Labels") or {}
        name = str(obj.get("Name") or "").lstrip("/")
        expected_project = self.inventory.teams[team]["compose_project"]

        required = {
            PROJECT_LABEL: "clublab",
            TEAM_LABEL: team,
            ROLE_LABEL: role,
            MANAGED_LABEL: "clublab",
            DISPOSABLE_LABEL: "true",
        }

        for key, expected in required.items():
            if labels.get(key) != expected:
                raise RuntimeError(
                    "Security guard: "
                    f"container {name} has invalid label "
                    f"{key}={labels.get(key)!r}"
                )

        if not (
            name.startswith(expected_project + "-")
            or name.startswith(expected_project + "_")
        ):
            raise RuntimeError(
                "Security guard: "
                f"container {name!r} does not match "
                f"project {expected_project!r}"
            )

        return ContainerRef(
            ids[0],
            name,
            team,
            role,
            labels,
        )

    def container_running(self, ref: ContainerRef) -> bool:
        result = self.runner.run(
            [
                "docker",
                "inspect",
                "--format",
                "{{.State.Running}}",
                ref.id,
            ],
            timeout=10,
        )
        if result.returncode != 0:
            raise RuntimeError(
                result.stderr.strip() or "docker inspect failed"
            )
        return result.stdout.strip().lower() == "true"

    def container_health(self, ref: ContainerRef) -> str:
        result = self.runner.run(
            [
                "docker",
                "inspect",
                "--format",
                "{{if .State.Health}}{{.State.Health.Status}}"
                "{{else}}{{.State.Status}}{{end}}",
                ref.id,
            ],
            timeout=10,
        )
        if result.returncode != 0:
            raise RuntimeError(
                result.stderr.strip() or "docker inspect failed"
            )
        return result.stdout.strip()

    def start(self, ref: ContainerRef) -> None:
        result = self.runner.run(
            ["docker", "start", ref.id],
            timeout=30,
        )
        if result.returncode != 0:
            raise RuntimeError(
                f"Unable to start {ref.name}: "
                f"{result.stderr.strip()}"
            )

    def stop(self, ref: ContainerRef) -> None:
        result = self.runner.run(
            ["docker", "stop", "--time", "10", ref.id],
            timeout=30,
        )
        if result.returncode != 0:
            raise RuntimeError(
                f"Unable to stop {ref.name}: "
                f"{result.stderr.strip()}"
            )

    def restart(self, ref: ContainerRef) -> None:
        result = self.runner.run(
            ["docker", "restart", "--time", "10", ref.id],
            timeout=40,
        )
        if result.returncode != 0:
            raise RuntimeError(
                f"Unable to restart {ref.name}: "
                f"{result.stderr.strip()}"
            )

    def _node_fetch(
        self,
        ref: ContainerRef,
        *,
        path: str,
        method: str = "GET",
        body: dict[str, Any] | None = None,
        control: bool = False,
        timeout: int = 10,
    ) -> tuple[int, Any]:
        if not path.startswith("/") or "\n" in path or "\r" in path:
            raise ValueError("Invalid internal path")

        token_code = (
            'const token=process.env.CLUBLAB_CONTROL_TOKEN;'
            'if(!token){console.error("missing control token");'
            'process.exit(31);}'
            'headers["X-ClubLab-Control-Token"]=token;'
            if control
            else ""
        )

        script = (
            'const headers={"Content-Type":"application/json"};'
            + token_code
            + f'const options={{method:{json.dumps(method)},headers}};'
            + f'const body={json.dumps(body) if body is not None else "null"};'
            + 'if(body!==null) options.body=JSON.stringify(body);'
            + f'fetch("http://127.0.0.1:3000{path}",options)'
            + '.then(async r=>{const text=await r.text();'
              'let payload=text;'
              'try{payload=text?JSON.parse(text):{};}catch(_e){}'
              'console.log(JSON.stringify({status:r.status,body:payload}));'
              'process.exit(r.ok?0:32);})'
            + '.catch(e=>{console.error(String(e));process.exit(33);});'
        )

        result = self.runner.run(
            ["docker", "exec", ref.id, "node", "-e", script],
            timeout=timeout,
        )

        if not result.stdout.strip():
            raise RuntimeError(
                result.stderr.strip()
                or "Internal API request produced no output"
            )

        try:
            payload = json.loads(
                result.stdout.strip().splitlines()[-1]
            )
        except json.JSONDecodeError as exc:
            raise RuntimeError(
                f"Invalid internal API response: {result.stdout!r}"
            ) from exc

        status = int(payload.get("status", 0))
        if result.returncode != 0 and status == 0:
            raise RuntimeError(
                result.stderr.strip()
                or "Internal API request failed"
            )

        return status, payload.get("body")

    def get_app_scenario(self, team: str) -> str:
        api = self.find_one(team, "api")
        if not self.container_running(api):
            return "api-down"

        status, body = self._node_fetch(
            api,
            path="/internal/lab/scenario",
            method="GET",
            control=True,
        )

        if (
            status != 200
            or not isinstance(body, dict)
            or "scenario" not in body
        ):
            raise RuntimeError(
                f"Unable to read app scenario for {team}: "
                f"HTTP {status}"
            )

        return str(body["scenario"])

    def set_app_scenario(
        self,
        team: str,
        scenario: str,
    ) -> None:
        api = self.find_one(team, "api")
        if not self.container_running(api):
            raise RuntimeError(
                f"API for {team} is not running"
            )

        status, body = self._node_fetch(
            api,
            path="/internal/lab/scenario",
            method="POST",
            body={"scenario": scenario},
            control=True,
        )

        if not 200 <= status < 300:
            raise RuntimeError(
                f"Unable to set scenario for {team}: "
                f"HTTP {status}: {body!r}"
            )

    def public_status(
        self,
        team: str,
        path: str,
    ) -> int:
        api = self.find_one(team, "api")
        if not self.container_running(api):
            return 0

        status, _ = self._node_fetch(
            api,
            path=path,
            method="GET",
            control=False,
        )
        return status

    def stop_api(self, team: str) -> None:
        api = self.find_one(team, "api")
        if self.container_running(api):
            self.stop(api)

    def start_api(self, team: str) -> None:
        api = self.find_one(team, "api")
        if not self.container_running(api):
            self.start(api)
        self.wait_api(team)

    def restart_api(self, team: str) -> None:
        api = self.find_one(team, "api")
        self.restart(api)
        self.wait_api(team)

    def wait_api(
        self,
        team: str,
        timeout: int = 30,
    ) -> None:
        deadline = time.monotonic() + timeout
        last_error = ""

        while time.monotonic() < deadline:
            try:
                api = self.find_one(team, "api")
                if (
                    self.container_running(api)
                    and self.public_status(
                        team,
                        "/api/health",
                    ) == 200
                ):
                    return
            except Exception as exc:
                last_error = str(exc)
            time.sleep(1)

        raise RuntimeError(
            f"API for {team} did not become healthy: "
            f"{last_error}"
        )

    def validate_scenario(
        self,
        team: str,
        scenario: str,
    ) -> None:
        if scenario == "normal":
            health = self.public_status(
                team,
                "/api/health",
            )
            ranking = self.public_status(
                team,
                "/api/ranking",
            )
            if health != 200 or ranking != 200:
                raise RuntimeError(
                    f"{team}: normal validation failed "
                    f"(health={health}, ranking={ranking})"
                )
            return

        if scenario == "ranking-db-failure":
            health = self.public_status(
                team,
                "/api/health",
            )
            ranking = self.public_status(
                team,
                "/api/ranking",
            )
            if health != 200 or ranking != 500:
                raise RuntimeError(
                    f"{team}: scenario validation failed "
                    f"(health={health}, ranking={ranking})"
                )
            return

        if scenario == "api-down":
            api = self.find_one(team, "api")
            if self.container_running(api):
                raise RuntimeError(
                    f"{team}: api-down requested "
                    "but API is still running"
                )
            return

        raise ValueError(
            f"Unknown scenario: {scenario}"
        )

    def _compose_base(
        self,
        team: str,
    ) -> list[str]:
        if not self.compose_file.is_file():
            raise RuntimeError(
                f"Compose manifest not found: "
                f"{self.compose_file}"
            )

        env_file = (
            self.runtime_dir
            / "teams"
            / f"{team}.env"
        )
        if not env_file.is_file():
            raise RuntimeError(
                f"Runtime env not found: {env_file}"
            )

        project = self.inventory.teams[team][
            "compose_project"
        ]

        return [
            "docker",
            "compose",
            "--project-name",
            project,
            "--env-file",
            str(env_file),
            "-f",
            str(self.compose_file),
        ]

    def _validated_reset_volumes(
        self,
        team: str,
    ) -> list[str]:
        args = [
            "docker",
            "volume",
            "ls",
            "--filter",
            f"label={PROJECT_LABEL}=clublab",
            "--filter",
            f"label={TEAM_LABEL}={team}",
            "--filter",
            f"label={DISPOSABLE_LABEL}=true",
            "--format",
            "{{.Name}}",
        ]

        result = self.runner.run(
            args,
            timeout=10,
        )
        if result.returncode != 0:
            raise RuntimeError(
                "Unable to list team volumes: "
                f"{result.stderr.strip()}"
            )

        names = [
            line.strip()
            for line in result.stdout.splitlines()
            if line.strip()
        ]
        project = self.inventory.teams[team][
            "compose_project"
        ]
        allowed_suffixes = {
            "db-data",
            "lablogs",
        }

        validated: list[str] = []

        for name in names:
            prefix_ok = (
                name.startswith(project + "_")
                or name.startswith(project + "-")
            )
            suffix_ok = any(
                name.endswith("_" + suffix)
                or name.endswith("-" + suffix)
                for suffix in allowed_suffixes
            )

            if not prefix_ok or not suffix_ok:
                raise RuntimeError(
                    "Security guard: refusing "
                    f"unexpected volume {name!r}"
                )

            inspect = self.runner.run(
                ["docker", "volume", "inspect", name],
                timeout=10,
            )
            if inspect.returncode != 0:
                raise RuntimeError(
                    f"Unable to inspect volume {name}: "
                    f"{inspect.stderr.strip()}"
                )

            obj = json.loads(inspect.stdout)[0]
            labels = obj.get("Labels") or {}

            required = {
                PROJECT_LABEL: "clublab",
                TEAM_LABEL: team,
                MANAGED_LABEL: "clublab",
                DISPOSABLE_LABEL: "true",
            }

            for key, expected in required.items():
                if labels.get(key) != expected:
                    raise RuntimeError(
                        "Security guard: refusing "
                        f"volume {name}; invalid label {key}"
                    )

            validated.append(name)

        return validated

    def reset_team(self, team: str) -> None:
        """Rebuild one team through the team.compose.yml contract."""

        base = self._compose_base(team)

        down = self.runner.run(
            base + ["down", "--remove-orphans"],
            timeout=90,
        )
        if down.returncode != 0:
            raise RuntimeError(
                f"Compose down failed for {team}: "
                f"{down.stderr.strip()}"
            )

        for volume in self._validated_reset_volumes(
            team
        ):
            result = self.runner.run(
                ["docker", "volume", "rm", volume],
                timeout=30,
            )
            if result.returncode != 0:
                raise RuntimeError(
                    f"Unable to remove {volume}: "
                    f"{result.stderr.strip()}"
                )

        up_db = self.runner.run(
            base + ["up", "-d", "database"],
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

        deadline = time.monotonic() + 45
        while time.monotonic() < deadline:
            if self.container_health(
                db
            ) in {"healthy", "running"}:
                break
            time.sleep(1)
        else:
            raise RuntimeError(
                f"Database for {team} did not become ready"
            )

        bootstrap = self.runner.run(
            base + ["run", "--rm", "bootstrap"],
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
                "Unable to start team services: "
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
