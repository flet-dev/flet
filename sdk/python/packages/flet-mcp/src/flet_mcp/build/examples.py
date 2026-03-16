"""Examples indexer. Walks a directory tree looking for pyproject.toml files
with [tool.flet.metadata] and indexes them into an SQLite database."""

from __future__ import annotations

import json
import logging
import re
import sqlite3
import sys
from pathlib import Path

if sys.version_info >= (3, 11):
    import tomllib
else:
    import tomli as tomllib

logger = logging.getLogger(__name__)

_CODE_EXTENSIONS = {".py", ".toml"}
_TEXT_EXTENSIONS = {".py", ".toml", ".md", ".txt"}


def _create_tables(conn: sqlite3.Connection) -> None:
    conn.executescript(
        """
        CREATE TABLE IF NOT EXISTS examples (
            id TEXT PRIMARY KEY,
            location TEXT,
            metadata TEXT
        );
        CREATE TABLE IF NOT EXISTS example_files (
            example_id TEXT,
            filename TEXT,
            content TEXT,
            FOREIGN KEY (example_id) REFERENCES examples(id)
        );
        CREATE VIRTUAL TABLE IF NOT EXISTS examples_fts USING fts5(
            title, description, tags, controls,
            layout_pattern, features, search_text, code,
            tokenize='porter unicode61'
        );
        """
    )


def _derive_id(relative_path: Path) -> str:
    return re.sub(r"[\\/]", "_", str(relative_path))


def _read_text_files(directory: Path) -> dict[str, str]:
    """Read all indexable text files in *directory* (non-recursive)."""
    files: dict[str, str] = {}
    for p in sorted(directory.iterdir()):
        if p.is_file() and p.suffix in _TEXT_EXTENSIONS:
            try:
                files[p.name] = p.read_text(encoding="utf-8", errors="replace")
            except OSError as exc:
                logger.warning("Cannot read %s: %s", p, exc)
    return files


def index_examples(conn: sqlite3.Connection, examples_dir: Path) -> int:
    """Index Flet example projects found under *examples_dir*.

    Returns the number of examples indexed.
    """
    _create_tables(conn)

    count = 0
    for pyproject_path in sorted(examples_dir.rglob("pyproject.toml")):
        try:
            with open(pyproject_path, "rb") as f:
                data = tomllib.load(f)
        except Exception as exc:
            logger.warning("Failed to parse %s: %s", pyproject_path, exc)
            continue

        flet_meta = data.get("tool", {}).get("flet", {}).get("metadata")
        if flet_meta is None:
            continue

        project = data.get("project", {})
        project_dir = pyproject_path.parent
        relative = project_dir.relative_to(examples_dir)

        example_id = _derive_id(relative)
        location = str(relative)
        title = flet_meta.get("title") or project.get("name", example_id)
        description = project.get("description", "")
        tags: list[str] = project.get("keywords", [])
        platforms: list[str] = (
            data.get("tool", {})
            .get("flet", {})
            .get("platforms", ["web", "ios", "android", "macos", "windows", "linux"])
        )
        controls: list[str] = flet_meta.get("controls", [])
        layout: str = flet_meta.get("layout_pattern", "")
        complexity: str = flet_meta.get("complexity", "basic")
        features: list[str] = flet_meta.get("features", [])

        # ---- read files in the example directory ----
        text_files = _read_text_files(project_dir)

        # ---- build search_text ----
        search_text = (
            f"{title}\n\n"
            f"{description}\n\n"
            f"tags: {', '.join(tags)}\n"
            f"platforms: {', '.join(platforms)}\n"
            f"controls: {', '.join(controls)}\n"
            f"complexity: {complexity}\n"
            f"layout_pattern: {layout}\n"
            f"features: {', '.join(features)}"
        )

        # ---- build code blob ----
        code_parts: list[str] = []
        for fname, content in text_files.items():
            if Path(fname).suffix in _CODE_EXTENSIONS:
                code_parts.append(content)
        code = "\n\n".join(code_parts)

        # ---- metadata JSON ----
        metadata = json.dumps(
            {
                "title": title,
                "description": description,
                "tags": tags,
                "platforms": platforms,
                "controls": controls,
                "layout_pattern": layout,
                "complexity": complexity,
                "features": features,
            }
        )

        # ---- insert rows ----
        conn.execute(
            "INSERT OR REPLACE INTO examples (id, location, metadata) VALUES (?, ?, ?)",
            (example_id, location, metadata),
        )

        for fname, content in text_files.items():
            conn.execute(
                "INSERT INTO example_files "
                "(example_id, filename, content) VALUES (?, ?, ?)",
                (example_id, fname, content),
            )

        conn.execute(
            "INSERT INTO examples_fts "
            "(title, description, tags, controls, "
            "layout_pattern, features, search_text, code) "
            "VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            (
                title,
                description,
                ", ".join(tags),
                ", ".join(controls),
                layout,
                ", ".join(features),
                search_text,
                code,
            ),
        )

        count += 1
        logger.debug("Indexed example %s (%s)", example_id, title)

    conn.commit()
    return count
