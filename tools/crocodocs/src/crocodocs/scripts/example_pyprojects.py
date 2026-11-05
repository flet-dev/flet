"""Strip example pyproject.toml files for the docs straight from flet-cli.

Reads a JSON list of pyproject.toml paths from stdin and prints a JSON object
mapping each path to its contents without the tables that
`flet_cli.utils.examples.strip_tooling_only_tables` removes. The docs then show
the same pyproject.toml that `flet create --example` creates.
"""

import json
import sys
from pathlib import Path


def main() -> None:
    from flet_cli.utils.examples import strip_tooling_only_tables

    paths = json.load(sys.stdin)
    print(
        json.dumps(
            {
                path: strip_tooling_only_tables(Path(path).read_text(encoding="utf-8"))
                for path in paths
            }
        )
    )


if __name__ == "__main__":
    main()
