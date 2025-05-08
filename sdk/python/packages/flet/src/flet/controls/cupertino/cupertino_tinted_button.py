from flet.controls.base_control import control
from flet.controls.cupertino.cupertino_button import CupertinoButton

__all__ = ["CupertinoTintedButton"]


@control("CupertinoTintedButton")
class CupertinoTintedButton(CupertinoButton):
    """
    An iOS-style button filled with default background color.

    Online docs: https://flet.dev/docs/controls/cupertinofilledbutton
    """
