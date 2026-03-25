"""Bootstrap migration command."""

from __future__ import annotations

import json
import re
from dataclasses import asdict
from pathlib import Path

from .assets import (
    resolve_local_asset_source,
    resolve_static_asset_url,
)
from .config import CrocoDocsConfig
from .docs import (
    INCLUDE_BLOCK_RE,
    collect_macro_calls,
    compute_output_path,
    convert_include_path,
    default_title,
    image_macro_to_component,
    import_alias_for_partial,
    iter_markdown_files,
    macro_call_to_component,
    normalize_migrated_image_width,
    parse_document,
    partial_name_for_macro,
    rebuild_document,
    route_for_output,
)
from .progress import ProgressReporter, Summary
from .sidebars import build_nav_title_map


def _slugify_tab_value(label: str) -> str:
    value = re.sub(r"[^a-zA-Z0-9]+", "-", label.strip().lower()).strip("-")
    return value or "tab"


def _tab_label_prop(label: str) -> str:
    stripped = label.strip()
    if len(stripped) >= 2 and stripped.startswith("`") and stripped.endswith("`"):
        stripped = stripped[1:-1]

    safe_label = stripped.replace('"', "&quot;")
    return f'label="{safe_label}"'


def _tab_group_id(labels: list[str]) -> str:
    normalized = []
    for label in labels:
        stripped = label.strip()
        if len(stripped) >= 2 and stripped.startswith("`") and stripped.endswith("`"):
            stripped = stripped[1:-1]
        normalized.append(_slugify_tab_value(stripped))
    return "--".join(normalized) or "tabs"


DIRECTIVE_OPEN_RE = re.compile(r"///\s*([a-z_]+)(?:\s*\|\s*(.+))?$")
DIRECTIVE_TYPE_RE = re.compile(r"\s*type:\s*(\w+)\s*$")
LOCAL_ASSET_REF_RE = re.compile(r"(?:\.\./)+[^/\s)\"'}>]+/[^\s)\"'}>]+")
STYLE_BLOCK_RE = re.compile(r"<style>\s*\n(.*?)\n</style>", re.DOTALL)
MARKDOWN_IMAGE_RE = re.compile(r"!\[([^\]]*)\]\((\.\./[^)]+)\)(\{[^}]*\})?")
MARKDOWN_IMAGE_ATTR_RE = re.compile(r'(\w+)="([^"]*)"')
HTML_STYLE_ATTR_RE = re.compile(r'style="([^"]*)"')
HTML_IMG_SRC_RE = re.compile(r'(<img\b[^>]*\bsrc=")([^"]+)(")')


