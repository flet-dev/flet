from flet.controls.base_control import control
from flet.controls.cupertino.cupertino_button import CupertinoButton

__all__ = ["CupertinoTintedButton"]


@control("CupertinoTintedButton")
class CupertinoTintedButton(CupertinoButton):
    """
    An iOS-style button filled with default background color.

    Example:
    ```
    import flet as ft


    def main(page: ft.Page):
        page.add(
            ft.CupertinoTintedButton(text="OK"),
        )

    ft.app(target=main)
    ```
    -----

    Online docs: https://flet.dev/docs/controls/cupertinofilledbutton
    """
