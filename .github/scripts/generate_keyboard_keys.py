# /// script
# dependencies = [
#   "requests",
#   "Jinja2",
# ]
# ///
"""Generate `flet.KeyboardKey` from Flutter's logical keyboard keys.

Run from the root of the repository:

    uv run .github/scripts/generate_keyboard_keys.py
    uv run .github/scripts/generate_keyboard_keys.py --verify

Each `LogicalKeyboardKey` constant in Flutter's `keyboard_key.g.dart` becomes a
member whose value is the key's `keyLabel`, the string the client sends in
keyboard events. The source is pinned to the Flutter version in `.fvmrc`, the
SDK the client is built with, so the labels match what the client sends.

`keyLabel` is the upper-cased character for printable keys, whose ids are their
Unicode code points, and an entry of the `_keyLabels` map for the others.
"""

import argparse
import json
import re
import sys
from pathlib import Path

import requests
from jinja2 import Environment, FileSystemLoader

REPO = Path(__file__).resolve().parents[2]
OUTPUT_FILE = "sdk/python/packages/flet/src/flet/controls/keyboard_key.py"

KEY_PATTERN = re.compile(
    r"static const LogicalKeyboardKey (\w+) = LogicalKeyboardKey\((0x[0-9a-f]+)\);"
)
LABEL_PATTERN = re.compile(r"(0x[0-9a-f]+): '([^']*)'")

# Ids up to this value are Unicode code points; larger ids carry a plane prefix.
UNICODE_MAX_ID = 0xFFFFFFFF

# Python names that read better than the mechanical conversion of the Dart ones.
RENAMES = {"SUPER_KEY": "SUPER", "NEW_KEY": "NEW", "TV_3_D_MODE": "TV_3D_MODE"}

# Single-letter names that ruff flags as easy to mistake for digits.
AMBIGUOUS_NAMES = {"I", "O"}

templates = Environment(
    loader=FileSystemLoader(Path(__file__).parent / "templates"),
    keep_trailing_newline=True,
)


def flutter_version() -> str:
    """Return the Flutter version pinned in `.fvmrc`."""
    return json.loads((REPO / ".fvmrc").read_text(encoding="utf-8"))["flutter"].strip()


def download_keyboard_keys() -> str:
    url = (
        f"https://raw.githubusercontent.com/flutter/flutter/{flutter_version()}"
        "/packages/flutter/lib/src/services/keyboard_key.g.dart"
    )
    print(f"Downloading Dart file from: {url}")
    response = requests.get(url)
    response.raise_for_status()
    return response.text


def python_name(dart_name: str) -> str:
    """Return the member name for a Dart constant name.

    `arrowRight` becomes `ARROW_RIGHT`, `keyA` becomes `A`, and a number after a
    word gets its own part (`digit0` becomes `DIGIT_0`, `numpad1` `NUMPAD_1`),
    while one after a single letter stays with it (`f5`, `colorF0Red`).
    """
    name = re.sub(
        r"(?<=[a-z0-9])(?=[A-Z])|(?<=[A-Z])(?=[A-Z][a-z])", "_", dart_name
    ).upper()
    name = re.sub(r"^KEY_(?=[A-Z]$)", "", name)
    name = re.sub(r"(?<=[A-Z]{2})(?=\d)", "_", name)
    return RENAMES.get(name, name)


def python_string(value: str) -> str:
    """Return `value` as a string literal in the style ruff formats it."""
    if '"' in value and "'" not in value:
        return f"'{value}'"
    return '"' + value.replace("\\", "\\\\").replace('"', '\\"') + '"'


def parse_keys(dart_content: str) -> list[tuple[str, str]]:
    """Return `(member name, value literal)` for each logical key, in Flutter's order."""
    start = dart_content.index("class LogicalKeyboardKey")
    logical = dart_content[start : dart_content.index("class PhysicalKeyboardKey")]
    labels = {int(k, 16): v for k, v in LABEL_PATTERN.findall(logical)}

    keys = []
    names = set()
    values = set()
    for dart_name, key_id in KEY_PATTERN.findall(logical):
        key_id = int(key_id, 16)
        label = chr(key_id).upper() if key_id <= UNICODE_MAX_ID else labels[key_id]
        name = python_name(dart_name)
        # A repeated value would make the member an alias of another one.
        if name in names or label in values:
            raise SystemExit(f"duplicate key name or label: {name} = {label!r}")
        names.add(name)
        values.add(label)
        literal = python_string(label)
        if name in AMBIGUOUS_NAMES:
            literal += "  # noqa: E741"
        keys.append((name, literal))

    print(f"🔍 Found {len(keys)} keyboard keys.")
    return keys


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--verify", action="store_true", help="fail if the file is missing or stale"
    )
    args = parser.parse_args()

    keys = parse_keys(download_keyboard_keys())
    content = templates.get_template("keyboard_key.py.jinja").render(keys=keys)
    path = REPO / OUTPUT_FILE

    if args.verify:
        if not path.is_file() or path.read_text(encoding="utf-8") != content:
            print(f"stale: {OUTPUT_FILE}")
            return 1
        print(f"up to date: {OUTPUT_FILE}")
        return 0

    path.write_text(content, encoding="utf-8")
    print(f"✅ File written to {OUTPUT_FILE}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
