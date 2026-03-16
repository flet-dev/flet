"""Build orchestrator for the Flet MCP data pipeline.

Coordinates indexing of examples, docs, and API reference into the
data directory consumed by the MCP server.
"""

from __future__ import annotations

import logging
import sqlite3
import time
from pathlib import Path

from flet_mcp.build.api import build_api
from flet_mcp.build.docs import index_docs
from flet_mcp.build.examples import index_examples

logger = logging.getLogger(__name__)

_DATA_DIR = Path(__file__).resolve().parent.parent / "data"


def _print_summary(metrics: list[tuple[str, str, float]]) -> None:
    """Print a summary table of build steps.

    Each entry is (step_name, result_text, elapsed_seconds).
    """
    try:
        from rich.console import Console
        from rich.table import Table

        console = Console()
        table = Table(title="MCP Build Summary")
        table.add_column("Step", style="bold")
        table.add_column("Result", justify="right")
        table.add_column("Time", justify="right", style="dim")

        for step, result, elapsed in metrics:
            table.add_row(step, result, f"{elapsed:.2f}s")

        console.print(table)
    except ImportError:
        # Fallback to plain output
        print("\n--- MCP Build Summary ---")
        for step, result, elapsed in metrics:
            print(f"  {step:<20s} {result:>30s}  ({elapsed:.2f}s)")
        print()


def build_all(
    examples_dir: Path | None = None,
    docs_index: Path | None = None,
    output_dir: Path | None = None,
) -> None:
    """Run the full MCP build pipeline.

    Parameters:
        examples_dir: Root directory containing Flet example projects.
        docs_index:   Path to the mkdocs search_index.json file.
        output_dir:   Where to write mcp.db and api.json.
                      Defaults to the ``flet_mcp/data/`` package directory.
    """
    if output_dir is None:
        output_dir = _DATA_DIR
    output_dir.mkdir(parents=True, exist_ok=True)

    db_path = output_dir / "mcp.db"
    api_path = output_dir / "api.json"

    # Remove existing DB so we start fresh
    if db_path.exists():
        db_path.unlink()

    metrics: list[tuple[str, str, float]] = []
    conn = sqlite3.connect(str(db_path))

    try:
        # ---- Examples ----
        if examples_dir is not None:
            t0 = time.perf_counter()
            n = index_examples(conn, examples_dir)
            elapsed = time.perf_counter() - t0
            metrics.append(("Examples", f"{n} indexed", elapsed))
            logger.info("Indexed %d examples in %.2fs", n, elapsed)

        # ---- Docs ----
        if docs_index is not None:
            t0 = time.perf_counter()
            n = index_docs(conn, docs_index)
            elapsed = time.perf_counter() - t0
            metrics.append(("Docs", f"{n} indexed", elapsed))
            logger.info("Indexed %d doc entries in %.2fs", n, elapsed)

        # ---- API reference ----
        t0 = time.perf_counter()
        stats = build_api(api_path)
        elapsed = time.perf_counter() - t0
        parts = [f"{v} {k}" for k, v in stats.items()]
        metrics.append(("API", ", ".join(parts), elapsed))
        logger.info("Built API reference in %.2fs: %s", elapsed, stats)

    finally:
        conn.close()

    _print_summary(metrics)
