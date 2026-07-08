"""Load and query the Griffe-generated API reference (api.json)."""

from __future__ import annotations

import importlib.resources
import json
import re
from pathlib import Path
from typing import Any

# Member docstrings are trimmed to their first sentence in listings (full
# docstrings often embed multi-paragraph examples — Page's methods alone
# carry ~9k chars of doc text). The full text stays reachable per member
# via `get(name, member=...)`.
_SUMMARY_MAX_CHARS = 160

# Controls use properties/events/methods; dataclass types and event
# classes keep their members under "fields" (same entry shape).
_MEMBER_SECTIONS = ("properties", "fields", "events", "methods")

_MEMBER_KIND = {
    "properties": "property",
    "fields": "field",
    "events": "event",
    "methods": "method",
}

# Buckets in preference order for ambiguous names, and the `kind` value
# stamped onto entries from buckets that don't carry their own.
_BUCKET_RANK = {"controls": 0, "types": 1, "events": 2, "enums": 3}
_BUCKET_KIND = {"types": "type", "events": "event"}

# Sphinx roles in docstrings (":attr:`style`", ":class:`~flet.Text`") are
# docs-site markup — render them as plain backticked names.
_RST_ROLE = re.compile(r":\w+(?::\w+)?:`~?([^`]+)`")

# Material icon style-variant suffixes: collapsed in member search so
# ADD / ADD_OUTLINED / ADD_ROUNDED / ADD_SHARP don't spend four result
# slots on one icon.
_STYLE_SUFFIXES = ("_OUTLINED", "_ROUNDED", "_SHARP")


def clean_rst(text: str) -> str:
    return _RST_ROLE.sub(r"`\1`", text)


def first_sentence(text: str, limit: int = _SUMMARY_MAX_CHARS) -> str:
    """First sentence (or line) of a docstring, capped at `limit` chars."""
    if not text:
        return text
    text = clean_rst(text)
    head = text.split("\n\n", 1)[0].split("\n", 1)[0]
    dot = head.find(". ")
    if dot != -1:
        head = head[: dot + 1]
    if len(head) > limit:
        head = head[: limit - 1].rstrip() + "…"
    return head


def _compact_member(entry: dict[str, Any]) -> dict[str, Any]:
    doc = entry.get("docstring")
    if not doc:
        return entry
    summary = first_sentence(doc)
    if summary == doc:
        return entry
    return {**entry, "docstring": summary}


# ── Text rendering ──────────────────────────────────────────────────────
#
# The default `get_api` response is signature-style text, not JSON: one
# line per member. Same information, ~44% fewer chars and far fewer
# tokens than the JSON encoding (keys/quoting repeat per member).
# `format="json"` on the tool returns the dict shape instead.


def _optional_inner(type_str: str) -> str | None:
    """`Optional[X]` -> `X`, else None."""
    if type_str.startswith("Optional[") and type_str.endswith("]"):
        return type_str[len("Optional[") : -1]
    return None


def _event_payload(type_str: str) -> str | None:
    """The event object type a handler receives, or None if the type
    string doesn't match the known handler shapes (caller falls back to
    the raw string — never guess):

    * `Optional[ControlEventHandler[X]]`        -> `ControlEvent`
    * `Optional[EventHandler[XEvent]]`          -> `XEvent`
    * `Optional[EventHandler[XEvent[Subject]]]` -> `XEvent`
    """
    s = _optional_inner(type_str) or type_str
    wrapper, bracket, rest = s.partition("[")
    if not bracket or not rest.endswith("]"):
        return None
    wrapper = wrapper.removeprefix("ft.")
    inner = rest[:-1]
    if wrapper == "ControlEventHandler":
        return "ControlEvent"
    if wrapper == "EventHandler":
        return inner.split("[", 1)[0]
    return None


def _fmt_default(default: Any) -> str | None:
    if default in (None, "None", ""):
        return None
    text = str(default)
    # Unwrap dataclass `field(...)` declarations — the metadata is
    # serialization plumbing, only the actual default value informs.
    if text.startswith("field("):
        if m := re.search(r"default_factory=(\w+)", text):
            factory = m.group(1)
            return {"list": "[]", "dict": "{}"}.get(factory, f"{factory}()")
        if m := re.search(r"default=([^,)]+)", text):
            return _fmt_default(m.group(1).strip())
        return None
    return text


