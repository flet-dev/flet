"""Render the Linux apt prerequisites straight from flet-cli.

The package list is owned by `flet_cli.utils.linux_deps`, which is also what
`flet --version --json` reports and what CI installs. Generating the docs
block from it keeps the three from drifting apart.
"""

import textwrap


def _load_linux_dependencies() -> tuple[str, ...]:
    """Load the canonical apt package list from flet-cli."""
    from flet_cli.utils.linux_deps import linux_dependencies

    return tuple(linux_dependencies)


def linux_dependencies_block(width: int = 76, indent: int = 2) -> str:
    """
    Render the apt install command as a Markdown code block.

    Args:
        width: Column to wrap the package list at.
        indent: Spaces to indent continuation lines by.

    Returns:
        A fenced bash code block installing every required package.
    """

    packages = _load_linux_dependencies()
    lines = textwrap.wrap(
        " ".join(packages),
        width=width - indent - 2,
        break_on_hyphens=False,
        break_long_words=False,
    )
    prefix = " " * indent
    body = " \\\n".join(f"{prefix}{line}" for line in lines)
    return f"""```bash
sudo apt update
sudo apt install -y \\
{body}
```
"""


if __name__ == "__main__":
    print(linux_dependencies_block())
