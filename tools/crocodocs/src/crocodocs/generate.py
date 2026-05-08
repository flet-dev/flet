"""Steady-state manifest and API generation."""

from __future__ import annotations

import json
import os
import re
import subprocess
import sys
from pathlib import Path
from typing import Any

from .assets import bulk_copy_assets
from .config import CrocoDocsConfig
from .docs import (
    IMPORT_PARTIAL_RE,
    extract_symbol_blocks_from_mdx,
    iter_markdown_files,
    parse_document,
)
from .partials import write_partials
from .progress import ProgressReporter, Summary
from .sidebars import write_sidebars_js_from_source


def _normalize_anchor(name: str) -> str:
    """Convert a name to a URL-safe anchor string by stripping/replacing special characters."""
    anchor = re.sub(r"""["']""", "", str(name))
    anchor = re.sub(r"\[([^\]]+)\]", r"-\1", anchor)
    anchor = re.sub(r"[^A-Za-z0-9._-]+", "-", anchor)
    anchor = re.sub(r"-+", "-", anchor)
    return anchor.strip("-")


def _root_anchor(symbol: str) -> str:
    """Return the anchor ID for the root heading of a symbol's documentation page."""
    return _normalize_anchor(symbol)


def _member_anchor(symbol: str, member_name: str) -> str:
    """Return the anchor ID for a named member (property, event, or method) of a symbol."""
    return _normalize_anchor(f"{symbol}.{member_name}")


def _apply_public_aliases(
    entries: dict[str, Any],
    aliases: dict[str, str],
) -> dict[str, Any]:
    """Return a copy of entries augmented with public-alias copies tagged with public_qualname.

    For each (public_name -> qualname) pair in aliases, a copy of the qualname entry is
    inserted under public_name with a 'public_qualname' field added.
    """
    aliased = dict(entries)
    for public_name, qualname in aliases.items():
        entry = entries.get(qualname)
        if entry is None:
            continue
        copied = dict(entry)
        copied["public_qualname"] = public_name
        aliased[public_name] = copied
    return aliased


def _extract_api_data_with_griffe(
    config: CrocoDocsConfig,
    symbols: list[str],
) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any], dict[str, str]]:
    """Run the griffe extraction script in a subprocess and return (classes, functions, aliases, public_aliases).

    The script receives a JSON payload on stdin and writes a JSON result to stdout.
    Raises RuntimeError if the subprocess exits with a non-zero code.
    """
    script_path = config.project_root / "src" / "crocodocs" / "griffe_extract_script.py"
    search_paths = [str(path) for path in config.packages.values()]
    payload = {
        "packages": sorted({symbol.split(".", 1)[0] for symbol in symbols}),
        "search_paths": search_paths,
        "extensions": config.extensions,
        "symbols": symbols,
        "member_filters": {
            key: sorted(values) for key, values in config.member_filters.items()
        },
    }
    env = os.environ.copy()
    existing_pythonpath = env.get("PYTHONPATH")
    env["PYTHONPATH"] = os.pathsep.join(
        [*search_paths, *([existing_pythonpath] if existing_pythonpath else [])]
    )
    result = subprocess.run(
        [sys.executable, str(script_path)],
        input=json.dumps(payload),
        text=True,
        capture_output=True,
        cwd=config.project_root.parent.parent,
        env=env,
    )
    if result.returncode != 0:
        details = ["CrocoDocs Griffe extraction failed."]
        if result.stdout.strip():
            details.append(f"stdout:\n{result.stdout.strip()}")
        if result.stderr.strip():
            details.append(f"stderr:\n{result.stderr.strip()}")
        raise RuntimeError("\n\n".join(details))
    data = json.loads(result.stdout)
    return (
        data["classes"],
        data["functions"],
        data.get("aliases", {}),
        data.get("public_aliases", {}),
    )


def _should_skip_example_path(root: Path, path: Path) -> bool:
    """Return True if path is inside a hidden directory or a build/dist/cache directory."""
    relative_parts = path.relative_to(root).parts
    return any(
        part.startswith(".") or part in {"__pycache__", "build", "dist"}
        for part in relative_parts
    )


