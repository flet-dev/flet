from typing import Any, Optional, Union

from flet.core.animation import AnimationValue
from flet.core.badge import BadgeValue
from flet.core.constrained_control import ConstrainedControl
from flet.core.control import OptionalNumber
from flet.core.ref import Ref
from flet.core.tooltip import TooltipValue
from flet.core.types import (
    ColorEnums,
    ColorValue,
    OffsetValue,
    OptionalControlEventCallable,
    ResponsiveNumber,
    RotateValue,
    ScaleValue,
    StrokeCap,
)


class ProgressRing(ConstrainedControl):
    """
    A material design circular progress indicator, which spins to indicate that the application is busy.

    A control that shows progress along a circle.

    Example:

    ```
    from time import sleep
    import flet as ft

    def main(page: ft.Page):
        pr = ft.ProgressRing(width=16, height=16, stroke_width = 2)

        page.add(
            ft.Text("Circular progress indicator", style="headlineSmall"),
            ft.Row([pr, ft.Text("Wait for the completion...")]),
            ft.Text("Indeterminate circular progress", style="headlineSmall"),
            ft.Column(
                [ft.ProgressRing(), ft.Text("I'm going to run for ages...")],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            ),
        )

        for i in range(0, 101):
            pr.value = i * 0.01
            sleep(0.1)
            page.update()

    ft.app(target=main)
    ```

    -----

    Online docs: https://flet.dev/docs/controls/progressring
    """

    def __init__(
        self,
        value: OptionalNumber = None,
        stroke_width: OptionalNumber = None,
        color: Optional[ColorValue] = None,
        bgcolor: Optional[ColorValue] = None,
        stroke_align: OptionalNumber = None,
        stroke_cap: Optional[StrokeCap] = None,
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
        animate_opacity: Optional[AnimationValue] = None,
        animate_size: Optional[AnimationValue] = None,
        animate_position: Optional[AnimationValue] = None,
        animate_rotation: Optional[AnimationValue] = None,
        animate_scale: Optional[AnimationValue] = None,
        animate_offset: Optional[AnimationValue] = None,
        on_animation_end: OptionalControlEventCallable = None,
        tooltip: TooltipValue = None,
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
        self.value = value
        self.stroke_width = stroke_width
        self.color = color
        self.bgcolor = bgcolor
        self.semantics_label = semantics_label
        self.semantics_value = semantics_value
        self.stroke_align = stroke_align
        self.stroke_cap = stroke_cap

    def _get_control_name(self):
        return "progressring"

    # value
    @property
    def value(self) -> OptionalNumber:
        return self._get_attr("value", data_type="float")

    @value.setter
    def value(self, value: OptionalNumber):
        self._set_attr("value", value)

    # stroke_width
    @property
    def stroke_width(self) -> float:
        return self._get_attr("strokeWidth", data_type="float", def_value=4.0)

    @stroke_width.setter
    def stroke_width(self, value: OptionalNumber):
        assert value is None or value >= 0, "stroke_width cannot be negative"
        self._set_attr("strokeWidth", value)

    # stroke_align
    @property
    def stroke_align(self) -> float:
        return self._get_attr("strokeAlign", data_type="float", def_value=0.0)

    @stroke_align.setter
    def stroke_align(self, value: OptionalNumber):
        self._set_attr("strokeAlign", value)

    # stroke_cap
    @property
    def stroke_cap(self) -> Optional[StrokeCap]:
        return self.__stroke_cap

    @stroke_cap.setter
    def stroke_cap(self, value: Optional[StrokeCap]):
        self.__stroke_cap = value
        self._set_enum_attr("strokeCap", value, StrokeCap)

    # color
    @property
    def color(self) -> Optional[ColorValue]:
        return self.__color

    @color.setter
    def color(self, value: Optional[ColorValue]):
        self.__color = value
        self._set_enum_attr("color", value, ColorEnums)

    # bgcolor
    @property
    def bgcolor(self) -> Optional[ColorValue]:
        return self.__bgcolor

    @bgcolor.setter
    def bgcolor(self, value: Optional[ColorValue]):
        self.__bgcolor = value
        self._set_enum_attr("bgcolor", value, ColorEnums)
