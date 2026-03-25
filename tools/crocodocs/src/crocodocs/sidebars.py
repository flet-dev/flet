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
    return ref.removesuffix(".md").removesuffix(".mdx")


def _load_yaml(text_path: Path) -> Any:
    if yaml is None:  # pragma: no cover
        raise RuntimeError(
            "PyYAML is required to parse sidebar YAML. Install CrocoDocs dependencies first."
        )
    return yaml.safe_load(text_path.read_text(encoding="utf-8"))


def _load_nav(mkdocs_yml: Path) -> list[Any]:
    text = mkdocs_yml.read_text(encoding="utf-8")
    marker = "\nnav:\n"
    if marker in text:
        text = text[text.index(marker) + 1 :]
    elif text.startswith("nav:\n"):
        text = text
    else:
        raise ValueError(f"Could not find 'nav:' section in {mkdocs_yml}")
    data = yaml.safe_load(text) or {}
    nav = data.get("nav")
    if not isinstance(nav, list):
        raise ValueError(f"Expected 'nav' list in {mkdocs_yml}")
    return nav


def _load_sidebar_source(sidebars_yml: Path) -> Any:
    data = _load_yaml(sidebars_yml) or {}
    docs = data.get("docs")
    if docs is None:
        raise ValueError(f"Expected top-level 'docs' key in {sidebars_yml}")
    return docs


def _normalize_label(value: str) -> str:
    return value.strip().lower()


def _collect_nav_titles(entries: list[Any], out: dict[str, str]) -> None:
    for entry in entries:
        if isinstance(entry, str):
            continue
        if not isinstance(entry, dict) or len(entry) != 1:
            continue
        label, value = next(iter(entry.items()))
        if isinstance(value, str):
            out[value] = label
            continue
        if isinstance(value, list):
            _collect_nav_titles(value, out)


def build_nav_title_map(mkdocs_yml: Path) -> dict[str, str]:
    titles: dict[str, str] = {}
    _collect_nav_titles(_load_nav(mkdocs_yml), titles)
    return titles


def _doc_item(label: str, ref: str) -> dict[str, Any]:
    item: dict[str, Any] = {"type": "doc", "id": _doc_id(ref)}
    if label:
        item["label"] = label
    return item


def _convert_source_entry(entry: Any) -> dict[str, Any]:
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


def build_sidebar_items_from_source(
    sidebars_yml: Path,
) -> list[dict[str, Any]]:
    docs = _load_sidebar_source(sidebars_yml)

    if isinstance(docs, dict):
        entries = [{label: value} for label, value in docs.items()]
    elif isinstance(docs, list):
        entries = docs
    else:
        raise ValueError(f"Unsupported 'docs' sidebar source in {sidebars_yml}")

    return [_convert_source_entry(entry) for entry in entries]


def render_sidebars_js(sidebar_items: list[dict[str, Any]]) -> str:
    payload = json.dumps({"docs": sidebar_items}, indent=2)
    return (
        "// Generated by CrocoDocs from website/sidebars.yml.\n"
        "// Do not edit by hand.\n\n"
        f"module.exports = {payload};\n"
    )


def write_sidebars_js_from_source(
    sidebars_yml: Path,
    output_path: Path,
) -> None:
    sidebar_items = build_sidebar_items_from_source(sidebars_yml)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(render_sidebars_js(sidebar_items), encoding="utf-8")
