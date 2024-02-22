from typing import Any, Optional, Union

from flet_core.alignment import Alignment
from flet_core.control import Control, OptionalNumber
from flet_core.cupertino_button import CupertinoButton
from flet_core.ref import Ref
from flet_core.types import BorderRadiusValue, PaddingValue, ResponsiveNumber


class CupertinoFilledButton(CupertinoButton):
    """
    An iOS-style button filled with default background color.

    Example:
    ```
    import flet as ft


    def main(page: ft.Page):
        page.add(
            ft.CupertinoFilledButton(text="OK"),
        )

    ft.app(target=main)
    ```
    -----

    Online docs: https://flet.dev/docs/controls/cupertinofilledbutton
    """

    def __init__(
        self,
        text: Optional[str] = None,
        disabled_color: Optional[str] = None,
        opacity_on_click: OptionalNumber = None,
        min_size: OptionalNumber = None,
        padding: PaddingValue = None,
        alignment: Optional[Alignment] = None,
        border_radius: BorderRadiusValue = None,
        ref: Optional[Ref] = None,
        key: Optional[str] = None,
        width: OptionalNumber = None,
        height: OptionalNumber = None,
        expand: Union[None, bool, int] = None,
        expand_loose: Optional[bool] = None,
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
        content: Optional[Control] = None,
        url: Optional[str] = None,
        url_target: Optional[str] = None,
        on_click=None,
    ):
        CupertinoButton.__init__(
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
            color="onPrimary",
            bgcolor="primary",
            disabled_color=disabled_color,
            text=text,
            icon=icon,
            icon_color=icon_color,
            content=content,
            url=url,
            url_target=url_target,
            on_click=on_click,
            border_radius=border_radius,
            min_size=min_size,
            opacity_on_click=opacity_on_click,
            padding=padding,
            alignment=alignment,
        )