def _consume_directive_body(
    lines: list[str], index: int
) -> tuple[list[str], int, bool, bool]:
    out: list[str] = []
    used_tabs = False
    has_remaining = False

    while index < len(lines):
        stripped = lines[index].strip()
        if stripped == "///":
            return out, index + 1, used_tabs, has_remaining

        directive_match = DIRECTIVE_OPEN_RE.fullmatch(stripped)
        if directive_match:
            name = directive_match.group(1)
            title = (directive_match.group(2) or "").strip()
            if name == "tab":
                tabs: list[tuple[str, list[str]]] = []
                while index < len(lines):
                    tab_match = DIRECTIVE_OPEN_RE.fullmatch(lines[index].strip())
                    if not tab_match or tab_match.group(1) != "tab":
                        break
                    tab_title = (tab_match.group(2) or "").strip()
                    tab_body, index, child_tabs, child_remaining = (
                        _consume_directive_body(lines, index + 1)
                    )
                    used_tabs = True
                    used_tabs |= child_tabs
                    has_remaining |= child_remaining
                    tabs.append((tab_title, tab_body))
                    while index < len(lines) and not lines[index].strip():
                        index += 1

                out.append(
                    f'<Tabs groupId="{_tab_group_id([tab_title for tab_title, _ in tabs])}">'
                )
                for tab_title, tab_body in tabs:
                    out.append(
                        f'<TabItem value="{_slugify_tab_value(tab_title)}" {_tab_label_prop(tab_title)}>'
                    )
                    out.extend(tab_body)
                    out.append("</TabItem>")
                out.append("</Tabs>")
                continue

            body, index, child_tabs, child_remaining = _consume_directive_body(
                lines, index + 1
            )
            used_tabs |= child_tabs
            has_remaining |= child_remaining

            if name == "admonition":
                admonition_type = "note"
                cleaned_body: list[str] = []
                for line in body:
                    type_match = DIRECTIVE_TYPE_RE.fullmatch(line)
                    if type_match:
                        admonition_type = type_match.group(1)
                    else:
                        cleaned_body.append(line)

                if admonition_type == "example":
                    admonition_type = "note"

                title_suffix = f"[{title}]" if title else ""
                out.append(f":::{admonition_type}{title_suffix}")
                out.extend(cleaned_body)
                out.append(":::")
                continue

            if name == "details":
                out.append("<details>")
                if title:
                    out.append(f"<summary>{title}</summary>")
                    out.append("")
                out.extend(body)
                out.append("</details>")
                continue

            if name == "caption":
                continue

            has_remaining = True
            header = f"/// {name}"
            if title:
                header += f" | {title}"
            out.append(header)
            out.extend(body)
            out.append("///")
            continue

        out.append(lines[index])
        index += 1

    return out, index, used_tabs, has_remaining


def _convert_directives(content: str) -> tuple[str, bool, bool]:
    lines = content.splitlines()
    out, _, used_tabs, has_remaining = _consume_directive_body(lines, 0)
    converted = "\n".join(out) + ("\n" if content.endswith("\n") else "")
    return converted, used_tabs, has_remaining


def _replace_macros(
    content: str,
    used_components: set[str],
    partial_imports: dict[str, str],
    symbol_blocks: list[dict],
) -> str:
    from .docs import MACRO_RE

    def replace(match: re.Match[str]) -> str:
        call = collect_macro_calls(match.group(0))[0]
        converted = macro_call_to_component(call)
        if converted is not None:
            component, block = converted
            used_components.add(component.split()[0][1:])
            symbol_blocks.append(asdict(block))
            return component

        image_component = image_macro_to_component(call)
        if image_component is not None:
            used_components.add("Image")
            return image_component

        partial_name = partial_name_for_macro(call)
        if partial_name is not None:
            alias = import_alias_for_partial(partial_name)
            partial_imports[partial_name] = alias
            return f"<{alias} />"
        return match.group(0)

    return MACRO_RE.sub(replace, content)


def _replace_includes(content: str) -> tuple[str, bool]:
    replaced = False

    def replace(match: re.Match[str]) -> str:
        nonlocal replaced
        replaced = True
        raw_path = convert_include_path(match.group("path"))
        info = match.group("info") or ""
        title_match = re.search(r'title="([^"]+)"', info)
        language = match.group("lang")
        if raw_path.startswith("{frontMatter.examples}/"):
            suffix = raw_path.removeprefix("{frontMatter.examples}/")
            path_expr = "{frontMatter.examples + " + repr("/" + suffix) + "}"
        else:
            path_expr = f'"{raw_path}"'
        props = [f"path={path_expr}"]
        if language:
            props.append(f'language="{language}"')
        if title_match:
            props.append(f'title="{title_match.group(1)}"')
        return "<CodeExample " + " ".join(props) + " />"

    return INCLUDE_BLOCK_RE.sub(replace, content), replaced


