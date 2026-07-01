"""SQLite helpers for the MCP server."""

import importlib.resources
from pathlib import Path


def get_db_path() -> Path:
    """Return filesystem path to the bundled mcp.db."""
    ref = importlib.resources.files("flet_mcp").joinpath("data/mcp.db")
    # For installed packages, this returns a real path
    return Path(str(ref))


def snippet(text: str, query: str, length: int = 200) -> str:
    """Extract a snippet around the first match of query tokens in text."""
    if not text or not query:
        return text[:length] if text else ""

    query_tokens = query.lower().split()
    text_lower = text.lower()

    # Find the earliest match position
    best_pos = len(text)
    for token in query_tokens:
        pos = text_lower.find(token)
        if pos != -1 and pos < best_pos:
            best_pos = pos

    if best_pos == len(text):
        return text[:length]

    # Center snippet around match
    start = max(0, best_pos - length // 4)
    end = min(len(text), start + length)

    result = text[start:end]
    if start > 0:
        result = "..." + result
    if end < len(text):
        result = result + "..."

    return result
