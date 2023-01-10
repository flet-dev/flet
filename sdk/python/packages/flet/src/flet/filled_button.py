from typing import Any, Optional, Union

from flet.buttons import ButtonStyle
from flet.control import Control, OptionalNumber
from flet.elevated_button import ElevatedButton
from flet.ref import Ref
from flet.types import ResponsiveNumber


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
    def __init__(
        self,
        text: Optional[str] = None,
        ref: Optional[Ref] = None,
        width: OptionalNumber = None,
        height: OptionalNumber = None,
        expand: Union[None, bool, int] = None,
        col: Optional[ResponsiveNumber] = None,
        opacity: OptionalNumber = None,
        tooltip: Optional[str] = None,
        visible: Optional[bool] = None,
        disabled: Optional[bool] = None,
        data: Any = None,
        #
        # Specific
        #
        icon: Optional[str] = None,
        icon_color: Optional[str] = None,
        style: Optional[ButtonStyle] = None,
        content: Optional[Control] = None,
        autofocus: Optional[bool] = None,
        on_click=None,
        on_long_press=None,
        on_hover=None,
    ):
        ElevatedButton.__init__(
            self,
            ref=ref,
            width=width,
            height=height,
            expand=expand,
            col=col,
            opacity=opacity,
            tooltip=tooltip,
            visible=visible,
            disabled=disabled,
            data=data,
            #
            # Specific
            #
            color="onPrimary",
            bgcolor="primary",
            elevation=0,
            style=style,
            text=text,
            icon=icon,
            icon_color=icon_color,
            content=content,
            autofocus=autofocus,
            on_click=on_click,
            on_long_press=on_long_press,
            on_hover=on_hover,
        )
