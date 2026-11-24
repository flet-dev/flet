"""Refresh the Material icon search metadata (data/icons.json).

Google publishes the search metadata that powers fonts.google.com/icons —
per icon: human synonym `tags` ("remove" carries minus/negative/delete…),
`categories`, and `popularity`. We transform it into the keyword map
`IconStore` consumes, keyed by the UPPER_SNAKE names used by flet's
`Icons` enum. Apache-2.0, same as the icon set itself.

Unlike api.json, `data/icons.json` is a *committed* package file (it
changes only when Google ships new icons), so the regular MCP build
stays network-free. Refresh it explicitly with:

    uv run python -m flet_mcp.build.icons

Cupertino icons have no published tag metadata; they are searched by
name tokens only (a curated/LLM-generated tag pass is a possible
follow-up).
"""

from __future__ import annotations

import json
import logging
import urllib.request
from pathlib import Path

logger = logging.getLogger(__name__)

METADATA_URL = "https://fonts.google.com/metadata/icons"

# The endpoint prefixes its JSON with an anti-XSSI guard line.
_XSSI_GUARD = ")]}'"

_DATA_PATH = Path(__file__).resolve().parent.parent / "data" / "icons.json"


def fetch_metadata() -> dict:
    with urllib.request.urlopen(METADATA_URL, timeout=30) as resp:
        text = resp.read().decode("utf-8")
    if text.startswith(_XSSI_GUARD):
        text = text[len(_XSSI_GUARD) :]
    return json.loads(text)


def build_icons(output_path: Path = _DATA_PATH) -> dict:
    """Fetch Google's icon metadata and write icons.json:
    {"material": {NAME: {"tags": [...], "popularity": N}}}."""
    meta = fetch_metadata()
    material: dict[str, dict] = {}
    for icon in meta.get("icons", []):
        name = str(icon.get("name", "")).upper()
        if not name:
            continue
        tags = sorted(
            {str(t).strip().lower() for t in icon.get("tags", []) if str(t).strip()}
        )
        material[name] = {
            "tags": tags,
            "popularity": int(icon.get("popularity", 0)),
        }
    # Trailing newline keeps the end-of-file pre-commit hook happy on
    # regeneration.
    output_path.write_text(
        json.dumps({"material": material}, ensure_ascii=False, indent=1) + "\n",
        encoding="utf-8",
    )
    logger.info("Wrote %d material icon entries to %s", len(material), output_path)
    return {"icons": len(material)}


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    stats = build_icons()
    print(f"icons.json refreshed: {stats['icons']} material icons tagged")
