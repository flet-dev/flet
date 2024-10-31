# from typing import Any, Optional, Union

# from flet.core.badge import BadgeValue
# from flet.core.buttons import ButtonStyle
# from flet.core.control import Control, OptionalNumber
from flet.core.elevated_button import ElevatedButton

# from flet.core.ref import Ref
# from flet.core.tooltip import TooltipValue
# from flet.core.types import ColorValue, IconValue, ResponsiveNumber, UrlTarget


class FilledButton(ElevatedButton):
    """
    Filled buttons have the most visual impact after the FloatingActionButton (https://flet.dev/docs/controls/floatingactionbutton), and should be used for important, final actions that complete a flow, like Save, Join now, or Confirm.

    Example:
    ```
    import flet as ft


    def main(page: ft.Page):
        page.title = "Basic filled buttons"
        page.add(
            ft.FilledButton(text="Filled button"),
            ft.FilledButton("Disabled button", disabled=True),
            ft.FilledButton("Button with icon", icon="add"),
        )

    ft.app(target=main)
    ```

    -----

    Online docs: https://flet.dev/docs/controls/filledbutton
    """

    def _get_control_name(self):
        return "filledbutton"
