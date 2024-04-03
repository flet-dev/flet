from typing import Any, Dict, Optional, Union

from flet_core.adaptive_control import AdaptiveControl
from flet_core.border import BorderSide
from flet_core.buttons import OutlinedBorder
from flet_core.constrained_control import ConstrainedControl
from flet_core.control import OptionalNumber
from flet_core.ref import Ref
from flet_core.text_style import TextStyle
from flet_core.theme import ThemeVisualDensity
from flet_core.types import (
    AnimationValue,
    LabelPosition,
    MaterialState,
    MouseCursor,
    OffsetValue,
    ResponsiveNumber,
    RotateValue,
    ScaleValue,
)


class Checkbox(ConstrainedControl, AdaptiveControl):
    """
    Checkbox allows to select one or more items from a group, or switch between two mutually exclusive options (checked or unchecked, on or off).

    Example:
    ```
    import flet as ft

    def main(page):
        def button_clicked(e):
            t.value = (
                f"Checkboxes values are:  {c1.value}, {c2.value}, {c3.value}, {c4.value}, {c5.value}."
            )
            page.update()

        t = ft.Text()
        c1 = ft.Checkbox(label="Unchecked by default checkbox", value=False)
        c2 = ft.Checkbox(label="Undefined by default tristate checkbox", tristate=True)
        c3 = ft.Checkbox(label="Checked by default checkbox", value=True)
        c4 = ft.Checkbox(label="Disabled checkbox", disabled=True)
        c5 = ft.Checkbox(
            label="Checkbox with rendered label_position='left'", label_position=ft.LabelPosition.LEFT
        )
        b = ft.ElevatedButton(text="Submit", on_click=button_clicked)
        page.add(c1, c2, c3, c4, c5, b, t)

    ft.app(target=main)
    ```

    -----

    Online docs: https://flet.dev/docs/controls/checkbox
    """

    def __init__(
        self,
        label: Optional[str] = None,
        value: Optional[bool] = None,
        label_position: Optional[LabelPosition] = None,
        label_style: Optional[TextStyle] = None,
        tristate: Optional[bool] = None,
        autofocus: Optional[bool] = None,
        fill_color: Union[None, str, Dict[MaterialState, str]] = None,
        overlay_color: Union[None, str, Dict[MaterialState, str]] = None,
        check_color: Optional[str] = None,
        active_color: Optional[str] = None,
        hover_color: Optional[str] = None,
        focus_color: Optional[str] = None,
        semantics_label: Optional[str] = None,
        shape: Optional[OutlinedBorder] = None,
        splash_radius: OptionalNumber = None,
        border_side: Union[None, BorderSide, Dict[MaterialState, BorderSide]] = None,
        is_error: Optional[bool] = None,
        visual_density: Optional[ThemeVisualDensity] = None,
        mouse_cursor: Optional[MouseCursor] = None,
        on_change=None,
        on_focus=None,
        on_blur=None,
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
            visible=visible,
            disabled=disabled,
            data=data,
        )

        AdaptiveControl.__init__(self, adaptive=adaptive)

        self.value = value
        self.tristate = tristate
        self.label = label
        self.label_style = label_style
        self.label_position = label_position
        self.autofocus = autofocus
        self.check_color = check_color
        self.fill_color = fill_color
        self.focus_color = focus_color
        self.hover_color = hover_color
        self.overlay_color = overlay_color
        self.active_color = active_color
        self.semantics_label = semantics_label
        self.shape = shape
        self.splash_radius = splash_radius
        self.border_side = border_side
        self.is_error = is_error
        self.on_change = on_change
        self.on_focus = on_focus
        self.on_blur = on_blur
        self.visual_density = visual_density
        self.mouse_cursor = mouse_cursor

    def _get_control_name(self):
        return "checkbox"

    def before_update(self):
        super().before_update()
        self._set_attr_json("fillColor", self.__fill_color)
        self._set_attr_json("overlayColor", self.__overlay_color)
        self._set_attr_json("shape", self.__shape)
        self._set_attr_json("borderSide", self.__border_side)
        if isinstance(self.__label_style, TextStyle):
            self._set_attr_json("labelStyle", self.__label_style)

    # value
    @property
    def value(self) -> Optional[bool]:
        return self._get_attr(
            "value", data_type="bool?", def_value=False if not self.tristate else None
        )

    @value.setter
    def value(self, value: Optional[bool]):
        self._set_attr("value", value)

    # tristate
    @property
    def tristate(self) -> Optional[bool]:
        return self._get_attr("tristate", data_type="bool", def_value=False)

    @tristate.setter
    def tristate(self, value: Optional[bool]):
        self._set_attr("tristate", value)

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
        self._set_attr(
            "labelPosition", value.value if isinstance(value, LabelPosition) else value
        )

    # mouse_cursor
    @property
    def mouse_cursor(self) -> Optional[MouseCursor]:
        return self.__mouse_cursor

    @mouse_cursor.setter
    def mouse_cursor(self, value: Optional[MouseCursor]):
        self.__mouse_cursor = value
        self._set_attr(
            "mouseCursor",
            value.value if isinstance(value, MouseCursor) else value,
        )

    # visual_density
    @property
    def visual_density(self) -> Optional[ThemeVisualDensity]:
        return self.__visual_density

    @visual_density.setter
    def visual_density(self, value: Optional[ThemeVisualDensity]):
        self.__visual_density = value
        self._set_attr(
            "visualDensity",
            value.value if isinstance(value, ThemeVisualDensity) else value,
        )

    # autofocus
    @property
    def autofocus(self) -> Optional[bool]:
        return self._get_attr("autofocus", data_type="bool", def_value=False)

    @autofocus.setter
    def autofocus(self, value: Optional[bool]):
        self._set_attr("autofocus", value)

    # check_color
    @property
    def check_color(self) -> Optional[str]:
        return self._get_attr("checkColor")

    @check_color.setter
    def check_color(self, value: Optional[str]):
        self._set_attr("checkColor", value)

    # active_color
    @property
    def active_color(self) -> Optional[str]:
        return self._get_attr("activeColor")

    @active_color.setter
    def active_color(self, value: Optional[str]):
        self._set_attr("activeColor", value)

    # focus_color
    @property
    def focus_color(self) -> Optional[str]:
        return self._get_attr("focusColor")

    @focus_color.setter
    def focus_color(self, value: Optional[str]):
        self._set_attr("focusColor", value)

    # hover_color
    @property
    def hover_color(self) -> Optional[str]:
        return self._get_attr("hoverColor")

    @hover_color.setter
    def hover_color(self, value: Optional[str]):
        self._set_attr("hoverColor", value)

    # fill_color
    @property
    def fill_color(self) -> Union[None, str, Dict[MaterialState, str]]:
        return self.__fill_color

    @fill_color.setter
    def fill_color(self, value: Union[None, str, Dict[MaterialState, str]]):
        self.__fill_color = value

    # overlay_color
    @property
    def overlay_color(self) -> Union[None, str, Dict[MaterialState, str]]:
        return self.__overlay_color

    @overlay_color.setter
    def overlay_color(self, value: Union[None, str, Dict[MaterialState, str]]):
        self.__overlay_color = value

    # label_style
    @property
    def label_style(self) -> Optional[TextStyle]:
        return self.__label_style

    @label_style.setter
    def label_style(self, value: Optional[TextStyle]):
        self.__label_style = value

    # semantics_label
    @property
    def semantics_label(self) -> Optional[str]:
        return self._get_attr("semanticsLabel")

    @semantics_label.setter
    def semantics_label(self, value: Optional[str]):
        self._set_attr("semanticsLabel", value)

    # shape
    @property
    def shape(self) -> Optional[OutlinedBorder]:
        return self.__shape

    @shape.setter
    def shape(self, value: Optional[OutlinedBorder]):
        self.__shape = value

    # splash_radius
    @property
    def splash_radius(self) -> Optional[float]:
        return self._get_attr("splashRadius", data_type="float")

    @splash_radius.setter
    def splash_radius(self, value: OptionalNumber):
        self._set_attr("splashRadius", value)

    # is_error
    @property
    def is_error(self) -> Optional[bool]:
        return self._get_attr("isError", data_type="bool", def_value=False)

    @is_error.setter
    def is_error(self, value: Optional[bool]):
        self._set_attr("isError", value)

    # border_side
    @property
    def border_side(self) -> Union[None, BorderSide, Dict[MaterialState, BorderSide]]:
        return self.__border_side

    @border_side.setter
    def border_side(
        self, value: Union[None, BorderSide, Dict[MaterialState, BorderSide]]
    ):
        self.__border_side = value

    # on_change
    @property
    def on_change(self):
        return self._get_event_handler("change")

    @on_change.setter
    def on_change(self, handler):
        self._add_event_handler("change", handler)

    # on_focus
    @property
    def on_focus(self):
        return self._get_event_handler("focus")

    @on_focus.setter
    def on_focus(self, handler):
        self._add_event_handler("focus", handler)

    # on_blur
    @property
    def on_blur(self):
        return self._get_event_handler("blur")

    @on_blur.setter
    def on_blur(self, handler):
        self._add_event_handler("blur", handler)
