"""API reference builder using Griffe.

Scans Flet packages with Griffe to extract controls, events, types, enums,
and CLI help, then writes a consolidated api.json file.
"""

from __future__ import annotations

import json
import logging
from pathlib import Path
from typing import Any

import griffe

logger = logging.getLogger(__name__)

DEFAULT_PACKAGES: list[str] = [
    "flet",
    "flet_ads",
    "flet_audio",
    "flet_audio_recorder",
    "flet_camera",
    "flet_charts",
    "flet_code_editor",
    "flet_color_pickers",
    "flet_datatable2",
    "flet_flashlight",
    "flet_geolocator",
    "flet_lottie",
    "flet_map",
    "flet_permission_handler",
    "flet_rive",
    "flet_secure_storage",
    "flet_video",
    "flet_webview",
]

_CONTROL_BASE_NAMES = {"BaseControl", "LayoutControl", "AdaptiveControl", "Service"}


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _first_line(docstring: griffe.Docstring | None) -> str:
    if docstring is None:
        return ""
    text = docstring.value.strip()
    return text.split("\n", 1)[0].strip()


def _full_docstring(docstring: griffe.Docstring | None) -> str:
    if docstring is None:
        return ""
    return docstring.value.strip()


def _annotation_str(annotation: Any) -> str:
    if annotation is None:
        return ""
    return str(annotation)


def _default_str(default: Any) -> str:
    if default is None:
        return ""
    return str(default)


def _is_control_class(cls: griffe.Class) -> bool:
    """Check if any base class name matches a known control base."""
    for base in cls.bases:
        base_name = str(base).rsplit(".", 1)[-1]
        if base_name in _CONTROL_BASE_NAMES:
            return True
    return False


def _is_service(cls: griffe.Class) -> bool:
    return any("Service" in str(base) for base in cls.bases)


def _is_enum(cls: griffe.Class) -> bool:
    for base in cls.bases:
        base_name = str(base).rsplit(".", 1)[-1]
        if base_name == "Enum" or base_name.endswith("Enum"):
            return True
    return False


def _is_event_class(cls: griffe.Class) -> bool:
    return any("Event" in str(base).rsplit(".", 1)[-1] for base in cls.bases)


def _is_dataclass(cls: griffe.Class) -> bool:
    for dec in cls.decorators:
        dec_str = str(dec.value)
        if "dataclass" in dec_str:
            return True
    return False


def _has_control_decorator(cls: griffe.Class) -> tuple[list[str], list[str]]:
    """Return (categories, tags) from @control decorator if present."""
    categories: list[str] = []
    tags: list[str] = []
    for dec in cls.decorators:
        dec_str = str(dec.value)
        if "control" not in dec_str:
            continue
        # Try to extract keyword args from the decorator's AST node
        try:
            node = dec.value
            # Griffe stores decorator values as Expressions or AST nodes
            if hasattr(node, "keywords"):
                for kw in node.keywords:
                    if kw.arg == "categories" and hasattr(kw.value, "elts"):
                        categories = [
                            str(getattr(e, "value", e)) for e in kw.value.elts
                        ]
                    elif kw.arg == "tags" and hasattr(kw.value, "elts"):
                        tags = [str(getattr(e, "value", e)) for e in kw.value.elts]
        except Exception:
            pass
        # Fallback: parse from string representation
        if not categories and "categories=" in dec_str:
            categories = _parse_tuple_from_str(dec_str, "categories")
        if not tags and "tags=" in dec_str:
            tags = _parse_tuple_from_str(dec_str, "tags")
    return categories, tags


def _parse_tuple_from_str(dec_str: str, key: str) -> list[str]:
    """Parse a keyword arg tuple from decorator string representation.

    e.g. 'control("TextField", categories=("input", "form"))' -> ["input", "form"]
    """
    import re

    pattern = rf"{key}\s*=\s*\(([^)]*)\)"
    match = re.search(pattern, dec_str)
    if not match:
        return []
    inner = match.group(1)
    return [s.strip().strip("\"'") for s in inner.split(",") if s.strip().strip("\"'")]


def _extract_properties(cls: griffe.Class) -> list[dict[str, Any]]:
    """Extract dataclass-style fields as properties."""
    props: list[dict[str, Any]] = []
    for name, member in cls.members.items():
        if name.startswith("_"):
            continue
        if isinstance(member, griffe.Attribute):
            annotation = _annotation_str(member.annotation)
            is_event = (
                "EventHandler" in annotation or "ControlEventHandler" in annotation
            )
            props.append(
                {
                    "name": name,
                    "type": annotation,
                    "default": _default_str(member.value),
                    "docstring": _full_docstring(member.docstring),
                    "is_event": is_event,
                }
            )
    return props


