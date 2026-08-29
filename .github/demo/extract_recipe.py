"""Pull a packaging recipe out of the Linux publishing docs.

Demo branch only.

The CI runs the recipes from `website/docs/publish/linux.md` rather than a
committed copy of them, so what a reader is told to do is what actually
produced the downloadable artifacts. A copy would drift; this cannot.

The only edits are the ones the docs themselves ask the reader to make --
"edit the variables at the top" -- applied here as `KEY=VALUE` arguments. A key
that no longer appears in the recipe is an error rather than a silent no-op, so
renaming a variable in the docs fails the run instead of quietly packaging
`my_app`.

Usage:
    extract_recipe.py <markdown> <tab value> [KEY=VALUE ...]
"""

import re
import sys


def tab_body(markdown: str, tab: str) -> str:
    """The contents of the `<TabItem value="<tab>">` block."""
    start = re.search(rf'<TabItem value="{re.escape(tab)}"[^>]*>', markdown)
    if start is None:
        raise SystemExit(f"no <TabItem value={tab!r}> in the docs")
    end = markdown.find("</TabItem>", start.end())
    if end == -1:
        raise SystemExit(f"unterminated <TabItem value={tab!r}>")
    return markdown[start.end() : end]


def script_block(body: str) -> str:
    """The first ```bash block in `body` that is a whole script."""
    for block in re.findall(r"```bash\n(.*?)```", body, re.DOTALL):
        if block.startswith("#!/usr/bin/env bash"):
            return block
    raise SystemExit("no shebanged bash block in that tab")


def strip_annotations(script: str) -> str:
    """Drop the trailing `# (N)!` markers the docs use for annotations."""
    return re.sub(r"[ \t]*# \(\d+\)!$", "", script, flags=re.MULTILINE)


def apply_overrides(script: str, overrides: dict) -> str:
    """Rewrite the recipe's top-level variable assignments."""
    for key, value in overrides.items():
        pattern = rf"^{re.escape(key)}=.*$"
        # A plain replacement string would read \1 and \g<> in a path as
        # backreferences, so hand re.subn a function instead.
        script, count = re.subn(
            pattern, lambda _m, v=f"{key}={value}": v, script, flags=re.MULTILINE
        )
        if count == 0:
            raise SystemExit(f"recipe has no {key}= line to edit")
    return script


def main() -> int:
    markdown_path, tab = sys.argv[1], sys.argv[2]
    overrides = dict(arg.split("=", 1) for arg in sys.argv[3:])

    with open(markdown_path, encoding="utf-8") as f:
        markdown = f.read()

    script = apply_overrides(
        strip_annotations(script_block(tab_body(markdown, tab))), overrides
    )
    sys.stdout.write(script)
    return 0


if __name__ == "__main__":
    sys.exit(main())
