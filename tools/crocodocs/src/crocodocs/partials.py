"""Generated partial handling."""

from __future__ import annotations

import contextlib
import importlib.util
import re
import subprocess
import sys
from pathlib import Path

from .config import CrocoDocsConfig

LOCAL_MARKDOWN_LINK_RE = re.compile(
    r"(?P<prefix>\]\()(?P<target>(?![a-z][a-z0-9+.-]*:|/|#)[^)]+?\.md)(?P<anchor>#[^)]+)?(?P<suffix>\))",
    re.IGNORECASE,
)


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
    return result.stdout


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
    return re.sub(r"<([a-z][a-z0-9_-]*)>", r"&lt;\1&gt;", rendered, flags=re.IGNORECASE)


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
    module_path = _macro_module_path(config, "controls_overview.py")
    if filename == "controls-overview.mdx":
        function_name = 'module.render_sub_nav_overview("Controls")'
    elif filename == "services-overview.mdx":
        function_name = 'module.render_sub_nav_overview("Services")'
    elif filename == "cookbook-overview.mdx":
        function_name = (
            'module.render_nav_overview(["Cookbook"], base_dir="cookbook", '
            'skip_paths={"cookbook/index.md"})'
        )
    else:
        raise ValueError(f"Unsupported overview partial filename: {filename}")

    script = f"""
import importlib.util
spec = importlib.util.spec_from_file_location("crocodocs_controls_overview", {str(module_path)!r})
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
print({function_name}, end="")
"""
    return _run_python_renderer(config, script=script)


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
