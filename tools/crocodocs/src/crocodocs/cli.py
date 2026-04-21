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
    """Register CLI options that both `generate` and `watch` understand."""
    parser.add_argument(
        "--docs-path",
        metavar="PATH",
        help="Path to the docs directory containing .md/.mdx files. "
        "Overrides 'docs_path' from pyproject.toml.",
    )
    parser.add_argument(
        "--manifest-output",
        metavar="PATH",
        help="Where to write the docs-manifest JSON file. "
        "Overrides 'manifest_output' from pyproject.toml.",
    )
    parser.add_argument(
        "--output",
        metavar="PATH",
        help="Where to write the api-data JSON file. "
        "Overrides 'api_output' from pyproject.toml.",
    )
    parser.add_argument(
        "--sidebars-source",
        metavar="PATH",
        help="Path to the sidebars YAML source file. "
        "Overrides 'sidebars_source' from pyproject.toml.",
    )
    parser.add_argument(
        "--sidebars-output",
        metavar="PATH",
        help="Where to write the generated sidebars.js file. "
        "Overrides 'sidebars_output' from pyproject.toml.",
    )
    parser.add_argument(
        "--base-url",
        metavar="URL",
        help="Base URL prefix for generated doc routes (e.g. '/docs'). "
        "Overrides 'base_url' from pyproject.toml.",
    )
    parser.add_argument(
        "--package",
        action="append",
        metavar="NAME:PATH",
        help="Add or override a Python package source root for API extraction. "
        "Can be specified multiple times. Example: --package flet:../../sdk/python/packages/flet/src",
    )
    parser.add_argument(
        "--extensions",
        action="append",
        metavar="MODULE",
        help="Griffe extension module to load during API extraction. "
        "Can be specified multiple times.",
    )


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
    parser = argparse.ArgumentParser(
        prog="crocodocs",
        description="CrocoDocs — documentation artifact generator for the Flet project. "
        "Reads configuration from [tool.crocodocs] in pyproject.toml. "
        "All path options are resolved relative to the working directory.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    generate = subparsers.add_parser(
        "generate",
        help="Run a one-shot generation of all documentation artifacts.",
        description="Generate all documentation artifacts: sidebars, docs manifest, "
        "MDX partials, code examples, API data (via Griffe), and asset copies. "
        "Defaults are loaded from [tool.crocodocs] in pyproject.toml; "
        "CLI flags override individual settings.",
    )
    _add_shared_generate_arguments(generate)

    watch = subparsers.add_parser(
        "watch",
        help="Watch source files and regenerate on changes, optionally running a child process.",
        description="Run an initial generation, then watch source files for changes and "
        "regenerate automatically. Optionally starts a child process (e.g. Docusaurus "
        "dev server) that runs alongside the watcher. The watcher stops when the child "
        "exits or when interrupted with Ctrl+C.",
    )
    _add_shared_generate_arguments(watch)
    watch.add_argument(
        "--debounce",
        type=float,
        default=0.5,
        metavar="SECS",
        help="Quiet period in seconds after the last detected change before "
        "triggering regeneration. Prevents redundant rebuilds during multi-file "
        "saves (default: %(default)s).",
    )
    watch.add_argument(
        "--child-cwd",
        metavar="PATH",
        help="Working directory for the child command. "
        "Resolved relative to the current working directory.",
    )
    watch.add_argument(
        "watch_command",
        nargs=argparse.REMAINDER,
        metavar="COMMAND",
        help="Command to run alongside the watcher (e.g. a dev server). "
        "Use -- before the command to separate it from CrocoDocs options. "
        "Example: crocodocs watch -- yarn exec docusaurus start",
    )

    return parser


def main(argv: list[str] | None = None) -> int:
    """Parse CLI arguments, apply any overrides to the loaded config, and run the command.

    Returns an exit code (0 on success, 2 on error).
    """
    parser = build_parser()
    args = parser.parse_args(argv)

    # Resolved relative to the CrocoDocs tool directory (Path.cwd() when invoked
    # via `uv --directory ./tools/crocodocs`), NOT the repo root. All relative
    # paths in pyproject.toml and CLI flags are interpreted from here.
    crocodocs_root = Path.cwd()
    config = load_config(crocodocs_root)

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
            (crocodocs_root / args.child_cwd).resolve() if args.child_cwd else None
        )
        return run_watch(
            config,
            debounce=args.debounce,
            command=command or None,
            command_cwd=child_cwd,
        )

    parser.error(f"Unsupported command: {args.command}")
    return 2
