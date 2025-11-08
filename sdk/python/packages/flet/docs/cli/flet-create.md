---
title: flet create
---

The `flet create` command scaffolds a new Flet project using a predefined template.
It sets up the initial directory structure, metadata,
and required files to help you get started quickly.

## Usage

```
flet create [OPTIONS] [OUTPUT_DIRECTORY]
```

## Arguments

### `OUTPUT_DIRECTORY`

Directory where the new Flet project will be created.
If omitted, the project is created in the current directory.

```python exec="true" updatetoc="no"
import argparse

from flet_cli.cli import get_parser

parser = get_parser()
lines = []
lines.append(f"## duty")
if parser.description:
    lines.append(parser.description)
lines.append("\nOptions:\n")
for action in parser._actions:
    opts = [f"`{opt}`" for opt in action.option_strings]
    if not opts:
        continue
    line = "- " + ",".join(opts)
    if action.metavar:
        line += f" `{action.metavar}`"
    line += f": {action.help}"
    if action.default and action.default != argparse.SUPPRESS:
        line += f" (default: {action.default})"
    lines.append(line)
print("\n".join(lines))
```
