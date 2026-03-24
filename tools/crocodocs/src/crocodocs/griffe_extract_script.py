"""Extract API data using Griffe inside the sdk/python environment."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any


def _normalize_path(value: str | None) -> str | None:
    if value is None:
        return None
    return str(value).replace("\\", "/")


MEMBER_FILTERS: dict[str, set[str]] = {
    "all": set(),
    "properties": set(),
    "events": set(),
    "methods": set(),
}


def _load_member_filters(payload: dict[str, Any]) -> None:
    raw = payload.get("member_filters", {})
    for key in MEMBER_FILTERS:
        values = raw.get(key, [])
        MEMBER_FILTERS[key] = {str(value) for value in values}


def _resolve_extensions(
    extensions: list[str],
    search_paths: list[str],
) -> list[str]:
    resolved: list[str] = []
    for extension in extensions:
        if extension == "flet.utils.griffe_deprecations":
            file_path = None
            for search_path in search_paths:
                candidate = (
                    Path(search_path) / "flet" / "utils" / "griffe_deprecations.py"
                )
                if candidate.exists():
                    file_path = candidate
                    break
            if file_path is not None:
                resolved.append(str(file_path))
                continue
        resolved.append(extension)
    return resolved


def _is_filtered_member(kind: str, name: str) -> bool:
    return name in MEMBER_FILTERS["all"] or name in MEMBER_FILTERS.get(kind, set())


def _unwrap(obj: Any) -> Any:
    target = obj
    seen: set[int] = set()
    while target.__class__.__name__ == "Alias" and id(target) not in seen:
        seen.add(id(target))
        try:
            target = target.target
        except Exception:
            return None
    return target


def _docstring_value(obj: Any) -> str | None:
    docstring = getattr(obj, "docstring", None)
    if docstring is None:
        return None
    return docstring.value or None


def _annotation_to_text(value: Any) -> str | None:
    if value is None:
        return None
    return str(value)


def _parameter_lookup(obj: Any) -> dict[str, Any]:
    target = _unwrap(obj)
    if target is None:
        return {}
    parameters = getattr(target, "parameters", []) or []
    return {parameter.name: parameter for parameter in parameters}


def _docstring_sections(obj: Any) -> list[dict[str, Any]]:
    try:
        from griffe import (
            DocstringSectionAdmonition,
            DocstringSectionParameters,
            DocstringSectionRaises,
            DocstringSectionReturns,
            DocstringSectionText,
        )
    except Exception:  # pragma: no cover
        return []

    docstring = getattr(obj, "docstring", None)
    if docstring is None:
        return []

    parameter_lookup = _parameter_lookup(obj)
    sections: list[dict[str, Any]] = []
    for section in docstring.parsed:
        if isinstance(section, DocstringSectionText):
            value = getattr(section, "value", None)
            if isinstance(value, str) and value.strip():
                sections.append({"kind": "text", "value": value})
        elif isinstance(section, DocstringSectionParameters):
            items = []
            for item in getattr(section, "value", []) or []:
                parameter = parameter_lookup.get(getattr(item, "name", ""))
                default = getattr(item, "value", None)
                if default is None and parameter is not None:
                    default = getattr(parameter, "default", None)
                items.append(
                    {
                        "name": getattr(item, "name", "") or "",
                        "type": _annotation_to_text(
                            getattr(item, "annotation", None)
                            or getattr(parameter, "annotation", None)
                            if parameter
                            else None
                        ),
                        "default": _annotation_to_text(default),
                        "description": getattr(item, "description", None) or None,
                    }
                )
            if items:
                sections.append({"kind": "parameters", "items": items})
        elif isinstance(section, DocstringSectionReturns):
            items = []
            for item in getattr(section, "value", []) or []:
                items.append(
                    {
                        "name": getattr(item, "name", "") or "",
                        "type": _annotation_to_text(getattr(item, "annotation", None)),
                        "description": getattr(item, "description", None) or None,
                    }
                )
            if items:
                sections.append({"kind": "returns", "items": items})
        elif isinstance(section, DocstringSectionRaises):
            items = []
            for item in getattr(section, "value", []) or []:
                items.append(
                    {
                        "type": _annotation_to_text(getattr(item, "annotation", None)),
                        "description": getattr(item, "description", None) or None,
                    }
                )
            if items:
                sections.append({"kind": "raises", "items": items})
        elif isinstance(section, DocstringSectionAdmonition):
            admonition = getattr(section, "value", None)
            if admonition is not None:
                kind = getattr(admonition, "annotation", "note") or "note"
                description = getattr(admonition, "description", "") or ""
                title = getattr(section, "title", None)
                if description.strip():
                    entry: dict[str, Any] = {
                        "kind": "admonition",
                        "admonition_kind": kind,
                        "value": description,
                    }
                    if title:
                        entry["title"] = title
                    sections.append(entry)
    return sections


def _deprecation_value(obj: Any) -> str | None:
    try:
        from griffe import DocstringSectionAdmonition
    except Exception:  # pragma: no cover
        return None

    docstring = getattr(obj, "docstring", None)
    if docstring is None:
        return None
    for section in docstring.parsed:
        if (
            isinstance(section, DocstringSectionAdmonition)
            and section.title == "Deprecated"
        ):
            value = getattr(section, "value", None)
            text = getattr(value, "contents", None) or getattr(
                value, "description", None
            )
            if isinstance(text, str) and text.strip():
                return text
    return None


def _labels(obj: Any) -> list[str]:
    target = _unwrap(obj)
    if target is None:
        return []
    return sorted(str(label) for label in getattr(target, "labels", set()))


def _annotation_text(obj: Any) -> str | None:
    target = _unwrap(obj)
    if target is None:
        return None
    annotation = getattr(target, "annotation", None)
    if annotation is None:
        return None
    return str(annotation)


def _value_text(obj: Any) -> str | None:
    target = _unwrap(obj)
    if target is None:
        return None
    value = getattr(target, "value", None)
    if value is None:
        return None
    return str(value)


def _bases_text(obj: Any) -> list[str]:
    target = _unwrap(obj)
    if target is None:
        return []
    return [str(base) for base in getattr(target, "bases", [])]


def _parameter_text(parameter: Any) -> str:
    prefix = ""
    kind = str(getattr(parameter, "kind", ""))
    if "keyword_variadic" in kind or "var_keyword" in kind:
        prefix = "**"
    elif "variadic" in kind or "var_positional" in kind:
        prefix = "*"

    text = prefix + parameter.name
    if getattr(parameter, "annotation", None) is not None:
        text += f": {parameter.annotation}"
    if getattr(parameter, "default", None) is not None:
        text += f" = {parameter.default}"
    return text


def _signature_text(obj: Any) -> str:
    target = _unwrap(obj)
    if target is None:
        return obj.name
    parameters = getattr(target, "parameters", [])
    rendered = ", ".join(_parameter_text(parameter) for parameter in parameters)
    return f"{obj.name}({rendered})"


def _attribute_entry(obj: Any) -> dict[str, Any]:
    target = _unwrap(obj)
    if target is None:
        return {
            "name": obj.name,
            "qualname": getattr(obj, "path", None),
            "canonical_path": None,
            "type": None,
            "default": None,
            "docstring": _docstring_value(obj),
            "docstring_sections": _docstring_sections(obj),
            "deprecation": _deprecation_value(obj),
            "labels": [],
            "inherited_from": None,
            "lineno": None,
        }
    return {
        "name": obj.name,
        "qualname": getattr(obj, "path", None),
        "canonical_path": getattr(target, "path", None),
        "type": _annotation_text(obj),
        "default": _value_text(obj),
        "docstring": _docstring_value(obj),
        "docstring_sections": _docstring_sections(obj),
        "deprecation": _deprecation_value(obj),
        "labels": _labels(obj),
        "inherited_from": None,
        "lineno": getattr(target, "lineno", None),
    }


def _function_entry(obj: Any) -> dict[str, Any]:
    target = _unwrap(obj)
    if target is None:
        return {
            "name": obj.name,
            "qualname": getattr(obj, "path", None),
            "canonical_path": None,
            "signature": obj.name,
            "docstring": _docstring_value(obj),
            "docstring_sections": _docstring_sections(obj),
            "parameters": [],
            "return_type": None,
            "deprecation": _deprecation_value(obj),
            "labels": [],
            "lineno": None,
        }
    returns = getattr(target, "returns", None)
    return {
        "name": obj.name,
        "qualname": getattr(obj, "path", None),
        "canonical_path": getattr(target, "path", None),
        "signature": _signature_text(obj),
        "docstring": _docstring_value(obj),
        "docstring_sections": _docstring_sections(obj),
        "parameters": [
            parameter.name for parameter in getattr(target, "parameters", [])
        ],
        "return_type": str(returns) if returns is not None else None,
        "deprecation": _deprecation_value(obj),
        "labels": _labels(obj),
        "lineno": getattr(target, "lineno", None),
    }


def _class_entry(obj: Any) -> dict[str, Any]:
    target = _unwrap(obj)
    if target is None:
        return {
            "name": obj.name,
            "qualname": getattr(obj, "path", None),
            "canonical_path": None,
            "docstring": _docstring_value(obj),
            "bases": [],
            "deprecation": _deprecation_value(obj),
            "labels": [],
            "properties": [],
            "events": [],
            "methods": [],
            "lineno": None,
        }
    properties: list[dict[str, Any]] = []
    events: list[dict[str, Any]] = []
    methods: list[dict[str, Any]] = []

    members = getattr(obj, "members", None) or getattr(target, "members", {})
    for member in members.values():
        resolved = _unwrap(member)
        if resolved is None:
            continue
        member_type = resolved.__class__.__name__
        if member_type == "Attribute":
            item = _attribute_entry(member)
            if item["name"].startswith("on_"):
                if _is_filtered_member("events", item["name"]):
                    continue
                events.append(item)
            elif not item["name"].startswith("_"):
                if _is_filtered_member("properties", item["name"]):
                    continue
                properties.append(item)
        elif member_type == "Function" and not member.name.startswith("_"):
            if _is_filtered_member("methods", member.name):
                continue
            methods.append(_function_entry(member))

    properties.sort(key=lambda item: item["name"].casefold())
    events.sort(key=lambda item: item["name"].casefold())
    methods.sort(key=lambda item: item["name"].casefold())

    return {
        "name": obj.name,
        "qualname": getattr(obj, "path", None),
        "canonical_path": getattr(target, "path", None),
        "docstring": _docstring_value(obj),
        "bases": _bases_text(obj),
        "deprecation": _deprecation_value(obj),
        "labels": _labels(obj),
        "properties": properties,
        "events": events,
        "methods": methods,
        "lineno": getattr(target, "lineno", None),
    }


def _alias_entry(obj: Any) -> dict[str, Any]:
    target = _unwrap(obj)
    target_kind = target.__class__.__name__ if target is not None else None
    return {
        "name": obj.name,
        "qualname": getattr(obj, "path", None),
        "canonical_path": getattr(target, "path", None) if target else None,
        "docstring": _docstring_value(obj),
        "docstring_sections": _docstring_sections(obj),
        "value": _value_text(obj),
        "target_kind": target_kind,
        "deprecation": _deprecation_value(obj),
        "labels": _labels(obj),
        "lineno": getattr(target, "lineno", None) if target else None,
    }


def main() -> int:
    payload = json.loads(sys.stdin.read())
    _load_member_filters(payload)

    from griffe import GriffeLoader, load_extensions

    search_paths = sorted({_normalize_path(path) for path in payload["search_paths"]})
    extensions = _resolve_extensions(payload["extensions"], search_paths)
    loader = GriffeLoader(
        search_paths=search_paths,
        extensions=load_extensions(*extensions),
        docstring_parser="google",
    )

    classes: dict[str, Any] = {}
    functions: dict[str, Any] = {}
    aliases: dict[str, Any] = {}
    public_aliases: dict[str, str] = {}

    for package_name in payload["packages"]:
        module = loader.load(package_name)
        for member_name, member in module.members.items():
            resolved = _unwrap(member)
            if resolved is None:
                continue
            kind = resolved.__class__.__name__
            if kind in {"Class", "Function"}:
                public_aliases[
                    getattr(member, "path", f"{package_name}.{member_name}")
                ] = getattr(resolved, "path", getattr(member, "path", ""))

    modules_collection = loader.modules_collection
    for symbol in payload["symbols"]:
        try:
            obj = modules_collection.get_member(symbol)
        except Exception:
            continue
        obj_kind = obj.__class__.__name__
        resolved = _unwrap(obj)
        if resolved is None:
            continue
        kind = resolved.__class__.__name__
        if obj_kind == "Alias":
            aliases[symbol] = _alias_entry(obj)
            if kind == "Class":
                classes[symbol] = _class_entry(obj)
            elif kind == "Function":
                functions[symbol] = _function_entry(obj)
        elif kind == "Class":
            classes[symbol] = _class_entry(obj)
        elif kind == "Function":
            functions[symbol] = _function_entry(obj)

    sys.stdout.write(
        json.dumps(
            {
                "aliases": aliases,
                "classes": classes,
                "functions": functions,
                "public_aliases": public_aliases,
            },
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
