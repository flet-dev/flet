import json
import os
import sqlite3
from typing import Optional, Union

from fastmcp import FastMCP

from flet_mcp.api_store import ApiStore, render_text
from flet_mcp.db import get_db_path
from flet_mcp.icons_store import IconStore


def _enabled(name: str, default: str = "0") -> bool:
    return os.getenv(f"FLET_MCP_ENABLE_{name}", default).lower() in ("1", "true", "yes")


# Tool groups can be toggled at server startup via FLET_MCP_ENABLE_*.
# Defaults focus on the hallucination-reduction starter set (API + icons).
_API_ON = _enabled("API", default="1")
_ICONS_ON = _enabled("ICONS", default="1")
_EXAMPLES_ON = _enabled("EXAMPLES", default="0")
_DOCS_ON = _enabled("DOCS", default="0")
_CLI_ON = _enabled("CLI", default="0")

# Single-response size budgets (chars). Tool output lands in the calling
# agent's conversation history where it is re-sent (and re-billed) on every
# subsequent LLM call, so oversized payloads are paged/truncated with a
# drill-down hint instead of returned whole. The largest bundled example is
# ~111k chars; doc sections are unbounded.
_EXAMPLE_CHARS_BUDGET = 24_000
_DOC_CHARS_BUDGET = 12_000


_enabled_groups = [
    name
    for name, on in (
        ("API", _API_ON),
        ("icons", _ICONS_ON),
        ("examples", _EXAMPLES_ON),
        ("docs", _DOCS_ON),
        ("CLI", _CLI_ON),
    )
    if on
]


mcp = FastMCP(
    "flet-mcp",
    instructions=(
        "Flet MCP server provides tools for building Flet applications. "
        f"Enabled tool groups in this session: {', '.join(_enabled_groups) or 'none'}. "
        "When you have a class name in mind (any control, service, dataclass, "
        "or event), call get_api(name) first — it is the cheapest verifier and "
        "a 'not found' result is definitive. Methods marked `\"async\": true` "
        "in the response must be awaited; the calling event handler must be "
        '`async def`. The response also carries a `"package"` field — if it '
        'is anything other than `"flet"`, that pip package must be added to '
        "the consuming project before the import will resolve. Use "
        "list_controls only to browse, and enum tools for enum lookups. If "
        "examples or docs tools are enabled, search first and retrieve full "
        "content with the matching get_* tool. Other groups can be toggled "
        "via FLET_MCP_ENABLE_{API,ICONS,EXAMPLES,DOCS,CLI}=1."
    ),
)

_api_store: Optional[ApiStore] = None
_icon_store: Optional[IconStore] = None


def _get_api_store() -> ApiStore:
    global _api_store
    if _api_store is None:
        _api_store = ApiStore()
    return _api_store


def _get_icon_store() -> IconStore:
    global _icon_store
    if _icon_store is None:
        # Icon names come from the bundled api.json enums, not the flet
        # package — flet is not installed on runtime-only consumers.
        # Synonym tags/popularity come from the committed data/icons.json
        # (Google's icon search metadata); absent, search degrades to
        # name tokens only.
        import importlib.resources

        api = _get_api_store()
        meta: dict = {}
        try:
            ref = importlib.resources.files("flet_mcp").joinpath("data/icons.json")
            meta = json.loads(ref.read_text(encoding="utf-8")).get("material", {})
        except (FileNotFoundError, json.JSONDecodeError):
            pass
        _icon_store = IconStore(
            material=api.enum_member_names("Icons"),
            cupertino=api.enum_member_names("CupertinoIcons"),
            material_meta=meta,
        )
    return _icon_store


def _get_db() -> sqlite3.Connection:
    db_path = get_db_path()
    conn = sqlite3.connect(f"file:{db_path}?mode=ro", uri=True)
    conn.row_factory = sqlite3.Row
    return conn


# ── Examples ──────────────────────────────────────────────────────────────


