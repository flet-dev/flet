from typing import Any, Optional, Union

from flet.core.buttons import ButtonStyle
from flet.core.control import Control, OptionalNumber
from flet.core.elevated_button import ElevatedButton
from flet.core.ref import Ref
from flet.core.tooltip import TooltipValue
from flet.core.types import ResponsiveNumber, UrlTarget


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
        adaptive: Optional[bool] = None,
        color: Optional[str] = None,
        bgcolor: Optional[str] = None,
        elevation: OptionalNumber = None,
        icon: Optional[str] = None,
        icon_color: Optional[str] = None,
        style: Optional[ButtonStyle] = None,
        content: Optional[Control] = None,
        autofocus: Optional[bool] = None,
        url: Optional[str] = None,
        url_target: Optional[UrlTarget] = None,
        on_click=None,
        on_long_press=None,
        on_hover=None,
        #
        # Control and AdaptiveControl
        #
        ref: Optional[Ref] = None,
        key: Optional[str] = None,
        width: OptionalNumber = None,
        height: OptionalNumber = None,
        expand: Union[None, bool, int] = None,
        expand_loose: Optional[bool] = None,
        col: Optional[ResponsiveNumber] = None,
        opacity: OptionalNumber = None,
        tooltip: TooltipValue = None,
        visible: Optional[bool] = None,
        disabled: Optional[bool] = None,
        data: Any = None,
    ):
        ElevatedButton.__init__(
            self,
            ref=ref,
            key=key,
            width=width,
            height=height,
            expand=expand,
            expand_loose=expand_loose,
            col=col,
            opacity=opacity,
            tooltip=tooltip,
            visible=visible,
            disabled=disabled,
            data=data,
            #
            # Specific
            #
            color=color,
            bgcolor=bgcolor,
            elevation=elevation,
            style=style,
            text=text,
            icon=icon,
            icon_color=icon_color,
            content=content,
            autofocus=autofocus,
            url=url,
            url_target=url_target,
            on_click=on_click,
            on_long_press=on_long_press,
            on_hover=on_hover,
            adaptive=adaptive,
        )

    def _get_control_name(self):
        return "filledbutton"