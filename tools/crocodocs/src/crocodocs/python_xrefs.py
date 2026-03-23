"""Migrate mkdocs-style Python docstring xrefs to Sphinx roles."""

from __future__ import annotations

import ast
import json
import re
from dataclasses import dataclass
from pathlib import Path

from .config import CrocoDocsConfig
from .progress import ProgressReporter, Summary

XREF_RE = re.compile(r"\[([^\]]+)\]\[([^\]]+)\]")
STRING_LITERAL_RE = re.compile(
    r"(?is)^(?P<prefix>[rubf]*)(?P<quote>'''|\"\"\"|'|\")(?P<body>.*)(?P=quote)$"
)


@dataclass
class ApiSymbol:
    name: str
    role: str
    canonical_path: str | None


@dataclass
class Replacement:
    start: int
    end: int
    text: str


@dataclass
class RewriteContext:
    distribution_name: str
    module_name: str
    module_scope: str
    package_scope: str
    canonical_package: str
    local_attrs: frozenset[str]
    local_methods: frozenset[str]
    local_classes: frozenset[str]
    ancestor_class_members: tuple[
        tuple[frozenset[str], frozenset[str], frozenset[str]], ...
    ]
    class_name: str | None = None
    class_symbol: str | None = None


class ApiMetadata:
    def __init__(self, api_data: dict):
        self.api_data = api_data
        self.symbols: dict[str, ApiSymbol] = {}
        self.member_roles: dict[str, str] = {}
        self.canonical_to_public: dict[str, str] = {}
        self.module_to_public_scope: dict[str, str] = {}
        self.top_level_namespaces: set[str] = set()
        self.class_bases: dict[str, list[str]] = {}
        self._load()

    def _load(self) -> None:
        for symbol, entry in self.api_data.get("classes", {}).items():
            canonical = entry.get("canonical_path") or symbol
            self.symbols[symbol] = ApiSymbol(symbol, "class", canonical)
            self._prefer_public(canonical, symbol)
            self._store_class_bases(symbol, canonical, entry.get("bases", []))
            for item in entry.get("properties", []):
                self.member_roles[f"{symbol}.{item['name']}"] = "attr"
                self.member_roles[f"{canonical}.{item['name']}"] = "attr"
            for item in entry.get("events", []):
                self.member_roles[f"{symbol}.{item['name']}"] = "attr"
                self.member_roles[f"{canonical}.{item['name']}"] = "attr"
            for item in entry.get("methods", []):
                self.member_roles[f"{symbol}.{item['name']}"] = "meth"
                self.member_roles[f"{canonical}.{item['name']}"] = "meth"

        for symbol, entry in self.api_data.get("functions", {}).items():
            canonical = entry.get("canonical_path") or symbol
            self.symbols[symbol] = ApiSymbol(symbol, "func", canonical)
            self._prefer_public(canonical, symbol)

        for symbol, entry in self.api_data.get("aliases", {}).items():
            canonical = entry.get("canonical_path") or symbol
            target_kind = entry.get("target_kind")
            role = (
                "class"
                if target_kind == "Class"
                else "func"
                if target_kind == "Function"
                else "data"
            )
            self.symbols[symbol] = ApiSymbol(symbol, role, canonical)
            self._prefer_public(canonical, symbol)

    def _prefer_public(self, canonical: str | None, symbol: str) -> None:
        self.top_level_namespaces.add(symbol.split(".", 1)[0])
        if not canonical:
            return
        existing = self.canonical_to_public.get(canonical)
        if existing is None or symbol.count(".") < existing.count("."):
            self.canonical_to_public[canonical] = symbol
        self.top_level_namespaces.add(canonical.split(".", 1)[0])
        canonical_module = canonical.rsplit(".", 1)[0]
        public_scope = symbol.rsplit(".", 1)[0] if "." in symbol else symbol
        existing_scope = self.module_to_public_scope.get(canonical_module)
        if existing_scope is None or public_scope.count(".") < existing_scope.count(
            "."
        ):
            self.module_to_public_scope[canonical_module] = public_scope

    def _store_class_bases(
        self, symbol: str, canonical: str | None, bases: list[str]
    ) -> None:
        resolved = self._resolve_base_symbols(symbol, bases)
        self.class_bases[symbol] = resolved
        if canonical:
            self.class_bases[canonical] = resolved

    def _resolve_base_symbols(self, owner_symbol: str, bases: list[str]) -> list[str]:
        if "." in owner_symbol:
            namespace = owner_symbol.split(".", 1)[0]
        else:
            namespace = owner_symbol
        resolved: list[str] = []
        for base in bases:
            candidate = base if "." in base else f"{namespace}.{base}"
            resolved.append(candidate)
        return resolved

    def preferred_symbol(self, symbol: str) -> str:
        entry = self.symbols.get(symbol)
        if entry and entry.canonical_path:
            return self.canonical_to_public.get(entry.canonical_path, symbol)
        if "." in symbol:
            owner, member = symbol.rsplit(".", 1)
            owner_entry = self.symbols.get(owner)
            if owner_entry and owner_entry.canonical_path:
                preferred_owner = self.canonical_to_public.get(
                    owner_entry.canonical_path, owner
                )
                return f"{preferred_owner}.{member}"
            module_scope = self.module_to_public_scope.get(owner)
            if module_scope:
                return f"{module_scope}.{member}"
            preferred_owner = self.canonical_to_public.get(owner)
            if preferred_owner:
                return f"{preferred_owner}.{member}"
        return self.canonical_to_public.get(symbol, symbol)

    def symbol_role(self, symbol: str) -> str | None:
        preferred = self.preferred_symbol(symbol)
        entry = self.symbols.get(preferred) or self.symbols.get(symbol)
        if entry:
            return entry.role
        member_role = self.member_role(preferred) or self.member_role(symbol)
        if member_role:
            return member_role
        if symbol.split(".")[-1].isupper():
            return "data"
        return None

    def has_symbol(self, symbol: str) -> bool:
        preferred = self.preferred_symbol(symbol)
        return (
            preferred in self.symbols
            or self.member_role(preferred) is not None
            or symbol in self.symbols
            or self.member_role(symbol) is not None
        )

    def local_member_role(
        self, class_symbol: str | None, member_name: str
    ) -> str | None:
        if not class_symbol:
            return None
        return self.member_role(f"{class_symbol}.{member_name}")

    def public_module_scope(self, module_name: str) -> str:
        normalized = module_name.removesuffix(".__init__")
        fallback = normalized.rsplit(".", 1)[0] if "." in normalized else normalized
        return self.module_to_public_scope.get(normalized, fallback)

    def member_role(self, symbol: str) -> str | None:
        preferred = self.preferred_symbol(symbol)
        if preferred in self.member_roles:
            return self.member_roles[preferred]
        if symbol in self.member_roles:
            return self.member_roles[symbol]
        if "." not in preferred:
            return None
        owner, member = preferred.rsplit(".", 1)
        return self._inherited_member_role(owner, member, set())

    def _inherited_member_role(
        self, owner: str, member: str, seen: set[str]
    ) -> str | None:
        owner = self.preferred_symbol(owner)
        if owner in seen:
            return None
        seen.add(owner)
        for base in self.class_bases.get(owner, []):
            preferred_base = self.preferred_symbol(base)
            direct = self.member_roles.get(f"{preferred_base}.{member}")
            if direct:
                return direct
            inherited = self._inherited_member_role(preferred_base, member, seen)
            if inherited:
                return inherited
        return None


