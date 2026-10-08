"""
Flet Lucide Icons Stub

To generate/update this file run from the root of the repository:

```
uv run .github/scripts/generate_icons.py
```
"""

from flet.controls.icon_data import IconData

__all__ = ["LucideIcons"]

class LucideIcons:
    {% for name in icons -%}
    {{ name }}: IconData
    {% endfor -%}
