"""
Flet Fluent Icons Stub

To generate/update this file run from the root of the repository:

```
uv run .github/scripts/generate_icons.py
```
"""

from flet.controls.icon_data import IconData

__all__ = ["FluentIcons"]

class _FluentIconsMeta(type):
    def __getitem__(cls, name: str) -> IconData: ...
    def __contains__(cls, item: object) -> bool: ...

class FluentIcons(metaclass=_FluentIconsMeta):
    {% for name in icons -%}
    {{ name }}: IconData
    {% endfor -%}
