from typing import Any, Optional, Union

from beartype import beartype

from flet.buttons import ButtonStyle
from flet.constrained_control import ConstrainedControl
from flet.control import Control, OptionalNumber
from flet.ref import Ref
from flet.types import (
    AnimationValue,
    OffsetValue,
    ResponsiveNumber,
    RotateValue,
    ScaleValue,
)


class OutlinedButton(ConstrainedControl):
    """
    Outlined buttons are medium-emphasis buttons. They contain actions that are important, but aren’t the primary action in an app. Outlined buttons pair well with filled buttons to indicate an alternative, secondary action.

    Example:
    ```
    import flet as ft

    def main(page: ft.Page):
        page.title = "Basic outlined buttons"
        page.add(
            ft.OutlinedButton(text="Outlined button"),
            ft.OutlinedButton("Disabled button", disabled=True),
        )

    ft.app(target=main)
    ```

    -----

    Online docs: https://flet.dev/docs/controls/outlinedbutton
    """
    def __init__(
        self,
        text: Optional[str] = None,
        ref: Optional[Ref] = None,
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
        icon: Optional[str] = None,
        icon_color: Optional[str] = None,
        style: Optional[ButtonStyle] = None,
        content: Optional[Control] = None,
        autofocus: Optional[bool] = None,
        on_click=None,
        on_long_press=None,
        on_hover=None,
    ):
        ConstrainedControl.__init__(
            self,
            ref=ref,
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
        self.icon = icon
        self.icon_color = icon_color
        self.style = style
        self.content = content
        self.autofocus = autofocus
        self.on_click = on_click
        self.on_long_press = on_long_press
        self.on_hover = on_hover

    def _get_control_name(self):
        return "outlinedbutton"

    def _before_build_command(self):
        super()._before_build_command()
        self._set_attr_json("style", self.__style)

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

    # icon
    @property
    def icon(self):
        return self._get_attr("icon")

    @icon.setter
    def icon(self, value):
        self._set_attr("icon", value)

    # icon_color
    @property
    def icon_color(self):
        return self._get_attr("iconColor")

    @icon_color.setter
    def icon_color(self, value):
        self._set_attr("iconColor", value)

    # style
    @property
    def style(self) -> Optional[ButtonStyle]:
        return self.__style

    @style.setter
    @beartype
    def style(self, value: Optional[ButtonStyle]):
        self.__style = value

    # on_click
    @property
    def on_click(self):
        return self._get_event_handler("click")

    @on_click.setter
    def on_click(self, handler):
        self._add_event_handler("click", handler)

    # on_long_press
    @property
    def on_long_press(self):
        return self._get_event_handler("long_press")

    @on_long_press.setter
    def on_long_press(self, handler):
        self._add_event_handler("long_press", handler)
        self._set_attr("onLongPress", True if handler is not None else None)

    # content
    @property
    def content(self) -> Optional[Control]:
        return self.__content

    @content.setter
    @beartype
    def content(self, value: Optional[Control]):
        self.__content = value

    # autofocus
    @property
    def autofocus(self) -> Optional[bool]:
        return self._get_attr("autofocus", data_type="bool", def_value=False)

    @autofocus.setter
    @beartype
    def autofocus(self, value: Optional[bool]):
        self._set_attr("autofocus", value)

    # on_hover
    @property
    def on_hover(self):
        return self._get_event_handler("hover")

    @on_hover.setter
    def on_hover(self, handler):
        self._add_event_handler("hover", handler)
        if handler is not None:
            self._set_attr("onHover", True)
        else:
            self._set_attr("onHover", None)
