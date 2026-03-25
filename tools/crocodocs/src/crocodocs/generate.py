"""Steady-state manifest and API generation."""

from __future__ import annotations

import ast
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
    default_title,
    extract_symbol_blocks_from_mdx,
    iter_markdown_files,
    parse_document,
    route_for_output,
)
from .partials import write_partial
from .progress import ProgressReporter, Summary
from .sidebars import write_sidebars_js_from_source


def _normalize_anchor(name: str) -> str:
    anchor = re.sub(r"""["']""", "", str(name))
    anchor = re.sub(r"\[([^\]]+)\]", r"-\1", anchor)
    anchor = re.sub(r"[^A-Za-z0-9._-]+", "-", anchor)
    anchor = re.sub(r"-+", "-", anchor)
    return anchor.strip("-")


def _root_anchor(symbol: str) -> str:
    return _normalize_anchor(symbol)


def _section_anchor(symbol: str, section_name: str) -> str:
    return _normalize_anchor(f"{symbol}-{section_name.lower()}")


def _member_anchor(symbol: str, member_name: str) -> str:
    return _normalize_anchor(f"{symbol}-{member_name}")


def _collect_public_aliases(package_name: str, root: Path) -> dict[str, str]:
    aliases: dict[str, str] = {}
    init_path = root / package_name / "__init__.py"
    if not init_path.exists():
        return aliases

    tree = ast.parse(init_path.read_text(encoding="utf-8"))
    for node in tree.body:
        if not isinstance(node, ast.ImportFrom):
            continue
        if node.module is None:
            continue
        if any(alias.name == "*" for alias in node.names):
            continue

        if node.level > 0:
            base_parts = package_name.split(".")
            if node.level > 1:
                base_parts = base_parts[: -(node.level - 1)]
            module_parts = base_parts + node.module.split(".")
        else:
            module_parts = node.module.split(".")
        module_name = ".".join(part for part in module_parts if part)

        for imported in node.names:
            public_name = imported.asname or imported.name
            aliases[f"{package_name}.{public_name}"] = f"{module_name}.{imported.name}"

    return aliases


def _apply_public_aliases(
    entries: dict[str, Any],
    aliases: dict[str, str],
) -> dict[str, Any]:
    aliased = dict(entries)
    for public_name, qualname in aliases.items():
        entry = entries.get(qualname)
        if entry is None:
            continue
        copied = dict(entry)
        copied["public_qualname"] = public_name
        aliased[public_name] = copied
    return aliased


def _signature_from_function(node: ast.FunctionDef | ast.AsyncFunctionDef) -> str:
    parts: list[str] = []
    for arg in node.args.posonlyargs + node.args.args:
        parts.append(arg.arg)
    if node.args.vararg:
        parts.append("*" + node.args.vararg.arg)
    for arg in node.args.kwonlyargs:
        parts.append(arg.arg)
    if node.args.kwarg:
        parts.append("**" + node.args.kwarg.arg)
    return f"{node.name}(" + ", ".join(parts) + ")"


def _extract_module_objects(
    module_name: str, path: Path
) -> tuple[dict[str, Any], dict[str, Any]]:
    tree = ast.parse(path.read_text(encoding="utf-8"))
    classes: dict[str, Any] = {}
    functions: dict[str, Any] = {}
    for node in tree.body:
        if isinstance(node, ast.ClassDef) and not node.name.startswith("_"):
            qualname = f"{module_name}.{node.name}"
            methods = []
            properties = []
            events = []
            for child in node.body:
                if isinstance(
                    child, (ast.FunctionDef, ast.AsyncFunctionDef)
                ) and not child.name.startswith("_"):
                    methods.append(
                        {
                            "name": child.name,
                            "signature": _signature_from_function(child),
                            "docstring": ast.get_docstring(child),
                            "parameters": [arg.arg for arg in child.args.args],
                            "return_type": None,
                            "deprecation": None,
                        }
                    )
                elif isinstance(child, ast.AnnAssign) and isinstance(
                    child.target, ast.Name
                ):
                    entry = {
                        "name": child.target.id,
                        "type": ast.unparse(child.annotation)
                        if child.annotation
                        else None,
                        "default": ast.unparse(child.value)
                        if child.value is not None
                        else None,
                        "docstring": None,
                        "deprecation": None,
                        "inherited_from": None,
                    }
                    if child.target.id.startswith("on_"):
                        events.append(entry)
                    elif not child.target.id.startswith("_"):
                        properties.append(entry)
            classes[qualname] = {
                "name": node.name,
                "qualname": qualname,
                "docstring": ast.get_docstring(node),
                "bases": [ast.unparse(base) for base in node.bases],
                "deprecation": None,
                "properties": properties,
                "events": events,
                "methods": methods,
            }
        elif isinstance(
            node, (ast.FunctionDef, ast.AsyncFunctionDef)
        ) and not node.name.startswith("_"):
            qualname = f"{module_name}.{node.name}"
            functions[qualname] = {
                "name": node.name,
                "qualname": qualname,
                "signature": _signature_from_function(node),
                "docstring": ast.get_docstring(node),
                "parameters": [arg.arg for arg in node.args.args],
                "return_type": None,
                "deprecation": None,
            }
    return classes, functions


