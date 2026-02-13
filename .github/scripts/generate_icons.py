# /// script
# dependencies = [
#   "requests",
#   "Jinja2",
# ]
# ///

import json
import re
from pathlib import Path

import requests
from jinja2 import Environment, FileSystemLoader

# Regex for parsing icon definitions (handles multi-line IconData)
ICON_VAR_PATTERN = re.compile(
    r"""^\s*static const IconData\s+(\w+)\s*=""", re.MULTILINE
)
ICON_CODEPOINT_PATTERN = re.compile(
    r"""^\s*static const IconData\s+(\w+)\s*=\s*IconData\(\s*(0x[0-9a-fA-F]+|\d+)""",
    re.MULTILINE,
)

file_loader = FileSystemLoader(Path(__file__).parent / "templates")
templates = Environment(loader=file_loader)


def download_dart_file(url: str) -> str:
    print(f"Downloading Dart file from: {url}")
    response = requests.get(url)
    response.raise_for_status()
    return response.text


def parse_dart_icons(dart_content: str, set_id: int):
    # Extract and sort icon names alphabetically
    icon_names = sorted(ICON_VAR_PATTERN.findall(dart_content))

    icons = []
    for i, icon_name in enumerate(icon_names):
        packed_value = (set_id << 16) | i
        icons.append((icon_name, packed_value))

    print(f"🔍 Found {len(icons)} icons for set ID {set_id} (sorted).")
    return icons


def parse_dart_icon_codepoints(dart_content: str) -> dict[str, int]:
    codepoints = {}
    for icon_name, raw_codepoint in ICON_CODEPOINT_PATTERN.findall(dart_content):
        codepoints[icon_name.upper()] = int(raw_codepoint, 0)
    print(f"🔍 Found {len(codepoints)} icon codepoints.")
    return codepoints


def generate_file(icons, template_name, output_file: str):
    template = templates.get_template(template_name)
    with open(
        Path(__file__).parent.joinpath(output_file).resolve(), "w", encoding="utf-8"
    ) as f:
        f.write(template.render(icons=icons))
    print(f"✅ File written to {output_file}")


def generate_json(icons, output_file: str):
    payload = {name.upper(): value for name, value in icons}
    output_path = Path(__file__).parent.joinpath(output_file).resolve()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(payload, separators=(",", ":")), encoding="utf-8")
    print(f"✅ JSON written to {output_file}")


def generate_json_from_dict(payload: dict[str, int], output_file: str):
    output_path = Path(__file__).parent.joinpath(output_file).resolve()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(payload, separators=(",", ":")), encoding="utf-8")
    print(f"✅ JSON written to {output_file}")


def main():
    # material icons
    url = "https://raw.githubusercontent.com/flutter/flutter/refs/heads/stable/packages/flutter/lib/src/material/icons.dart"
    set_id = 1
    dart_content = download_dart_file(url)
    icons = parse_dart_icons(dart_content, set_id)

    generate_file(
        icons,
        "material_icons.dart",
        "../../packages/flet/lib/src/utils/material_icons.dart",
    )

    generate_file(
        icons,
        "material_icons.pyi",
        "../../sdk/python/packages/flet/src/flet/controls/material/icons.pyi",
    )

    generate_json(
        icons,
        "../../sdk/python/packages/flet/src/flet/controls/material/icons.json",
    )

    # cupertino icons
    url = "https://raw.githubusercontent.com/flutter/flutter/refs/heads/stable/packages/flutter/lib/src/cupertino/icons.dart"
    set_id = 2
    dart_content = download_dart_file(url)
    icons = parse_dart_icons(dart_content, set_id)
    codepoints = parse_dart_icon_codepoints(dart_content)

    generate_file(
        icons,
        "cupertino_icons.dart",
        "../../packages/flet/lib/src/utils/cupertino_icons.dart",
    )

    generate_file(
        icons,
        "cupertino_icons.pyi",
        "../../sdk/python/packages/flet/src/flet/controls/cupertino/cupertino_icons.pyi",
    )

    generate_json(
        icons,
        "../../sdk/python/packages/flet/src/flet/controls/cupertino/cupertino_icons.json",
    )

    if len(codepoints) != len(icons):
        raise RuntimeError(
            f"Cupertino icon count mismatch: {len(icons)} packed icons vs {len(codepoints)} codepoints."
        )
    generate_json_from_dict(
        codepoints,
        "../../sdk/python/packages/flet/src/flet/controls/cupertino/cupertino_icons_codepoints.json",
    )


if __name__ == "__main__":
    main()
