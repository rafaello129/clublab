#!/usr/bin/env python3
"""Instructor-side ClubLab control CLI — Phase 5 Block A scaffold."""

from __future__ import annotations

import argparse
import ipaddress
import json
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any

VERSION = "0.1.0"

OK = 0
CONFIG = 3
CHECK_FAILED = 4
OPERATION_FAILED = 5
STATE_CONFLICT = 6
PARTIAL_SUCCESS = 7
DEPENDENCY_UNAVAILABLE = 8
SECURITY_GUARD = 9
NOT_IMPLEMENTED = 10

REPO_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_INVENTORY = REPO_ROOT / "infrastructure" / "teams" / "teams.json"


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
        ingress = ipaddress.ip_network(ingress_value, strict=True)
        networks.append(("gateway.ingress", ingress))
    except Exception:
        errors.append(f"Invalid gateway ingress_subnet: {ingress_value!r}")

    for name, cfg in teams.items():
        if name != "spare" and not (name.startswith("team") and len(name) == 6 and name[4:].isdigit()):
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
                net = ipaddress.ip_network(value, strict=True)
                networks.append((f"{name}.{field}", net))
            except ValueError:
                errors.append(f"{name}: invalid {field} {value!r}")

    for i, (left_name, left) in enumerate(networks):
        for right_name, right in networks[i + 1:]:
            if left.overlaps(right):
                errors.append(f"Network overlap: {left_name} {left} <-> {right_name} {right}")

    return errors


def require_target(inv: Inventory, target: str, *, allow_all: bool = False) -> None:
    if allow_all and target == "all":
        return
    if target not in inv.teams:
        raise ValueError(f"Unknown target: {target}")


def planned(action: str) -> int:
    print(f"{action}: reserved by the Phase 5 contract; implementation arrives in Blocks B/C.", file=sys.stderr)
    return NOT_IMPLEMENTED


def cmd_version(_: argparse.Namespace, __: Inventory) -> int:
    print(VERSION)
    return OK


def cmd_inventory_list(_: argparse.Namespace, inv: Inventory) -> int:
    print(f"{'TARGET':<8} {'PORT':<6} {'APP SUBNET':<18} {'DATA SUBNET':<18} {'DEFAULT'}")
    for name, cfg in inv.teams.items():
        print(
            f"{name:<8} {cfg['access_port']:<6} {cfg['app_subnet']:<18} "
            f"{cfg['data_subnet']:<18} {'yes' if cfg['enabled_by_default'] else 'no'}"
        )
    return OK


def cmd_inventory_show(args: argparse.Namespace, inv: Inventory) -> int:
    require_target(inv, args.target)
    print(json.dumps(inv.teams[args.target], indent=2, ensure_ascii=False))
    return OK


def cmd_inventory_validate(_: argparse.Namespace, inv: Inventory) -> int:
    errors = validate_inventory(inv)
    if errors:
        for error in errors:
            print(f"FAIL {error}")
        return CHECK_FAILED
    print(f"PASS inventory valid ({len(inv.teams)} targets)")
    return OK


def cmd_planned(args: argparse.Namespace, inv: Inventory) -> int:
    target = getattr(args, "target", None)
    if target is not None:
        require_target(inv, target, allow_all=True)
    scenario = getattr(args, "scenario", None)
    if scenario is not None and scenario not in inv.scenarios:
        raise ValueError(f"Unknown scenario: {scenario}")
    role = getattr(args, "role", None)
    if role is not None and role not in inv.roles:
        raise ValueError(f"Unknown role: {role}")
    return planned(args.command_path)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="clublabctl", description="ClubLab instructor control plane")
    parser.add_argument("--inventory", type=Path, default=DEFAULT_INVENTORY)
    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser("version")
    p.set_defaults(func=cmd_version)

    inv = sub.add_parser("inventory")
    inv_sub = inv.add_subparsers(dest="inventory_command", required=True)
    p = inv_sub.add_parser("list")
    p.set_defaults(func=cmd_inventory_list)
    p = inv_sub.add_parser("show")
    p.add_argument("target")
    p.set_defaults(func=cmd_inventory_show)
    p = inv_sub.add_parser("validate")
    p.set_defaults(func=cmd_inventory_validate)

    p = sub.add_parser("preflight")
    p.add_argument("target", nargs="?", default="all")
    p.set_defaults(func=cmd_planned, command_path="preflight")

    p = sub.add_parser("deploy")
    p.add_argument("target")
    p.set_defaults(func=cmd_planned, command_path="deploy")

    p = sub.add_parser("status")
    p.add_argument("target", nargs="?", default="all")
    p.set_defaults(func=cmd_planned, command_path="status")

    p = sub.add_parser("resources")
    p.add_argument("target", nargs="?", default="all")
    p.set_defaults(func=cmd_planned, command_path="resources")

    p = sub.add_parser("logs")
    p.add_argument("target")
    p.add_argument("role")
    p.set_defaults(func=cmd_planned, command_path="logs")

    scenario = sub.add_parser("scenario")
    scenario_sub = scenario.add_subparsers(dest="scenario_command", required=True)
    p = scenario_sub.add_parser("load")
    p.add_argument("target")
    p.add_argument("scenario")
    p.set_defaults(func=cmd_planned, command_path="scenario load")
    p = scenario_sub.add_parser("clear")
    p.add_argument("target")
    p.set_defaults(func=cmd_planned, command_path="scenario clear")
    p = scenario_sub.add_parser("status")
    p.add_argument("target")
    p.set_defaults(func=cmd_planned, command_path="scenario status")

    p = sub.add_parser("recover")
    p.add_argument("target")
    p.set_defaults(func=cmd_planned, command_path="recover")

    p = sub.add_parser("reset")
    p.add_argument("target")
    p.add_argument("--yes", action="store_true")
    p.set_defaults(func=cmd_planned, command_path="reset")

    spare = sub.add_parser("spare")
    spare_sub = spare.add_subparsers(dest="spare_command", required=True)
    p = spare_sub.add_parser("status")
    p.set_defaults(func=cmd_planned, command_path="spare status")
    p = spare_sub.add_parser("assign")
    p.add_argument("target")
    p.set_defaults(func=cmd_planned, command_path="spare assign")

    audit = sub.add_parser("audit")
    audit_sub = audit.add_subparsers(dest="audit_command", required=True)
    p = audit_sub.add_parser("tail")
    p.add_argument("--lines", type=int, default=30)
    p.set_defaults(func=cmd_planned, command_path="audit tail")

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    try:
        inv = load_inventory(args.inventory)
        return int(args.func(args, inv))
    except ValueError as exc:
        print(f"ERROR {exc}", file=sys.stderr)
        return CONFIG


if __name__ == "__main__":
    raise SystemExit(main())