if _EXAMPLES_ON:

    @mcp.tool()
    def search_examples(
        query: str, platform: Optional[str] = None, limit: int = 5
    ) -> list[dict]:
        """Search Flet example projects by keyword.

        Returns a ranked list of examples with id, title, description, and snippet.
        Use get_example() to retrieve full source code.

        Args:
            query: Search keywords (e.g. "counter", "form validation", "navigation").
            platform: Optional platform filter (web, ios, android, macos, windows,
                linux).
            limit: Maximum number of results to return.
        """
        conn = _get_db()
        try:
            table_check = conn.execute(
                "SELECT name FROM sqlite_master "
                "WHERE type='table' AND name='examples_fts'"
            ).fetchone()
            if not table_check:
                return []

            # BM25 weights: title=8, description=5, tags=4, controls=5,
            # layout_pattern=6, features=4, search_text=2, code=1
            rows = conn.execute(
                """
                SELECT e.id, e.location, e.metadata,
                       snippet(examples_fts, 6, '**', '**', '...', 40) AS snip,
                       bm25(
                           examples_fts,
                           8.0, 5.0, 4.0, 5.0, 6.0, 4.0, 2.0, 1.0
                       ) AS rank
                FROM examples_fts
                JOIN examples e ON examples_fts.rowid = e.rowid
                WHERE examples_fts MATCH ?
                ORDER BY rank
                LIMIT ?
                """,
                (query, limit),
            ).fetchall()

            results = []
            for row in rows:
                meta = json.loads(row["metadata"])
                if platform and platform.lower() not in [
                    p.lower() for p in meta.get("platforms", [])
                ]:
                    continue
                results.append(
                    {
                        "id": row["id"],
                        "title": meta.get("title", ""),
                        "description": meta.get("description", ""),
                        "controls": meta.get("controls", []),
                        "complexity": meta.get("complexity", ""),
                        "snippet": row["snip"] or "",
                    }
                )
            return results
        finally:
            conn.close()

    @mcp.tool()
    def get_example(example_id: str, filename: Optional[str] = None) -> dict:
        """Get full source code and metadata for a specific example.

        Small examples are returned whole. For large multi-file examples the
        response lists every file with its size but inlines contents only up
        to a budget — fetch the remaining files one at a time via `filename`.

        Args:
            example_id: The example ID returned by search_examples().
            filename: Optional single file to fetch in full.
        """
        conn = _get_db()
        try:
            table_check = conn.execute(
                "SELECT name FROM sqlite_master WHERE type='table' AND name='examples'"
            ).fetchone()
            if not table_check:
                return {"error": "No examples indexed"}

            row = conn.execute(
                "SELECT id, location, metadata FROM examples WHERE id = ?",
                (example_id,),
            ).fetchone()
            if not row:
                return {"error": f"Example '{example_id}' not found"}

            files = conn.execute(
                "SELECT filename, content FROM example_files WHERE example_id = ?",
                (example_id,),
            ).fetchall()

            if filename is not None:
                for f in files:
                    if f["filename"] == filename:
                        return {
                            "id": row["id"],
                            "filename": filename,
                            "content": f["content"],
                        }
                return {
                    "error": f"Example '{example_id}' has no file '{filename}'",
                    "available_files": [f["filename"] for f in files],
                }

            meta = json.loads(row["metadata"])
            contents: dict[str, str] = {}
            omitted: list[str] = []
            budget = _EXAMPLE_CHARS_BUDGET
            for f in files:
                content = f["content"]
                if len(content) <= budget:
                    contents[f["filename"]] = content
                    budget -= len(content)
                else:
                    omitted.append(f["filename"])
            result = {
                "id": row["id"],
                "location": row["location"],
                **meta,
                "file_sizes": {f["filename"]: len(f["content"]) for f in files},
                "files": contents,
            }
            if omitted:
                result["note"] = (
                    "Large example — contents omitted for "
                    f"{omitted}; call get_example({example_id!r}, "
                    "filename=<name>) to fetch each in full."
                )
            return result
        finally:
            conn.close()


# ── Documentation ─────────────────────────────────────────────────────────


