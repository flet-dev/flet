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


def _doc_id_for_output_path(output_path: str) -> str:
    return output_path.removesuffix(".md").removesuffix(".mdx")


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


def _page_indexes(
    pages: list[dict[str, Any]],
) -> tuple[dict[str, dict[str, Any]], dict[str, dict[str, Any]]]:
    return (
        {page["source_path"]: page for page in pages},
        {page["output_path"]: page for page in pages},
    )


def _resolve_page(
    ref: str,
    page_by_output: dict[str, dict[str, Any]],
    page_by_source: dict[str, dict[str, Any]],
) -> dict[str, Any]:
    page = page_by_output.get(ref) or page_by_source.get(ref)
    if page is None:
        raise KeyError(f"Navigation path not found in manifest: {ref}")
    return page


def _page_output_path(
    ref: str,
    page_by_output: dict[str, dict[str, Any]],
    page_by_source: dict[str, dict[str, Any]],
) -> str:
    return _resolve_page(ref, page_by_output, page_by_source)["output_path"]


def _page_title(
    ref: str,
    page_by_output: dict[str, dict[str, Any]],
    page_by_source: dict[str, dict[str, Any]],
) -> str:
    return str(_resolve_page(ref, page_by_output, page_by_source).get("title") or "")


def _doc_item(
    label: str,
    ref: str,
    page_by_output: dict[str, dict[str, Any]],
    page_by_source: dict[str, dict[str, Any]],
) -> dict[str, Any]:
    page = _resolve_page(ref, page_by_output, page_by_source)
    item: dict[str, Any] = {
        "type": "doc",
        "id": _doc_id_for_output_path(page["output_path"]),
    }
    if label and label != page.get("title"):
        item["label"] = label
    return item


def _should_use_category_link(
    category_label: str,
    first_item: dict[str, Any],
    first_source_path: str | None,
) -> bool:
    if first_item.get("type") != "doc":
        return False
    item_label = _normalize_label(first_item.get("label") or "")
    category_name = _normalize_label(category_label)
    if item_label in {"overview", category_name}:
        return True
    return bool(first_source_path and first_source_path.endswith("/index.md"))


def _compact_doc_entry(
    label: str,
    ref: str,
    page_by_output: dict[str, dict[str, Any]],
    page_by_source: dict[str, dict[str, Any]],
) -> str | dict[str, Any]:
    output_path = _page_output_path(ref, page_by_output, page_by_source)
    title = _page_title(ref, page_by_output, page_by_source)
    if not label or label == title:
        return output_path
    return {label: output_path}


def _category_body_from_children(
    children: list[Any],
    index_ref: str | None,
    page_by_output: dict[str, dict[str, Any]],
    page_by_source: dict[str, dict[str, Any]],
) -> list[Any] | dict[str, Any]:
    if index_ref is None:
        return children

    body: dict[str, Any] = {
        "_index": _page_output_path(index_ref, page_by_output, page_by_source)
    }
    for child in children:
        if isinstance(child, str):
            body[_page_title(child, page_by_output, page_by_source)] = child
            continue
        if isinstance(child, dict) and len(child) == 1:
            body.update(child)
            continue
        raise ValueError(f"Unsupported compact sidebar child: {child!r}")
    return body


def _convert_nav_entry_to_source(
    entry: Any,
    page_by_output: dict[str, dict[str, Any]],
    page_by_source: dict[str, dict[str, Any]],
) -> tuple[str | dict[str, Any], str | None]:
    if isinstance(entry, str):
        return (
            _compact_doc_entry("", entry, page_by_output, page_by_source),
            entry,
        )

    if not isinstance(entry, dict) or len(entry) != 1:
        raise ValueError(f"Unsupported nav entry: {entry!r}")

    label, value = next(iter(entry.items()))
    if isinstance(value, str):
        return (
            _compact_doc_entry(label, value, page_by_output, page_by_source),
            value,
        )

    if not isinstance(value, list):
        raise ValueError(f"Unsupported nav group for {label!r}: {value!r}")

    converted_children: list[str | dict[str, Any]] = []
    child_sources: list[str | None] = []
    for child in value:
        converted, source_path = _convert_nav_entry_to_source(
            child, page_by_output, page_by_source
        )
        converted_children.append(converted)
        child_sources.append(source_path)

    first_item: dict[str, Any] = {}
    if child_sources and child_sources[0]:
        first_item = _doc_item(
            "",
            child_sources[0],
            page_by_output,
            page_by_source,
        )
    use_index = bool(
        converted_children
        and _should_use_category_link(label, first_item, child_sources[0])
    )
    index_ref = child_sources[0] if use_index else None
    children = converted_children[1:] if use_index else converted_children
    return (
        {
            label: _category_body_from_children(
                children, index_ref, page_by_output, page_by_source
            )
        },
        None,
    )


