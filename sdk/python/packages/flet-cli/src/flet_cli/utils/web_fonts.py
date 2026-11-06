"""Fonts of a `flet build web` app that are loaded on first use, or not at all.

Flutter web downloads every font in `assets/FontManifest.json` before the
app's first frame. Some Dart packages bring fonts only a few controls need:
their families move to `assets/DeferredFontManifest.json` (the same format),
and the flet package loads them the first time such a control is built
(`packages/flet/lib/src/utils/deferred_fonts.dart`). Families no Flet control
uses are left out of the build.

Run by `flet build web`, and by CI on Flet's built-in web client (flet-web,
served by `flet run --web` and copied by `flet publish`).
"""

import json
import re
from pathlib import Path

DEFERRED_FONT_MANIFEST = "DeferredFontManifest.json"

# Dart packages whose fonts are loaded on first use:
# - flutter_math_fork: KaTeX, for math in `Markdown`;
# - lucide_icons_flutter: Lucide, for flet-shadcn-ui's icons;
# - shadcn_ui: Geist and Geist Mono, for flet-shadcn-ui's text.
DEFERRED_FONT_PACKAGES = ("flutter_math_fork", "lucide_icons_flutter", "shadcn_ui")

# lucide_icons_flutter's weight variants (2.9 MB): flet-shadcn-ui maps every
# icon to the regular `Lucide` family.
UNUSED_FONT_FAMILIES = re.compile(r"packages/lucide_icons_flutter/Lucide\d00")


def defer_web_fonts(web_dir: Path) -> tuple[list[str], list[str]]:
    """
    Split the fonts of the web build in `web_dir`: deferred families go to
    `DeferredFontManifest.json`, unused ones are removed with their files.

    Returns the deferred and the removed family names. A build without
    `FontManifest.json` is left alone.
    """

    assets = web_dir / "assets"
    manifest_path = assets / "FontManifest.json"
    if not manifest_path.exists():
        return [], []

    families = json.loads(manifest_path.read_text(encoding="utf-8"))
    kept, deferred, unused = [], [], []
    for family in families:
        name = family.get("family", "")
        if UNUSED_FONT_FAMILIES.fullmatch(name):
            unused.append(family)
        elif any(name.startswith(f"packages/{p}/") for p in DEFERRED_FONT_PACKAGES):
            deferred.append(family)
        else:
            kept.append(family)

    manifest_path.write_text(json.dumps(kept), encoding="utf-8")
    (assets / DEFERRED_FONT_MANIFEST).write_text(json.dumps(deferred), encoding="utf-8")
    for family in unused:
        for font in family.get("fonts", []):
            # The manifest's paths are URL-encoded, as Flutter writes them,
            # and so are the file names: `Geist%5Bwght%5D.ttf`.
            (assets / font["asset"]).unlink(missing_ok=True)

    return [f["family"] for f in deferred], [f["family"] for f in unused]
