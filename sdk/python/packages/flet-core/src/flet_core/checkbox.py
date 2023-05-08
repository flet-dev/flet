from typing import Any, Dict, Optional, Union

from flet_core.constrained_control import ConstrainedControl
from flet_core.control import OptionalNumber
from flet_core.ref import Ref
from flet_core.types import (
    AnimationValue,
    LabelPosition,
    LabelPositionString,
    MaterialState,
    OffsetValue,
    ResponsiveNumber,
    RotateValue,
    ScaleValue,
)

try:
    from typing import Literal
except ImportError:
    from typing_extensions import Literal


class Checkbox(ConstrainedControl):
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
        label: Optional[str] = None,
        label_position: LabelPosition = LabelPosition.NONE,
        value: Optional[bool] = None,
        tristate: Optional[bool] = None,
        autofocus: Optional[bool] = None,
        fill_color: Union[None, str, Dict[MaterialState, str]] = None,
        check_color: Optional[str] = None,
        on_change=None,
        on_focus=None,
        on_blur=None,
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
        self.value = value
        self.tristate = tristate
        self.label = label
        self.label_position = label_position
        self.autofocus = autofocus
        self.check_color = check_color
        self.fill_color = fill_color
        self.on_change = on_change
        self.on_focus = on_focus
        self.on_blur = on_blur

    def _get_control_name(self):
        return "checkbox"

    def _before_build_command(self):
        super()._before_build_command()
        self._set_attr_json("fillColor", self.__fill_color)

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
    def label(self):
        return self._get_attr("label")

    @label.setter
    def label(self, value):
        self._set_attr("label", value)

    # label_position
    @property
    def label_position(self) -> LabelPosition:
        return self.__label_position

    @label_position.setter
    def label_position(self, value: LabelPosition):
        self.__label_position = value
        if isinstance(value, LabelPosition):
            self._set_attr("labelPosition", value.value)
        else:
            self.__set_label_position(value)

    def __set_label_position(self, value: LabelPositionString):
        self._set_attr("labelPosition", value)

    # autofocus
    @property
    def autofocus(self) -> Optional[bool]:
        return self._get_attr("autofocus", data_type="bool", def_value=False)

    @autofocus.setter
    def autofocus(self, value: Optional[bool]):
        self._set_attr("autofocus", value)

    # check_color
    @property
    def check_color(self):
        return self._get_attr("checkColor")

    @check_color.setter
    def check_color(self, value):
        self._set_attr("checkColor", value)

    # fill_color
    @property
    def fill_color(self) -> Union[None, str, Dict[MaterialState, str]]:
        return self.__fill_color

    @fill_color.setter
    def fill_color(self, value: Union[None, str, Dict[MaterialState, str]]):
        self.__fill_color = value

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
