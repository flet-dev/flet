from typing import Any, Optional, Union

from flet_core.constrained_control import ConstrainedControl
from flet_core.control import OptionalNumber
from flet_core.ref import Ref
from flet_core.types import (
    AnimationValue,
    BorderRadiusValue,
    OffsetValue,
    ResponsiveNumber,
    RotateValue,
    ScaleValue,
    OptionalEventCallable,
)


class ProgressBar(ConstrainedControl):
    """
    A material design linear progress indicator, also known as a progress bar.

    A control that shows progress along a line.

    Example:

    ```
    from time import sleep

    import flet as ft

    def main(page: ft.Page):
        pb = ft.ProgressBar(width=400)

        page.add(
            ft.Text("Linear progress indicator", style="headlineSmall"),
            ft.Column([ ft.Text("Doing something..."), pb]),
            ft.Text("Indeterminate progress bar", style="headlineSmall"),
            ft.ProgressBar(width=400, color="amber", bgcolor="#eeeeee"),
        )

        for i in range(0, 101):
            pb.value = i * 0.01
            sleep(0.1)
            page.update()

    ft.app(target=main)
    ```

    -----

    Online docs: https://flet.dev/docs/controls/progressbar
    """

    def __init__(
        self,
        value: OptionalNumber = None,
        bar_height: OptionalNumber = None,
        color: Optional[str] = None,
        bgcolor: Optional[str] = None,
        border_radius: BorderRadiusValue = None,
        semantics_label: Optional[str] = None,
        semantics_value: OptionalNumber = None,
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
        on_animation_end: OptionalEventCallable = None,
        tooltip: Optional[str] = None,
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
            visible=visible,
            disabled=disabled,
            data=data,
        )
        self.value = value
        self.bar_height = bar_height
        self.color = color
        self.bgcolor = bgcolor
        self.border_radius = border_radius
        self.semantics_label = semantics_label
        self.semantics_value = semantics_value

    def _get_control_name(self):
        return "progressbar"

    def before_update(self):
        super().before_update()
        self._set_attr_json("borderRadius", self.__border_radius)

    # value
    @property
    def value(self) -> OptionalNumber:
        return self._get_attr("value", data_type="float")

    @value.setter
    def value(self, value: OptionalNumber):
        assert value is None or value >= 0, "value cannot be negative"
        self._set_attr("value", value)

    # bar_height
    @property
    def bar_height(self) -> OptionalNumber:
        return self._get_attr("barHeight", data_type="float")

    @bar_height.setter
    def bar_height(self, value: OptionalNumber):
        assert value is None or value >= 0, "bar_height cannot be negative"
        self._set_attr("barHeight", value)

    # semantics_value
    @property
    def semantics_value(self) -> OptionalNumber:
        return self._get_attr("semanticsValue", data_type="float")

    @semantics_value.setter
    def semantics_value(self, value: OptionalNumber):
        assert value is None or value >= 0, "semantics_value cannot be negative"
        self._set_attr("semanticsValue", value)

    # color
    @property
    def color(self) -> Optional[str]:
        return self._get_attr("color")

    @color.setter
    def color(self, value: Optional[str]):
        self._set_attr("color", value)

    # semantics_label
    @property
    def semantics_label(self) -> Optional[str]:
        return self._get_attr("semanticsLabel")

    @semantics_label.setter
    def semantics_label(self, value: Optional[str]):
        self._set_attr("semanticsLabel", value)

    # bgcolor
    @property
    def bgcolor(self) -> Optional[str]:
        return self._get_attr("bgcolor")

    @bgcolor.setter
    def bgcolor(self, value: Optional[str]):
        self._set_attr("bgcolor", value)

    # border_radius
    @property
    def border_radius(self) -> BorderRadiusValue:
        return self.__border_radius

    @border_radius.setter
    def border_radius(self, value: BorderRadiusValue):
        self.__border_radius = value