def _extract_methods(cls: griffe.Class) -> list[dict[str, Any]]:
    """Extract public methods."""
    methods: list[dict[str, Any]] = []
    for name, member in cls.members.items():
        if name.startswith("_"):
            continue
        if isinstance(member, griffe.Function):
            args = []
            for param in member.parameters:
                if param.name == "self":
                    continue
                args.append(
                    {
                        "name": param.name,
                        "type": _annotation_str(param.annotation),
                        "default": _default_str(param.default),
                    }
                )
            methods.append(
                {
                    "name": name,
                    "args": args,
                    "return_type": _annotation_str(member.annotation),
                    "docstring": _full_docstring(member.docstring),
                }
            )
    return methods


def _extract_enum_members(cls: griffe.Class) -> list[dict[str, str]]:
    members: list[dict[str, str]] = []
    for name, member in cls.members.items():
        if name.startswith("_"):
            continue
        if isinstance(member, griffe.Attribute):
            entry: dict[str, str] = {"name": name, "value": _default_str(member.value)}
            doc = _full_docstring(member.docstring)
            if doc:
                entry["docstring"] = doc
            members.append(entry)
    return members


# ---------------------------------------------------------------------------
# Module walker
# ---------------------------------------------------------------------------


def _walk_module(
    module: griffe.Module,
    controls: list[dict],
    events: list[dict],
    types: list[dict],
    enums: list[dict],
) -> None:
    """Recursively walk a griffe Module and classify its members."""
    for name, obj in module.members.items():
        if isinstance(obj, griffe.Module):
            _walk_module(obj, controls, events, types, enums)

        elif isinstance(obj, griffe.Class):
            try:
                if _is_enum(obj):
                    members = _extract_enum_members(obj)
                    entry: dict[str, Any] = {
                        "name": obj.name,
                        "module": obj.canonical_path.rsplit(".", 1)[0],
                        "docstring": _full_docstring(obj.docstring),
                        "members": members,
                    }
                    if len(members) > 50:
                        entry["kind"] = "large_enum"
                    enums.append(entry)

                elif _is_control_class(obj):
                    categories, tags = _has_control_decorator(obj)
                    props = _extract_properties(obj)
                    event_fields = [p for p in props if p.get("is_event")]
                    regular_props = [p for p in props if not p.get("is_event")]
                    # Remove is_event flag from output
                    for p in regular_props:
                        p.pop("is_event", None)
                    for e in event_fields:
                        e.pop("is_event", None)

                    kind = "service" if _is_service(obj) else "control"
                    controls.append(
                        {
                            "name": obj.name,
                            "module": obj.canonical_path.rsplit(".", 1)[0],
                            "kind": kind,
                            "summary": _first_line(obj.docstring),
                            "bases": [str(b) for b in obj.bases],
                            "categories": categories,
                            "tags": tags,
                            "properties": regular_props,
                            "events": event_fields,
                            "methods": _extract_methods(obj),
                        }
                    )

                elif _is_event_class(obj):
                    fields = _extract_properties(obj)
                    for f in fields:
                        f.pop("is_event", None)
                    events.append(
                        {
                            "name": obj.name,
                            "module": obj.canonical_path.rsplit(".", 1)[0],
                            "docstring": _full_docstring(obj.docstring),
                            "fields": fields,
                        }
                    )

                elif _is_dataclass(obj):
                    fields = _extract_properties(obj)
                    for f in fields:
                        f.pop("is_event", None)
                    class_methods = []
                    for mname, member in obj.members.items():
                        if mname.startswith("_"):
                            continue
                        if isinstance(member, griffe.Function) and (
                            "classmethod" in member.labels
                            or "staticmethod" in member.labels
                        ):
                            args = []
                            for param in member.parameters:
                                if param.name in ("self", "cls"):
                                    continue
                                args.append(
                                    {
                                        "name": param.name,
                                        "type": _annotation_str(param.annotation),
                                        "default": _default_str(param.default),
                                    }
                                )
                            class_methods.append(
                                {
                                    "name": mname,
                                    "args": args,
                                    "return_type": _annotation_str(member.annotation),
                                    "docstring": _full_docstring(member.docstring),
                                }
                            )
                    types.append(
                        {
                            "name": obj.name,
                            "module": obj.canonical_path.rsplit(".", 1)[0],
                            "docstring": _full_docstring(obj.docstring),
                            "fields": fields,
                            "methods": class_methods,
                        }
                    )
            except Exception as exc:
                logger.warning("Error processing class %s: %s", name, exc)


# ---------------------------------------------------------------------------
# CLI help extraction
# ---------------------------------------------------------------------------


