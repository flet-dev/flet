from typing import Any, Optional, Union

from flet.core.badge import BadgeValue
from flet.core.buttons import ButtonStyle
from flet.core.control import Control, OptionalNumber
from flet.core.elevated_button import ElevatedButton
from flet.core.ref import Ref
from flet.core.tooltip import TooltipValue
from flet.core.types import ColorValue, IconValue, ResponsiveNumber, UrlTarget


class Button(ElevatedButton):
    """
    Elevated buttons or Buttons are essentially filled tonal buttons with a shadow. To prevent shadow creep, only use them when absolutely necessary, such as when the button requires visual separation from a patterned background.

    Example:
    ```
    import flet as ft

    def main(page: ft.Page):
        page.title = "Basic buttons"
        page.add(
            ft.Button(text="Button"),
            ft.Button("Disabled button", disabled=True),
        )

    ft.app(target=main)
    ```

    -----

    Online docs: https://flet.dev/docs/controls/elevatedbutton
    """

    def _get_control_name(self):
        return "elevatedbutton"
