"""Generated partial handling."""

from __future__ import annotations

import contextlib
import importlib.util
import os
import re
import subprocess
import sys
from pathlib import Path
from typing import Any

from .config import CrocoDocsConfig
from .sidebars import _load_nav

LOCAL_MARKDOWN_LINK_RE = re.compile(
    r"(?P<prefix>\]\()(?P<target>(?![a-z][a-z0-9+.-]*:|/|#)[^)]+?\.md)(?P<anchor>#[^)]+)?(?P<suffix>\))",
    re.IGNORECASE,
)
CLI_H3_TICK_RE = re.compile(r"^(### )`([^`]+)`$", re.MULTILINE)
ANGLE_TAG_RE = re.compile(r"<([a-z][a-z0-9_-]*)>", re.IGNORECASE)
ESCAPED_PLACEHOLDER_RE = re.compile(r"&lt;([^>\n]+?)&gt;")


def _load_module(module_name: str, path: Path):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise ImportError(f"Could not load module from {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


@contextlib.contextmanager
def _temporary_sys_path(paths: list[Path]):
    originals = list(sys.path)
    for path in reversed(paths):
        sys.path.insert(0, str(path))
    try:
        yield
    finally:
        sys.path[:] = originals


def _macro_module_path(config: CrocoDocsConfig, filename: str) -> Path:
    return config.source_docs_path / "extras" / "macros" / filename


def _run_python_renderer(
    config: CrocoDocsConfig,
    *,
    script: str,
) -> str:
    repo_root = config.project_root.parent.parent
    result = subprocess.run(
        [
            "uv",
            "--directory",
            str(repo_root / "sdk/python"),
            "run",
            "python",
            "-c",
            script,
        ],
        check=True,
        capture_output=True,
        text=True,
        cwd=repo_root,
    )
    if result.returncode != 0:
        details = ["CrocoDocs Python renderer failed."]
        if result.stdout.strip():
            details.append(f"stdout:\n{result.stdout.strip()}")
        if result.stderr.strip():
            details.append(f"stderr:\n{result.stderr.strip()}")
        raise RuntimeError("\n\n".join(details))
    return result.stdout


def _find_nav_branch(items: list[Any] | None, label: str):
    if not isinstance(items, list):
        return None
    for entry in items:
        if isinstance(entry, dict) and label in entry:
            return entry[label]
    return None


def _find_nav_branch_for_path(nav_items: list[Any], nav_path: list[str]):
    items = nav_items
    for label in nav_path:
        items = _find_nav_branch(items, label)
        if items is None:
            return None
    return items


def _relative_markdown_path(path: str, base_dir: str) -> str:
    base = base_dir or "."
    return os.path.relpath(path, base).replace(os.sep, "/")


def _build_link(target: str, title: str, base_dir: str) -> str:
    return f"[`{title}`]({_relative_markdown_path(target, base_dir)})"


def _partition_section_entries(
    entries: list[Any], skip_paths: set[str]
) -> tuple[str | None, list[Any]]:
    overview_path: str | None = None
    remaining: list[Any] = []
    for item in entries:
        if isinstance(item, str):
            if overview_path is None and item not in skip_paths:
                overview_path = item
                continue
        elif isinstance(item, dict):
            used_for_overview = False
            if overview_path is None:
                for title, value in item.items():
                    if (
                        isinstance(value, str)
                        and title.casefold() == "overview"
                        and value not in skip_paths
                    ):
                        overview_path = value
                        used_for_overview = True
                        break
            if used_for_overview:
                continue
        remaining.append(item)
    return overview_path, remaining


def _build_nav_nodes(entries: list[Any] | None, skip_paths: set[str]):
    nodes: list[dict[str, Any]] = []
    for entry in entries or []:
        if isinstance(entry, str):
            continue
        if isinstance(entry, dict):
            for title, value in entry.items():
                if isinstance(value, list):
                    overview_path, remainder = _partition_section_entries(
                        value, skip_paths
                    )
                    children = _build_nav_nodes(remainder, skip_paths)
                    nodes.append(
                        {"title": title, "path": overview_path, "children": children}
                    )
                elif value not in skip_paths:
                    nodes.append({"title": title, "path": value, "children": []})
    return nodes


def _format_nav_list(
    nodes: list[dict[str, Any]], base_dir: str, depth: int = 0
) -> list[str]:
    lines: list[str] = []
    indent = " " * (depth * 4)
    for node in nodes:
        children = node.get("children") or []
        path = node.get("path")
        title = node["title"]
        label = _build_link(path, title, base_dir) if path else f"**{title}**"
        lines.append(f"{indent}- {label}")
        if children:
            lines.extend(_format_nav_list(children, base_dir, depth + 1))
    return lines


def _render_nav_overview_from_mkdocs(
    config: CrocoDocsConfig,
    nav_path: list[str],
    *,
    base_dir: str,
    skip_paths: set[str] | None = None,
) -> str:
    nav_items = _load_nav(config.mkdocs_yml)
    branch = _find_nav_branch_for_path(nav_items, nav_path)
    nodes = (
        _build_nav_nodes(branch, skip_paths or set())
        if isinstance(branch, list)
        else []
    )
    if not nodes:
        return ""
    return "\n".join(_format_nav_list(nodes, base_dir)) + "\n"


def _normalize_local_markdown_links(content: str) -> str:
    def replace(match: re.Match[str]) -> str:
        path = match.group("target")
        anchor = match.group("anchor") or ""
        if path == "index.md":
            normalized = "."
        elif path.endswith("/index.md"):
            normalized = path.removesuffix("/index.md")
        else:
            normalized = path.removesuffix(".md")
        return f"{match.group('prefix')}{normalized}{anchor}{match.group('suffix')}"

    return LOCAL_MARKDOWN_LINK_RE.sub(replace, content)


def _escape_mdx_text_outside_code(content: str) -> str:
    lines = content.splitlines()
    normalized: list[str] = []
    in_fence = False

    for line in lines:
        stripped = line.strip()
        if stripped.startswith("```"):
            in_fence = not in_fence
            normalized.append(line)
            continue

        if in_fence:
            normalized.append(line)
            continue

        parts = line.split("`")
        for index in range(0, len(parts), 2):
            parts[index] = ANGLE_TAG_RE.sub(r"&lt;\1&gt;", parts[index])
        normalized.append("`".join(parts))

    return "\n".join(normalized) + ("\n" if content.endswith("\n") else "")


def _normalize_cli_partial_markdown(content: str) -> str:
    content = CLI_H3_TICK_RE.sub(r"\1\2", content)
    content = _escape_mdx_text_outside_code(content)
    return ESCAPED_PLACEHOLDER_RE.sub(r"`<\1>`", content)


def _render_cli_partial(config: CrocoDocsConfig, command: str) -> str:
    module_path = _macro_module_path(config, "cli_to_md.py")
    script = f"""
import importlib.util
spec = importlib.util.spec_from_file_location("crocodocs_cli_to_md", {str(module_path)!r})
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
print(module.render_flet_cli_as_markdown(command={command!r}, subcommands_only=True), end="")
"""
    rendered = _run_python_renderer(config, script=script)
    return _normalize_cli_partial_markdown(rendered)


def _render_pypi_partial(config: CrocoDocsConfig) -> str:
    module_path = _macro_module_path(config, "pypi_index.py")
    script = f"""
import importlib.util
spec = importlib.util.spec_from_file_location("crocodocs_pypi_index", {str(module_path)!r})
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
print(module.render_pypi_index(base_url="https://pypi.flet.dev/", timeout_s=20.0, workers=12, output_format="md", strict=False), end="")
"""
    rendered = _run_python_renderer(config, script=script)
    lines = rendered.splitlines()
    if len(lines) < 2:
        return rendered

    filtered_lines = lines[:2]
    row_pattern = re.compile(r"^\|\s*\[`([^`]+)`\]\([^)]+\)(?:\s*\([^)]*\))?\s*\|")
    for line in lines[2:]:
        match = row_pattern.match(line)
        if not match:
            filtered_lines.append(line)
            continue
        package_name = match.group(1)
        if not package_name.startswith("flet") or package_name.startswith("flet-lib"):
            filtered_lines.append(line)
    normalized_lines: list[str] = []
    index = 0
    while index < len(filtered_lines):
        if filtered_lines[index].strip() != "!!! warning":
            normalized_lines.append(filtered_lines[index])
            index += 1
            continue

        normalized_lines.append(":::warning")
        index += 1
        while index < len(filtered_lines):
            line = filtered_lines[index]
            if line.startswith("    "):
                line = line[4:]
            elif line.strip():
                break

            if line.startswith("- ") and ": " in line:
                package_name, error_text = line[2:].split(": ", 1)
                escaped_error = error_text.replace("`", "\\`")
                line = f"- {package_name}: `{escaped_error}`"
            normalized_lines.append(line)
            index += 1
        normalized_lines.append(":::")

    return "\n".join(normalized_lines) + ("\n" if rendered.endswith("\n") else "")


def _render_permissions_partial(config: CrocoDocsConfig) -> str:
    module_path = _macro_module_path(config, "cross_platform_permissions.py")
    script = f"""
import importlib.util
spec = importlib.util.spec_from_file_location("crocodocs_cross_platform_permissions", {str(module_path)!r})
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
print(module.cross_platform_permissions_list(), end="")
"""
    return _run_python_renderer(config, script=script)


def _render_overview_partial(config: CrocoDocsConfig, filename: str) -> str:
    if filename == "controls-overview.mdx":
        return _render_nav_overview_from_mkdocs(
            config,
            ["API Reference", "Controls"],
            base_dir="controls",
            skip_paths={"controls/index.md", "services/index.md"},
        )
    if filename == "services-overview.mdx":
        return _render_nav_overview_from_mkdocs(
            config,
            ["API Reference", "Services"],
            base_dir="services",
            skip_paths={"controls/index.md", "services/index.md"},
        )
    if filename == "cookbook-overview.mdx":
        return _render_nav_overview_from_mkdocs(
            config,
            ["Cookbook"],
            base_dir="cookbook",
            skip_paths={"cookbook/index.md"},
        )
    raise ValueError(f"Unsupported overview partial filename: {filename}")


def render_partial(config: CrocoDocsConfig, filename: str) -> str:
    if filename == "pypi-index.mdx":
        return _render_pypi_partial(config)
    if filename == "cross-platform-permissions.mdx":
        return _render_permissions_partial(config)
    if filename in {
        "controls-overview.mdx",
        "services-overview.mdx",
        "cookbook-overview.mdx",
    }:
        return _render_overview_partial(config, filename)
    if filename.startswith("cli-") and filename.endswith(".mdx"):
        command = filename.removesuffix(".mdx").removeprefix("cli-").replace("-", " ")
        if command == "root":
            command = ""
        return _render_cli_partial(config, command)
    raise ValueError(f"Unsupported partial filename: {filename}")


def write_partial(config: CrocoDocsConfig, filename: str) -> Path:
    target = config.partials_output_dir / filename
    target.parent.mkdir(parents=True, exist_ok=True)
    content = _normalize_local_markdown_links(render_partial(config, filename))
    target.write_text(content, encoding="utf-8")
    return target
