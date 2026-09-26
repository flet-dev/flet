import json
import re
from pathlib import Path

import pytest

import flet as ft

REPO = Path(__file__).resolve().parents[5]
CUPERTINO_JSON = (
    REPO / "sdk/python/packages/flet/src/flet/controls/cupertino/cupertino_icons.json"
)


def test_material_icons_random_with_weights_and_exclude():
    """Test random material icon selection with weights and exclusion list."""
    results = [
        ft.Icons.random(
            exclude=[ft.Icons.FAVORITE],
            weights={ft.Icons.SCHOOL: 150},
        )
        for _ in range(1000)
    ]
    assert ft.Icons.FAVORITE not in results
    assert ft.Icons.SCHOOL in results


def test_cupertino_icons_random_with_weights_and_exclude():
    """Test random cupertino icon selection with weights and exclusion list."""
    results = [
        ft.CupertinoIcons.random(
            exclude=[ft.CupertinoIcons.CAMERA_CIRCLE],
            weights={ft.CupertinoIcons.TABLE: 150},
        )
        for _ in range(1000)
    ]
    assert ft.CupertinoIcons.CAMERA_CIRCLE not in results
    assert ft.CupertinoIcons.TABLE in results


def _dart_icon_order(dart_file: Path) -> list[str]:
    """Return the icon member names in the order the generated Dart list holds them."""
    source = dart_file.read_text(encoding="utf-8")
    return re.findall(r"^\s*(?:Icons|CupertinoIcons)\.(\w+),$", source, re.MULTILINE)


@pytest.mark.parametrize(
    ("json_file", "dart_file", "set_id"),
    [
        (
            REPO / "sdk/python/packages/flet/src/flet/controls/material/icons.json",
            REPO / "packages/flet/lib/src/utils/material_icons.dart",
            1,
        ),
        (
            CUPERTINO_JSON,
            REPO / "packages/flet/lib/src/utils/cupertino_icons.dart",
            2,
        ),
    ],
    ids=["material", "cupertino"],
)
def test_packed_value_indexes_the_dart_list(json_file, dart_file, set_id):
    """The packed value a control sends must index the Dart list back to the same icon.

    The protocol carries `(set_id << 16) | index`, and the client resolves it by
    indexing the generated list - so the Nth Dart entry has to be the icon whose
    JSON value is N. Nothing else enforces that the two generated files stayed in
    step, and a drift would silently render the wrong glyph rather than fail.
    """
    packed = json.loads(json_file.read_text(encoding="utf-8"))
    dart_names = _dart_icon_order(dart_file)

    assert len(packed) == len(dart_names)
    for name, value in packed.items():
        assert value >> 16 == set_id
        assert dart_names[value & 0xFFFF].upper() == name


@pytest.mark.parametrize(
    ("json_file", "codepoints_file"),
    [
        (
            REPO / "sdk/python/packages/flet/src/flet/controls/material/icons.json",
            REPO / "website/src/data/material-icon-codepoints.json",
        ),
        (
            CUPERTINO_JSON,
            REPO / "website/src/data/cupertino-icon-codepoints.json",
        ),
    ],
    ids=["material", "cupertino"],
)
def test_docs_codepoints_cover_every_icon(json_file, codepoints_file):
    """The docs gallery must have a glyph for exactly the icons the SDK exposes.

    The two files are emitted from one parse of Flutter's `icons.dart`, so a
    mismatch means someone regenerated one without the other - which shows up as
    a blank tile in the docs, not as an error.
    """
    packed = json.loads(json_file.read_text(encoding="utf-8"))
    codepoints = json.loads(codepoints_file.read_text(encoding="utf-8"))

    assert packed.keys() == codepoints.keys()
    assert all(isinstance(value, int) and value > 0 for value in codepoints.values())
