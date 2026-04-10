"""CrocoDocs CLI entrypoint."""

from __future__ import annotations

import argparse
from pathlib import Path

from .config import (
    apply_package_overrides,
    apply_path_override,
    apply_value_override,
    load_config,
)
from .generate import run_generate
from .watch import run_watch


def _add_shared_generate_arguments(parser: argparse.ArgumentParser) -> None:
    """Register CLI options that both ``generate`` and ``watch`` understand."""
    parser.add_argument("--docs-path")
    parser.add_argument("--manifest-output")
    parser.add_argument("--output")
    parser.add_argument("--sidebars-source")
    parser.add_argument("--sidebars-output")
    parser.add_argument("--base-url")
    parser.add_argument("--package", action="append")
    parser.add_argument("--extensions", action="append")


def _apply_shared_generate_overrides(config, args: argparse.Namespace) -> None:
    """Apply path/value/package overrides shared by generation-oriented commands."""
    apply_path_override(config, "docs_path", args.docs_path)
    apply_path_override(config, "manifest_output", args.manifest_output)
    apply_path_override(config, "api_output", args.output)
    apply_path_override(config, "sidebars_source", args.sidebars_source)
    apply_path_override(config, "sidebars_output", args.sidebars_output)
    apply_value_override(config, "base_url", args.base_url)
    apply_package_overrides(config, args.package)
    if args.extensions:
        config.extensions = args.extensions


def build_parser() -> argparse.ArgumentParser:
    """Build and return the top-level argument parser with all subcommands registered."""
    parser = argparse.ArgumentParser(prog="crocodocs")
    subparsers = parser.add_subparsers(dest="command", required=True)

    generate = subparsers.add_parser("generate")
    _add_shared_generate_arguments(generate)

    watch = subparsers.add_parser("watch")
    _add_shared_generate_arguments(watch)
    watch.add_argument(
        "--interval",
        type=float,
        default=0.75,
        help="Polling interval in seconds between filesystem scans.",
    )
    watch.add_argument(
        "--debounce",
        type=float,
        default=0.5,
        help="Quiet period in seconds before a detected change triggers regeneration.",
    )
    watch.add_argument(
        "--child-cwd",
        help="Working directory for the optional child command started after initial generation.",
    )
    watch.add_argument(
        "watch_command",
        nargs=argparse.REMAINDER,
        help="Optional command to run alongside the watcher. Prefix with -- to separate it from CrocoDocs options.",
    )

    return parser


def main(argv: list[str] | None = None) -> int:
    """Parse CLI arguments, apply any overrides to the loaded config, and run the command.

    Returns an exit code (0 on success, 2 on error).
    """
    parser = build_parser()
    args = parser.parse_args(argv)

    project_root = Path.cwd()
    config = load_config(project_root)

    if args.command == "generate":
        _apply_shared_generate_overrides(config, args)
        run_generate(
            config,
            docs_path=config.docs_path,
            manifest_output=config.manifest_output,
            api_output=config.api_output,
            base_url=config.base_url,
        )
        return 0

    if args.command == "watch":
        _apply_shared_generate_overrides(config, args)
        command = list(args.watch_command)
        if command and command[0] == "--":
            command = command[1:]
        child_cwd = (
            (project_root / args.child_cwd).resolve() if args.child_cwd else None
        )
        return run_watch(
            config,
            interval=args.interval,
            debounce=args.debounce,
            command=command or None,
            command_cwd=child_cwd,
        )

    parser.error(f"Unsupported command: {args.command}")
    return 2
