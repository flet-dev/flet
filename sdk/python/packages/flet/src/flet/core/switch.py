from typing import Any, Optional, Union

from flet.core.adaptive_control import AdaptiveControl
from flet.core.animation import AnimationValue
from flet.core.badge import BadgeValue
from flet.core.constrained_control import ConstrainedControl
from flet.core.control import OptionalNumber
from flet.core.ref import Ref
from flet.core.text_style import TextStyle
from flet.core.tooltip import TooltipValue
from flet.core.types import (
    ColorEnums,
    ColorValue,
    ControlStateValue,
    LabelPosition,
    MouseCursor,
    OffsetValue,
    OptionalControlEventCallable,
    ResponsiveNumber,
    RotateValue,
    ScaleValue,
)


class Switch(ConstrainedControl, AdaptiveControl):
    """
    A toggle represents a physical switch that allows someone to choose between two mutually exclusive options.

    or example, "On/Off", "Show/Hide". Choosing an option should produce an immediate result.

    Example:
    ```
    import flet as ft

    def main(page: ft.Page):
        def theme_changed(e):
            page.theme_mode = (
                ft.ThemeMode.DARK
                if page.theme_mode == ft.ThemeMode.LIGHT
                else ft.ThemeMode.LIGHT
            )
            c.label = (
                "Light theme" if page.theme_mode == ft.ThemeMode.LIGHT else "Dark theme"
            )
            page.update()

        page.theme_mode = ft.ThemeMode.LIGHT
        c = ft.Switch(label="Light theme", on_change=theme_changed)
        page.add(c)

    ft.app(target=main)
    ```

    -----

    Online docs: https://flet.dev/docs/controls/switch
    """

    def __init__(
        self,
        label: Optional[str] = None,
        label_position: Optional[LabelPosition] = None,
        label_style: Optional[TextStyle] = None,
        value: Optional[bool] = None,
        autofocus: Optional[bool] = None,
        active_color: Optional[ColorValue] = None,
        active_track_color: Optional[ColorValue] = None,
        focus_color: Optional[ColorValue] = None,
        inactive_thumb_color: Optional[ColorValue] = None,
        inactive_track_color: Optional[ColorValue] = None,
        thumb_color: ControlStateValue[ColorValue] = None,
        thumb_icon: ControlStateValue[str] = None,
        track_color: ControlStateValue[ColorValue] = None,
        adaptive: Optional[bool] = None,
        hover_color: Optional[ColorValue] = None,
        splash_radius: OptionalNumber = None,
        overlay_color: ControlStateValue[ColorValue] = None,
        track_outline_color: ControlStateValue[ColorValue] = None,
        mouse_cursor: Optional[MouseCursor] = None,
        on_change: OptionalControlEventCallable = None,
        on_focus: OptionalControlEventCallable = None,
        on_blur: OptionalControlEventCallable = None,
        #
        # ConstrainedControl
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

        self.value = value
        self.label = label
        self.label_style = label_style
        self.label_position = label_position
        self.autofocus = autofocus
        self.active_color = active_color
        self.active_track_color = active_track_color
        self.focus_color = focus_color
        self.inactive_thumb_color = inactive_thumb_color
        self.inactive_track_color = inactive_track_color
        self.thumb_color = thumb_color
        self.thumb_icon = thumb_icon
        self.track_color = track_color
        self.on_change = on_change
        self.on_focus = on_focus
        self.on_blur = on_blur
        self.hover_color = hover_color
        self.splash_radius = splash_radius
        self.overlay_color = overlay_color
        self.track_outline_color = track_outline_color
        self.mouse_cursor = mouse_cursor

    def _get_control_name(self):
        return "switch"

    def before_update(self):
        super().before_update()
        self._set_attr_json("thumbColor", self.__thumb_color, wrap_attr_dict=True)
        self._set_attr_json("overlayColor", self.__overlay_color, wrap_attr_dict=True)
        self._set_attr_json(
            "trackOutlineColor", self.__track_outline_color, wrap_attr_dict=True
        )
        self._set_attr_json("thumbIcon", self.__thumb_icon, wrap_attr_dict=True)
        self._set_attr_json("trackColor", self.__track_color, wrap_attr_dict=True)
        self._set_attr_json("labelStyle", self.__label_style)

    # value
    @property
    def value(self) -> bool:
        return self._get_attr("value", data_type="bool", def_value=False)

    @value.setter
    def value(self, value: Optional[bool]):
        self._set_attr("value", value)

    # label
    @property
    def label(self) -> Optional[str]:
        return self._get_attr("label")

    @label.setter
    def label(self, value: Optional[str]):
        self._set_attr("label", value)

    # hover_color
    @property
    def hover_color(self) -> Optional[ColorValue]:
        return self.__hover_color

    @hover_color.setter
    def hover_color(self, value: Optional[ColorValue]):
        self.__hover_color = value
        self._set_enum_attr("hoverColor", value, ColorEnums)

    # track_outline_color
    @property
    def track_outline_color(self) -> ControlStateValue[str]:
        return self.__track_outline_color

    @track_outline_color.setter
    def track_outline_color(self, value: ControlStateValue[str]):
        self.__track_outline_color = value

    # overlay_color
    @property
    def overlay_color(self) -> ControlStateValue[str]:
        return self.__overlay_color

    @overlay_color.setter
    def overlay_color(self, value: ControlStateValue[str]):
        self.__overlay_color = value

    # splash_radius
    @property
    def splash_radius(self) -> OptionalNumber:
        return self._get_attr("splashRadius", data_type="float")

    @splash_radius.setter
    def splash_radius(self, value: OptionalNumber):
        assert value is None or value >= 0, "splash_radius cannot be negative"
        self._set_attr("splashRadius", value)

    # label_style
    @property
    def label_style(self) -> Optional[TextStyle]:
        return self.__label_style

    @label_style.setter
    def label_style(self, value: Optional[TextStyle]):
        self.__label_style = value

    # label_position
    @property
    def label_position(self) -> Optional[LabelPosition]:
        return self.__label_position

    @label_position.setter
    def label_position(self, value: Optional[LabelPosition]):
        self.__label_position = value
        self._set_enum_attr("labelPosition", value, LabelPosition)

    # mouse_cursor
    @property
    def mouse_cursor(self) -> Optional[MouseCursor]:
        return self.__mouse_cursor

    @mouse_cursor.setter
    def mouse_cursor(self, value: Optional[MouseCursor]):
        self.__mouse_cursor = value
        self._set_enum_attr("mouseCursor", value, MouseCursor)

    # autofocus
    @property
    def autofocus(self) -> bool:
        return self._get_attr("autofocus", data_type="bool", def_value=False)

    @autofocus.setter
    def autofocus(self, value: Optional[bool]):
        self._set_attr("autofocus", value)

    # active_color
    @property
    def active_color(self) -> Optional[ColorValue]:
        return self.__active_color

    @active_color.setter
    def active_color(self, value: Optional[ColorValue]):
        self.__active_color = value
        self._set_enum_attr("activeColor", value, ColorEnums)

    # active_track_color
    @property
    def active_track_color(self) -> Optional[ColorValue]:
        return self.__active_track_color

    @active_track_color.setter
    def active_track_color(self, value: Optional[ColorValue]):
        self.__active_track_color = value
        self._set_enum_attr("activeTrackColor", value, ColorEnums)

    # focus_color
    @property
    def focus_color(self) -> Optional[ColorValue]:
        return self.__focus_color

    @focus_color.setter
    def focus_color(self, value: Optional[ColorValue]):
        self.__focus_color = value
        self._set_enum_attr("focusColor", value, ColorEnums)

    # inactive_thumb_color
    @property
    def inactive_thumb_color(self) -> Optional[ColorValue]:
        return self.__inactive_thumb_color

    @inactive_thumb_color.setter
    def inactive_thumb_color(self, value: Optional[ColorValue]):
        self.__inactive_thumb_color = value
        self._set_enum_attr("inactiveThumbColor", value, ColorEnums)

    # inactive_track_color
    @property
    def inactive_track_color(self) -> Optional[ColorValue]:
        return self.__inactive_track_color

    @inactive_track_color.setter
    def inactive_track_color(self, value: Optional[ColorValue]):
        self.__inactive_track_color = value
        self._set_enum_attr("inactiveTrackColor", value, ColorEnums)

    # thumb_color
    @property
    def thumb_color(self) -> ControlStateValue[str]:
        return self.__thumb_color

    @thumb_color.setter
    def thumb_color(self, value: ControlStateValue[str]):
        self.__thumb_color = value

    # thumb_icon
    @property
    def thumb_icon(self) -> ControlStateValue[str]:
        return self.__thumb_icon

    @thumb_icon.setter
    def thumb_icon(self, value: ControlStateValue[str]):
        self.__thumb_icon = value

    # track_color
    @property
    def track_color(self) -> ControlStateValue[str]:
        return self.__track_color

    @track_color.setter
    def track_color(self, value: ControlStateValue[str]):
        self.__track_color = value

    # on_change
    @property
    def on_change(self) -> OptionalControlEventCallable:
        return self._get_event_handler("change")

    @on_change.setter
    def on_change(self, handler: OptionalControlEventCallable):
        self._add_event_handler("change", handler)

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
