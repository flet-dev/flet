import time
from typing import Any, Optional, Union

from flet_core.buttons import ButtonStyle
from flet_core.constrained_control import ConstrainedControl
from flet_core.control import Control, OptionalNumber
from flet_core.ref import Ref
from flet_core.types import (
    AnimationValue,
    OffsetValue,
    ResponsiveNumber,
    RotateValue,
    ScaleValue,
)
from flet_core.text_style import TextStyle


class CupertinoDialogAction(ConstrainedControl):
    """
    A button typically used in a CupertinoAlertDialog.

    Example:
    ```
    import flet as ft


    def main(page: ft.Page):
        cupertino_alert_dialog = ft.CupertinoAlertDialog(
            title=ft.Text("Cupertino Alert Dialog"),
            content=ft.Text("body"),
            on_dismiss=lambda e: print("Dismissed!"),
            actions=[
                ft.CupertinoDialogAction(
                    "OK",
                    text_style=ft.TextStyle(italic=True),
                    is_destructive_action=True,
                ),
                ft.CupertinoDialogAction(text="Cancel", is_default_action=False),
            ],
        )

        def open_cupertino_dialog(e):
            page.dialog = cupertino_alert_dialog
            cupertino_alert_dialog.open = True
            page.update()

        page.add(
            ft.OutlinedButton("Open Cupertino Dialog", on_click=open_cupertino_dialog),
        )


    ft.app(target=main)
    ```

    -----

    Online docs: https://flet.dev/docs/controls/cupertinodialogaction
    """

    def __init__(
        self,
        text: Optional[str] = None,
        ref: Optional[Ref] = None,
        key: Optional[str] = None,
        width: OptionalNumber = None,
        height: OptionalNumber = None,
        left: OptionalNumber = None,
        top: OptionalNumber = None,
        right: OptionalNumber = None,
        bottom: OptionalNumber = None,
        expand: Union[None, bool, int] = None,
        col: Optional[ResponsiveNumber] = None,
        opacity: OptionalNumber = None,
        rotate: RotateValue = None,
        scale: ScaleValue = None,
        offset: OffsetValue = None,
        aspect_ratio: OptionalNumber = None,
        animate_opacity: AnimationValue = None,
        animate_size: AnimationValue = None,
        animate_position: AnimationValue = None,
        animate_rotation: AnimationValue = None,
        animate_scale: AnimationValue = None,
        animate_offset: AnimationValue = None,
        on_animation_end=None,
        tooltip: Optional[str] = None,
        visible: Optional[bool] = None,
        disabled: Optional[bool] = None,
        data: Any = None,
        #
        # Specific
        #
        content: Optional[Control] = None,
        is_default_action: Optional[bool] = None,
        is_destructive_action: Optional[bool] = None,
        text_style: Optional[TextStyle] = None,
        on_click=None,
    ):
        ConstrainedControl.__init__(
            self,
            ref=ref,
            key=key,
            width=width,
            height=height,
            left=left,
            top=top,
            right=right,
            bottom=bottom,
            expand=expand,
            col=col,
            opacity=opacity,
            rotate=rotate,
            scale=scale,
            offset=offset,
            aspect_ratio=aspect_ratio,
            animate_opacity=animate_opacity,
            animate_size=animate_size,
            animate_position=animate_position,
            animate_rotation=animate_rotation,
            animate_scale=animate_scale,
            animate_offset=animate_offset,
            on_animation_end=on_animation_end,
            tooltip=tooltip,
            visible=visible,
            disabled=disabled,
            data=data,
        )

        self.text = text
        self.text_style = text_style
        self.content = content
        self.on_click = on_click
        self.is_default_action = is_default_action
        self.is_destructive_action = is_destructive_action

    def _get_control_name(self):
        return "cupertinodialogaction"

    def _before_build_command(self):
        super()._before_build_command()
        self._set_attr_json("textStyle", self.__text_style)

    def _get_children(self):
        if self.__content is None:
            return []
        self.__content._set_attr_internal("n", "content")
        return [self.__content]

    # text
    @property
    def text(self):
        return self._get_attr("text")

    @text.setter
    def text(self, value):
        self._set_attr("text", value)

    # text_style
    @property
    def text_style(self):
        return self.__text_style

    @text_style.setter
    def text_style(self, value: Optional[TextStyle]):
        self.__text_style = value

    # is_default_action
    @property
    def is_default_action(self) -> Optional[bool]:
        return self._get_attr("isDefaultAction")

    @is_default_action.setter
    def is_default_action(self, value: Optional[bool]):
        self._set_attr("isDefaultAction", value)

    # is_destructive_action
    @property
    def is_destructive_action(self) -> Optional[bool]:
        return self._get_attr("isDestructiveAction")

    @is_destructive_action.setter
    def is_destructive_action(self, value: Optional[bool]):
        self._set_attr("isDestructiveAction", value)

    # on_click
    @property
    def on_click(self):
        return self._get_event_handler("click")

    @on_click.setter
    def on_click(self, handler):
        self._add_event_handler("click", handler)

    # content
    @property
    def content(self) -> Optional[Control]:
        return self.__content

    @content.setter
    def content(self, value: Optional[Control]):
        self.__content = value