def _extract_cli_help() -> dict[str, Any]:
    """Try to extract structured CLI help from flet_cli."""
    import argparse as _argparse

    cli_help: dict[str, Any] = {}

    def _parse_parser(parser: _argparse.ArgumentParser) -> dict[str, Any]:
        """Extract structured option data from an ArgumentParser."""
        options: list[dict[str, Any]] = []
        for action in parser._actions:
            if isinstance(action, _argparse._HelpAction):
                continue
            if isinstance(action, _argparse._SubParsersAction):
                continue

            opt: dict[str, Any] = {}

            if action.option_strings:
                opt["name"] = action.option_strings[-1]  # --long form
                if len(action.option_strings) > 1:
                    opt["alias"] = action.option_strings[0]  # -short form
            else:
                opt["name"] = action.dest
                opt["positional"] = True

            # Type
            if isinstance(
                action, (_argparse._StoreTrueAction, _argparse._StoreFalseAction)
            ):
                opt["type"] = "bool"
            elif isinstance(action, _argparse._CountAction):
                opt["type"] = "count"
            elif action.type is not None:
                opt["type"] = action.type.__name__
            else:
                opt["type"] = "str"

            if action.nargs in ("*", "+"):
                opt["multiple"] = True

            if action.default is not None and action.default != _argparse.SUPPRESS:
                opt["default"] = action.default

            if action.required:
                opt["required"] = True

            if action.choices:
                opt["choices"] = list(action.choices)

            if action.help and action.help != _argparse.SUPPRESS:
                opt["help"] = action.help

            options.append(opt)

        result: dict[str, Any] = {"options": options}
        if parser.description:
            result["description"] = parser.description
        return result

    try:
        from flet_cli.cli import get_parser

        parser = get_parser()
        cli_help["flet"] = _parse_parser(parser)
        for action in parser._subparsers._actions:
            if hasattr(action, "choices") and action.choices:
                for cmd_name, cmd_parser in action.choices.items():
                    try:
                        cmd_data = _parse_parser(cmd_parser)
                        if cmd_parser.description:
                            cmd_data["description"] = cmd_parser.description
                        cli_help[cmd_name] = cmd_data
                    except Exception:
                        pass
    except Exception as exc:
        logger.warning("Could not extract CLI help: %s", exc)
    return cli_help


# ---------------------------------------------------------------------------
# Icon enum injection
# ---------------------------------------------------------------------------


def _inject_icon_enums(enums: list[dict]) -> None:
    """Add Icons and CupertinoIcons as large_enum entries from JSON files."""
    try:
        import importlib.resources

        material_path = (
            importlib.resources.files("flet") / "controls" / "material" / "icons.json"
        )
        cupertino_path = (
            importlib.resources.files("flet")
            / "controls"
            / "cupertino"
            / "cupertino_icons.json"
        )

        with importlib.resources.as_file(material_path) as p:
            material_icons: dict[str, int] = json.loads(p.read_text("utf-8"))
        with importlib.resources.as_file(cupertino_path) as p:
            cupertino_icons: dict[str, int] = json.loads(p.read_text("utf-8"))

        enums.append(
            {
                "name": "Icons",
                "module": "flet.controls.material.icons",
                "docstring": "Material Design icon constants.",
                "kind": "large_enum",
                "members": [
                    {"name": name, "value": str(val)}
                    for name, val in material_icons.items()
                ],
            }
        )
        enums.append(
            {
                "name": "CupertinoIcons",
                "module": "flet.controls.cupertino.cupertino_icons",
                "docstring": "Cupertino (iOS-style) icon constants.",
                "kind": "large_enum",
                "members": [
                    {"name": name, "value": str(val)}
                    for name, val in cupertino_icons.items()
                ],
            }
        )
        logger.info(
            "Injected Icons (%d members) and CupertinoIcons (%d members)",
            len(material_icons),
            len(cupertino_icons),
        )
    except Exception as exc:
        logger.warning("Could not inject icon enums: %s", exc)


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------


def build_api(output_path: Path, packages: list[str] | None = None) -> dict[str, Any]:
    """Build the API reference JSON from installed Flet packages.

    Parameters:
        output_path: Where to write the resulting api.json.
        packages: List of package names to scan. Defaults to all known Flet packages.

    Returns:
        A stats dict with counts per category.
    """
    if packages is None:
        packages = DEFAULT_PACKAGES

    controls: list[dict] = []
    events: list[dict] = []
    types: list[dict] = []
    enums: list[dict] = []

    for pkg in packages:
        try:
            module = griffe.load(pkg)
        except Exception as exc:
            logger.warning("Failed to load package %s: %s", pkg, exc)
            continue
        _walk_module(module, controls, events, types, enums)

    # Inject Icons and CupertinoIcons from JSON files (not Python Enums)
    _inject_icon_enums(enums)

    cli_help = _extract_cli_help()

    api_data: dict[str, Any] = {
        "controls": controls,
        "events": events,
        "types": types,
        "enums": enums,
        "cli": cli_help,
    }

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(api_data, indent=2), encoding="utf-8")

    stats = {
        "controls": len(controls),
        "events": len(events),
        "types": len(types),
        "enums": len(enums),
        "cli_commands": len(cli_help),
    }
    logger.info("API build stats: %s", stats)
    return stats
