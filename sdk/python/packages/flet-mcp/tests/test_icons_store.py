"""Unit tests for IconStore: constructor takes plain name lists plus the
icons.json tag metadata (no flet package dependency), ranked
deterministic search, variant collapse, synonym tags, and a golden query
set against the committed Google metadata."""

import json
from pathlib import Path

import pytest

from flet_mcp.icons_store import IconStore

MATERIAL = [
    "ADD",
    "ADD_A_PHOTO",
    "ADD_A_PHOTO_OUTLINED",
    "ADD_BOX",
    "REMOVE",
    "REMOVE_OUTLINED",
    "REMOVE_ROUNDED",
    "GROUP_REMOVE",
    "DELETE",
]
CUPERTINO = ["ADD", "TRASH", "MINUS"]

META = {
    "ADD": {"tags": ["plus", "create", "new"], "popularity": 50000},
    "ADD_BOX": {"tags": ["plus"], "popularity": 900},
    "REMOVE": {"tags": ["minus", "negative", "delete"], "popularity": 20000},
    "DELETE": {"tags": ["trash", "bin", "garbage"], "popularity": 40000},
}

ICONS_JSON = (
    Path(__file__).resolve().parents[1] / "src" / "flet_mcp" / "data" / "icons.json"
)


def _store() -> IconStore:
    return IconStore(material=MATERIAL, cupertino=CUPERTINO, material_meta=META)


def test_exact_match_first_and_deterministic():
    out = _store().find("remove", limit=5)
    assert out[0] == "Icons.REMOVE"
    assert out == _store().find("remove", limit=5)  # stable across instances


def test_style_variants_collapsed():
    out = _store().find("remove", limit=10)
    assert "Icons.REMOVE_OUTLINED" not in out
    assert "Icons.REMOVE_ROUNDED" not in out
    assert "Icons.GROUP_REMOVE" in out


def test_family_filter():
    out = _store().find("add", family="cupertino", limit=5)
    assert out == ["CupertinoIcons.ADD"]


def test_synonym_tags_resolve_concepts():
    s = _store()
    # An exact name match always wins (CupertinoIcons.MINUS / .TRASH),
    # with the synonym-tagged Material icon right behind it...
    minus = s.find("minus", limit=3)
    assert minus[0] == "CupertinoIcons.MINUS" and "Icons.REMOVE" in minus
    trash = s.find("trash", limit=3)
    assert trash[0] == "CupertinoIcons.TRASH" and "Icons.DELETE" in trash
    # ...and within a family, tags + popularity rank the right icon first.
    assert s.find("minus", family="material", limit=3)[0] == "Icons.REMOVE"
    assert s.find("trash", family="material", limit=3)[0] == "Icons.DELETE"


def test_popularity_breaks_ties():
    # "plus" tag matches ADD (popularity 50000) and ADD_BOX (900).
    out = _store().find("plus", limit=3)
    assert out.index("Icons.ADD") < out.index("Icons.ADD_BOX")


def test_variants_inherit_base_tags():
    # REMOVE_OUTLINED has no meta entry of its own; it inherits REMOVE's
    # tags so a tag query still finds it when the base is filtered out.
    out = _store().find("minus", family="material", limit=10)
    assert "Icons.REMOVE" in out


def test_no_meta_degrades_to_name_tokens():
    s = IconStore(material=MATERIAL, cupertino=CUPERTINO)
    assert s.find("remove", limit=3)[0] == "Icons.REMOVE"
    assert s.find("trash", limit=3) == ["CupertinoIcons.TRASH"]


# ---------- golden queries against the committed Google metadata ----------


@pytest.mark.skipif(not ICONS_JSON.exists(), reason="icons.json not present")
@pytest.mark.parametrize(
    ("query", "expected"),
    [
        ("minus", "Icons.REMOVE"),
        ("plus", "Icons.ADD"),
        ("trash", "Icons.DELETE"),
        ("garbage", "Icons.DELETE"),
        ("magnify", "Icons.SEARCH"),
        ("gear", "Icons.SETTINGS"),
        ("pencil", "Icons.EDIT"),
        ("user", "Icons.PERSON"),
    ],
)
def test_golden_queries(query: str, expected: str):
    meta = json.loads(ICONS_JSON.read_text(encoding="utf-8"))["material"]
    store = IconStore(material=list(meta), cupertino=[], material_meta=meta)
    top3 = store.find(query, family="material", limit=3)
    assert expected in top3, f"{query!r} -> {top3}"
