import time
from typing import Any, Optional, Union

from flet.core.adaptive_control import AdaptiveControl
from flet.core.alignment import Alignment
from flet.core.animation import AnimationValue
from flet.core.badge import BadgeValue
from flet.core.box import BoxConstraints
from flet.core.buttons import ButtonStyle
from flet.core.constrained_control import ConstrainedControl
from flet.core.control import Control, OptionalNumber
from flet.core.ref import Ref
from flet.core.tooltip import TooltipValue
from flet.core.types import (
    ColorEnums,
    ColorValue,
    IconEnums,
    IconValue,
    MouseCursor,
    OffsetValue,
    OptionalControlEventCallable,
    PaddingValue,
    ResponsiveNumber,
    RotateValue,
    ScaleValue,
    ThemeVisualDensity,
    UrlTarget,
    VisualDensity,
)


class IconButton(ConstrainedControl, AdaptiveControl):
    """
    An icon button is a round button with an icon in the middle that reacts to touches by filling with color (ink).

    Icon buttons are commonly used in the toolbars, but they can be used in many other places as well.

    Example:
    ```
    import flet as ft

    def main(page: ft.Page):
        page.title = "Icon buttons"
        page.add(
            ft.Row(
                [
                    ft.IconButton(
                        icon=ft.icons.PAUSE_CIRCLE_FILLED_ROUNDED,
                        icon_color="blue400",
                        icon_size=20,
                        tooltip="Pause record",
                    ),
                    ft.IconButton(
                        icon=ft.icons.DELETE_FOREVER_ROUNDED,
                        icon_color="pink600",
                        icon_size=40,
                        tooltip="Delete record",
                    ),
                ]
            ),
        )

    ft.app(target=main)
    ```

    -----

    Online docs: https://flet.dev/docs/controls/iconbutton
    """

    def __init__(
        self,
        icon: Optional[IconValue] = None,
        icon_color: Optional[ColorValue] = None,
        icon_size: OptionalNumber = None,
        selected: Optional[bool] = None,
        selected_icon: Optional[IconValue] = None,
        selected_icon_color: Optional[ColorValue] = None,
        bgcolor: Optional[ColorValue] = None,
        highlight_color: Optional[ColorValue] = None,
        style: Optional[ButtonStyle] = None,
        content: Optional[Control] = None,
        autofocus: Optional[bool] = None,
        disabled_color: Optional[ColorValue] = None,
        hover_color: Optional[ColorValue] = None,
        focus_color: Optional[ColorValue] = None,
        splash_color: Optional[ColorValue] = None,
        splash_radius: OptionalNumber = None,
        alignment: Optional[Alignment] = None,
        padding: Optional[PaddingValue] = None,
        enable_feedback: Optional[bool] = None,
        url: Optional[str] = None,
        url_target: Optional[UrlTarget] = None,
        mouse_cursor: Optional[MouseCursor] = None,
        visual_density: Union[None, ThemeVisualDensity, VisualDensity] = None,
        size_constraints: Optional[BoxConstraints] = None,
        on_click: OptionalControlEventCallable = None,
        on_focus: OptionalControlEventCallable = None,
        on_blur: OptionalControlEventCallable = None,
        #
        # ConstrainedControl and AdaptiveControl
        #
        ref: Optional[Ref] = None,
        key: Optional[str] = None,
        width: OptionalNumber = None,
        height: OptionalNumber = None,
        left: OptionalNumber = None,
        top: OptionalNumber = None,
        right: OptionalNumber = None,
        bottom: OptionalNumber = None,
        expand: Union[None, bool, int] = None,
        expand_loose: Optional[bool] = None,
        col: Optional[ResponsiveNumber] = None,
        opacity: OptionalNumber = None,
        rotate: Optional[RotateValue] = None,
        scale: Optional[ScaleValue] = None,
        offset: Optional[OffsetValue] = None,
        aspect_ratio: OptionalNumber = None,
        animate_opacity: Optional[AnimationValue] = None,
        animate_size: Optional[AnimationValue] = None,
        animate_position: Optional[AnimationValue] = None,
        animate_rotation: Optional[AnimationValue] = None,
        animate_scale: Optional[AnimationValue] = None,
        animate_offset: Optional[AnimationValue] = None,
        on_animation_end: OptionalControlEventCallable = None,
        tooltip: Optional[TooltipValue] = None,
        badge: Optional[BadgeValue] = None,
        visible: Optional[bool] = None,
        disabled: Optional[bool] = None,
        data: Any = None,
        adaptive: Optional[bool] = None,
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
            expand_loose=expand_loose,
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
            badge=badge,
            visible=visible,
            disabled=disabled,
            data=data,
        )
        AdaptiveControl.__init__(self, adaptive=adaptive)

        self.icon = icon
        self.icon_size = icon_size
        self.icon_color = icon_color
        self.highlight_color = highlight_color
        self.selected_icon = selected_icon
        self.selected_icon_color = selected_icon_color
        self.selected = selected
        self.bgcolor = bgcolor
        self.style = style
        self.content = content
        self.autofocus = autofocus
        self.disabled_color = disabled_color
        self.hover_color = hover_color
        self.alignment = alignment
        self.padding = padding
        self.enable_feedback = enable_feedback
        self.splash_color = splash_color
        self.splash_radius = splash_radius
        self.focus_color = focus_color
        self.url = url
        self.url_target = url_target
        self.on_click = on_click
        self.on_focus = on_focus
        self.on_blur = on_blur
        self.mouse_cursor = mouse_cursor
        self.visual_density = visual_density
        self.size_constraints = size_constraints

    def _get_control_name(self):
        return "iconbutton"

    def before_update(self):
        super().before_update()
        if self.__style is not None:
            self.__style.side = self._wrap_attr_dict(self.__style.side)
            self.__style.shape = self._wrap_attr_dict(self.__style.shape)
            self.__style.padding = self._wrap_attr_dict(self.__style.padding)
        self._set_attr_json("style", self.__style)
        self._set_attr_json("alignment", self.__alignment)
        self._set_attr_json("padding", self.__padding)
        self._set_attr_json("sizeConstraints", self.__size_constraints)

    def _get_children(self):
        if self.__content is None:
            return []
        self.__content._set_attr_internal("n", "content")
        return [self.__content]

    def focus(self):
        self._set_attr_json("focus", str(time.time()))
        self.update()

    # icon
    @property
    def icon(self) -> Optional[IconValue]:
        return self.__icon

    @icon.setter
    def icon(self, value: Optional[IconValue]):
        self.__icon = value
        self._set_enum_attr("icon", value, IconEnums)

    # selected_icon
    @property
    def selected_icon(self) -> Optional[IconValue]:
        return self.__selected_icon

    @selected_icon.setter
    def selected_icon(self, value: Optional[IconValue]):
        self.__selected_icon = value
        self._set_enum_attr("selectedIcon", value, IconEnums)

    # icon_size
    @property
    def icon_size(self) -> OptionalNumber:
        return self._get_attr("iconSize", data_type="float")

    @icon_size.setter
    def icon_size(self, value: OptionalNumber):
        self._set_attr("iconSize", value)

    # splash_radius
    @property
    def splash_radius(self) -> OptionalNumber:
        return self._get_attr("splashRadius", data_type="float")

    @splash_radius.setter
    def splash_radius(self, value: OptionalNumber):
        self._set_attr("splashRadius", value)

    # splash_color
    @property
    def splash_color(self) -> Optional[ColorValue]:
        return self.__splash_color

    @splash_color.setter
    def splash_color(self, value: Optional[ColorValue]):
        self.__splash_color = value
        self._set_enum_attr("splashColor", value, ColorEnums)

    # icon_color
    @property
    def icon_color(self) -> Optional[ColorValue]:
        return self.__icon_color

    @icon_color.setter
    def icon_color(self, value: Optional[ColorValue]):
        self.__icon_color = value
        self._set_enum_attr("iconColor", value, ColorEnums)

    # highlight_color
    @property
    def highlight_color(self) -> Optional[ColorValue]:
        return self.__highlight_color

    @highlight_color.setter
    def highlight_color(self, value: Optional[ColorValue]):
        self.__highlight_color = value
        self._set_enum_attr("highlightColor", value, ColorEnums)

    # selected_icon_color
    @property
    def selected_icon_color(self) -> Optional[ColorValue]:
        return self.__selected_icon_color

    @selected_icon_color.setter
    def selected_icon_color(self, value: Optional[ColorValue]):
        self.__selected_icon_color = value
        self._set_enum_attr("selectedIconColor", value, ColorEnums)

    # bgcolor
    @property
    def bgcolor(self) -> Optional[ColorValue]:
        return self.__bgcolor

    @bgcolor.setter
    def bgcolor(self, value: Optional[ColorValue]):
        self.__bgcolor = value
        self._set_enum_attr("bgcolor", value, ColorEnums)

    # hover_color
    @property
    def hover_color(self) -> Optional[ColorValue]:
        return self.__hover_color

    @hover_color.setter
    def hover_color(self, value: Optional[ColorValue]):
        self.__hover_color = value
        self._set_enum_attr("hoverColor", value, ColorEnums)

    # focus_color
    @property
    def focus_color(self) -> Optional[ColorValue]:
        return self.__focus_color

    @focus_color.setter
    def focus_color(self, value: Optional[ColorValue]):
        self.__focus_color = value
        self._set_enum_attr("focusColor", value, ColorEnums)

    # disabled_color
    @property
    def disabled_color(self) -> Optional[ColorValue]:
        return self.__disabled_color

    @disabled_color.setter
    def disabled_color(self, value: Optional[ColorValue]):
        self.__disabled_color = value
        self._set_enum_attr("disabledColor", value, ColorEnums)

    # padding
    @property
    def padding(self) -> Optional[PaddingValue]:
        return self.__padding

    @padding.setter
    def padding(self, value: Optional[PaddingValue]):
        self.__padding = value

    # size_constraints
    @property
    def size_constraints(self) -> Optional[BoxConstraints]:
        return self.__size_constraints

    @size_constraints.setter
    def size_constraints(self, value: Optional[BoxConstraints]):
        self.__size_constraints = value

    # selected
    @property
    def selected(self) -> bool:
        return self._get_attr("selected", data_type="bool", def_value=False)

    @selected.setter
    def selected(self, value: Optional[bool]):
        self._set_attr("selected", value)

    # enable_feedback
    @property
    def enable_feedback(self) -> bool:
        return self._get_attr("enableFeedback", data_type="bool", def_value=True)

    @enable_feedback.setter
    def enable_feedback(self, value: Optional[bool]):
        self._set_attr("enableFeedback", value)

    # style
    @property
    def style(self) -> Optional[ButtonStyle]:
        return self.__style

    @style.setter
    def style(self, value: Optional[ButtonStyle]):
        self.__style = value

    # url
    @property
    def url(self) -> Optional[str]:
        return self._get_attr("url")

    @url.setter
    def url(self, value: Optional[str]):
        self._set_attr("url", value)

    # url_target
    @property
    def url_target(self) -> Optional[UrlTarget]:
        return self.__url_target

    @url_target.setter
    def url_target(self, value: Optional[UrlTarget]):
        self.__url_target = value
        self._set_enum_attr("urlTarget", value, UrlTarget)

    # mouse_cursor
    @property
    def mouse_cursor(self) -> Optional[MouseCursor]:
        return self.__mouse_cursor

    @mouse_cursor.setter
    def mouse_cursor(self, value: Optional[MouseCursor]):
        self.__mouse_cursor = value
        self._set_enum_attr("mouseCursor", value, MouseCursor)

    # visual_density
    @property
    def visual_density(self) -> Union[None, ThemeVisualDensity, VisualDensity]:
        return self.__visual_density

    @visual_density.setter
    def visual_density(self, value: Union[None, ThemeVisualDensity, VisualDensity]):
        self.__visual_density = value
        self._set_enum_attr("visualDensity", value, (ThemeVisualDensity, VisualDensity))

    # on_click
    @property
    def on_click(self) -> OptionalControlEventCallable:
        return self._get_event_handler("click")

    @on_click.setter
    def on_click(self, handler: OptionalControlEventCallable):
        self._add_event_handler("click", handler)

    # content
    @property
    def content(self) -> Optional[Control]:
        return self.__content

    @content.setter
    def content(self, value: Optional[Control]):
        self.__content = value

    # autofocus
    @property
    def autofocus(self) -> bool:
        return self._get_attr("autofocus", data_type="bool", def_value=False)

    @autofocus.setter
    def autofocus(self, value: Optional[bool]):
        self._set_attr("autofocus", value)

    # on_focus
    @property
    def on_focus(self) -> OptionalControlEventCallable:
        return self._get_event_handler("focus")

    @on_focus.setter
    def on_focus(self, handler: OptionalControlEventCallable):
        self._add_event_handler("focus", handler)

    # on_blur
    @property
    def on_blur(self) -> OptionalControlEventCallable:
        return self._get_event_handler("blur")

    @on_blur.setter
    def on_blur(self, handler: OptionalControlEventCallable):
        self._add_event_handler("blur", handler)

    # alignment
    @property
    def alignment(self) -> Optional[Alignment]:
        return self.__alignment

    @alignment.setter
    def alignment(self, value: Optional[Alignment]):
        self.__alignment = value
