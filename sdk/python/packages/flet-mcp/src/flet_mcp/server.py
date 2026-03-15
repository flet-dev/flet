import json
import sqlite3
from typing import Optional

from fastmcp import FastMCP

from flet_mcp.api_store import ApiStore
from flet_mcp.db import get_db_path
from flet_mcp.icons_store import IconStore

mcp = FastMCP(
    "flet-mcp",
    instructions=(
        "Flet MCP server provides tools to search examples, documentation, "
        "and API reference for building Flet applications. "
        "Use search tools first to discover relevant content, "
        "then use get tools to retrieve full details."
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
        _icon_store = IconStore()
    return _icon_store


def _get_db() -> sqlite3.Connection:
    db_path = get_db_path()
    conn = sqlite3.connect(f"file:{db_path}?mode=ro", uri=True)
    conn.row_factory = sqlite3.Row
    return conn


# ── Examples ──────────────────────────────────────────────────────────────


@mcp.tool()
def search_examples(
    query: str, platform: Optional[str] = None, limit: int = 5
) -> list[dict]:
    """Search Flet example projects by keyword.

    Returns a ranked list of examples with id, title, description, and snippet.
    Use get_example() to retrieve full source code.

    Args:
        query: Search keywords (e.g. "counter", "form validation", "navigation").
        platform: Optional platform filter (web, ios, android, macos, windows, linux).
        limit: Maximum number of results to return.
    """
    conn = _get_db()
    try:
        # Check if examples table exists
        table_check = conn.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name='examples_fts'"
        ).fetchone()
        if not table_check:
            return []

        # BM25 weights: title=8, description=5, tags=4, controls=5,
        # layout_pattern=6, features=4, search_text=2, code=1
        rows = conn.execute(
            """
            SELECT e.id, e.location, e.metadata,
                   snippet(examples_fts, 6, '**', '**', '...', 40) AS snip,
                   bm25(examples_fts, 8.0, 5.0, 4.0, 5.0, 6.0, 4.0, 2.0, 1.0) AS rank
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
def get_example(example_id: str) -> dict:
    """Get full source code and metadata for a specific example.

    Args:
        example_id: The example ID returned by search_examples().
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

        meta = json.loads(row["metadata"])
        return {
            "id": row["id"],
            "location": row["location"],
            **meta,
            "files": {f["filename"]: f["content"] for f in files},
        }
    finally:
        conn.close()


# ── Documentation ─────────────────────────────────────────────────────────


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
        row = conn.execute(
            "SELECT location, title, content FROM docs WHERE location = ?",
            (location,),
        ).fetchone()
        if not row:
            return {"error": f"Document '{location}' not found"}
        return {
            "location": row["location"],
            "title": row["title"],
            "content": row["content"],
        }
    finally:
        conn.close()


# ── API Reference ─────────────────────────────────────────────────────────


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
def get_control_api(name: str) -> dict:
    """Get detailed API reference for a specific control or service.

    Returns properties (with types and docstrings), events, and methods
    (with argument signatures). The response includes a 'kind' field
    indicating whether it's a visual "control" or a non-visual "service".

    Args:
        name: Control or service class name (e.g. "TextField", "FilePicker", "Audio").
    """
    store = _get_api_store()
    result = store.get_control(name)
    if result is None:
        return {"error": f"Control or service '{name}' not found"}
    return result


@mcp.tool()
def get_type_api(name: str) -> dict:
    """Get API reference for a non-control type (dataclass).

    Returns fields, class methods, and factory methods for types like
    ButtonStyle, TextStyle, Padding, Border, Theme, ColorScheme, etc.

    Args:
        name: Type class name (e.g. "ButtonStyle", "Padding", "TextStyle").
    """
    store = _get_api_store()
    result = store.get_type(name)
    if result is None:
        return {"error": f"Type '{name}' not found"}
    return result


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


# ── Enum Search ───────────────────────────────────────────────────────────


@mcp.tool()
def search_enum_members(name: str, query: str, limit: int = 10) -> dict:
    """Search enum members by name pattern.

    Useful for large enums like Icons and CupertinoIcons.

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