if _DOCS_ON:

    @mcp.tool()
    def search_docs(query: str, limit: int = 5) -> list[dict]:
        """Search Flet documentation by keyword.

        Returns ranked results with title, location, and snippet.
        Use get_doc() to retrieve full content.

        Args:
            query: Search keywords (e.g. "TextField validation", "routing", "theme").
            limit: Maximum number of results to return.
        """
        conn = _get_db()
        try:
            table_check = conn.execute(
                "SELECT name FROM sqlite_master WHERE type='table' AND name='docs_fts'"
            ).fetchone()
            if not table_check:
                return []

            # BM25 weights: title=6, location_text=4, content=1
            rows = conn.execute(
                """
                SELECT d.location, d.title,
                       snippet(docs_fts, 2, '**', '**', '...', 40) AS snip,
                       bm25(docs_fts, 6.0, 4.0, 1.0) AS rank
                FROM docs_fts
                JOIN docs d ON docs_fts.rowid = d.rowid
                WHERE docs_fts MATCH ?
                ORDER BY rank
                LIMIT ?
                """,
                (query, limit),
            ).fetchall()

            return [
                {
                    "title": row["title"],
                    "location": row["location"],
                    "snippet": row["snip"] or "",
                }
                for row in rows
            ]
        finally:
            conn.close()

    @mcp.tool()
    def get_doc(location: str) -> dict:
        """Get full content of a documentation section by its location path.

        Args:
            location: The location path returned by search_docs()
                (e.g. "controls/textfield/", "controls/textfield/#validation").
        """
        conn = _get_db()
        try:
            table_check = conn.execute(
                "SELECT name FROM sqlite_master WHERE type='table' AND name='docs'"
            ).fetchone()
            if not table_check:
                return {"error": "No docs indexed"}

            row = conn.execute(
                "SELECT location, title, content FROM docs WHERE location = ?",
                (location,),
            ).fetchone()
            if not row:
                return {"error": f"Document '{location}' not found"}
            content = row["content"]
            result = {
                "location": row["location"],
                "title": row["title"],
                "content": content[:_DOC_CHARS_BUDGET],
            }
            if len(content) > _DOC_CHARS_BUDGET:
                result["note"] = (
                    f"Truncated at {_DOC_CHARS_BUDGET:,} of {len(content):,} "
                    "chars — search_docs() with a narrower query to land on a "
                    "more specific section (e.g. a '#fragment' location)."
                )
            return result
        finally:
            conn.close()


# ── API Reference ─────────────────────────────────────────────────────────


