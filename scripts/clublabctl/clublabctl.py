#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

from clublabctl_lib import (  # noqa: E402
    CHECK_FAILED,
    CONFIG,
    NOT_IMPLEMENTED,
    OK,
    OPERATION_FAILED,
    SECURITY_GUARD,
    CommandRunner,
    Inventory,
    ScenarioManager,
    StateStore,
    aggregate,
    load_inventory,
    require_target,
    validate_inventory,
)
from clublabctl_lib.docker_runtime import DockerRuntime  # noqa: E402


VERSION = "0.2.0"
REPO_ROOT = HERE.parents[1]
DEFAULT_INVENTORY = (
    REPO_ROOT
    / "infrastructure"
    / "teams"
    / "teams.json"
)
DEFAULT_RUNTIME_DIR = Path(
    os.getenv(
        "CLUBLAB_RUNTIME_DIR",
        "/home/tulum/infra/clublab/runtime",
    )
)


def cmd_version(
    _: argparse.Namespace,
    __: Inventory,
    ___: ScenarioManager,
) -> int:
    print(VERSION)
    return OK


def cmd_inventory_list(
    _: argparse.Namespace,
    inv: Inventory,
    __: ScenarioManager,
) -> int:
    print(
        f"{'TARGET':<8} "
        f"{'PORT':<6} "
        f"{'APP SUBNET':<18} "
        f"{'DATA SUBNET':<18} "
        f"{'DEFAULT'}"
    )
    for name, cfg in inv.teams.items():
        print(
            f"{name:<8} "
            f"{cfg['access_port']:<6} "
            f"{cfg['app_subnet']:<18} "
            f"{cfg['data_subnet']:<18} "
            f"{'yes' if cfg['enabled_by_default'] else 'no'}"
        )
    return OK


def cmd_inventory_show(
    args: argparse.Namespace,
    inv: Inventory,
    __: ScenarioManager,
) -> int:
    require_target(
        inv,
        args.target,
    )
    print(
        json.dumps(
            inv.teams[args.target],
            indent=2,
            ensure_ascii=False,
        )
    )
    return OK


def cmd_inventory_validate(
    _: argparse.Namespace,
    inv: Inventory,
    __: ScenarioManager,
) -> int:
    errors = validate_inventory(inv)
    if errors:
        for error in errors:
            print(f"FAIL {error}")
        return CHECK_FAILED

    print(
        f"PASS inventory valid "
        f"({len(inv.teams)} targets)"
    )
    return OK


def print_results(results) -> int:
    for result in results:
        print(
            f"{result.team:<8} "
            f"{'SUCCESS' if result.ok else 'FAIL':<7} "
            f"{result.detail}"
        )
    return aggregate(results)


def cmd_scenario_load(
    args: argparse.Namespace,
    inv: Inventory,
    manager: ScenarioManager,
) -> int:
    if args.scenario not in inv.scenarios:
        raise ValueError(
            f"Unknown scenario: {args.scenario}"
        )

    teams = manager.expand_target(
        args.target
    )
    results = [
        manager.load_one(
            team,
            args.scenario,
        )
        for team in teams
    ]
    return print_results(results)


def cmd_scenario_clear(
    args: argparse.Namespace,
    _: Inventory,
    manager: ScenarioManager,
) -> int:
    teams = manager.expand_target(
        args.target
    )
    results = [
        manager.clear_one(team)
        for team in teams
    ]
    return print_results(results)


def cmd_scenario_status(
    args: argparse.Namespace,
    _: Inventory,
    manager: ScenarioManager,
) -> int:
    teams = manager.expand_target(
        args.target
    )

    print(
        f"{'TEAM':<8} "
        f"{'INFRA':<12} "
        f"{'EXPECTED':<24} "
        f"{'OBSERVED'}"
    )

    failed = False
    for team in teams:
        try:
            status = manager.status_one(
                team
            )
            print(
                f"{team:<8} "
                f"{status['infra_state']:<12} "
                f"{status['expected_scenario']:<24} "
                f"{status['observed_scenario']}"
            )
        except Exception as exc:
            print(
                f"{team:<8} "
                f"{'FAILED':<12} "
                f"{'?':<24} "
                f"{exc}"
            )
            failed = True

    return (
        CHECK_FAILED
        if failed
        else OK
    )


def cmd_recover(
    args: argparse.Namespace,
    _: Inventory,
    manager: ScenarioManager,
) -> int:
    teams = manager.expand_target(
        args.target
    )
    results = [
        manager.recover_one(team)
        for team in teams
    ]
    return print_results(results)


def cmd_reset(
    args: argparse.Namespace,
    _: Inventory,
    manager: ScenarioManager,
) -> int:
    teams = manager.expand_target(
        args.target,
        include_spare=args.target == "all",
    )

    if (
        args.target == "all"
        and args.confirm != "RESET-ALL"
    ):
        print(
            "reset all requires --confirm RESET-ALL",
            file=sys.stderr,
        )
        return SECURITY_GUARD

    if not args.yes:
        print(
            "reset requires --yes",
            file=sys.stderr,
        )
        return SECURITY_GUARD

    results = [
        manager.reset_one(
            team,
            confirmed=True,
        )
        for team in teams
    ]
    return print_results(results)


