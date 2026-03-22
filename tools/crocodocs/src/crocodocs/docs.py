"""Markdown and MDX parsing helpers."""

from __future__ import annotations

import ast
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from .frontmatter import FrontMatterDocument, dump_front_matter, parse_front_matter

MACRO_RE = re.compile(r"\{\{\s*([a-zA-Z_][a-zA-Z0-9_]*)\((.*?)\)\s*\}\}", re.DOTALL)
REF_RE = re.compile(r"\[[^\]]+\]\[([^\]]+)\]")
ADMONITION_RE = re.compile(r"^/// admonition \|", re.MULTILINE)
TAB_RE = re.compile(r"^/// tab \|", re.MULTILINE)
DETAILS_RE = re.compile(r"^/// details \|", re.MULTILINE)
CODE_ANNOTATION_RE = re.compile(r"# \(\d+\)!")
INCLUDE_BLOCK_RE = re.compile(
    r"```(?P<lang>[a-zA-Z0-9_+-]+)\n--8<--\s+\"(?P<path>[^\"]+)\"\n```", re.MULTILINE
)
COMPONENT_TAG_RE = re.compile(r"<(ClassSummary|ClassMembers|ClassAll)\b([^>]*)/>")
IMPORT_PARTIAL_RE = re.compile(r"@site/\.crocodocs/([a-z0-9._-]+\.mdx)")
CODE_EXAMPLE_TAG_RE = re.compile(r"<CodeExample\b([^>]*)/>")
PERCENT_WIDTH_RE = re.compile(r"^\s*(\d+(?:\.\d+)?)%\s*$")


@dataclass
class MacroCall:
    name: str
    args: list[ast.AST]
    kwargs: dict[str, ast.AST]
    source: str


@dataclass
class SymbolBlock:
    kind: str
    symbol: str | None
    options: dict[str, Any] = field(default_factory=dict)


@dataclass
class PageManifest:
    source_path: str
    output_path: str
    route: str
    title: str
    front_matter: dict[str, Any]
    symbol_blocks: list[SymbolBlock]


def iter_markdown_files(root: Path) -> list[Path]:
    return sorted(
        path
        for path in root.rglob("*")
        if path.is_file() and path.suffix.lower() in {".md", ".mdx"}
    )


def parse_macro_call(name: str, args_source: str) -> MacroCall:
    expression = ast.parse(f"{name}({args_source})", mode="eval").body
    if not isinstance(expression, ast.Call):
        raise ValueError(f"Expected call expression for macro {name}")
    kwargs = {
        keyword.arg: keyword.value
        for keyword in expression.keywords
        if keyword.arg is not None
    }
    return MacroCall(
        name=name, args=list(expression.args), kwargs=kwargs, source=args_source
    )


def collect_macro_calls(text: str) -> list[MacroCall]:
    calls: list[MacroCall] = []
    for match in MACRO_RE.finditer(text):
        calls.append(parse_macro_call(match.group(1), match.group(2)))
    return calls


def extract_reference_targets(text: str) -> list[str]:
    return REF_RE.findall(text)


def compute_output_path(
    source_root: Path, output_root: Path, source_path: Path
) -> Path:
    return output_root / source_path.relative_to(source_root)


def route_for_output(base_url: str, output_root: Path, output_path: Path) -> str:
    relative = output_path.relative_to(output_root).with_suffix("")
    parts = list(relative.parts)
    if parts and parts[-1] == "index":
        parts = parts[:-1]
    route = "/".join(part for part in parts if part)
    if route:
        return f"{base_url.rstrip('/')}/{route}"
    return base_url.rstrip("/") or "/"


def default_title(front_matter: dict[str, Any], body: str, fallback: str) -> str:
    title = front_matter.get("title")
    if isinstance(title, str) and title.strip():
        return title
    class_name = front_matter.get("class_name")
    if isinstance(class_name, str) and class_name.strip():
        return class_name.split(".")[-1]
    for line in body.splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    return fallback


def normalize_migrated_image_width(value: str) -> str:
    match = PERCENT_WIDTH_RE.fullmatch(value)
    if not match:
        return value
    percent = float(match.group(1))
    if percent < 60:
        return value
    scaled = round((percent * (2 / 3)) / 5) * 5
    scaled = max(30, min(70, scaled))
    return f"{scaled}%"