if _API_ON:

    @mcp.tool()
    def list_controls(
        category: Optional[str] = None,
        kind: Optional[str] = None,
        limit: int = 50,
    ) -> list[dict]:
        """List available Flet controls and services.

        Args:
            category: Optional category filter (e.g. "input", "layout", "navigation").
            kind: Optional kind filter - "control" for visual controls,
                "service" for non-visual services (Audio, FilePicker, sensors, etc.).
            limit: Maximum number of results to return.
        """
        store = _get_api_store()
        return store.list_controls(category=category, kind=kind, limit=limit)

    @mcp.tool()
    def get_api(
        name: str,
        member: Optional[str] = None,
        query: Optional[str] = None,
        format: str = "text",
    ) -> Union[str, dict]:
        """Get the API reference for any Flet symbol by name.

        Looks across visual controls, non-visual services, dataclass types
        (ButtonStyle, Padding, TextStyle, Border, Theme, ColorScheme, ...),
        event classes, and enums (MainAxisAlignment, TextAlign, Icons, ...).

        This is the primary verification tool — when you have a name in mind,
        call this first. A "not found" response is a definitive negative: the
        name does not exist in this Flet version.

        The default response is compact text, one line per member:

            Page (control) — High-level root control for an app view.
            bases: AdaptiveControl
            properties:
              bgcolor: ColorValue? — Background color of the page.
              multi_views: list[MultiView] = [] — The list of multi-views...
            events:
              on_route_change(RouteChangeEvent) — Called when route changes.
            methods:
              async push_route(route, kwargs) -> None — Pushes a new route...

        Layout conventions:
        * `(control)` / `(service)` / `(type)` / `(event)` / `(enum)` after
          the symbol name says which bucket matched.
        * `?` suffix on a property type = optional (may be None).
        * `on_x(SomeEvent)` — the handler receives a `SomeEvent` argument.
        * `async ` prefix — the method must be awaited (so the event handler
          calling it must be `async def`).
        * A `package: <name>` line means the class lives in that pip package,
          which must be added to the project's dependencies before importing
          it — surface this to the user. No line = core `flet`, always
          available.
        * `DEPRECATED: <reason>` — do not use; pick the replacement named in
          the reason.
        * Member docstrings are trimmed to their first sentence; the `note:`
          line reminds you how to drill down.

        Drill-down / filtering:
        * `member="push_route"` — one member's full, untrimmed docstring and
          exact type.
        * `query="border"` — only members whose name contains the substring
          (case-insensitive). `member` wins if both are passed.
        * A few names are shared by multiple classes (e.g. the Text control
          vs the canvas Text shape) — the primary one is returned and the
          `note:` line lists the others with a dotted name that selects
          them, e.g. `get_api("canvas.Text")`.
        * Neither applies to enums — use search_enum_members /
          enum_has_member / find_icon there. Large enums (Icons,
          CupertinoIcons) are always truncated to a sample.

        Errors are returned as JSON objects (`{"error": ...}`), sometimes
        with `available_members`/`available_files` hints.

        Args:
            name: Symbol name (e.g. "Button", "Window", "AlertDialog", "Audio",
                "ButtonStyle", "TapEvent", "MainAxisAlignment", "Icons").
            member: Optional property/event/method name (e.g. "on_scroll",
                "push_route") to fetch with its full, untrimmed docstring.
            query: Optional case-insensitive substring to filter member names.
            format: "text" (default, compact) or "json" (structured dicts,
                full raw type strings; for programmatic consumers).
        """
        store = _get_api_store()
        result = store.get(name, member=member, query=query)
        if result is None:
            return {"error": f"'{name}' not found"}
        if "error" in result or format == "json":
            return result
        return render_text(result)

    @mcp.tool()
    def get_enum(name: str) -> dict:
        """Get enum definition.

        For small enums (< 50 members), returns all members.
        For large enums (Icons, CupertinoIcons), returns metadata and sample members.
        Use search_enum_members() for large enum lookup.

        Args:
            name: Enum class name (e.g. "TextAlign", "Icons", "CupertinoIcons").
        """
        store = _get_api_store()
        result = store.get_enum(name)
        if result is None:
            return {"error": f"Enum '{name}' not found"}
        return result

    @mcp.tool()
    def search_enum_members(name: str, query: str, limit: int = 10) -> dict:
        """Search enum members by name substring (ranked: exact, prefix,
        then substring matches).

        For finding an *icon by concept* ("delete", "user", "back")
        prefer find_icon — it is synonym-aware. This tool matches member
        names literally, which suits other large enums and verifying
        specific icon names. Material style variants
        (_OUTLINED/_ROUNDED/_SHARP) are collapsed into their base icon;
        append a suffix to any base name to use a variant.

        Args:
            name: Enum class name (e.g. "Icons", "CupertinoIcons").
            query: Search pattern (e.g. "arrow", "settings", "home").
            limit: Maximum number of results to return.
        """
        store = _get_api_store()
        members = store.search_enum_members(name, query, limit=limit)
        return {"enum": name, "matches": members}

    @mcp.tool()
    def enum_has_member(name: str, member: str) -> dict:
        """Check if an enum has a specific member.

        Use this to verify that an enum value exists before using it in code.

        Args:
            name: Enum class name (e.g. "Icons", "TextAlign").
            member: Member name to check (e.g. "ARROW_BACK", "CENTER").
        """
        store = _get_api_store()
        return {
            "enum": name,
            "member": member,
            "exists": store.enum_has_member(name, member),
        }


# ── Icons ─────────────────────────────────────────────────────────────────


if _ICONS_ON:

    @mcp.tool()
    def find_icon(query: str, family: Optional[str] = None, limit: int = 10) -> dict:
        """Search Material and Cupertino icons by keyword.

        Supports synonym matching (e.g. "user" finds "account_circle").

        Args:
            query: Descriptive keywords (e.g. "back arrow", "settings", "user profile").
            family: Optional icon family filter - "material" or "cupertino".
            limit: Maximum number of results to return.
        """
        store = _get_icon_store()
        return {"icons": store.find(query, family=family, limit=limit)}


# ── CLI Help ──────────────────────────────────────────────────────────────


if _CLI_ON:

    @mcp.tool()
    def get_cli_help(command: Optional[str] = None) -> dict:
        """Get Flet CLI usage and options.

        Without arguments, returns an overview of all available commands.
        With a command name, returns detailed flags and options.

        Args:
            command: Optional command name (e.g. "run", "build", "publish", "create").
        """
        store = _get_api_store()
        result = store.get_cli_help(command)
        if command is None:
            return {"commands": result}
        if result is None:
            return {"error": f"Unknown command: {command}"}
        return result