def _generate_code_examples(examples_root: Path, output_path: Path) -> int:
    """Write a JSON file mapping relative example paths to their source text.

    Skips hidden directories and build/dist artifacts. Returns the count of entries written.
    """
    mapping: dict[str, str] = {}
    if not examples_root.exists():
        output_path.write_text("{}", encoding="utf-8")
        return 0

    for source_path in sorted(examples_root.rglob("*.py")):
        if _should_skip_example_path(examples_root, source_path):
            continue
        relative = source_path.relative_to(examples_root).as_posix()
        content = source_path.read_text(encoding="utf-8")
        mapping[relative] = content

    output_path.write_text(
        json.dumps(mapping, indent=2, sort_keys=True), encoding="utf-8"
    )
    return len(mapping)


def run_generate(
    config: CrocoDocsConfig,
    docs_path: Path,
    manifest_output: Path,
    api_output: Path,
    base_url: str,
) -> None:
    """Orchestrate the full generate pipeline.

    Steps in order:
    1. Write the Docusaurus sidebars.js from the YAML source.
    2. Scan docs to build the page manifest (symbol blocks + partials).
    3. Write the manifest JSON file.
    4. Generate MDX partial files for CLI docs, permissions, and PyPI index.
    5. Write the code-examples JSON file.
    6. Extract API data (classes, functions, aliases) via Griffe.
    7. Write the api-data JSON file with xref map.
    8. Sync asset files to the static directory.
    """
    reporter = ProgressReporter("generate")
    summary = Summary("generate")

    reporter.stage("Generating sidebar runtime config")
    write_sidebars_js_from_source(config.sidebars_source, config.sidebars_output)

    reporter.stage("Scanning docs for API symbols and partials")
    docs = iter_markdown_files(docs_path)
    pages: list[dict[str, Any]] = []
    partial_filenames: set[str] = set()
    for path in docs:
        content = path.read_text(encoding="utf-8")
        document = parse_document(content)
        blocks = [
            {"kind": b.kind, "symbol": b.symbol, "options": b.options}
            for b in extract_symbol_blocks_from_mdx(document.body, document.data)
        ]
        if blocks:
            relative = path.relative_to(docs_path).as_posix()
            doc_id = relative.removesuffix(".md").removesuffix(".mdx")
            route_path = (
                doc_id.removesuffix("/index") if doc_id.endswith("/index") else doc_id
            )
            pages.append({"route": f"{base_url}/{route_path}", "symbol_blocks": blocks})
        partial_filenames.update(IMPORT_PARTIAL_RE.findall(content))

    reporter.stage("Writing manifest")
    manifest_output.parent.mkdir(parents=True, exist_ok=True)
    manifest_output.write_text(
        json.dumps({"version": "1.0", "pages": pages}, indent=2, sort_keys=True),
        encoding="utf-8",
    )

    reporter.stage("Generating MDX partials")
    try:
        generated_partials = write_partials(config, partial_filenames)
    except Exception as exc:  # noqa: BLE001
        generated_partials = 0
        summary.warn(f"Could not generate partials: {exc}")

    reporter.stage("Generating code example data")
    code_examples_output = config.partials_output_dir / "code-examples.json"
    code_example_entries = _generate_code_examples(
        config.examples_root, code_examples_output
    )

    reporter.stage("Extracting API data")
    missing_roots = [path for path in config.packages.values() if not path.exists()]
    for package_root in missing_roots:
        summary.warn(f"Configured package root does not exist: {package_root}")
    requested_symbols = sorted(
        {
            block["symbol"]
            for page in pages
            for block in page["symbol_blocks"]
            if isinstance(block.get("symbol"), str) and block["symbol"]
        }
    )
    classes, functions, aliases, public_aliases = _extract_api_data_with_griffe(
        config, requested_symbols
    )

    class_aliases = {
        public_name: qualname
        for public_name, qualname in public_aliases.items()
        if qualname in classes
    }
    function_aliases = {
        public_name: qualname
        for public_name, qualname in public_aliases.items()
        if qualname in functions
    }

    classes = _apply_public_aliases(classes, class_aliases)
    functions = _apply_public_aliases(functions, function_aliases)

    # Build reverse map: internal qualname -> public name
    reverse_aliases: dict[str, str] = {
        qualname: public_name for public_name, qualname in public_aliases.items()
    }

    # Normalize bases in all class entries to use public names
    for cls_entry in classes.values():
        bases = cls_entry.get("bases")
        if not bases:
            continue
        cls_entry["bases"] = [reverse_aliases.get(b, b) for b in bases]

    xref_map: dict[str, str] = {}
    for page in pages:
        route = page["route"]
        for block in page["symbol_blocks"]:
            symbol = block.get("symbol")
            if isinstance(symbol, str) and symbol:
                use_root_anchor = block.get("options", {}).get("showRootHeading")
                xref_map[symbol] = (
                    f"{route}#{_root_anchor(symbol)}" if use_root_anchor else route
                )
                api_entry = classes.get(symbol)
                if api_entry:
                    for prop in api_entry.get("properties", []):
                        xref_map[f"{symbol}.{prop['name']}"] = (
                            f"{route}#{_member_anchor(symbol, prop['name'])}"
                        )
                    for event in api_entry.get("events", []):
                        xref_map[f"{symbol}.{event['name']}"] = (
                            f"{route}#{_member_anchor(symbol, event['name'])}"
                        )
                    for method in api_entry.get("methods", []):
                        xref_map[f"{symbol}.{method['name']}"] = (
                            f"{route}#{_member_anchor(symbol, method['name'])}"
                        )

    # Add public-alias xref entries so short names like flet_ads.BaseAd resolve
    for public_name, qualname in class_aliases.items():
        if qualname in xref_map and public_name not in xref_map:
            xref_map[public_name] = xref_map[qualname]
            # Also alias members: flet_ads.BaseAd.on_open -> flet_ads.base_ad.BaseAd.on_open
            prefix = f"{qualname}."
            public_prefix = f"{public_name}."
            for key, url in list(xref_map.items()):
                if key.startswith(prefix):
                    member_alias = public_prefix + key[len(prefix) :]
                    if member_alias not in xref_map:
                        xref_map[member_alias] = url

    reporter.stage("Writing API data")
    api_output.parent.mkdir(parents=True, exist_ok=True)
    api_output.write_text(
        json.dumps(
            {
                "version": "1.0",
                "canonical_map": reverse_aliases,
                "classes": classes,
                "functions": functions,
                "aliases": aliases,
                "enums": {},
                "xref_map": xref_map,
            },
            indent=2,
            sort_keys=True,
        ),
        encoding="utf-8",
    )

    reporter.stage("Syncing assets")
    static_root = docs_path.parent / "static"
    synced_assets = 0
    for mapping in config.asset_mappings.values():
        if not mapping.source_path.exists():
            continue
        dest = static_root / mapping.static_subpath
        synced_assets += bulk_copy_assets(
            mapping.source_path, dest, mapping.include_exts
        )

    summary.add("docs scanned", len(docs))
    summary.add("packages loaded", len(config.packages))
    summary.add("symbols serialized", len(classes) + len(functions) + len(aliases))
    summary.add("partials generated", generated_partials)
    summary.add("code example entries", code_example_entries)
    try:
        sidebar_source = config.sidebars_source.relative_to(
            config.project_root
        ).as_posix()
    except ValueError:
        sidebar_source = config.sidebars_source.as_posix()
    try:
        sidebar_output = config.sidebars_output.relative_to(
            config.project_root
        ).as_posix()
    except ValueError:
        sidebar_output = config.sidebars_output.as_posix()
    summary.add("sidebar source", sidebar_source)
    summary.add("sidebar output", sidebar_output)
    summary.add("assets copied", synced_assets)
    summary.add("xref entries", len(xref_map))
    summary.print()