def _snake_to_camel(name: str) -> str:
    head, *tail = name.split("_")
    return head + "".join(part.capitalize() for part in tail)


def ast_to_python_value(node: ast.AST) -> Any:
    if isinstance(node, ast.Constant):
        return node.value
    if isinstance(node, ast.Name):
        return {"$frontMatter": node.id}
    if isinstance(node, ast.BinOp) and isinstance(node.op, ast.Add):
        return {
            "$concat": [ast_to_python_value(node.left), ast_to_python_value(node.right)]
        }
    if isinstance(node, ast.Dict):
        return {
            ast_to_python_value(key): ast_to_python_value(value)
            for key, value in zip(node.keys, node.values)
            if key is not None
        }
    if isinstance(node, ast.List):
        return [ast_to_python_value(item) for item in node.elts]
    if isinstance(node, ast.Tuple):
        return [ast_to_python_value(item) for item in node.elts]
    if isinstance(node, ast.UnaryOp) and isinstance(node.op, ast.USub):
        inner = ast_to_python_value(node.operand)
        if isinstance(inner, (int, float)):
            return -inner
    return {"$raw": ast.unparse(node)}


def ast_to_jsx(node: ast.AST) -> str:
    value = ast_to_python_value(node)
    return python_value_to_jsx(value)


def python_value_to_jsx(value: Any) -> str:
    if isinstance(value, str):
        return f'"{value}"'
    if isinstance(value, bool):
        return "{true}" if value else "{false}"
    if value is None:
        return "{null}"
    if isinstance(value, (int, float)):
        return f"{{{value}}}"
    if isinstance(value, dict):
        if "$frontMatter" in value:
            return f"{{frontMatter.{value['$frontMatter']}}}"
        if "$concat" in value:
            parts = []
            for item in value["$concat"]:
                if isinstance(item, dict) and "$frontMatter" in item:
                    parts.append(f"frontMatter.{item['$frontMatter']}")
                else:
                    parts.append(repr(item))
            return "{" + " + ".join(parts) + "}"
        if "$raw" in value:
            return "{" + value["$raw"] + "}"
        items = []
        for key, nested in value.items():
            items.append(f"{key}: {python_value_to_jsx(nested).strip('{}')}")
        return "{{ " + ", ".join(items) + " }}"
    if isinstance(value, list):
        items = ", ".join(python_value_to_jsx(item).strip("{}") for item in value)
        return "{[" + items + "]}"
    return "{null}"


def macro_call_to_component(call: MacroCall) -> tuple[str, SymbolBlock] | None:
    component_map = {
        "class_summary": ("ClassSummary", "class_summary"),
        "class_members": ("ClassMembers", "class_members"),
        "class_all_options": ("ClassAll", "class_all_options"),
    }
    if call.name not in component_map:
        return None
    component_name, kind = component_map[call.name]
    props: list[str] = []
    symbol: str | None = None
    if call.args:
        symbol_value = ast_to_python_value(call.args[0])
        if isinstance(symbol_value, str):
            symbol = symbol_value
        elif isinstance(symbol_value, dict) and "$frontMatter" in symbol_value:
            symbol = None
        props.append(f"name={ast_to_jsx(call.args[0])}")
    if call.name == "class_summary":
        positional_summary_props = {
            1: "image",
            2: "imageWidth",
            3: "imageCaption",
        }
        for index, prop_name in positional_summary_props.items():
            if len(call.args) > index:
                if prop_name == "imageWidth":
                    value = ast_to_python_value(call.args[index])
                    if isinstance(value, str):
                        props.append(
                            f'imageWidth="{normalize_migrated_image_width(value)}"'
                        )
                        continue
                props.append(f"{prop_name}={ast_to_jsx(call.args[index])}")
    options: dict[str, Any] = {}
    special_prop_names = {
        "image_url": "image",
        "image_width": "imageWidth",
        "image_caption": "imageCaption",
    }
    for key, value in call.kwargs.items():
        options[key] = ast_to_python_value(value)
        prop_name = special_prop_names.get(key, _snake_to_camel(key))
        if prop_name == "imageWidth":
            normalized = options[key]
            if isinstance(normalized, str):
                props.append(
                    f'imageWidth="{normalize_migrated_image_width(normalized)}"'
                )
                continue
        props.append(f"{prop_name}={ast_to_jsx(value)}")
    component = f"<{component_name} " + " ".join(props) + " />"
    return component, SymbolBlock(kind=kind, symbol=symbol, options=options)


