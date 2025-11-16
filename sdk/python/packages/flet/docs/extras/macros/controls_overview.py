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
    return f"[{title}]({_relative_markdown_path(target)})"


def _find_nav_branch(items: list[Any] | None, label: str):
    if not isinstance(items, list):
        return None
    for entry in items:
        if isinstance(entry, dict) and label in entry:
            return entry[label]
    return None


def _build_nav_nodes(entries: list[Any] | None):
    """Convert MkDocs nav entries into a tree of dict nodes."""
    nodes: list[dict[str, Any]] = []
    for entry in entries or []:
        if isinstance(entry, str):
            # Unlabeled entries represent overview pages inside sections.
            # They are omitted from the flat list to keep only named controls.
            continue
        if isinstance(entry, dict):
            for title, value in entry.items():
                if isinstance(value, list):
                    children = _build_nav_nodes(value)
                    nodes.append({"title": title, "path": None, "children": children})
                else:
                    if value in SKIP_PATHS:
                        continue
                    nodes.append({"title": title, "path": value, "children": []})
    return nodes


def _collect_link_nodes(nodes: list[dict[str, Any]]) -> list[dict[str, str]]:
    """Flatten the tree of nav nodes into title/path pairs."""
    entries: list[dict[str, str]] = []
    for node in nodes:
        path = node.get("path")
        if path:
            entries.append({"title": node["title"], "path": path})
        children = node.get("children") or []
        if children:
            entries.extend(_collect_link_nodes(children))
    return entries


def _format_link_grid(entries: list[dict[str, str]]) -> str:
    """Wrap entries in markup consumed by controls.css."""
    lines = ['<div class="controls-grid" markdown="1">']
    for entry in entries:
        lines.append(f"- {_build_link(entry['path'], entry['title'])}")
    lines.append("</div>")
    return "\n".join(lines)


def render_controls_overview() -> str:
    """Produce the controls overview section from mkdocs.yml."""
    from mkdocs.config import load_config

    docs_root = Path(__file__).resolve().parents[3]
    config = load_config(str(docs_root / "mkdocs.yml"))
    nav_items = config.get("nav") or []

    api_reference = _find_nav_branch(nav_items, "API Reference")
    controls = _find_nav_branch(api_reference, "Controls") if api_reference else None
    nodes = _build_nav_nodes(controls) if isinstance(controls, list) else []

    links = _collect_link_nodes(nodes)
    links.sort(key=lambda entry: entry["title"].casefold())
    if not links:
        return ""
    return _format_link_grid(links) + "\n"


if __name__ == "__main__":
    print(render_controls_overview())
