from __future__ import annotations

import os
from pathlib import Path
from typing import Any

CONTROLS_INDEX_PATH = "controls/index.md"
CONTROLS_DIR = os.path.dirname(CONTROLS_INDEX_PATH)
SKIP_PATHS = {CONTROLS_INDEX_PATH}


def _relative_markdown_path(path: str) -> str:
    """Return a path relative to the controls index for stable links."""
    base = CONTROLS_DIR or "."
    return os.path.relpath(path, base).replace(os.sep, "/")


def _build_link(target: str, title: str) -> str:
    """Render a Markdown link for a control entry."""
    return f"[`{title}`]({_relative_markdown_path(target)})"


def _find_nav_branch(items: list[Any] | None, label: str):
    if not isinstance(items, list):
        return None
    for entry in items:
        if isinstance(entry, dict) and label in entry:
            return entry[label]
    return None


def _partition_section_entries(entries: list[Any]) -> tuple[str | None, list[Any]]:
    """Return (overview_path, child_entries) for a nav section.

    MkDocs lets sections include raw file paths (treated as implicit "Overview"
    pages) or an explicit `{ "Overview": "path.md" }` mapping. The overview
    entry should power the parent link, so we peel it out and ensure it doesn't
    reappear as a standalone bullet.
    """
    overview_path: str | None = None
    remaining: list[Any] = []
    for item in entries:
        if isinstance(item, str):
            if overview_path is None and item not in SKIP_PATHS:
                overview_path = item
                continue
        elif isinstance(item, dict):
            used_for_overview = False
            if overview_path is None:
                for title, value in item.items():
                    if (
                        isinstance(value, str)
                        and title.casefold() == "overview"
                        and value not in SKIP_PATHS
                    ):
                        overview_path = value
                        used_for_overview = True
                        break
            if used_for_overview:
                continue
        remaining.append(item)
    return overview_path, remaining


def _build_nav_nodes(entries: list[Any] | None):
    """Convert MkDocs nav entries into a tree of dict nodes."""
    nodes: list[dict[str, Any]] = []
    for entry in entries or []:
        if isinstance(entry, str):
            # Unlabeled entries (e.g. "controls/canvas/index.md") serve as
            # section landing pages and are attached to their parent.
            continue
        if isinstance(entry, dict):
            for title, value in entry.items():
                if isinstance(value, list):
                    # Sections are represented as lists; grab their overview
                    # link (if any) and continue recursively with the rest.
                    overview_path, remainder = _partition_section_entries(value)
                    children = _build_nav_nodes(remainder)
                    nodes.append(
                        {"title": title, "path": overview_path, "children": children}
                    )
                else:
                    if value in SKIP_PATHS:
                        continue
                    nodes.append({"title": title, "path": value, "children": []})
    return nodes


def _format_nav_list(nodes: list[dict[str, Any]], depth: int = 0) -> list[str]:
    """Render the navigation nodes as a simple Markdown list."""
    lines: list[str] = []
    indent = " " * (depth * 4)  # 4 spaces per level to keep Markdown happy
    for node in nodes:
        children = node.get("children") or []
        path = node.get("path")
        title = node["title"]
        label = _build_link(path, title) if path else f"**{title}**"
        lines.append(f"{indent}- {label}")
        if children:
            lines.extend(_format_nav_list(children, depth + 1))
    return lines


def render_controls_overview() -> str:
    """Produce the controls overview section from mkdocs.yml."""
    from mkdocs.config import load_config

    docs_root = Path(__file__).resolve().parents[3]
    config = load_config(str(docs_root / "mkdocs.yml"))
    nav_items = config.get("nav") or []

    api_reference = _find_nav_branch(nav_items, "API Reference")
    controls = _find_nav_branch(api_reference, "Controls") if api_reference else None
    nodes = _build_nav_nodes(controls) if isinstance(controls, list) else []
    if not nodes:
        return ""
    lines = _format_nav_list(nodes)
    return "\n".join(lines) + "\n"


if __name__ == "__main__":
    print(render_controls_overview())
