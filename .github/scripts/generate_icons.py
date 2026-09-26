# /// script
# dependencies = [
#   "requests",
#   "Jinja2",
# ]
# ///
"""Generate the Material and Cupertino icon sets from Flutter's own sources.

Run from the root of the repository:

    uv run .github/scripts/generate_icons.py
    uv run .github/scripts/generate_icons.py --verify

Flutter's `icons.dart` is the single upstream definition of every icon Flet can
render, so names, the packed values the protocol sends, and the Unicode
codepoints the docs draw with are all derived from it in one pass. Deriving
them separately is how they drift.

The source is pinned to the Flutter version in `.fvmrc` rather than tracking
`stable`. The client renders with the font shipped inside that exact SDK, so an
icon taken from a newer `stable` would have a name and a packed value here and
no glyph there - which renders as an empty box with no error anywhere.
"""

import argparse
import json
import re
import sys
from pathlib import Path

import requests
from jinja2 import Environment, FileSystemLoader

REPO = Path(__file__).resolve().parents[2]

# Captures both the member name and the codepoint of its IconData. The `\s*`
# before `0x` has to span newlines: 826 of the 8,825 material declarations wrap
# the IconData arguments onto following lines, and a same-line-only match would
# silently drop them.
ICON_VAR_PATTERN = re.compile(
    r"""^\s*static const IconData\s+(\w+)\s*=\s*IconData\(\s*(0x[0-9a-fA-F]+)""",
    re.MULTILINE,
)

file_loader = FileSystemLoader(Path(__file__).parent / "templates")
templates = Environment(loader=file_loader)


def flutter_version() -> str:
    """Return the Flutter version pinned in `.fvmrc`."""
    return json.loads((REPO / ".fvmrc").read_text(encoding="utf-8"))["flutter"].strip()


def icons_url(library: str) -> str:
    """Return the raw URL of a Flutter icon library at the pinned version."""
    return (
        f"https://raw.githubusercontent.com/flutter/flutter/{flutter_version()}"
        f"/packages/flutter/lib/src/{library}/icons.dart"
    )


def download_dart_file(url: str) -> str:
    print(f"Downloading Dart file from: {url}")
    response = requests.get(url)
    response.raise_for_status()
    return response.text


def parse_dart_icons(dart_content: str, set_id: int):
    """Return `(icons, codepoints)` for one icon set.

    `icons` is the `(name, packed_value)` list the templates and the protocol
    JSON are rendered from; `codepoints` maps the upper-cased member name to the
    Unicode codepoint its glyph sits at in the icon font.

    The packed value is the member's alphabetical index, so the Nth entry of the
    generated Dart list must be the icon whose JSON value is `(set_id << 16) | N`.
    Sorting once here is what keeps that true.
    """
    matches = ICON_VAR_PATTERN.findall(dart_content)
    by_name = dict(matches)
    if len(by_name) != len(matches):
        raise SystemExit(f"duplicate icon names in set {set_id}")

    icons = []
    codepoints = {}
    for i, icon_name in enumerate(sorted(by_name)):
        icons.append((icon_name, (set_id << 16) | i))
        codepoints[icon_name.upper()] = int(by_name[icon_name], 16)

    print(f"🔍 Found {len(icons)} icons for set ID {set_id} (sorted).")
    return icons, codepoints


def render_file(icons, template_name: str) -> str:
    """Render a template the way the committed file actually looks on disk.

    Jinja leaves trailing whitespace and no final newline, both of which the
    `trailing-whitespace` and `end-of-file-fixer` pre-commit hooks then rewrite.
    Normalising here rather than leaving it to the hooks is what lets `--verify`
    compare against the committed bytes instead of always reporting them stale.
    """
    rendered = templates.get_template(template_name).render(icons=icons)
    return (
        "\n".join(line.rstrip() for line in rendered.splitlines()).rstrip("\n") + "\n"
    )


def render_json(payload: dict) -> str:
    # Trailing newline so re-running the generator is a no-op under the
    # end-of-file-fixer pre-commit hook.
    return json.dumps(payload, separators=(",", ":")) + "\n"


def emit(content: str, output_file: str, verify: bool) -> int:
    """Write `content` to `output_file`, or report whether it is already current."""
    path = (REPO / output_file).resolve()
    if verify:
        if not path.is_file():
            print(f"missing: {output_file}")
            return 1
        if path.read_text(encoding="utf-8") != content:
            print(f"stale: {output_file}")
            return 1
        return 0
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    print(f"✅ File written to {output_file}")
    return 0


# (library, set_id, dart_template, dart_out, pyi_template, pyi_out, json_out, codepoints_out)
ICON_SETS = (
    (
        "material",
        1,
        "material_icons.dart",
        "packages/flet/lib/src/utils/material_icons.dart",
        "material_icons.pyi",
        "sdk/python/packages/flet/src/flet/controls/material/icons.pyi",
        "sdk/python/packages/flet/src/flet/controls/material/icons.json",
        "website/src/data/material-icon-codepoints.json",
    ),
    (
        "cupertino",
        2,
        "cupertino_icons.dart",
        "packages/flet/lib/src/utils/cupertino_icons.dart",
        "cupertino_icons.pyi",
        "sdk/python/packages/flet/src/flet/controls/cupertino/cupertino_icons.pyi",
        "sdk/python/packages/flet/src/flet/controls/cupertino/cupertino_icons.json",
        "website/src/data/cupertino-icon-codepoints.json",
    ),
)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--verify", action="store_true", help="fail if any file is missing or stale"
    )
    args = parser.parse_args()

    failures = 0
    for (
        library,
        set_id,
        dart_template,
        dart_out,
        pyi_template,
        pyi_out,
        json_out,
        codepoints_out,
    ) in ICON_SETS:
        icons, codepoints = parse_dart_icons(
            download_dart_file(icons_url(library)), set_id
        )
        failures += emit(render_file(icons, dart_template), dart_out, args.verify)
        failures += emit(render_file(icons, pyi_template), pyi_out, args.verify)
        failures += emit(
            render_json({name.upper(): value for name, value in icons}),
            json_out,
            args.verify,
        )
        failures += emit(render_json(codepoints), codepoints_out, args.verify)

    if args.verify:
        print(f"{failures} failure(s)")
        return 1 if failures else 0
    return 0


if __name__ == "__main__":
    sys.exit(main())
