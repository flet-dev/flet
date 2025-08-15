# /// script
# dependencies = [
#   "requests",
#   "Jinja2",
# ]
# ///

import re
from pathlib import Path

import requests
from jinja2 import Environment, FileSystemLoader

# Regex for parsing icon definitions (handles multi-line IconData)
ICON_VAR_PATTERN = re.compile(
    r"""^\s*static const IconData\s+(\w+)\s*=""", re.MULTILINE
)

file_loader = FileSystemLoader(Path(__file__).parent / "templates")
templates = Environment(loader=file_loader)

# def normalize_enum_name(var_name: str) -> str:
#     return var_name.upper()


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


def generate_file(icons, template_name, output_file: str):
    template = templates.get_template(template_name)
    with open(
        Path(__file__).parent.joinpath(output_file).resolve(), "w", encoding="utf-8"
    ) as f:
        f.write(template.render(icons=icons))
    print(f"✅ File written to {output_file}")


def main():
    # material icons
    url = "https://raw.githubusercontent.com/flutter/flutter/refs/heads/stable/packages/flutter/lib/src/material/icons.dart"
    set_id = 1
    dart_content = download_dart_file(url)
    icons = parse_dart_icons(dart_content, set_id)

    generate_file(
        icons,
        "material_icons.dart",
        "../packages/flet/lib/src/utils/material_icons.dart",
    )

    generate_file(
        icons,
        "material_icons.py",
        "../sdk/python/packages/flet/src/flet/controls/material/icons.py",
    )

    # cupertino icons
    url = "https://raw.githubusercontent.com/flutter/flutter/refs/heads/stable/packages/flutter/lib/src/cupertino/icons.dart"
    set_id = 2
    dart_content = download_dart_file(url)
    icons = parse_dart_icons(dart_content, set_id)

    generate_file(
        icons,
        "cupertino_icons.dart",
        "../packages/flet/lib/src/utils/cupertino_icons.dart",
    )

    generate_file(
        icons,
        "cupertino_icons.py",
        "../sdk/python/packages/flet/src/flet/controls/cupertino/cupertino_icons.py",
    )


if __name__ == "__main__":
    main()