def _cleanup_mdx_syntax(content: str) -> str:
    content = re.sub(r"^\{\%\s*raw\s*\%\}\n?", "", content, flags=re.MULTILINE)
    content = re.sub(r"^\{\%\s*endraw\s*\%\}\n?", "", content, flags=re.MULTILINE)
    content = re.sub(r"^\{\s*\.annotate\s*\}\n?", "", content, flags=re.MULTILINE)
    content = re.sub(r"(?m)^\s*type:\s*\w+\s*$", "", content)
    content = re.sub(
        r"(?m)^::(note|info|tip|warning|danger|caution|important)\s*$",
        r":::\1",
        content,
    )
    content = re.sub(r"(?m)^::\s*$", ":::", content)
    content = content.replace(":::example[", ":::note[")
    content = STYLE_BLOCK_RE.sub(
        lambda match: "<style>{`" + match.group(1) + "`}</style>",
        content,
    )
    content = re.sub(r"\n{3,}", "\n\n", content)
    return content


def _apply_doc_slug(front_matter: dict, source_root: Path, source_path: Path) -> dict:
    updated = dict(front_matter)
    if "slug" in updated:
        return updated

    relative = source_path.relative_to(source_root)
    parent = relative.parent
    sibling_index = source_path.parent / "index.md"
    if parent.name and relative.stem == parent.name and sibling_index.exists():
        updated["slug"] = "/" + relative.with_suffix("").as_posix()
    return updated


def _replace_missing_markdown_images(
    input_root: Path,
    asset_mappings: dict,
    content: str,
    summary: Summary,
    source_path: Path,
) -> str:
    def replace(match: re.Match[str]) -> str:
        alt_text = match.group(1).strip() or "image"
        ref = match.group(2).strip()
        resolved = resolve_local_asset_source(ref, asset_mappings)
        if resolved is None or resolved.exists():
            return match.group(0)
        summary.warn(
            f"Missing local image omitted in {source_path.relative_to(input_root).as_posix()}: {ref}"
        )
        return f"> Missing image omitted: {alt_text}"

    return MARKDOWN_IMAGE_RE.sub(replace, content)


def _style_object_from_css(style_text: str) -> str:
    parts: list[str] = []
    for declaration in style_text.split(";"):
        declaration = declaration.strip()
        if not declaration or ":" not in declaration:
            continue
        raw_name, raw_value = declaration.split(":", 1)
        name = raw_name.strip()
        value = raw_value.strip()
        camel_name = re.sub(r"-([a-z])", lambda match: match.group(1).upper(), name)
        parts.append(f'{camel_name}: "{value}"')
    return "{{" + ", ".join(parts) + "}}"


def _normalize_html_for_mdx(content: str, asset_mappings: dict) -> str:
    content = re.sub(r"\browspan=", "rowSpan=", content)
    content = re.sub(r"\bcolspan=", "colSpan=", content)
    content = re.sub(r"\bcellspacing=", "cellSpacing=", content)
    content = re.sub(r"\bcellpadding=", "cellPadding=", content)
    content = HTML_IMG_SRC_RE.sub(
        lambda match: (
            match.group(1)
            + (
                resolve_static_asset_url(match.group(2), asset_mappings)
                or match.group(2)
            )
            + match.group(3)
        ),
        content,
    )
    content = HTML_STYLE_ATTR_RE.sub(
        lambda match: f"style={_style_object_from_css(match.group(1))}",
        content,
    )
    return content


def _convert_markdown_image_attrs_to_mdx(
    content: str,
    asset_mappings: dict,
) -> str:
    def replace(match: re.Match[str]) -> str:
        alt_text = match.group(1)
        ref = match.group(2)
        attrs = match.group(3)
        static_url = resolve_static_asset_url(ref, asset_mappings)
        parsed_attrs = {
            key: value for key, value in MARKDOWN_IMAGE_ATTR_RE.findall(attrs or "")
        }
        style_parts: list[str] = []
        if "width" in parsed_attrs:
            style_parts.append(
                f'width: "{normalize_migrated_image_width(parsed_attrs["width"])}"'
            )
        if "height" in parsed_attrs:
            style_parts.append(f'height: "{parsed_attrs["height"]}"')
        style_attr = ""
        if style_parts:
            style_attr = " style={{" + ", ".join(style_parts) + "}}"
        src = static_url or ref
        return (
            f'<figure className="doc-screenshot-figure">'
            f'<img alt="{alt_text}" className="doc-screenshot" src="{src}"{style_attr} />'
            f"</figure>"
        )

    return MARKDOWN_IMAGE_RE.sub(replace, content)


