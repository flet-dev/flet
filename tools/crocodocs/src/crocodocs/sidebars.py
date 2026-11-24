"""Sidebar source and Docusaurus sidebar generation."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

try:
    import yaml
except ModuleNotFoundError:  # pragma: no cover
    yaml = None

SPECIAL_KEYS = {"_index", "_generated_index", "_meta"}


def _doc_id(ref: str) -> str:
    """Strip .md and .mdx suffixes from a doc reference to produce a Docusaurus doc ID."""
    return ref.removesuffix(".md").removesuffix(".mdx")


def _load_yaml(text_path: Path) -> Any:
    """Read and parse a YAML file. Raises RuntimeError if PyYAML is not installed."""
    if yaml is None:  # pragma: no cover
        raise RuntimeError(
            "PyYAML is required to parse sidebar YAML. Install CrocoDocs dependencies first."
        )
    return yaml.safe_load(text_path.read_text(encoding="utf-8"))


def _load_sidebar_source(sidebars_yml: Path) -> dict[str, Any]:
    """Load the sidebar YAML and return the top-level mapping of sidebar name to source."""
    data = _load_yaml(sidebars_yml) or {}
    if not isinstance(data, dict) or not data:
        raise ValueError(
            f"Expected at least one top-level sidebar key in {sidebars_yml}"
        )
    return data


def _doc_item(label: str, ref: str) -> dict[str, Any]:
    """Build a Docusaurus doc-type sidebar item with an optional label."""
    item: dict[str, Any] = {"type": "doc", "id": _doc_id(ref)}
    if label:
        item["label"] = label
    return item


def _convert_source_entry(entry: Any) -> dict[str, Any]:
    """Convert a sidebar source entry (bare string or {label: value} dict) to a Docusaurus item dict."""
    if isinstance(entry, str):
        return _doc_item("", entry)

    if not isinstance(entry, dict) or len(entry) != 1:
        raise ValueError(f"Unsupported sidebar source entry: {entry!r}")

    label, value = next(iter(entry.items()))
    return _convert_labeled_source_entry(str(label), value)


def _convert_category_mapping(
    label: str,
    mapping: dict[str, Any],
) -> dict[str, Any]:
    """Convert a dict-form sidebar category to a Docusaurus category item.

    Handles optional _meta (for collapsed state), _index (category link doc), and
    _generated_index (generated-index link) special keys.
    """
    collapsed = True
    meta = mapping.get("_meta")
    if isinstance(meta, dict) and "collapsed" in meta:
        collapsed = bool(meta["collapsed"])

    items: list[dict[str, Any]] = []
    for child_label, child_value in mapping.items():
        if child_label in SPECIAL_KEYS:
            continue
        items.append(_convert_labeled_source_entry(str(child_label), child_value))

    category: dict[str, Any] = {
        "type": "category",
        "label": label,
        "collapsed": collapsed,
        "items": items,
    }
    generated_index = mapping.get("_generated_index")
    if isinstance(generated_index, dict):
        link: dict[str, Any] = {"type": "generated-index"}
        if "title" in generated_index:
            link["title"] = generated_index["title"]
        if "slug" in generated_index:
            link["slug"] = generated_index["slug"]
        if "description" in generated_index:
            link["description"] = generated_index["description"]
        category["link"] = link
    else:
        index_ref = mapping.get("_index")
        if isinstance(index_ref, str):
            category["link"] = _doc_item("", index_ref)
    return category


def _convert_labeled_source_entry(
    label: str,
    value: Any,
) -> dict[str, Any]:
    """Convert a labeled sidebar entry (str, list, or dict) to a Docusaurus item dict."""
    if isinstance(value, str):
        return _doc_item(label, value)
    if isinstance(value, list):
        return {
            "type": "category",
            "label": label,
            "collapsed": True,
            "items": [_convert_source_entry(child) for child in value],
        }
    if isinstance(value, dict):
        return _convert_category_mapping(label, value)
    raise ValueError(f"Unsupported sidebar source group for {label!r}: {value!r}")


def _build_sidebar_items(
    name: str, source: Any, sidebars_yml: Path
) -> list[dict[str, Any]]:
    """Convert one top-level sidebar source (dict or list) to a list of Docusaurus items."""
    if isinstance(source, dict):
        entries: list[Any] = [{label: value} for label, value in source.items()]
    elif isinstance(source, list):
        entries = source
    else:
        raise ValueError(f"Unsupported sidebar source for {name!r} in {sidebars_yml}")
    return [_convert_source_entry(entry) for entry in entries]


def build_sidebars_from_source(
    sidebars_yml: Path,
) -> dict[str, list[dict[str, Any]]]:
    """Read the sidebar YAML and return a dict mapping each sidebar name to its items."""
    sources = _load_sidebar_source(sidebars_yml)
    return {
        name: _build_sidebar_items(name, source, sidebars_yml)
        for name, source in sources.items()
    }


def render_sidebars_js(sidebars: dict[str, list[dict[str, Any]]]) -> str:
    """Wrap named sidebars in a CommonJS module.exports string for Docusaurus."""
    payload = json.dumps(sidebars, indent=2)
    return (
        "// Generated by CrocoDocs from website/sidebars.yml.\n"
        "// Do not edit by hand.\n\n"
        f"module.exports = {payload};\n"
    )


def write_sidebars_js_from_source(
    sidebars_yml: Path,
    output_path: Path,
) -> None:
    """Read the sidebar YAML and write the generated sidebars.js to output_path."""
    sidebars = build_sidebars_from_source(sidebars_yml)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(render_sidebars_js(sidebars), encoding="utf-8")
