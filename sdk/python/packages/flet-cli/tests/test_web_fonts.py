"""`flet build web` defers the fonts only some controls need and drops unused ones."""

import json

from flet_cli.utils.web_fonts import DEFERRED_FONT_MANIFEST, defer_web_fonts


def family(name, *assets):
    return {"family": name, "fonts": [{"asset": a} for a in assets]}


MATERIAL = family("MaterialIcons", "fonts/MaterialIcons-Regular.otf")
ROBOTO = family("Roboto", "web/assets/fonts/roboto.woff2")
KATEX = family(
    "packages/flutter_math_fork/KaTeX_Main",
    "packages/flutter_math_fork/lib/katex_fonts/fonts/KaTeX_Main-Regular.ttf",
    "packages/flutter_math_fork/lib/katex_fonts/fonts/KaTeX_Main-Bold.ttf",
)
LUCIDE = family(
    "packages/lucide_icons_flutter/Lucide",
    "packages/lucide_icons_flutter/assets/lucide.ttf",
)
GEIST = family(
    "packages/shadcn_ui/Geist", "packages/shadcn_ui/fonts/Geist%5Bwght%5D.ttf"
)
LUCIDE_WEIGHTS = [
    family(
        f"packages/lucide_icons_flutter/Lucide{w}",
        f"packages/lucide_icons_flutter/assets/build_font/LucideVariable-w{w}.ttf",
    )
    for w in range(100, 700, 100)
]


def web_build(tmp_path, families):
    assets = tmp_path / "assets"
    for f in families:
        for font in f["fonts"]:
            path = assets / font["asset"]
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(b"font")
    (assets / "FontManifest.json").write_text(json.dumps(families))
    return assets


def read(path):
    return json.loads(path.read_text())


def test_splits_the_manifest(tmp_path):
    assets = web_build(
        tmp_path, [MATERIAL, ROBOTO, KATEX, LUCIDE, GEIST, *LUCIDE_WEIGHTS]
    )

    deferred, unused = defer_web_fonts(tmp_path)

    assert read(assets / "FontManifest.json") == [MATERIAL, ROBOTO]
    assert read(assets / DEFERRED_FONT_MANIFEST) == [KATEX, LUCIDE, GEIST]
    assert deferred == [KATEX["family"], LUCIDE["family"], GEIST["family"]]
    assert unused == [f["family"] for f in LUCIDE_WEIGHTS]
    # Deferred fonts stay in the build, unused ones are removed.
    assert (assets / LUCIDE["fonts"][0]["asset"]).exists()
    assert (assets / GEIST["fonts"][0]["asset"]).exists()
    assert not list(
        (assets / "packages/lucide_icons_flutter/assets/build_font").iterdir()
    )


def test_without_deferred_fonts_writes_an_empty_list(tmp_path):
    """The Dart side then reads an empty list instead of getting a 404."""
    assets = web_build(tmp_path, [MATERIAL])

    assert defer_web_fonts(tmp_path) == ([], [])
    assert read(assets / "FontManifest.json") == [MATERIAL]
    assert read(assets / DEFERRED_FONT_MANIFEST) == []


def test_build_without_a_manifest_is_left_alone(tmp_path):
    assert defer_web_fonts(tmp_path) == ([], [])
    assert not (tmp_path / "assets").exists()
