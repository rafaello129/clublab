from __future__ import annotations

import ipaddress
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class Inventory:
    raw: dict[str, Any]

    @property
    def teams(self) -> dict[str, dict[str, Any]]:
        return self.raw.get("teams", {})

    @property
    def scenarios(self) -> list[str]:
        return self.raw.get("scenarios", [])

    @property
    def roles(self) -> list[str]:
        return self.raw.get("roles", [])


def load_inventory(path: Path) -> Inventory:
    try:
        raw = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise ValueError(f"Inventory not found: {path}") from exc
    except json.JSONDecodeError as exc:
        raise ValueError(f"Inventory JSON is invalid: {exc}") from exc
    if not isinstance(raw, dict):
        raise ValueError("Inventory root must be an object")
    return Inventory(raw)


def validate_inventory(inv: Inventory) -> list[str]:
    errors: list[str] = []
    teams = inv.teams
    if not teams:
        return ["No teams are defined"]

    required = {
        "display_name",
        "access_port",
        "app_subnet",
        "data_subnet",
        "compose_project",
        "enabled_by_default",
    }
    seen_ports: set[int] = set()
    seen_projects: set[str] = set()
    networks: list[tuple[str, ipaddress._BaseNetwork]] = []

    ingress_value = inv.raw.get("gateway", {}).get("ingress_subnet")
    try:
        networks.append(("gateway.ingress", ipaddress.ip_network(ingress_value, strict=True)))
    except Exception:
        errors.append(f"Invalid gateway ingress_subnet: {ingress_value!r}")

    for name, cfg in teams.items():
        if name != "spare" and not (
            name.startswith("team") and len(name) == 6 and name[4:].isdigit()
        ):
            errors.append(f"Invalid target name: {name}")

        missing = sorted(required - set(cfg))
        if missing:
            errors.append(f"{name}: missing fields: {', '.join(missing)}")
            continue

        port = cfg["access_port"]
        if not isinstance(port, int) or not (1024 <= port <= 65535):
            errors.append(f"{name}: invalid access_port {port!r}")
        elif port in seen_ports:
            errors.append(f"{name}: duplicate access_port {port}")
        else:
            seen_ports.add(port)

        project = cfg["compose_project"]
        if project in seen_projects:
            errors.append(f"{name}: duplicate compose_project {project}")
        seen_projects.add(project)

        for field in ("app_subnet", "data_subnet"):
            value = cfg[field]
            try:
                networks.append(
                    (f"{name}.{field}", ipaddress.ip_network(value, strict=True))
                )
            except ValueError:
                errors.append(f"{name}: invalid {field} {value!r}")

    for i, (left_name, left) in enumerate(networks):
        for right_name, right in networks[i + 1 :]:
            if left.overlaps(right):
                errors.append(
                    f"Network overlap: {left_name} {left} <-> {right_name} {right}"
                )

    return errors


def require_target(inv: Inventory, target: str, *, allow_all: bool = False) -> None:
    if allow_all and target == "all":
        return
    if target not in inv.teams:
        raise ValueError(f"Unknown target: {target}")
