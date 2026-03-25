"""Generated partial handling."""

from __future__ import annotations

import json
import os
import re
import subprocess
from pathlib import Path

from .config import CrocoDocsConfig

LOCAL_MARKDOWN_LINK_RE = re.compile(
    r"(?P<prefix>\]\()(?P<target>(?![a-z][a-z0-9+.-]*:|/|#)[^)]+?\.md)(?P<anchor>#[^)]+)?(?P<suffix>\))",
    re.IGNORECASE,
)
CLI_H3_TICK_RE = re.compile(r"^(### )`([^`]+)`$", re.MULTILINE)
ANGLE_TAG_RE = re.compile(r"<([a-z][a-z0-9_-]*)>", re.IGNORECASE)
ESCAPED_PLACEHOLDER_RE = re.compile(r"&lt;([^>\n]+?)&gt;")


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


# ---------------------------------------------------------------------------
# Flet-CLI-dependent partials (batched subprocess)
# ---------------------------------------------------------------------------

_FLET_CLI_SCRIPT_DIR = Path(__file__).parent / "scripts"


def _run_flet_cli_partials(
    config: CrocoDocsConfig, requests: dict[str, dict]
) -> dict[str, str]:
    """Run a single subprocess that generates all flet-cli-dependent partials.

    *requests* maps partial keys to their parameters.  Returns a dict
    mapping the same keys to rendered Markdown strings.
    """
    cli_script = _FLET_CLI_SCRIPT_DIR / "cli_to_md.py"
    permissions_script = _FLET_CLI_SCRIPT_DIR / "cross_platform_permissions.py"
    script = f"""
import importlib.util, json, sys

def _load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

cli_mod = _load("cli_to_md", {str(cli_script)!r})
perm_mod = _load("cross_platform_permissions", {str(permissions_script)!r})

requests = json.loads({json.dumps(requests)!r})
results = {{}}
for key, params in requests.items():
    if params.get("type") == "cli":
        results[key] = cli_mod.render_flet_cli_as_markdown(
            command=params["command"], subcommands_only=True
        )
    elif params.get("type") == "permissions":
        results[key] = perm_mod.cross_platform_permissions_list()
print(json.dumps(results))
"""
    repo_root = config.project_root.parent.parent
    env = {k: v for k, v in os.environ.items() if k != "VIRTUAL_ENV"}
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
        env=env,
    )
    stdout = result.stdout
    # Strip non-JSON lines (e.g. flet-cli "Error getting Git version" warnings)
    json_start = stdout.find("{")
    if json_start > 0:
        stdout = stdout[json_start:]
    try:
        return json.loads(stdout)
    except json.JSONDecodeError as exc:
        raise RuntimeError(
            f"JSON parse failed: {exc}\nstdout: {result.stdout[:500]}\nstderr: {result.stderr[:500]}"
        ) from exc


# ---------------------------------------------------------------------------
# PyPI index partial (in-process, no flet dependency)
# ---------------------------------------------------------------------------


def _render_pypi_partial() -> str:
    from .pypi_index import render_pypi_index

    rendered = render_pypi_index(
        base_url="https://pypi.flet.dev/",
        timeout_s=20.0,
        workers=12,
        output_format="md",
        strict=False,
    )
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


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------


def render_partials(config: CrocoDocsConfig, filenames: set[str]) -> dict[str, str]:
    """Render all requested partials, batching subprocess calls."""
    results: dict[str, str] = {}

    # Classify partials
    flet_cli_requests: dict[str, dict] = {}
    pypi_filenames: list[str] = []
    for filename in filenames:
        if filename == "pypi-index.mdx":
            pypi_filenames.append(filename)
        elif filename == "cross-platform-permissions.mdx":
            flet_cli_requests[filename] = {"type": "permissions"}
        elif filename.startswith("cli-") and filename.endswith(".mdx"):
            command = (
                filename.removesuffix(".mdx").removeprefix("cli-").replace("-", " ")
            )
            if command == "root":
                command = ""
            flet_cli_requests[filename] = {"type": "cli", "command": command}

    # Batch flet-cli subprocess
    if flet_cli_requests:
        rendered = _run_flet_cli_partials(config, flet_cli_requests)
        for filename, content in rendered.items():
            if filename.startswith("cli-"):
                results[filename] = _normalize_cli_partial_markdown(content)
            else:
                results[filename] = content

    # PyPI index (in-process)
    for filename in pypi_filenames:
        results[filename] = _render_pypi_partial()

    return results


def write_partials(config: CrocoDocsConfig, filenames: set[str]) -> int:
    """Render and write all requested partials. Returns count written."""
    rendered = render_partials(config, filenames)
    count = 0
    for filename, content in rendered.items():
        target = config.partials_output_dir / filename
        target.parent.mkdir(parents=True, exist_ok=True)
        normalized = _normalize_local_markdown_links(content)
        target.write_text(normalized, encoding="utf-8")
        count += 1
    return count
