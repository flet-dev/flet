"""Minimal front matter parsing helpers."""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Any


@dataclass
class FrontMatterDocument:
    data: dict[str, Any]
    body: str


_FRONT_MATTER_RE = re.compile(r"\A---\n(.*?)\n---\n?", re.DOTALL)


def _parse_scalar(value: str) -> Any:
    value = value.strip()
    if value == "":
        return ""
    if value.lower() == "true":
        return True
    if value.lower() == "false":
        return False
    if value.lower() == "null":
        return None
    if (value.startswith('"') and value.endswith('"')) or (
        value.startswith("'") and value.endswith("'")
    ):
        return value[1:-1]
    try:
        return int(value)
    except ValueError:
        pass
    return value


def parse_front_matter(text: str) -> FrontMatterDocument:
    match = _FRONT_MATTER_RE.match(text)
    if not match:
        return FrontMatterDocument(data={}, body=text)

    raw = match.group(1).splitlines()
    data: dict[str, Any] = {}
    current_list_key: str | None = None

    for line in raw:
        if not line.strip():
            continue
        if line.startswith("  - ") and current_list_key is not None:
            value = _parse_scalar(line[4:])
            data.setdefault(current_list_key, []).append(value)
            continue
        current_list_key = None
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        key = key.strip()
        if value.strip() == "":
            data[key] = []
            current_list_key = key
        else:
            data[key] = _parse_scalar(value)

    body = text[match.end() :]
    return FrontMatterDocument(data=data, body=body)
