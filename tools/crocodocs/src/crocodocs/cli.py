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


def build_parser() -> argparse.ArgumentParser:
    """Build and return the top-level argument parser with all subcommands registered."""
    parser = argparse.ArgumentParser(prog="crocodocs")
    subparsers = parser.add_subparsers(dest="command", required=True)

    generate = subparsers.add_parser("generate")
    generate.add_argument("--docs-path")
    generate.add_argument("--manifest-output")
    generate.add_argument("--output")
    generate.add_argument("--sidebars-source")
    generate.add_argument("--sidebars-output")
    generate.add_argument("--base-url")
    generate.add_argument("--package", action="append")
    generate.add_argument("--extensions", action="append")

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
        apply_path_override(config, "docs_path", args.docs_path)
        apply_path_override(config, "manifest_output", args.manifest_output)
        apply_path_override(config, "api_output", args.output)
        apply_path_override(config, "sidebars_source", args.sidebars_source)
        apply_path_override(config, "sidebars_output", args.sidebars_output)
        apply_value_override(config, "base_url", args.base_url)
        apply_package_overrides(config, args.package)
        if args.extensions:
            config.extensions = args.extensions
        run_generate(
            config,
            docs_path=config.docs_path,
            manifest_output=config.manifest_output,
            api_output=config.api_output,
            base_url=config.base_url,
        )
        return 0

    parser.error(f"Unsupported command: {args.command}")
    return 2
