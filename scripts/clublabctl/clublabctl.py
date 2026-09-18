#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import sys
from dataclasses import dataclass
from pathlib import Path

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

from clublabctl_lib import (  # noqa: E402
    AuditLogger,
    CHECK_FAILED,
    CONFIG,
    NOT_IMPLEMENTED,
    OK,
    OPERATION_FAILED,
    SECURITY_GUARD,
    CommandRunner,
    Inventory,
    OperationalMonitor,
    PreflightRunner,
    ScenarioManager,
    SpareManager,
    StateStore,
    aggregate,
    has_critical_failure,
    load_inventory,
    require_target,
    validate_inventory,
)
from clublabctl_lib.operational_runtime import OperationalRuntime  # noqa: E402


VERSION = "0.3.0"
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


@dataclass
class Context:
    inventory: Inventory
    manager: ScenarioManager
    monitor: OperationalMonitor
    preflight: PreflightRunner
    spare: SpareManager
    audit: AuditLogger


def cmd_version(
    _: argparse.Namespace,
    __: Context,
) -> int:
    print(VERSION)
    return OK


def cmd_inventory_list(
    _: argparse.Namespace,
    ctx: Context,
) -> int:
    inv = ctx.inventory
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
    ctx: Context,
) -> int:
    require_target(
        ctx.inventory,
        args.target,
    )
    print(
        json.dumps(
            ctx.inventory.teams[args.target],
            indent=2,
            ensure_ascii=False,
        )
    )
    return OK


def cmd_inventory_validate(
    _: argparse.Namespace,
    ctx: Context,
) -> int:
    errors = validate_inventory(
        ctx.inventory
    )
    if errors:
        for error in errors:
            print(f"FAIL {error}")
        return CHECK_FAILED

    print(
        f"PASS inventory valid "
        f"({len(ctx.inventory.teams)} targets)"
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
    ctx: Context,
) -> int:
    if args.scenario not in ctx.inventory.scenarios:
        raise ValueError(
            f"Unknown scenario: {args.scenario}"
        )

    teams = ctx.manager.expand_target(
        args.target
    )
    results = [
        ctx.manager.load_one(
            team,
            args.scenario,
        )
        for team in teams
    ]
    return print_results(results)


def cmd_scenario_clear(
    args: argparse.Namespace,
    ctx: Context,
) -> int:
    teams = ctx.manager.expand_target(
        args.target
    )
    results = [
        ctx.manager.clear_one(team)
        for team in teams
    ]
    return print_results(results)