def _label_text(label: str) -> str:
    return label.strip().strip("`")


def _strip_call_suffix(value: str) -> str:
    return value[:-2] if value.endswith("()") else value


def _should_use_shortened_global(label: str, symbol: str) -> bool:
    clean = _strip_call_suffix(_label_text(label))
    return clean == symbol.split(".")[-1]


def _choose_role_for_global(symbol: str, metadata: ApiMetadata) -> str | None:
    role = metadata.symbol_role(symbol)
    if role is None and symbol in metadata.api_data.get("xref_map", {}):
        clean_symbol = symbol.split(".")[-1]
        if clean_symbol.isupper():
            role = "data"
        elif clean_symbol and clean_symbol[0].isupper():
            role = "class"
        else:
            role = "attr"
    if role == "obj":
        return "data"
    return role


def _is_project_symbol(symbol: str, metadata: ApiMetadata) -> bool:
    return symbol.split(".", 1)[0] in metadata.top_level_namespaces


def _plain_code_target(target: str) -> str | None:
    if target in {"(c)", "(c).", "(m)", "(m).", "(p)", "(p).", ".."}:
        return None
    if (
        target.startswith("(c).")
        or target.startswith("(m).")
        or target.startswith("(p).")
    ):
        return None
    if target.endswith("."):
        return None
    return target.lstrip("?")