def _member_line(section: str, entry: dict[str, Any]) -> str:
    """One text line for a property/event/method entry (docstring already
    compacted by `_compact_member`)."""
    name = entry.get("name", "")
    if section == "methods":
        params = ", ".join(p.get("name", "") for p in entry.get("params") or [])
        sig = f"{name}({params})"
        ret = entry.get("return_type")
        if ret:
            sig += f" -> {ret}"
        if entry.get("async"):
            sig = "async " + sig
    elif section == "events":
        payload = _event_payload(entry.get("type", ""))
        sig = f"{name}({payload})" if payload else f"{name}: {entry.get('type', '')}"
    else:
        type_str = entry.get("type", "")
        inner = _optional_inner(type_str)
        sig = f"{name}: {inner}?" if inner else f"{name}: {type_str}"
        default = _fmt_default(entry.get("default"))
        if default:
            sig += f" = {default}"
    dep = entry.get("deprecated")
    if dep:
        reason = dep.get("reason") if isinstance(dep, dict) else str(dep)
        sig += f" [DEPRECATED: {reason}]"
    doc = entry.get("docstring")
    if doc:
        sig += f" — {doc}"
    return sig


def render_text(hit: dict[str, Any]) -> str:
    """Render a `get()` result as signature-style text (see the `get_api`
    tool docstring for the layout conventions the model relies on)."""
    name = hit.get("name", "")

    # Single-member drill-down (`get_api(name, member=...)`).
    if "member" in hit and "member_kind" in hit:
        entry = hit["member"]
        section = next(
            (s for s, k in _MEMBER_KIND.items() if k == hit["member_kind"]),
            "properties",
        )
        lines = [f"{name}.{entry.get('name')} ({hit['member_kind']})"]
        lines.append(_member_line(section, {**entry, "docstring": None}))
        if entry.get("type"):
            lines.append(f"type: {entry['type']}")
        if entry.get("docstring"):
            lines.append(clean_rst(entry["docstring"]))
        return "\n".join(lines)

    lines = []
    header = f"{name} ({hit.get('kind', '')})"
    summary = hit.get("summary") or first_sentence(hit.get("docstring") or "")
    if summary:
        header += f" — {clean_rst(summary)}"
    lines.append(header)
    dep = hit.get("deprecated")
    if dep:
        reason = dep.get("reason") if isinstance(dep, dict) else str(dep)
        lines.append(f"DEPRECATED: {reason}")
    pkg = hit.get("package")
    if pkg and pkg != "flet":
        lines.append(f"package: {pkg} (add this pip package to the project)")
    if hit.get("bases"):
        lines.append("bases: " + ", ".join(hit["bases"]))
    if hit.get("note"):
        lines.append(f"note: {hit['note']}")

    if hit.get("kind") == "large_enum":
        lines.append(f"total members: {hit.get('total_members')}")
        samples = [
            m.get("name") if isinstance(m, dict) else str(m)
            for m in hit.get("sample_members") or []
        ]
        lines.append("sample members: " + ", ".join(samples))
    elif hit.get("members") is not None:
        lines.append("members:")
        for m in hit.get("members") or []:
            if isinstance(m, dict):
                line = f"  {m.get('name')} = {m.get('value')}"
                if m.get("docstring"):
                    line += f" — {first_sentence(m['docstring'])}"
                lines.append(line)
            else:
                lines.append(f"  {m}")

    for section in _MEMBER_SECTIONS:
        entries = hit.get(section)
        if not entries:
            continue
        lines.append(f"{section}:")
        for entry in entries:
            lines.append("  " + _member_line(section, entry))

    # Inherited matches from a query= base-class walk.
    for block in hit.get("inherited") or []:
        lines.append(f"from {block.get('from')}:")
        for section in _MEMBER_SECTIONS:
            for entry in block.get(section) or []:
                lines.append("  " + _member_line(section, entry))
    return "\n".join(lines)


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
        self._by_name: dict[str, list[tuple[str, dict]]] | None = None

    def _load(self) -> dict[str, Any]:
        if self._raw is None:
            ref = importlib.resources.files("flet_mcp").joinpath("data/api.json")
            self._raw = json.loads(Path(str(ref)).read_text(encoding="utf-8"))
            # Build name-keyed dicts from lists
            self._controls = {c["name"]: c for c in self._raw.get("controls", [])}
            self._events = {e["name"]: e for e in self._raw.get("events", [])}
            self._types = {t["name"]: t for t in self._raw.get("types", [])}
            self._enums = {e["name"]: e for e in self._raw.get("enums", [])}
            # Names are NOT unique across (or even within) buckets — e.g.
            # the Text control vs the canvas Text shape. Keep every entry
            # per name so `get` can rank candidates instead of letting the
            # last dict insert silently win.
            self._by_name = {}
            for bucket in ("controls", "types", "events", "enums"):
                for e in self._raw.get(bucket, []):
                    self._by_name.setdefault(e["name"], []).append((bucket, e))
        return self._raw

    def _candidates(self, name: str) -> list[tuple[str, dict[str, Any]]]:
        """Entries matching `name`, best first. A dotted name
        ("canvas.Text", "flet_map.Camera") filters candidates by module
        segment, so shadowed symbols stay reachable. Preference for bare
        names: non-canvas modules first (the canvas shapes namespace
        shadows core controls like Text/Image), then bucket order."""
        self._load()
        if name in self._by_name:
            cands = self._by_name[name]
        elif "." in name:
            prefix, cls = name.rsplit(".", 1)
            cands = [
                (b, e)
                for (b, e) in self._by_name.get(cls, [])
                if f".{prefix}." in f".{e.get('module') or ''}."
            ]
        else:
            return []

        def rank(item: tuple[str, dict[str, Any]]) -> tuple[bool, int]:
            bucket, entry = item
            in_canvas = ".canvas." in f".{entry.get('module') or ''}."
            return (in_canvas, _BUCKET_RANK[bucket])

        return sorted(cands, key=rank)

    @staticmethod
    def _qualified_hint(entry: dict[str, Any], name: str) -> str:
        """A dotted name that selects `entry` unambiguously in `get`."""
        parts = (entry.get("module") or "").split(".")
        if "canvas" in parts:
            return f"canvas.{name}"
        return f"{parts[0]}.{name}" if parts and parts[0] else name

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

    # ------------------------------------------------------------------
    # Unified lookup (controls/services/types/events)
    # ------------------------------------------------------------------

    def get(
        self,
        name: str,
        member: str | None = None,
        query: str | None = None,
    ) -> dict[str, Any] | None:
        """Look up `name` across controls, services, types, events, and enums.

        Every match carries a `kind` field — `"control"`, `"service"`, `"type"`,
        `"event"`, or `"enum"` (`"large_enum"` for Icons/CupertinoIcons) — so the
        caller can distinguish them without inspecting the response shape.
        Controls and services already carry `kind`; the other buckets are
        augmented here. Returns `None` only when the name matches nothing.

        Member docstrings (properties/events/methods) are trimmed to their
        first sentence. Pass `member` for one member's full entry, or `query`
        for a case-insensitive substring filter over member names (`member`
        wins if both are given). Enum responses use the same truncation as
        `get_enum` for large enums; `member`/`query` don't apply to enums —
        use search_enum_members / enum_has_member there.

        Names are not globally unique (e.g. the Text control vs the canvas
        Text shape): the best candidate wins and the response notes the
        alternatives, each reachable via a dotted name ("canvas.Text").
        """
        cands = self._candidates(name)
        if not cands:
            return None
        bucket, entry = cands[0]

        if bucket == "enums":
            if member is not None or query is not None:
                return {
                    "error": (
                        f"'{name}' is an enum — use search_enum_members or "
                        "enum_has_member to look up its members"
                    )
                }
            enum = self.get_enum(entry["name"])
            return {"kind": enum.get("kind", "enum"), **enum}

        hit = entry if bucket == "controls" else {"kind": _BUCKET_KIND[bucket], **entry}
        if member is not None:
            return self._get_member(hit, name, member)
        out = self._compact(hit)
        if query is not None:
            out = self._filter_members(out, name, query)
        if "error" not in out and len(cands) > 1:
            alternates = "; ".join(
                f"{e.get('module')}.{e.get('name')} — get_api"
                f"('{self._qualified_hint(e, e.get('name'))}')"
                for _, e in cands[1:]
            )
            combined = f"Other symbols share this name: {alternates}."
            if out.get("note"):
                combined += " " + out["note"]
            out = {**out, "note": combined}
            # Keep the note leading so it survives downstream capping.
            out = {"note": out.pop("note"), **out}
        return out

    def _filter_members(
        self, compacted: dict[str, Any], name: str, query: str
    ) -> dict[str, Any]:
        """Keep only members whose name contains `query` (case-insensitive).

        Base classes are searched too (transitively): api.json stores only
        a class's *own* members, so e.g. TextField's border properties live
        on FormFieldControl — without the walk, a query would return a
        misleading "no members" for members the control actually inherits.
        Inherited matches land under an `inherited` key, grouped by the
        defining class.
        """
        q = query.lower()

        def _matches(hit: dict[str, Any]) -> tuple[dict[str, list], int]:
            found: dict[str, list] = {}
            count = 0
            for section in _MEMBER_SECTIONS:
                kept = [
                    _compact_member(e)
                    for e in hit.get(section) or []
                    if q in e.get("name", "").lower()
                ]
                found[section] = kept
                count += len(kept)
            return found, count

        out = dict(compacted)
        own, matched = _matches(compacted)
        out.update(own)

        inherited: list[dict[str, Any]] = []
        visited: set[str] = set()
        queue = list(compacted.get("bases") or [])
        while queue:
            base_name = queue.pop(0)
            if base_name in visited:
                continue
            visited.add(base_name)
            base = self._controls.get(base_name) or self._types.get(base_name)
            if base is None:
                continue
            base_found, base_count = _matches(base)
            if base_count:
                inherited.append({"from": base_name, **base_found})
                matched += base_count
            queue.extend(base.get("bases") or [])
        if inherited:
            out["inherited"] = inherited

        if not matched:
            bases_hint = (
                f" (own and inherited via {', '.join(sorted(visited))})"
                if visited
                else ""
            )
            return {
                "error": (f"'{name}' has no members matching '{query}'{bases_hint}"),
                "available_members": [
                    e.get("name")
                    for section in _MEMBER_SECTIONS
                    for e in compacted.get(section) or []
                ],
            }
        out["note"] = (
            f"Showing only members matching '{query}' (including inherited). "
            f"Call get_api({name!r}) for the full listing."
        )
        return out

    def _compact(self, hit: dict[str, Any]) -> dict[str, Any]:
        """Trim member docstrings to their first sentence, with a note
        pointing at the per-member drill-down when anything was cut."""
        out = dict(hit)
        trimmed = False
        for section in _MEMBER_SECTIONS:
            entries = out.get(section)
            if not entries:
                continue
            compacted = [_compact_member(e) for e in entries]
            if any(c is not e for c, e in zip(compacted, entries)):
                trimmed = True
            out[section] = compacted
        if trimmed:
            # Lead with the note so it survives any downstream size capping
            # (agent frameworks may truncate the serialized result tail).
            note = (
                "Member docstrings are trimmed to their first sentence. "
                f"Call get_api({out.get('name')!r}, member=<name>) for one "
                "member's full docs and examples, or query=<substring> to "
                "list matching members only."
            )
            out = {"note": note, **out}
        return out

    def _get_member(
        self, hit: dict[str, Any], name: str, member: str
    ) -> dict[str, Any]:
        for section in _MEMBER_SECTIONS:
            for entry in hit.get(section) or []:
                if entry.get("name") == member:
                    return {
                        "name": name,
                        "kind": hit.get("kind"),
                        "member_kind": _MEMBER_KIND[section],
                        "member": entry,
                    }
        available = [
            e.get("name")
            for section in _MEMBER_SECTIONS
            for e in hit.get(section) or []
        ]
        return {
            "error": f"'{name}' has no member '{member}'",
            "available_members": available,
        }

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
                    f"This enum has {len(members)} members. Use find_icon() "
                    "to search icons by concept, or search_enum_members() "
                    "for literal name lookup."
                ),
            }

        return enum

    def search_enum_members(self, name: str, query: str, limit: int = 10) -> list[str]:
        """Search enum members by case-insensitive substring match.

        Ranked: exact match, then prefix matches, then substring matches
        (shortest/alphabetical within each tier) — so "remove" surfaces
        REMOVE before BOOKMARK_REMOVE. Material style variants
        (_OUTLINED/_ROUNDED/_SHARP) are collapsed into their base member
        when the base also matches, so they don't exhaust the limit.
        """
        self._load()
        enum = self._enums.get(name)
        if enum is None:
            return []

        q = query.lower()
        names = [
            m["name"] if isinstance(m, dict) else str(m)
            for m in enum.get("members", [])
        ]
        matched = [n for n in names if q in n.lower()]

        def tier(n: str) -> int:
            ln = n.lower()
            if ln == q:
                return 0
            return 1 if ln.startswith(q) else 2

        matched.sort(key=lambda n: (tier(n), len(n), n))
        present = set(matched)
        results: list[str] = []
        for n in matched:
            base = next((n[: -len(s)] for s in _STYLE_SUFFIXES if n.endswith(s)), None)
            if base and base in present:
                continue
            results.append(n)
            if len(results) >= limit:
                break
        return results

    def enum_member_names(self, name: str) -> list[str]:
        """All member names of an enum (untruncated — also for large
        enums). Used to seed the icon search index from bundled data."""
        self._load()
        enum = self._enums.get(name)
        if enum is None:
            return []
        return [
            m["name"] if isinstance(m, dict) else str(m)
            for m in enum.get("members", [])
        ]

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
