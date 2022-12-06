from typing import Any, Optional, Union

from flet.buttons import ButtonStyle
from flet.control import Control, OptionalNumber
from flet.elevated_button import ElevatedButton
from flet.ref import Ref
from flet.types import ResponsiveNumber


class FilledTonalButton(ElevatedButton):
    """
    A filled tonal button is an alternative middle ground between FilledButton and OutlinedButton buttons. They’re useful in contexts where a lower-priority button requires slightly more emphasis than an outline would give, such as "Next" in an onboarding flow. Tonal buttons use the secondary color mapping. 
    
    Example:
    ```
    import flet as ft


    def main(page: ft.Page):
        page.title = "Basic filled tonal buttons"
        page.add(
            ft.FilledTonalButton(text="Filled tonal button"),
            ft.FilledTonalButton("Disabled button", disabled=True),
            ft.FilledTonalButton("Button with icon", icon="add"),
        )

    ft.app(target=main)
    ```

    -----

    Online docs: https://flet.dev/docs/controls/filledtonalbutton
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
            color="onSecondaryContainer",
            bgcolor="secondaryContainer",
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
