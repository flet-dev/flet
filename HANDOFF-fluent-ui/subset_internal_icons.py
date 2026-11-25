"""Cut FluentSystemIcons-Resizable.ttf down to the glyphs fluent_ui uses internally.

Usage: python subset_internal_icons.py FluentSystemIcons-Resizable.ttf out.ttf

The font comes from https://github.com/microsoft/fluentui-system-icons (MIT).
This only subsets; remapping the glyphs to fluent_ui's codepoints is still to do.
"""

import gzip
import os
import sys

from fontTools import subset
from fontTools.ttLib import TTFont

NAMES = (
    "chevron_down chevron_up chevron_left chevron_right "
    "caret_down caret_up caret_left caret_right "
    "dismiss checkmark navigation info error_circle warning circle add arrow_left "
    "calendar camera dismiss_circle copy cut clipboard_paste delete star "
    "more_horizontal eye search share arrow_undo checkmark_circle"
).split()


def main(src: str, out: str) -> None:
    cmap = TTFont(src).getBestCmap()
    want = {f"ic_fluent_{n}_20_{s}" for n in NAMES for s in ("regular", "filled")}
    codes = [c for c, g in cmap.items() if g in want]

    options = subset.Options()
    options.glyph_names = True
    options.layout_features = []
    font = TTFont(src)
    subsetter = subset.Subsetter(options)
    subsetter.populate(unicodes=codes)
    subsetter.subset(font)
    font.save(out)

    with open(out, "rb") as f:
        gz = len(gzip.compress(f.read(), 9))
    size = os.path.getsize(out)
    print(f"icons={len(codes)} ttf={size / 1000:.1f} KB gzip={gz / 1000:.1f} KB")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
