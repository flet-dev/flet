from flet.controls.base_control import control
from flet.controls.cupertino.cupertino_button import CupertinoButton

__all__ = ["CupertinoTintedButton"]


@control("CupertinoTintedButton")
class CupertinoTintedButton(CupertinoButton):
    """
    An iOS-style button filled with default background color.

    ```python
    ft.CupertinoTintedButton("Tap me")
    ```
    """
