"""Load and query the Griffe-generated API reference (api.json)."""

from __future__ import annotations

import importlib.resources
import json
from pathlib import Path
from typing import Any


class ApiStore:
    """Lazy-loading store for the bundled api.json data.

    The api.json file uses lists for controls/events/types/enums,
    each entry having a "name" key. This store builds name-keyed dicts
    for fast lookup.
    """

    def __init__(self) -> None:
        self._raw: dict[str, Any] | None = None
        self._controls: dict[str, dict] | None = None
        self._events: dict[str, dict] | None = None
        self._types: dict[str, dict] | None = None
        self._enums: dict[str, dict] | None = None

    def _load(self) -> dict[str, Any]:
        if self._raw is None:
            ref = importlib.resources.files("flet_mcp").joinpath("data/api.json")
            self._raw = json.loads(Path(str(ref)).read_text(encoding="utf-8"))
            # Build name-keyed dicts from lists
            self._controls = {c["name"]: c for c in self._raw.get("controls", [])}
            self._events = {e["name"]: e for e in self._raw.get("events", [])}
            self._types = {t["name"]: t for t in self._raw.get("types", [])}
            self._enums = {e["name"]: e for e in self._raw.get("enums", [])}
        return self._raw

    # ------------------------------------------------------------------
    # Controls
    # ------------------------------------------------------------------

    def list_controls(
        self,
        category: str | None = None,
        kind: str | None = None,
        limit: int = 50,
    ) -> list[dict[str, Any]]:
        """List controls, optionally filtered by category or kind."""
        self._load()
        results: list[dict[str, Any]] = []
        for name, ctrl in self._controls.items():
            if kind and ctrl.get("kind") != kind:
                continue
            if category and category not in ctrl.get("categories", []):
                continue
            results.append(
                {
                    "name": name,
                    "kind": ctrl.get("kind"),
                    "summary": ctrl.get("summary", ""),
                    "categories": ctrl.get("categories", []),
                }
            )
            if len(results) >= limit:
                break
        return results

    def get_control(self, name: str) -> dict[str, Any] | None:
        """Return full control dict by name, or None."""
        self._load()
        return self._controls.get(name)

    # ------------------------------------------------------------------
    # Types & Events
    # ------------------------------------------------------------------

    def get_type(self, name: str) -> dict[str, Any] | None:
        """Return full type dict by name, or None."""
        self._load()
        return self._types.get(name) or self._events.get(name)

    # ------------------------------------------------------------------
    # Enums
    # ------------------------------------------------------------------

    def get_enum(self, name: str) -> dict[str, Any] | None:
        """Return enum data. Large enums are truncated with a hint to search."""
        self._load()
        enum = self._enums.get(name)
        if enum is None:
            return None

        if enum.get("kind") == "large_enum":
            members = enum.get("members", [])
            return {
                "name": name,
                "kind": "large_enum",
                "total_members": len(members),
                "sample_members": members[:10],
                "note": (
                    f"This enum has {len(members)} members. "
                    "Use search_enum_members() to find specific values."
                ),
            }

        return enum

    def search_enum_members(self, name: str, query: str, limit: int = 10) -> list[str]:
        """Search enum members by case-insensitive substring match."""
        self._load()
        enum = self._enums.get(name)
        if enum is None:
            return []

        query_lower = query.lower()
        results: list[str] = []
        for member in enum.get("members", []):
            member_name = member["name"] if isinstance(member, dict) else str(member)
            if query_lower in member_name.lower():
                results.append(member_name)
                if len(results) >= limit:
                    break
        return results

    def enum_has_member(self, name: str, member: str) -> bool:
        """Check whether an enum contains a specific member."""
        self._load()
        enum = self._enums.get(name)
        if enum is None:
            return False
        members = enum.get("members", [])
        member_lower = member.lower()
        return any(
            (m["name"] if isinstance(m, dict) else str(m)).lower() == member_lower
            for m in members
        )

    # ------------------------------------------------------------------
    # CLI
    # ------------------------------------------------------------------

    def get_cli_help(self, command: str | None = None) -> Any:
        """Return CLI help. None -> list commands; otherwise command help text."""
        self._load()
        cli = self._raw.get("cli", {})
        if command is None:
            return list(cli.keys())
        return cli.get(command)