XREF_RE = re.compile(r"\[([^\]]+)\]\[([^\]]+)\]")


def _fenced_ranges(text: str) -> list[tuple[int, int]]:
    ranges: list[tuple[int, int]] = []
    offset = 0
    in_fence = False
    fence_start = 0
    fence_char = ""
    fence_len = 0
    for line in text.split("\n"):
        stripped = line.lstrip()
        if not in_fence:
            if stripped.startswith("```") or stripped.startswith("~~~"):
                ch = stripped[0]
                n = len(stripped) - len(stripped.lstrip(ch))
                in_fence = True
                fence_start = offset
                fence_char = ch
                fence_len = n
        else:
            if (
                stripped.startswith(fence_char * fence_len)
                and stripped.rstrip() == fence_char * len(stripped.rstrip())
                and len(stripped.rstrip()) >= fence_len
            ):
                in_fence = False
                ranges.append((fence_start, offset + len(line)))
        offset += len(line) + 1  # +1 for the \n
    return ranges


def _in_fenced_block(pos: int, ranges: list[tuple[int, int]]) -> bool:
    for start, end in ranges:
        if start <= pos < end:
            return True
        if pos < start:
            break
    return False


def _resolve_xref_route(target: str, xref_map: dict[str, str]) -> str | None:
    url = xref_map.get(target)
    if url:
        return url
    # For member targets like flet.Page.views, link to the parent class page
    parts = target.rsplit(".", 1)
    if len(parts) == 2:
        parent_url = xref_map.get(parts[0])
        if parent_url:
            return parent_url
    return None


def _route_to_md_path(route: str, base_url: str, source_root: Path) -> str | None:
    relative = route.removeprefix(base_url.rstrip("/") + "/")
    anchor = ""
    if "#" in relative:
        relative, anchor = relative.split("#", 1)
    for suffix in (".md", ".mdx", "/index.md", "/index.mdx"):
        candidate = source_root / f"{relative}{suffix}"
        if candidate.exists():
            result = candidate.relative_to(source_root).as_posix()
            if anchor:
                return f"{result}#{anchor}"
            return result
    return None


def _convert_xrefs(
    content: str,
    xref_map: dict[str, str],
    source_path: Path,
    source_root: Path,
    base_url: str,
) -> tuple[str, int]:
    if not xref_map:
        return content, 0

    fenced = _fenced_ranges(content)
    converted = 0
    source_rel_dir = source_path.parent.relative_to(source_root)

    def replace(match: re.Match[str]) -> str:
        nonlocal converted
        if _in_fenced_block(match.start(), fenced):
            return match.group(0)

        label, target = match.group(1), match.group(2)
        if "." not in target:
            return match.group(0)

        route = _resolve_xref_route(target, xref_map)
        if not route:
            return match.group(0)

        md_path = _route_to_md_path(route, base_url, source_root)
        if not md_path:
            return match.group(0)

        anchor = ""
        if "#" in md_path:
            md_path, anchor = md_path.rsplit("#", 1)

        from os.path import relpath

        rel_str = relpath(md_path, source_rel_dir).replace("\\", "/")

        link = rel_str if anchor == "" else f"{rel_str}#{anchor}"
        converted += 1
        return f"[{label}]({link})"

    result = XREF_RE.sub(replace, content)
    return result, converted


def _load_xref_map(config: CrocoDocsConfig) -> dict[str, str]:
    api_output = config.api_output
    if not api_output.exists():
        return {}
    data = json.loads(api_output.read_text(encoding="utf-8"))
    return data.get("xref_map", {})


