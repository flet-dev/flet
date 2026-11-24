"""Docs indexer. Parses search_index.json produced by mkdocs and indexes
the entries into an SQLite FTS5 database."""

from __future__ import annotations

import json
import logging
import re
import sqlite3
from pathlib import Path

from markdownify import markdownify

logger = logging.getLogger(__name__)

_HTML_TAG_RE = re.compile(r"<[^>]+>")
_WHITESPACE_RE = re.compile(r"\s{3,}")
_LOCATION_SPLIT_RE = re.compile(r"[/\-_\.#]")
# mkdocstrings labels like <code>class-attribute</code>, <code>instance-attribute</code>
_MKDOCS_LABEL_RE = re.compile(
    r"\s*<code>(?:class-attribute|instance-attribute|property|cached-property|"
    r"writable|static-method|class-method|module-attribute)</code>",
    re.IGNORECASE,
)


def _create_tables(conn: sqlite3.Connection) -> None:
    conn.executescript(
        """
        CREATE TABLE IF NOT EXISTS docs (
            location TEXT PRIMARY KEY,
            location_text TEXT,
            title TEXT,
            content TEXT
        );
        CREATE VIRTUAL TABLE IF NOT EXISTS docs_fts USING fts5(
            title, location_text, content,
            tokenize='porter unicode61'
        );
        """
    )


def _html_to_markdown(html: str) -> str:
    """Convert HTML to markdown and clean up."""
    md = markdownify(html, strip=["img"])
    md = _HTML_TAG_RE.sub("", md)
    md = _WHITESPACE_RE.sub("\n\n", md)
    return md.strip()


def _strip_html(text: str) -> str:
    text = _MKDOCS_LABEL_RE.sub("", text)
    return _HTML_TAG_RE.sub("", text).strip()


def _location_to_text(location: str) -> str:
    """Turn a location string into a space-separated searchable string.

    Example:
        "ads/bannerad/#flet_ads.banner_ad.BannerAd.on_paid"
        -> "ads bannerad flet_ads banner_ad BannerAd on_paid"
    """
    parts = _LOCATION_SPLIT_RE.split(location)
    return " ".join(p for p in parts if p)


def index_docs(conn: sqlite3.Connection, search_index_path: Path) -> int:
    """Index mkdocs search_index.json into *conn*.

    Returns the number of doc entries indexed.
    """
    _create_tables(conn)

    raw = json.loads(search_index_path.read_text(encoding="utf-8"))
    entries: list[dict] = raw.get("docs", [])

    count = 0
    root_title: str = ""
    section_title: str = ""
    for entry in entries:
        location: str = entry.get("location", "")
        title: str = entry.get("title", "")
        text: str = entry.get("text", "")

        has_anchor = "#" in location
        clean_title = _strip_html(title)

        # ---- new page (no anchor) ----
        if not has_anchor:
            root_title = clean_title
            section_title = ""
            if not text:
                continue

        # ---- empty-text anchor = section group heading ----
        if has_anchor and not text:
            anchor = location.split("#", 1)[1] if "#" in location else ""
            # Only track well-known API doc section groups as intermediate titles
            if anchor.endswith(("-properties", "-methods", "-events")):
                section_title = clean_title
            else:
                # Reset section title — this is a peer heading, not a group
                section_title = ""
            continue

        # ---- entry with content: build composite title ----
        parts = [root_title]
        if section_title:
            parts.append(section_title)
        parts.append(clean_title)
        composite_title = " - ".join(parts)

        # ---- process content ----
        location_text = _location_to_text(location)
        content = _html_to_markdown(text)

        # ---- insert ----
        conn.execute(
            "INSERT OR REPLACE INTO docs (location, location_text, title, content) "
            "VALUES (?, ?, ?, ?)",
            (location, location_text, composite_title, content),
        )
        conn.execute(
            "INSERT INTO docs_fts (title, location_text, content) VALUES (?, ?, ?)",
            (composite_title, location_text, content),
        )

        count += 1

    conn.commit()
    return count