def cmd_scenario_status(
    args: argparse.Namespace,
    ctx: Context,
) -> int:
    teams = ctx.manager.expand_target(
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
            status = ctx.manager.status_one(
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
    ctx: Context,
) -> int:
    teams = ctx.manager.expand_target(
        args.target
    )
    results = [
        ctx.manager.recover_one(team)
        for team in teams
    ]
    return print_results(results)


def cmd_reset(
    args: argparse.Namespace,
    ctx: Context,
) -> int:
    teams = ctx.manager.expand_target(
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
        ctx.manager.reset_one(
            team,
            confirmed=True,
        )
        for team in teams
    ]
    return print_results(results)


def cmd_preflight(
    args: argparse.Namespace,
    ctx: Context,
) -> int:
    results = ctx.preflight.run(
        args.target
    )

    print(
        f"{'CATEGORY':<10} "
        f"{'STATUS':<6} "
        f"{'CHECK':<28} "
        f"DETAIL"
    )

    for item in results:
        print(
            f"{item.category:<10} "
            f"{item.status:<6} "
            f"{item.name:<28} "
            f"{item.detail}"
        )

    failed = has_critical_failure(
        results
    )
    ctx.audit.write(
        action="preflight",
        result="failure" if failed else "success",
        team=args.target,
        meta={
            "code": (
                CHECK_FAILED
                if failed
                else OK
            )
        },
    )
    return (
        CHECK_FAILED
        if failed
        else OK
    )


def cmd_status(
    args: argparse.Namespace,
    ctx: Context,
) -> int:
    targets = ctx.monitor.targets(
        args.target
    )

    print(
        f"{'TEAM':<8} "
        f"{'FRONT':<8} "
        f"{'API':<8} "
        f"{'DB':<8} "
        f"{'TOOLBOX':<8} "
        f"{'SCENARIO':<24} "
        f"{'STATE'}"
    )

    failed = False
    for team in targets:
        status = ctx.monitor.status_one(
            team
        )
        print(
            f"{status.team:<8} "
            f"{status.frontend:<8} "
            f"{status.api:<8} "
            f"{status.database:<8} "
            f"{status.toolbox:<8} "
            f"{status.scenario:<24} "
            f"{status.infra_state}"
        )

        if status.infra_state in {
            "DEGRADED",
            "FAILED",
        }:
            failed = True
        if (
            args.target != "all"
            and status.infra_state == "ABSENT"
        ):
            failed = True

    return (
        CHECK_FAILED
        if failed
        else OK
    )


def cmd_resources(
    args: argparse.Namespace,
    ctx: Context,
) -> int:
    rows = ctx.monitor.resources(
        args.target
    )

    if not rows:
        print("No deployed ClubLab resources found.")
        return OK

    print(
        f"{'TEAM':<8} "
        f"{'ROLE':<10} "
        f"{'CPU':<10} "
        f"{'MEMORY':<24} "
        f"{'PIDS':<8} "
        f"NET I/O"
    )

    for row in rows:
        print(
            f"{row['team']:<8} "
            f"{row['role']:<10} "
            f"{str(row['cpu']):<10} "
            f"{str(row['memory']):<24} "
            f"{str(row['pids']):<8} "
            f"{row['net_io']}"
        )
    return OK


def cmd_logs(
    args: argparse.Namespace,
    ctx: Context,
) -> int:
    content = ctx.monitor.logs(
        args.target,
        args.role,
        lines=args.lines,
    )
    if content:
        print(content)
    return OK


def cmd_spare_status(
    _: argparse.Namespace,
    ctx: Context,
) -> int:
    status = ctx.spare.status()
    assignment = status["assignment"]
    assigned = (
        assignment.get("assigned_team")
        if assignment
        else "-"
    )

    print(
        f"Spare state:    {status['infra_state']}"
    )
    print(
        f"Scenario:       {status['scenario']}"
    )
    print(
        f"Frontend:       {status['frontend']}"
    )
    print(
        f"API:            {status['api']}"
    )
    print(
        f"Database:       {status['database']}"
    )
    print(
        f"Toolbox:        {status['toolbox']}"
    )
    print(
        f"Access port:    {status['access_port']}"
    )
    print(
        f"Assigned team:  {assigned}"
    )

    return (
        OK
        if status["infra_state"] == "READY"
        and status["scenario"] == "normal"
        else CHECK_FAILED
    )


def cmd_spare_assign(
    args: argparse.Namespace,
    ctx: Context,
) -> int:
    require_target(
        ctx.inventory,
        args.target,
    )
    value = ctx.spare.assign(
        args.target
    )
    port = value["access_port"]
    bind_ip = os.getenv(
        ctx.inventory.raw.get(
            "gateway",
            {},
        ).get(
            "bind_ip_env",
            "CLUBLAB_BIND_IP",
        ),
        "",
    ).strip()

    print(
        f"Spare assigned to {value['assigned_team']}."
    )
    if bind_ip:
        print(
            f"Access URL: http://{bind_ip}:{port}"
        )
    else:
        print(
            f"Access port: {port}"
        )
    print(
        "Use the spare access credentials prepared for the session."
    )
    return OK


def cmd_spare_release(
    _: argparse.Namespace,
    ctx: Context,
) -> int:
    changed = ctx.spare.release()
    print(
        "Spare assignment released."
        if changed
        else "Spare was not assigned."
    )
    return OK


def cmd_audit_tail(
    args: argparse.Namespace,
    ctx: Context,
) -> int:
    events = ctx.audit.tail(
        args.lines
    )
    if not events:
        print("Audit log is empty.")
        return OK

    for event in events:
        print(
            f"{event.get('ts', '?')} "
            f"{event.get('actor', '?'):<12} "
            f"{event.get('action', '?'):<18} "
            f"{event.get('team', '-'):<8} "
            f"{event.get('result', '?')}"
        )
    return OK


def cmd_planned(
    args: argparse.Namespace,
    ctx: Context,
) -> int:
    target = getattr(
        args,
        "target",
        None,
    )
    if target is not None:
        require_target(
            ctx.inventory,
            target,
            allow_all=True,
        )

    print(
        f"{args.command_path}: "
        "reserved by Phase 5; "
        "implementation arrives in Block D.",
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

    p = sub.add_parser("preflight")
    p.add_argument(
        "target",
        nargs="?",
        default="all",
    )
    p.set_defaults(
        func=cmd_preflight
    )

    p = sub.add_parser("status")
    p.add_argument(
        "target",
        nargs="?",
        default="all",
    )
    p.set_defaults(
        func=cmd_status
    )

    p = sub.add_parser("resources")
    p.add_argument(
        "target",
        nargs="?",
        default="all",
    )
    p.set_defaults(
        func=cmd_resources
    )

    p = sub.add_parser("logs")
    p.add_argument("target")
    p.add_argument("role")
    p.add_argument(
        "--lines",
        type=int,
        default=100,
    )
    p.set_defaults(
        func=cmd_logs
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

    p = sub.add_parser("deploy")
    p.add_argument(
        "target",
        nargs="?",
        default="all",
    )
    p.set_defaults(
        func=cmd_planned,
        command_path="deploy",
    )

    spare = sub.add_parser("spare")
    spare_sub = spare.add_subparsers(
        dest="spare_command",
        required=True,
    )

    p = spare_sub.add_parser("status")
    p.set_defaults(
        func=cmd_spare_status
    )

    p = spare_sub.add_parser("assign")
    p.add_argument("target")
    p.set_defaults(
        func=cmd_spare_assign
    )

    p = spare_sub.add_parser("release")
    p.set_defaults(
        func=cmd_spare_release
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
        func=cmd_audit_tail
    )

    return parser


def build_context(
    args: argparse.Namespace,
) -> Context:
    inv = load_inventory(
        args.inventory
    )

    errors = validate_inventory(inv)
    if (
        errors
        and args.command != "inventory"
    ):
        raise ValueError(
            "; ".join(errors)
        )

    runner = CommandRunner()
    state = StateStore(
        args.runtime_dir
    )
    audit = AuditLogger(
        args.runtime_dir
    )
    runtime = OperationalRuntime(
        inv,
        runner,
        REPO_ROOT,
        args.runtime_dir,
    )
    manager = ScenarioManager(
        inv,
        runtime,
        state,
        audit=audit,
    )
    monitor = OperationalMonitor(
        inv,
        runtime,
        state,
    )
    preflight = PreflightRunner(
        inv,
        runtime,
        runner,
        REPO_ROOT,
        args.runtime_dir,
    )
    spare = SpareManager(
        inv,
        monitor,
        args.runtime_dir,
        audit=audit,
    )

    return Context(
        inventory=inv,
        manager=manager,
        monitor=monitor,
        preflight=preflight,
        spare=spare,
        audit=audit,
    )


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    try:
        ctx = build_context(
            args
        )
        return int(
            args.func(
                args,
                ctx,
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