def run_migrate_bootstrap(
    config: CrocoDocsConfig,
    input_root: Path,
    output_root: Path,
    manifest_output: Path,
    base_url: str,
) -> None:
    reporter = ProgressReporter("migrate")
    summary = Summary("migrate")
    reporter.stage("Scanning source docs")
    docs = iter_markdown_files(input_root)
    nav_titles = build_nav_title_map(config.mkdocs_yml)
    xref_map = _load_xref_map(config)
    pages: list[dict] = []
    converted_pages = 0
    converted_xrefs = 0
    follow_up_pages = 0

    for index, path in enumerate(docs, start=1):
        if index == 1 or index % 100 == 0 or index == len(docs):
            reporter.info(f"Processed {index}/{len(docs)} files")
        document = parse_document(path.read_text(encoding="utf-8"))
        source_path = path.relative_to(input_root).as_posix()
        front_matter = _apply_doc_slug(document.data, input_root, path)
        if (
            not isinstance(front_matter.get("title"), str)
            or not front_matter.get("title", "").strip()
        ):
            front_matter["title"] = nav_titles.get(
                source_path,
                default_title(front_matter, document.body, path.stem),
            )
        used_components: set[str] = set()
        partial_imports: dict[str, str] = {}
        symbol_blocks: list[dict] = []
        content = _replace_macros(
            document.body, used_components, partial_imports, symbol_blocks
        )
        content, used_code_example = _replace_includes(content)
        if used_code_example:
            used_components.add("CodeExample")
        content, used_tabs, has_remaining_directives = _convert_directives(content)
        content = _cleanup_mdx_syntax(content)
        content = _replace_missing_markdown_images(
            input_root, config.asset_mappings, content, summary, path
        )
        content = _convert_markdown_image_attrs_to_mdx(content, config.asset_mappings)
        content = _normalize_html_for_mdx(content, config.asset_mappings)
        content, xref_count = _convert_xrefs(
            content, xref_map, path, input_root, base_url
        )
        converted_xrefs += xref_count
        if has_remaining_directives:
            follow_up_pages += 1
            summary.warn(
                f"Manual review still needed for unsupported directive syntax in {path.relative_to(input_root).as_posix()}"
            )

        imports: list[str] = []
        if used_components:
            component_names = ", ".join(sorted(used_components))
            imports.append(
                f"import {{{component_names}}} from '@site/src/components/crocodocs';"
            )
        if used_tabs:
            imports.append("import Tabs from '@theme/Tabs';")
            imports.append("import TabItem from '@theme/TabItem';")
        for filename, alias in sorted(partial_imports.items()):
            imports.append(f"import {alias} from '@site/.crocodocs/{filename}';")

        output_path = compute_output_path(input_root, output_root, path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(
            rebuild_document(front_matter, imports, content),
            encoding="utf-8",
        )
        converted_pages += 1

        route = route_for_output(base_url, output_root, output_path)
        pages.append(
            {
                "source_path": source_path,
                "output_path": output_path.relative_to(output_root).as_posix(),
                "route": route,
                "title": front_matter["title"],
                "front_matter": front_matter,
                "symbol_blocks": symbol_blocks,
            }
        )

    reporter.stage("Writing bootstrap manifest")
    manifest_output.parent.mkdir(parents=True, exist_ok=True)
    manifest_output.write_text(
        __import__("json").dumps({"version": "1.0", "pages": pages}, indent=2),
        encoding="utf-8",
    )

    summary.add("pages converted", converted_pages)
    summary.add("xrefs converted", converted_xrefs)
    summary.add(
        "component imports inserted", sum(len(page["symbol_blocks"]) for page in pages)
    )
    summary.add("pages needing follow-up", follow_up_pages)
    try:
        sidebar_output = config.sidebars_source.relative_to(
            config.project_root
        ).as_posix()
    except ValueError:
        sidebar_output = config.sidebars_source.as_posix()
    summary.add("sidebar source", sidebar_output)
    summary.print()
