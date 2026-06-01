#!/usr/bin/env python3
"""Remove static ### headers before <CodeExample> tags in control docs.

The headers are now injected dynamically by the remark-inject-example-headings
plugin from examples-metadata.json (sourced from pyproject.toml titles).
"""

import re
from pathlib import Path

DOCS_DIR = Path(__file__).parent.parent.parent.parent / "website/docs/controls"

# Matches: ### Header\n\n<CodeExample path={frontMatter.examples + '/subfolder/...
PATTERN = re.compile(
    r"### [^\n]+\n\n(<CodeExample path=\{frontMatter\.examples \+ '/[^/']+/)",
    re.MULTILINE,
)


def process_file(md_file: Path) -> bool:
    content = md_file.read_text()
    new_content = PATTERN.sub(r"\1", content)
    if new_content != content:
        md_file.write_text(new_content)
        return True
    return False


def main() -> None:
    changed = 0
    for md_file in sorted(DOCS_DIR.rglob("*.md")):
        if process_file(md_file):
            changed += 1
    print(f"Updated {changed} files.")


if __name__ == "__main__":
    main()
