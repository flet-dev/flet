"""
Reads the Flutter version from a .fvmrc file and prints it.

Usage:
    uv run read_fvmrc.py <fvmrc_file>
"""

import json
import sys


def main() -> None:
    try:
        with open(sys.argv[1], encoding="utf-8") as f:
            v = json.load(f)["flutter"].strip()
            if not v:
                raise ValueError("Empty 'flutter' value in .fvmrc")
            print(v)
    except Exception as e:
        print(f"Error parsing {sys.argv[1]}: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
