from flet.controls.base_control import control
from flet.controls.cupertino.cupertino_button import CupertinoButton

__all__ = ["CupertinoFilledButton"]


@control("CupertinoFilledButton")
class CupertinoFilledButton(CupertinoButton):
    """
    An iOS-style button filled with default background color.

    Online docs: https://flet.dev/docs/controls/cupertinofilledbutton
    """