def _plain_code_label(label: str) -> str:
    return _label_text(label)


def _literal_body(raw_literal: str) -> str | None:
    match = STRING_LITERAL_RE.match(raw_literal)
    if not match:
        return None
    return match.group("body")


def _rewrite_raw_literal_body(raw_literal: str, body: str) -> str:
    match = STRING_LITERAL_RE.match(raw_literal)
    if not match:
        return repr(body)
    prefix = match.group("prefix")
    quote = match.group("quote")
    original_body = match.group("body")
    if original_body == body:
        return raw_literal
    return f"{prefix}{quote}{body}{quote}"


def _offsets(source: str) -> list[int]:
    starts = [0]
    index = 0
    for line in source.splitlines(keepends=True):
        index += len(line)
        starts.append(index)
    return starts


def _position_to_offset(line_offsets: list[int], lineno: int, col: int) -> int:
    return line_offsets[lineno - 1] + col


def _iter_string_exprs(tree: ast.AST, context: RewriteContext, metadata: ApiMetadata):
    body = getattr(tree, "body", None)
    if not isinstance(body, list):
        return
    for node in body:
        if (
            isinstance(node, ast.Expr)
            and isinstance(node.value, ast.Constant)
            and isinstance(node.value.value, str)
        ):
            yield node.value, context
        elif isinstance(node, ast.ClassDef):
            module_name = context.module_name.removesuffix(".__init__")
            canonical_symbol = f"{module_name}.{node.name}"
            public_symbol = metadata.preferred_symbol(canonical_symbol)
            local_attrs, local_methods, local_classes = _class_local_members(node)
            yield from _iter_string_exprs(
                node,
                RewriteContext(
                    distribution_name=context.distribution_name,
                    module_name=context.module_name,
                    module_scope=context.module_scope,
                    package_scope=context.package_scope,
                    canonical_package=context.canonical_package,
                    local_attrs=local_attrs,
                    local_methods=local_methods,
                    local_classes=local_classes,
                    ancestor_class_members=(
                        *context.ancestor_class_members,
                        (local_attrs, local_methods, local_classes),
                    ),
                    class_name=node.name,
                    class_symbol=public_symbol,
                ),
                metadata,
            )
        elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            yield from _iter_string_exprs(
                node,
                RewriteContext(
                    distribution_name=context.distribution_name,
                    module_name=context.module_name,
                    module_scope=context.module_scope,
                    package_scope=context.package_scope,
                    canonical_package=context.canonical_package,
                    local_attrs=context.local_attrs,
                    local_methods=context.local_methods,
                    local_classes=context.local_classes,
                    ancestor_class_members=context.ancestor_class_members,
                    class_name=context.class_name,
                    class_symbol=context.class_symbol,
                ),
                metadata,
            )


def _class_local_members(
    node: ast.ClassDef,
) -> tuple[frozenset[str], frozenset[str], frozenset[str]]:
    attrs: set[str] = set()
    methods: set[str] = set()
    classes: set[str] = set()
    for child in node.body:
        if isinstance(child, (ast.FunctionDef, ast.AsyncFunctionDef)):
            methods.add(child.name)
        elif isinstance(child, ast.ClassDef):
            classes.add(child.name)
        elif isinstance(child, ast.AnnAssign) and isinstance(child.target, ast.Name):
            attrs.add(child.target.id)
        elif isinstance(child, ast.Assign):
            for target in child.targets:
                if isinstance(target, ast.Name):
                    attrs.add(target.id)
    return frozenset(attrs), frozenset(methods), frozenset(classes)


