import argparse
from pathlib import Path

from flet_cli.commands.base import BaseCommand


class Command(BaseCommand):
    """Flet MCP server for LLM agents."""

    def add_arguments(self, parser: argparse.ArgumentParser) -> None:
        sub = parser.add_subparsers(dest="mcp_command")

        # `flet mcp build` sub-subcommand
        build_parser = sub.add_parser("build", help="Build MCP index data")
        build_parser.add_argument(
            "--examples",
            type=Path,
            help="Path to examples directory",
        )
        build_parser.add_argument(
            "--docs",
            type=Path,
            help="Path to search_index.json",
        )
        build_parser.add_argument(
            "--output",
            type=Path,
            help="Output directory (default: flet_mcp/data/)",
        )

        # `flet mcp` (serve) options — applied to the mcp parser itself
        parser.add_argument(
            "--transport",
            choices=["stdio", "streamable-http"],
            default="stdio",
            help="MCP transport mode",
        )
        parser.add_argument(
            "--port",
            type=int,
            default=8000,
            help="Port for HTTP transport mode",
        )

    def handle(self, options: argparse.Namespace) -> None:
        if options.mcp_command == "build":
            self._handle_build(options)
        else:
            self._handle_serve(options)

    def _handle_serve(self, options: argparse.Namespace) -> None:
        from flet_mcp.server import mcp

        if options.transport == "streamable-http":
            mcp.run(transport="streamable-http", port=options.port)
        else:
            mcp.run(transport="stdio")

    def _handle_build(self, options: argparse.Namespace) -> None:
        from flet_mcp.build.indexer import build_all

        build_all(
            examples_dir=options.examples,
            docs_index=options.docs,
            output_dir=options.output,
        )
