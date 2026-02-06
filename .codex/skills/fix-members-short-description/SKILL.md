---
name: fix-members-short-description
description: Use when asked to fix short descriptions of Python type members.
---

## Inputs

* File or directory with Python modules.

## Instructions

When Flet documentation is generated from docstrings the first sentence of a member docstring is used as a short description, for example:

```py
@dataclass
class MyControl:
    property_a: str
    """
    Short description of a property.

    Full description.
    Another line of full description.
    """
```

Here "Short description of a property." will be used as a short description.

However, when a sentence is broken into multiple lines the lines must be "concatenated" with `\`, for example:

```py
@dataclass
class MyControl:
    property_a: str
    """
    Short description of a property which could \
    take multiple lines.

    Full description.
    Another line of full description.
    """
```

Your goal is to go through all members (properties, methods, etc.) of all types (classes, enums) in input file or directory and ensure the first sentence in their docstrings is broken into multiple lines correctly with `\` symbol.

Apply the fix regardless of whether the first sentence starts on the same line as the opening `"""` or on a following line.

Ensure every docstring line is at most 88 characters long (including any trailing `\`). If a line cannot be wrapped without breaking a single unbreakable token (e.g., a long URL or Windows registry path like `HKEY_LOCAL_MACHINE\\...`), add `# noqa: E501` to the docstring closing `"""` line instead of the long line.
