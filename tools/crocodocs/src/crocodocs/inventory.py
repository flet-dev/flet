"""Inventory command implementation."""

from __future__ import annotations

import json
from collections import Counter
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .docs import (
    ADMONITION_RE,
    CODE_ANNOTATION_RE,
    DETAILS_RE,
    TAB_RE,
    collect_macro_calls,
    extract_reference_targets,
    iter_markdown_files,
    parse_document,
)
from .progress import ProgressReporter, Summary


@dataclass
class InventoryResult:
    docs_scanned: int
    front_matter_keys: dict[str, int]
    macros: dict[str, int]
    reference_targets: dict[str, int]
    special_patterns: dict[str, int]
    flagged_pages: list[str]


def run_inventory(input_root: Path, output_path: Path) -> InventoryResult:
    reporter = ProgressReporter("inventory")
    summary = Summary("inventory")
    reporter.stage("Scanning markdown files")
    docs = iter_markdown_files(input_root)

    front_matter_keys: Counter[str] = Counter()
    macros: Counter[str] = Counter()
    reference_targets: Counter[str] = Counter()
    special_patterns: Counter[str] = Counter()
    flagged_pages: list[str] = []

    for index, path in enumerate(docs, start=1):
        if index == 1 or index % 100 == 0 or index == len(docs):
            reporter.info(f"Processed {index}/{len(docs)} files")
        relative = path.relative_to(input_root).as_posix()
        document = parse_document(path.read_text(encoding="utf-8"))
        front_matter_keys.update(document.data.keys())
        macro_calls = collect_macro_calls(document.body)
        macros.update(call.name for call in macro_calls)
        reference_targets.update(extract_reference_targets(document.body))

        if ADMONITION_RE.search(document.body):
            special_patterns["admonition"] += 1
        if TAB_RE.search(document.body):
            special_patterns["tab"] += 1
        if DETAILS_RE.search(document.body):
            special_patterns["details"] += 1
        if CODE_ANNOTATION_RE.search(document.body):
            special_patterns["code_annotation"] += 1
            flagged_pages.append(relative)

        for call in macro_calls:
            if call.name not in {
                "class_summary",
                "class_members",
                "class_all_options",
                "image",
                "flet_cli_as_markdown",
                "flet_pypi_index",
                "cross_platform_permissions",
                "controls_overview",
                "services_overview",
                "cookbook_overview",
            }:
                flagged_pages.append(relative)
                break

    output_path.parent.mkdir(parents=True, exist_ok=True)
    payload: dict[str, Any] = {
        "docs_scanned": len(docs),
        "front_matter_keys": dict(front_matter_keys.most_common()),
        "macros": dict(macros.most_common()),
        "reference_targets": dict(reference_targets.most_common(100)),
        "special_patterns": dict(special_patterns.most_common()),
        "flagged_pages": sorted(dict.fromkeys(flagged_pages)),
    }
    reporter.stage("Writing inventory report")
    output_path.write_text(
        json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8"
    )

    summary.add("docs scanned", len(docs))
    summary.add("macro kinds found", len(macros))
    summary.add("front matter keys found", len(front_matter_keys))
    summary.add("pages flagged for manual review", len(payload["flagged_pages"]))
    summary.print()

    return InventoryResult(
        docs_scanned=len(docs),
        front_matter_keys=dict(front_matter_keys),
        macros=dict(macros),
        reference_targets=dict(reference_targets),
        special_patterns=dict(special_patterns),
        flagged_pages=payload["flagged_pages"],
    )