def _resolve_global_candidate(
    target: str, label: str, context: RewriteContext
) -> str | None:
    clean = _strip_call_suffix(_label_text(label))
    if target == "(p).":
        return f"{context.package_scope}.{clean}"
    if target.startswith("(p)."):
        suffix = target[4:]
        if suffix.endswith("."):
            return f"{context.canonical_package}.{suffix}{clean}"
        return f"{context.package_scope}.{suffix}"
    if target == "(m).":
        return f"{context.module_scope}.{clean}"
    if target.startswith("(m)."):
        suffix = target[4:]
        if suffix.endswith("."):
            return f"{context.module_scope}.{suffix}{clean}"
        return f"{context.module_scope}.{suffix}"
    if target in {"(c)", "(c).", ".."} or target.startswith("(c)."):
        return None
    if target.endswith("."):
        return f"{target}{clean}"
    return target


def _local_replacement(
    target: str, label: str, context: RewriteContext, metadata: ApiMetadata
) -> str | None:
    if not context.class_name:
        return None
    if target == "(c)":
        return f":class:`{context.class_name}`"

    if target == "(c)." or target == "..":
        member_name = _strip_call_suffix(_label_text(label))
    elif target.startswith("(c)."):
        member_name = _strip_call_suffix(target[4:])
    else:
        return None

    role = metadata.local_member_role(context.class_symbol, member_name)
    if role is None:
        role = _local_source_role(member_name, context)
    if role is None and member_name.isupper():
        role = "data"
    if role is None:
        return None
    return f":{role}:`{member_name}`"


def _local_source_role(member_name: str, context: RewriteContext) -> str | None:
    if member_name in context.local_methods:
        return "meth"
    if member_name in context.local_attrs:
        return "attr"
    if member_name in context.local_classes:
        return "class"
    for attrs, methods, classes in reversed(context.ancestor_class_members[:-1]):
        if member_name in methods:
            return "meth"
        if member_name in attrs:
            return "attr"
        if member_name in classes:
            return "class"
    return None


def _global_replacement(
    target: str, label: str, context: RewriteContext, metadata: ApiMetadata
) -> str | None:
    candidate = _resolve_global_candidate(target, label, context)
    if not candidate:
        return None
    preferred = metadata.preferred_symbol(candidate)
    if not _is_project_symbol(preferred, metadata):
        return None
    role = _choose_role_for_global(preferred, metadata)
    if role is None:
        return None
    if label.strip().strip("`").endswith("()") and role == "attr":
        role = "meth"
    if _should_use_shortened_global(label, preferred):
        return f":{role}:`~{preferred}`"
    return f":{role}:`{preferred}`"


def _plain_code_replacement(
    target: str, label: str, context: RewriteContext, metadata: ApiMetadata
) -> str | None:
    candidate = _plain_code_target(target)
    if not candidate:
        candidate = _resolve_global_candidate(target, label, context)
        if not candidate:
            return None
        preferred = metadata.preferred_symbol(candidate)
        if not _is_project_symbol(preferred, metadata):
            return None
        if metadata.has_symbol(preferred):
            return None
        return f"`{_plain_code_label(label)}`"
    if candidate.split(".", 1)[0] in metadata.top_level_namespaces:
        if metadata.has_symbol(candidate):
            return None
        return f"`{_plain_code_label(label)}`"
    return f"`{candidate}`"


def _module_plain_code_replacement(target: str, label: str) -> str | None:
    if target == "(m)." or target.startswith("(m)."):
        return f"`{_plain_code_label(label)}`"
    return None


def _local_plain_code_replacement(target: str, label: str) -> str | None:
    if target in {"(c).", ".."} or target.startswith("(c)."):
        return f"`{_plain_code_label(label)}`"
    return None


def _rewrite_docstring(
    docstring: str, context: RewriteContext, metadata: ApiMetadata
) -> tuple[str, int, list[tuple[str, str]]]:
    converted = 0
    skipped: list[tuple[str, str]] = []

    def replace(match: re.Match[str]) -> str:
        nonlocal converted
        label, target = match.group(1), match.group(2)

        local = _local_replacement(target, label, context, metadata)
        if local:
            converted += 1
            return local

        global_ref = _global_replacement(target, label, context, metadata)
        if global_ref:
            converted += 1
            return global_ref

        module_plain_code = _module_plain_code_replacement(target, label)
        if module_plain_code:
            converted += 1
            return module_plain_code

        local_plain_code = _local_plain_code_replacement(target, label)
        if local_plain_code:
            converted += 1
            return local_plain_code

        plain_code = _plain_code_replacement(target, label, context, metadata)
        if plain_code:
            converted += 1
            return plain_code

        skipped.append((label, target))
        return match.group(0)

    return XREF_RE.sub(replace, docstring), converted, skipped