def cmd_planned(
    args: argparse.Namespace,
    inv: Inventory,
    _: ScenarioManager,
) -> int:
    target = getattr(
        args,
        "target",
        None,
    )
    if target is not None:
        require_target(
            inv,
            target,
            allow_all=True,
        )

    role = getattr(
        args,
        "role",
        None,
    )
    if (
        role is not None
        and role not in inv.roles
    ):
        raise ValueError(
            f"Unknown role: {role}"
        )

    print(
        f"{args.command_path}: "
        "reserved by Phase 5; "
        "implementation arrives in Block C.",
        file=sys.stderr,
    )
    return NOT_IMPLEMENTED


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="clublabctl",
        description="ClubLab instructor control plane",
    )
    parser.add_argument(
        "--inventory",
        type=Path,
        default=DEFAULT_INVENTORY,
    )
    parser.add_argument(
        "--runtime-dir",
        type=Path,
        default=DEFAULT_RUNTIME_DIR,
    )

    sub = parser.add_subparsers(
        dest="command",
        required=True,
    )

    p = sub.add_parser("version")
    p.set_defaults(func=cmd_version)

    inv = sub.add_parser("inventory")
    inv_sub = inv.add_subparsers(
        dest="inventory_command",
        required=True,
    )

    p = inv_sub.add_parser("list")
    p.set_defaults(
        func=cmd_inventory_list
    )

    p = inv_sub.add_parser("show")
    p.add_argument("target")
    p.set_defaults(
        func=cmd_inventory_show
    )

    p = inv_sub.add_parser("validate")
    p.set_defaults(
        func=cmd_inventory_validate
    )

    scenario = sub.add_parser("scenario")
    scenario_sub = scenario.add_subparsers(
        dest="scenario_command",
        required=True,
    )

    p = scenario_sub.add_parser("load")
    p.add_argument("target")
    p.add_argument("scenario")
    p.set_defaults(
        func=cmd_scenario_load
    )

    p = scenario_sub.add_parser("clear")
    p.add_argument("target")
    p.set_defaults(
        func=cmd_scenario_clear
    )

    p = scenario_sub.add_parser("status")
    p.add_argument(
        "target",
        nargs="?",
        default="all",
    )
    p.set_defaults(
        func=cmd_scenario_status
    )

    p = sub.add_parser("recover")
    p.add_argument("target")
    p.set_defaults(
        func=cmd_recover
    )

    p = sub.add_parser("reset")
    p.add_argument("target")
    p.add_argument(
        "--yes",
        action="store_true",
    )
    p.add_argument("--confirm")
    p.set_defaults(
        func=cmd_reset
    )

    for name in (
        "preflight",
        "deploy",
        "status",
        "resources",
    ):
        p = sub.add_parser(name)
        p.add_argument(
            "target",
            nargs="?",
            default="all",
        )
        p.set_defaults(
            func=cmd_planned,
            command_path=name,
        )

    p = sub.add_parser("logs")
    p.add_argument("target")
    p.add_argument("role")
    p.set_defaults(
        func=cmd_planned,
        command_path="logs",
    )

    spare = sub.add_parser("spare")
    spare_sub = spare.add_subparsers(
        dest="spare_command",
        required=True,
    )

    p = spare_sub.add_parser("status")
    p.set_defaults(
        func=cmd_planned,
        command_path="spare status",
    )

    p = spare_sub.add_parser("assign")
    p.add_argument("target")
    p.set_defaults(
        func=cmd_planned,
        command_path="spare assign",
    )

    audit = sub.add_parser("audit")
    audit_sub = audit.add_subparsers(
        dest="audit_command",
        required=True,
    )

    p = audit_sub.add_parser("tail")
    p.add_argument(
        "--lines",
        type=int,
        default=30,
    )
    p.set_defaults(
        func=cmd_planned,
        command_path="audit tail",
    )

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    try:
        inv = load_inventory(
            args.inventory
        )

        errors = validate_inventory(inv)
        if (
            errors
            and args.command != "inventory"
        ):
            for error in errors:
                print(
                    f"FAIL {error}",
                    file=sys.stderr,
                )
            return CONFIG

        runner = CommandRunner()
        state = StateStore(
            args.runtime_dir
        )
        runtime = DockerRuntime(
            inv,
            runner,
            REPO_ROOT,
            args.runtime_dir,
        )
        manager = ScenarioManager(
            inv,
            runtime,
            state,
        )

        return int(
            args.func(
                args,
                inv,
                manager,
            )
        )

    except ValueError as exc:
        print(
            f"ERROR {exc}",
            file=sys.stderr,
        )
        return CONFIG
    except RuntimeError as exc:
        print(
            f"ERROR {exc}",
            file=sys.stderr,
        )
        return OPERATION_FAILED


if __name__ == "__main__":
    raise SystemExit(main())