def build_sidebar_source(
    mkdocs_yml: Path,
    pages: list[dict[str, Any]],
) -> dict[str, Any]:
    page_by_source, page_by_output = _page_indexes(pages)
    docs: dict[str, Any] = {}
    for entry in _load_nav(mkdocs_yml):
        converted, _ = _convert_nav_entry_to_source(
            entry, page_by_output, page_by_source
        )
        if isinstance(converted, dict) and len(converted) == 1:
            docs.update(converted)
            continue
        raise ValueError(f"Top-level sidebar entries must be labeled groups: {entry!r}")
    return {"docs": docs}


def render_sidebars_yml(sidebar_source: dict[str, Any]) -> str:
    if yaml is None:  # pragma: no cover
        raise RuntimeError(
            "PyYAML is required to render sidebars.yml. Install CrocoDocs dependencies first."
        )
    payload = yaml.safe_dump(
        sidebar_source,
        sort_keys=False,
        default_flow_style=False,
        allow_unicode=True,
    )
    return (
        "# Generated by CrocoDocs bootstrap migration from mkdocs.yml.\n"
        "# This is the CrocoDocs sidebar source consumed by `crocodocs generate`.\n\n"
        + payload
    )


def write_sidebars_yml(
    mkdocs_yml: Path,
    pages: list[dict[str, Any]],
    output_path: Path,
) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        render_sidebars_yml(build_sidebar_source(mkdocs_yml, pages)),
        encoding="utf-8",
    )


def _convert_source_entry(
    entry: Any,
    page_by_output: dict[str, dict[str, Any]],
    page_by_source: dict[str, dict[str, Any]],
) -> dict[str, Any]:
    if isinstance(entry, str):
        return _doc_item("", entry, page_by_output, page_by_source)

    if not isinstance(entry, dict) or len(entry) != 1:
        raise ValueError(f"Unsupported sidebar source entry: {entry!r}")

    label, value = next(iter(entry.items()))
    return _convert_labeled_source_entry(
        str(label), value, page_by_output, page_by_source
    )


def _convert_category_mapping(
    label: str,
    mapping: dict[str, Any],
    page_by_output: dict[str, dict[str, Any]],
    page_by_source: dict[str, dict[str, Any]],
) -> dict[str, Any]:
    collapsed = True
    meta = mapping.get("_meta")
    if isinstance(meta, dict) and "collapsed" in meta:
        collapsed = bool(meta["collapsed"])

    items: list[dict[str, Any]] = []
    for child_label, child_value in mapping.items():
        if child_label in SPECIAL_KEYS:
            continue
        items.append(
            _convert_labeled_source_entry(
                str(child_label), child_value, page_by_output, page_by_source
            )
        )

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
            category["link"] = _doc_item("", index_ref, page_by_output, page_by_source)
    return category


def _convert_labeled_source_entry(
    label: str,
    value: Any,
    page_by_output: dict[str, dict[str, Any]],
    page_by_source: dict[str, dict[str, Any]],
) -> dict[str, Any]:
    if isinstance(value, str):
        return _doc_item(label, value, page_by_output, page_by_source)
    if isinstance(value, list):
        return {
            "type": "category",
            "label": label,
            "collapsed": True,
            "items": [
                _convert_source_entry(child, page_by_output, page_by_source)
                for child in value
            ],
        }
    if isinstance(value, dict):
        return _convert_category_mapping(label, value, page_by_output, page_by_source)
    raise ValueError(f"Unsupported sidebar source group for {label!r}: {value!r}")


def build_sidebar_items_from_source(
    sidebars_yml: Path,
    pages: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    page_by_source, page_by_output = _page_indexes(pages)
    docs = _load_sidebar_source(sidebars_yml)

    if isinstance(docs, dict):
        entries = [{label: value} for label, value in docs.items()]
    elif isinstance(docs, list):
        entries = docs
    else:
        raise ValueError(f"Unsupported 'docs' sidebar source in {sidebars_yml}")

    return [
        _convert_source_entry(entry, page_by_output, page_by_source)
        for entry in entries
    ]


def render_sidebars_js(sidebar_items: list[dict[str, Any]]) -> str:
    payload = json.dumps({"docs": sidebar_items}, indent=2)
    return (
        "// Generated by CrocoDocs from website/sidebars.yml.\n"
        "// Do not edit by hand.\n\n"
        f"module.exports = {payload};\n"
    )


def write_sidebars_js_from_source(
    sidebars_yml: Path,
    pages: list[dict[str, Any]],
    output_path: Path,
) -> None:
    sidebar_items = build_sidebar_items_from_source(sidebars_yml, pages)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(render_sidebars_js(sidebar_items), encoding="utf-8")