def _rewrite_file(
    path: Path, package_name: str, module_name: str, metadata: ApiMetadata
) -> tuple[int, list[tuple[str, str, str]]]:
    source = path.read_text(encoding="utf-8")
    tree = ast.parse(source)
    offsets = _offsets(source)
    replacements: list[Replacement] = []
    converted = 0
    skipped: list[tuple[str, str, str]] = []
    module_scope = metadata.public_module_scope(module_name)
    package_scope = module_scope
    normalized_module = module_name.removesuffix(".__init__")
    canonical_package = (
        normalized_module.rsplit(".", 1)[0]
        if "." in normalized_module
        else normalized_module
    )

    for string_node, context in _iter_string_exprs(
        tree,
        RewriteContext(
            distribution_name=package_name,
            module_name=module_name,
            module_scope=module_scope,
            package_scope=package_scope,
            canonical_package=canonical_package,
            local_attrs=frozenset(),
            local_methods=frozenset(),
            local_classes=frozenset(),
            ancestor_class_members=(),
        ),
        metadata,
    ):
        raw_literal = ast.get_source_segment(source, string_node)
        if raw_literal is None:
            continue
        raw_body = _literal_body(raw_literal)
        if raw_body is None:
            continue

        new_body, count, node_skips = _rewrite_docstring(raw_body, context, metadata)
        if count == 0 and not node_skips:
            continue

        if new_body != raw_body:
            start = _position_to_offset(
                offsets, string_node.lineno, string_node.col_offset
            )
            end = _position_to_offset(
                offsets, string_node.end_lineno, string_node.end_col_offset
            )
            replacements.append(
                Replacement(
                    start=start,
                    end=end,
                    text=_rewrite_raw_literal_body(raw_literal, new_body),
                )
            )
            converted += count
        for label, target in node_skips:
            skipped.append((str(path), label, target))

    if replacements:
        updated = source
        for item in sorted(replacements, key=lambda repl: repl.start, reverse=True):
            updated = updated[: item.start] + item.text + updated[item.end :]
        path.write_text(updated, encoding="utf-8")

    return converted, skipped


def _package_sources(
    config: CrocoDocsConfig, selected: set[str] | None
) -> list[tuple[str, Path]]:
    items = []
    for package_name, root in sorted(config.packages.items()):
        accepted_names = {package_name, package_name.replace("_", "-")}
        if selected and not (accepted_names & selected):
            continue
        items.append((package_name, root))
    return items


def run_migrate_python_xrefs(
    config: CrocoDocsConfig,
    package_names: list[str] | None = None,
) -> None:
    reporter = ProgressReporter("migrate-python-xrefs")
    summary = Summary("migrate-python-xrefs")

    api_output = config.api_output
    if not api_output.exists():
        raise FileNotFoundError(
            f"API data not found: {api_output}. Run `crocodocs generate` first."
        )

    metadata = ApiMetadata(json.loads(api_output.read_text(encoding="utf-8")))
    selected = set(package_names or []) or None
    packages = _package_sources(config, selected)

    converted_total = 0
    skipped_total: list[tuple[str, str, str]] = []
    files_touched = 0

    for package_name, root in packages:
        reporter.stage(f"Scanning {package_name}")
        package_dir = root / package_name.replace("-", "_")
        if not package_dir.exists():
            package_dir = root / package_name
        for path in sorted(package_dir.rglob("*.py")):
            if "__pycache__" in path.parts:
                continue
            module_name = ".".join(path.relative_to(root).with_suffix("").parts)
            converted, skipped = _rewrite_file(
                path, package_name, module_name, metadata
            )
            if converted:
                files_touched += 1
                converted_total += converted
            skipped_total.extend(skipped)

    summary.add("files touched", files_touched)
    summary.add("xrefs converted", converted_total)
    summary.add("xrefs skipped", len(skipped_total))
    for file_path, label, target in skipped_total[:50]:
        summary.warn(f"Skipped xref in {file_path}: [{label}][{target}]")
    summary.print()
