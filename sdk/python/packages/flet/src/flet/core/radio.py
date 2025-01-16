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
    ThemeVisualDensity,
    VisualDensity,
)

try:
    from typing import Literal
except ImportError:
    from typing_extensions import Literal


class Radio(ConstrainedControl, AdaptiveControl):
    """
    Radio buttons let people select a single option from two or more choices.

    Example:
    ```
    import flet as ft

    def main(page):
    def button_clicked(e):
        t.value = f"Your favorite color is:  {cg.value}"
        page.update()

    t = ft.Text()
    b = ft.ElevatedButton(text='Submit', on_click=button_clicked)
    cg = ft.RadioGroup(content=ft.Column([
        ft.Radio(value="red", label="Red"),
        ft.Radio(value="green", label="Green"),
        ft.Radio(value="blue", label="Blue")]))

    page.add(ft.Text("Select your favorite color:"), cg, b, t)

    ft.app(target=main)
    ```

    -----

    Online docs: https://flet.dev/docs/controls/radio
    """

    def __init__(
        self,
        label: Optional[str] = None,
        label_position: Optional[LabelPosition] = None,
        label_style: Optional[TextStyle] = None,
        value: Optional[str] = None,
        autofocus: Optional[bool] = None,
        fill_color: ControlStateValue[ColorValue] = None,
        active_color: Optional[ColorValue] = None,
        overlay_color: ControlStateValue[ColorValue] = None,
        hover_color: Optional[ColorValue] = None,
        focus_color: Optional[ColorValue] = None,
        splash_radius: OptionalNumber = None,
        toggleable: Optional[bool] = None,
        visual_density: Union[None, ThemeVisualDensity, VisualDensity] = None,
        mouse_cursor: Optional[MouseCursor] = None,
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

        self.value = value
        self.label = label
        self.label_style = label_style
        self.label_position = label_position
        self.autofocus = autofocus
        self.fill_color = fill_color
        self.active_color = active_color
        self.on_focus = on_focus
        self.on_blur = on_blur
        self.overlay_color = overlay_color
        self.hover_color = hover_color
        self.focus_color = focus_color
        self.splash_radius = splash_radius
        self.toggleable = toggleable
        self.visual_density = visual_density
        self.mouse_cursor = mouse_cursor

    def _get_control_name(self):
        return "radio"

    def before_update(self):
        super().before_update()
        self._set_attr_json("fillColor", self.__fill_color, wrap_attr_dict=True)
        self._set_attr_json("overlayColor", self.__overlay_color, wrap_attr_dict=True)
        self._set_attr_json("labelStyle", self.__label_style)

    # value
    @property
    def value(self) -> Optional[str]:
        return self._get_attr("value", def_value="")

    @value.setter
    def value(self, value: Optional[str]):
        self._set_attr("value", value)

    # active_color
    @property
    def active_color(self) -> Optional[ColorValue]:
        return self.__active_color

    @active_color.setter
    def active_color(self, value: Optional[ColorValue]):
        self.__active_color = value
        self._set_enum_attr("activeColor", value, ColorEnums)

    # focus_color
    @property
    def focus_color(self) -> Optional[ColorValue]:
        return self.__focus_color

    @focus_color.setter
    def focus_color(self, value: Optional[ColorValue]):
        self.__focus_color = value
        self._set_enum_attr("focusColor", value, ColorEnums)

    # splash_radius
    @property
    def splash_radius(self) -> OptionalNumber:
        return self._get_attr("splashRadius", data_type="float")

    @splash_radius.setter
    def splash_radius(self, value: OptionalNumber):
        self._set_attr("splashRadius", value)

    # toggleable
    @property
    def toggleable(self) -> bool:
        return self._get_attr("toggleable", data_type="bool", def_value=False)

    @toggleable.setter
    def toggleable(self, value: Optional[bool]):
        self._set_attr("toggleable", value)

    # visual_density
    @property
    def visual_density(self) -> Union[None, ThemeVisualDensity, VisualDensity]:
        return self.__visual_density

    @visual_density.setter
    def visual_density(self, value: Union[None, ThemeVisualDensity, VisualDensity]):
        self.__visual_density = value
        self._set_enum_attr("visualDensity", value, (ThemeVisualDensity, VisualDensity))

    # label
    @property
    def label(self) -> Optional[str]:
        return self._get_attr("label")

    @label.setter
    def label(self, value: Optional[str]):
        self._set_attr("label", value)

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

    # label_style
    @property
    def label_style(self) -> Optional[TextStyle]:
        return self.__label_style

    @label_style.setter
    def label_style(self, value: Optional[TextStyle]):
        self.__label_style = value

    # fill_color
    @property
    def fill_color(self) -> ControlStateValue[str]:
        return self.__fill_color

    @fill_color.setter
    def fill_color(self, value: ControlStateValue[str]):
        self.__fill_color = value

    # overlay_color
    @property
    def overlay_color(self) -> ControlStateValue[str]:
        return self.__overlay_color

    @overlay_color.setter
    def overlay_color(self, value: ControlStateValue[str]):
        self.__overlay_color = value

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

    # autofocus
    @property
    def autofocus(self) -> bool:
        return self._get_attr("autofocus", data_type="bool", def_value=False)

    @autofocus.setter
    def autofocus(self, value: Optional[bool]):
        self._set_attr("autofocus", value)