def _extract_api_data(
    package_name: str, root: Path
) -> tuple[dict[str, Any], dict[str, Any]]:
    classes: dict[str, Any] = {}
    functions: dict[str, Any] = {}
    package_dir = root / package_name
    if not package_dir.exists():
        return classes, functions
    for path in sorted(package_dir.rglob("*.py")):
        if "__pycache__" in path.parts:
            continue
        rel = path.relative_to(root).with_suffix("")
        module_name = ".".join(rel.parts)
        module_classes, module_functions = _extract_module_objects(module_name, path)
        classes.update(module_classes)
        functions.update(module_functions)
    return classes, functions


def _extract_api_data_with_griffe(
    config: CrocoDocsConfig,
    symbols: list[str],
) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any], dict[str, str]]:
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
    relative_parts = path.relative_to(root).parts
    return any(
        part.startswith(".") or part in {"__pycache__", "build", "dist"}
        for part in relative_parts
    )


def _generate_code_examples(examples_root: Path, output_path: Path) -> int:
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
        mapping[f"../../examples/{relative}"] = content
        mapping[f"../../../examples/{relative}"] = content

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
    reporter = ProgressReporter("generate")
    summary = Summary("generate")

    reporter.stage("Scanning Docusaurus docs")
    docs = iter_markdown_files(docs_path)
    pages: list[dict[str, Any]] = []
    partial_filenames: set[str] = set()
    for index, path in enumerate(docs, start=1):
        if index == 1 or index % 100 == 0 or index == len(docs):
            reporter.info(f"Processed {index}/{len(docs)} files")
        document = parse_document(path.read_text(encoding="utf-8"))
        route = route_for_output(base_url, docs_path, path)
        pages.append(
            {
                "source_path": path.relative_to(docs_path).as_posix(),
                "output_path": path.relative_to(docs_path).as_posix(),
                "route": route,
                "title": default_title(document.data, document.body, path.stem),
                "front_matter": document.data,
                "symbol_blocks": [
                    {
                        "kind": block.kind,
                        "symbol": block.symbol,
                        "options": block.options,
                    }
                    for block in extract_symbol_blocks_from_mdx(
                        document.body, document.data
                    )
                ],
            }
        )
        partial_filenames.update(IMPORT_PARTIAL_RE.findall(document.body))

    reporter.stage("Writing manifest")
    manifest_output.parent.mkdir(parents=True, exist_ok=True)
    manifest_output.write_text(
        json.dumps({"version": "1.0", "pages": pages}, indent=2, sort_keys=True),
        encoding="utf-8",
    )

    reporter.stage("Generating sidebar runtime config")
    write_sidebars_js_from_source(config.sidebars_source, pages, config.sidebars_output)

    reporter.stage("Generating MDX partials")
    generated_partials = 0
    sorted_partials = sorted(partial_filenames)
    if not sorted_partials:
        reporter.info("No MDX partials referenced by docs")
    for index, filename in enumerate(sorted_partials, start=1):
        reporter.info(f"[{index}/{len(sorted_partials)}] {filename}")
        try:
            write_partial(config, filename)
            generated_partials += 1
        except Exception as exc:  # noqa: BLE001
            summary.warn(f"Could not generate partial {filename}: {exc}")

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
