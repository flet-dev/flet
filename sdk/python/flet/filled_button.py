from typing import Union

from flet.control import Control, OptionalNumber
from flet.elevated_button import ElevatedButton
from flet.ref import Ref


class FilledButton(ElevatedButton):
    def __init__(
        self,
        text: str = None,
        ref: Ref = None,
        width: OptionalNumber = None,
        height: OptionalNumber = None,
        expand: Union[bool, int] = None,
        opacity: OptionalNumber = None,
        tooltip: str = None,
        visible: bool = None,
        disabled: bool = None,
        data: any = None,
        #
        # Specific
        #
        icon: str = None,
        icon_color: str = None,
        content: Control = None,
        autofocus: bool = None,
        on_click=None,
    ):
        ElevatedButton.__init__(
            self,
            ref=ref,
            width=width,
            height=height,
            expand=expand,
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
            text=text,
            icon=icon,
            icon_color=icon_color,
            content=content,
            autofocus=autofocus,
            on_click=on_click,
        )
