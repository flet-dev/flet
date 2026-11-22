"""
Flet Material Icons Stub

To generate/update this file run from the root of the repository:

```
uv run .github/scripts/generate_icons.py
```
"""

from flet.controls.icon_data import IconData

__all__ = ["Icons"]

class _IconsMeta(type):
    def __getitem__(cls, name: str) -> IconData: ...
    def __contains__(cls, item: object) -> bool: ...

class Icons(metaclass=_IconsMeta):
    {% for name, code in icons -%}
    {{ name.upper() }}: IconData
    {% endfor -%}
