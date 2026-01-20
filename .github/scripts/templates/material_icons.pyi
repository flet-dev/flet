"""
Flet Material Icons Stub

To generate/update this file run from the root of the repository:

```
uv run .github/scripts/generate_icons.py
```
"""

from flet.controls.icon_data import IconData

__all__ = ["Icons"]


class Icons(IconData, package_name="flet", class_name="Icons"):
    {% for name, code in icons -%}
    {{ name.upper() }}: IconData
    {% endfor -%}
