"""Markdown and MDX parsing helpers."""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from .frontmatter import FrontMatterDocument, parse_front_matter

COMPONENT_TAG_RE = re.compile(r"<(ClassSummary|ClassMembers|ClassAll)\b([^>]*)/>")
IMPORT_PARTIAL_RE = re.compile(r"@site/\.crocodocs/([a-z0-9._-]+\.mdx)")


@dataclass
class SymbolBlock:
    kind: str
    symbol: str | None
    options: dict[str, Any] = field(default_factory=dict)


def iter_markdown_files(root: Path) -> list[Path]:
    """Return all .md and .mdx files under root, sorted by path."""
    return sorted(
        path
        for path in root.rglob("*")
        if path.is_file() and path.suffix.lower() in {".md", ".mdx"}
    )


def extract_symbol_blocks_from_mdx(
    text: str, front_matter: dict[str, Any]
) -> list[SymbolBlock]:
    """Scan MDX body for ClassSummary/ClassMembers/ClassAll JSX tags and return SymbolBlock entries.

    Symbol names may be literal (name="Foo") or resolved from front matter
    (name={frontMatter.key}).
    """
    blocks: list[SymbolBlock] = []
    for match in COMPONENT_TAG_RE.finditer(text):
        component = match.group(1)
        attrs = match.group(2)
        symbol = None
        options: dict[str, Any] = {}
        name_match = re.search(r'name="([^"]+)"', attrs)
        if name_match:
            symbol = name_match.group(1)
        else:
            fm_match = re.search(r"name=\{frontMatter\.([a-zA-Z0-9_]+)\}", attrs)
            if fm_match:
                raw = front_matter.get(fm_match.group(1))
                if isinstance(raw, str):
                    symbol = raw
        if re.search(r"showRootHeading=\{true\}", attrs):
            options["showRootHeading"] = True
        kind = {
            "ClassSummary": "class_summary",
            "ClassMembers": "class_members",
            "ClassAll": "class_all_options",
        }[component]
        blocks.append(SymbolBlock(kind=kind, symbol=symbol, options=options))
    return blocks


def parse_document(text: str) -> FrontMatterDocument:
    """Parse a Markdown/MDX document string into a FrontMatterDocument with data and body."""
    return parse_front_matter(text)
