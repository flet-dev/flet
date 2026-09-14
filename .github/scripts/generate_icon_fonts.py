# /// script
# requires-python = ">=3.10"
# dependencies = [
#   "fonttools==4.62.0",
#   "brotli==1.2.0",
# ]
# ///
"""Build the icon webfonts the documentation gallery draws with.

Run from the root of the repository:

    uv run .github/scripts/generate_icon_fonts.py
    uv run .github/scripts/generate_icon_fonts.py --verify

The fonts are the ones the Flet client itself renders with - Flutter's
`MaterialIcons-Regular.otf` from the SDK pinned in `.fvmrc`, and
`CupertinoIcons.ttf` from the `cupertino_icons` version pinned in
`client/pubspec.lock`. Taking them from anywhere else would let the docs show a
glyph the app does not draw.

Two transformations are applied:

- `GSUB` is dropped. It is a ligature table mapping icon *names* to glyphs, and
  it is 23% of the Material font. The gallery addresses glyphs by codepoint, so
  none of it is reachable. It is also actively hazardous: the ligature names
  follow the SDK `codepoints` spelling (`arrow_upward_outlined`, `10k_baseline`)
  rather than the Dart member names, so only 6,412 of 8,825 names would resolve
  and the rest would render blank with no error.
- The result is compressed to WOFF2, which is what makes a 1.6 MB desktop font
  a ~355 KB web asset.

`--verify` is deliberately structural rather than byte-exact: WOFF2 encoding is
not reproducible (three identical runs produce three different files), so a hash
comparison would fail on every clean checkout. What is actually worth asserting
is that the shipped font can draw every icon the codepoint map claims, and that
is what is checked.
"""

import argparse
import json
import os
import re
import subprocess
import sys
from pathlib import Path

from fontTools.ttLib import TTFont

REPO = Path(__file__).resolve().parents[2]
OUT = REPO / "website/static/fonts"

# Layout tables the gallery cannot reach: it positions nothing and substitutes
# nothing, it just asks for one codepoint at a time.
DROP_TABLES = ("GSUB", "GPOS")


def flutter_root() -> Path:
    """Return the root of the Flutter SDK on PATH, which `.fvmrc` should pin."""
    if env := os.environ.get("FLUTTER_ROOT"):
        return Path(env)
    try:
        out = subprocess.run(
            ["flutter", "--version", "--machine"],
            capture_output=True,
            text=True,
            check=True,
        ).stdout
    except (OSError, subprocess.CalledProcessError) as e:
        raise SystemExit(
            "cannot locate a Flutter SDK: set FLUTTER_ROOT or put `flutter` on PATH"
        ) from e
    info = json.loads(out)
    pinned = json.loads((REPO / ".fvmrc").read_text(encoding="utf-8"))["flutter"].strip()
    if info.get("frameworkVersion") != pinned:
        print(
            f"warning: Flutter on PATH is {info.get('frameworkVersion')}, "
            f".fvmrc pins {pinned} - the glyphs may not match the shipped client"
        )
    return Path(info["flutterRoot"])


def pub_cache() -> Path:
    if env := os.environ.get("PUB_CACHE"):
        return Path(env)
    return Path.home() / ".pub-cache"


def cupertino_icons_dir() -> Path:
    """Return the pinned `cupertino_icons` package directory in the pub cache."""
    lock = (REPO / "client/pubspec.lock").read_text(encoding="utf-8")
    match = re.search(
        r"^  cupertino_icons:\n(?:.*\n)*?    version: \"([^\"]+)\"$", lock, re.MULTILINE
    )
    if not match:
        raise SystemExit("cupertino_icons not found in client/pubspec.lock")
    version = match.group(1)
    path = pub_cache() / "hosted/pub.dev" / f"cupertino_icons-{version}"
    if not path.is_dir():
        raise SystemExit(
            f"{path} is missing - run `flutter pub get` in client/ to populate the "
            "pub cache, then re-run this script"
        )
    return path


def build_font(source: Path) -> TTFont:
    font = TTFont(source)
    for table in DROP_TABLES:
        if table in font:
            del font[table]
    font.flavor = "woff2"
    return font


def codepoints(name: str) -> set[int]:
    """Return every codepoint the committed map for `name` claims a glyph for."""
    data = json.loads(
        (REPO / "website/src/data" / f"{name}-icon-codepoints.json").read_text(
            encoding="utf-8"
        )
    )
    return set(data.values())


def check(font_path: Path, name: str) -> int:
    """Assert the shipped font is stripped and can draw every mapped codepoint."""
    if not font_path.is_file():
        print(f"missing: {font_path.relative_to(REPO)}")
        return 1

    font = TTFont(font_path)
    failures = 0
    if present := [t for t in DROP_TABLES if t in font]:
        print(f"stale: {font_path.name} still carries {', '.join(present)}")
        failures += 1

    covered = set(font.getBestCmap())
    if missing := codepoints(name) - covered:
        sample = ", ".join(hex(c) for c in sorted(missing)[:5])
        print(f"stale: {font_path.name} is missing {len(missing)} codepoints ({sample})")
        failures += 1

    if not failures:
        print(f"ok: {font_path.name} covers all {len(codepoints(name))} codepoints")
    return failures


FONTS = (
    # (name, source resolver, output font name, licence source, licence out name)
    (
        "material",
        lambda: flutter_root() / "bin/cache/artifacts/material_fonts",
        "MaterialIcons-Regular.otf",
        "MaterialIcons-Regular.woff2",
        "MaterialIcons_LICENSE.txt",
        "MaterialIcons_LICENSE.txt",
    ),
    (
        "cupertino",
        cupertino_icons_dir,
        "assets/CupertinoIcons.ttf",
        "CupertinoIcons.woff2",
        "LICENSE",
        "CupertinoIcons_LICENSE.txt",
    ),
)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--verify",
        action="store_true",
        help="check the committed fonts are stripped and cover every codepoint",
    )
    args = parser.parse_args()

    failures = 0
    for name, source_dir, font_rel, out_name, licence_rel, licence_out in FONTS:
        out_path = OUT / out_name
        if args.verify:
            failures += check(out_path, name)
            continue

        source = source_dir() / font_rel
        if not source.is_file():
            raise SystemExit(f"missing source font: {source}")

        OUT.mkdir(parents=True, exist_ok=True)
        font = build_font(source)
        font.save(out_path)

        # Normalised rather than copied verbatim: the `end-of-file-fixer`
        # pre-commit hook rewrites a licence that ends without a newline, which
        # would show up as a spurious diff every time this script is re-run.
        licence = (source_dir() / licence_rel).read_text(encoding="utf-8")
        (OUT / licence_out).write_text(licence.rstrip("\n") + "\n", encoding="utf-8")
        print(
            f"✅ {out_name}: {source.stat().st_size:,} -> {out_path.stat().st_size:,} "
            f"bytes ({len(codepoints(name)):,} codepoints)"
        )

    if args.verify:
        print(f"{failures} failure(s)")
        return 1 if failures else 0
    return 0


if __name__ == "__main__":
    sys.exit(main())