def image_macro_to_component(call: MacroCall) -> str | None:
    if call.name != "image":
        return None
    props: list[str] = []
    src_node: ast.AST | None = call.args[0] if call.args else call.kwargs.get("src")
    if src_node is None:
        return None
    props.append(f"src={ast_to_jsx(src_node)}")
    if len(call.args) > 1:
        props.append(f"alt={ast_to_jsx(call.args[1])}")
    for key in ("alt", "width", "caption", "link"):
        if key in call.kwargs:
            if key == "width":
                value = ast_to_python_value(call.kwargs[key])
                if isinstance(value, str):
                    props.append(f'width="{normalize_migrated_image_width(value)}"')
                    continue
            props.append(f"{key}={ast_to_jsx(call.kwargs[key])}")
    return "<Image " + " ".join(props) + " />"


def partial_name_for_macro(call: MacroCall) -> str | None:
    if call.name == "flet_pypi_index":
        return "pypi-index.mdx"
    if call.name == "cross_platform_permissions":
        return "cross-platform-permissions.mdx"
    if call.name == "controls_overview":
        return "controls-overview.mdx"
    if call.name == "services_overview":
        return "services-overview.mdx"
    if call.name == "cookbook_overview":
        return "cookbook-overview.mdx"
    if call.name == "flet_cli_as_markdown":
        command = ""
        if call.args:
            value = ast_to_python_value(call.args[0])
            if isinstance(value, str):
                command = value
        if not command:
            return "cli-root.mdx"
        slug = command.replace(" ", "-")
        return f"cli-{slug}.mdx"
    return None


def import_alias_for_partial(filename: str) -> str:
    stem = filename.removesuffix(".mdx")
    parts = re.split(r"[-_.]+", stem)
    return "".join(part.capitalize() for part in parts if part)


def convert_include_path(raw_path: str) -> str:
    path = raw_path.strip()
    path = path.replace("{{ examples }}/", "{frontMatter.examples}/")
    if path.startswith("../../examples/"):
        return path[len("../../examples/") :]
    return path


def extract_symbol_blocks_from_mdx(
    text: str, front_matter: dict[str, Any]
) -> list[SymbolBlock]:
    blocks: list[SymbolBlock] = []
    for match in COMPONENT_TAG_RE.finditer(text):
        component = match.group(1)
        attrs = match.group(2)
        symbol = None
        name_match = re.search(r'name="([^"]+)"', attrs)
        if name_match:
            symbol = name_match.group(1)
        else:
            fm_match = re.search(r"name=\{frontMatter\.([a-zA-Z0-9_]+)\}", attrs)
            if fm_match:
                raw = front_matter.get(fm_match.group(1))
                if isinstance(raw, str):
                    symbol = raw
        kind = {
            "ClassSummary": "class_summary",
            "ClassMembers": "class_members",
            "ClassAll": "class_all_options",
        }[component]
        blocks.append(SymbolBlock(kind=kind, symbol=symbol, options={}))
    return blocks


def extract_code_example_paths_from_mdx(
    text: str, front_matter: dict[str, Any]
) -> list[str]:
    paths: list[str] = []
    for match in CODE_EXAMPLE_TAG_RE.finditer(text):
        attrs = match.group(1)
        literal_match = re.search(r'path="([^"]+)"', attrs)
        if literal_match:
            paths.append(literal_match.group(1))
            continue

        concat_match = re.search(
            r"""path=\{frontMatter\.([a-zA-Z0-9_]+)\s*\+\s*(['"])(.+?)\2\}""",
            attrs,
        )
        if concat_match:
            base_value = front_matter.get(concat_match.group(1))
            suffix = concat_match.group(3)
            if isinstance(base_value, str):
                paths.append(base_value + suffix)
    return paths


def parse_document(text: str) -> FrontMatterDocument:
    return parse_front_matter(text)


def rebuild_document(
    front_matter: dict[str, Any], imports: list[str], body: str
) -> str:
    pieces: list[str] = []
    fm = dump_front_matter(front_matter)
    if fm:
        pieces.append(fm.rstrip())
    if imports:
        pieces.append("\n".join(sorted(dict.fromkeys(imports))))
    pieces.append(body.strip() + "\n")
    return "\n\n".join(piece for piece in pieces if piece)
