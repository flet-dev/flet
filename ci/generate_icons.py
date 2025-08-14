import re
import sys

import requests

# Regex for parsing icon definitions (handles multi-line IconData)
ICON_ENTRY_PATTERN = re.compile(
    r"""
    ^\s*///.*?"(?P<name>.+?)"(?:\s+\((?P<style>\w+)\))?.*?\n  # doc line
    ^\s*static\s+const\s+IconData\s+(?P<var_name>\w+)\s*=\s*IconData\s*\(\s*  # var line
    0x(?P<codepoint>[0-9a-fA-F]+),  # codepoint
    """,
    re.MULTILINE | re.VERBOSE,
)


def normalize_enum_name(var_name: str) -> str:
    return var_name.upper()


def download_dart_file(url: str) -> str:
    print(f"Downloading Dart file from: {url}")
    response = requests.get(url)
    response.raise_for_status()
    return response.text


def parse_dart_icons(dart_content: str, set_id: int):
    icons = []
    for match in ICON_ENTRY_PATTERN.finditer(dart_content):
        var_name = match.group("var_name")
        codepoint = int(match.group("codepoint"), 16)
        packed_value = (set_id << 16) | codepoint
        icons.append((normalize_enum_name(var_name), hex(packed_value)))
    print(f"🔍 Found {len(icons)} icons for set ID {set_id}.")
    return icons


def generate_python_enum(icons, output_file: str, class_name: str):
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(f"class {class_name}(BaseIcon):\n")
        for name, code in icons:
            f.write(f"    {name} = {code}\n")
    print(f"✅ Enum written to {output_file}")


def main():
    if len(sys.argv) < 5:
        print(
            "Usage: python generate_icons.py <https://path/to/Icons.dart> <output-file> <class-name> <set-id>"
        )
        sys.exit(1)

    url = sys.argv[1]
    output_file = sys.argv[2]
    class_name = sys.argv[3]
    set_id = int(sys.argv[4])

    dart_content = download_dart_file(url)

    icons = parse_dart_icons(dart_content, set_id)

    if not icons:
        print("⚠️ No icons found. Please check the format.")
        sys.exit(1)

    generate_python_enum(icons, output_file, class_name)


if __name__ == "__main__":
    main()
