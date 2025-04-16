from typing import Any, Optional, Union

from flet.core.animation import AnimationValue
from flet.core.badge import BadgeValue
from flet.core.constrained_control import ConstrainedControl
from flet.core.control import OptionalNumber
from flet.core.ref import Ref
from flet.core.tooltip import TooltipValue
from flet.core.types import (
    BorderRadiusValue,
    ColorEnums,
    ColorValue,
    OffsetValue,
    OptionalControlEventCallable,
    ResponsiveNumber,
    RotateValue,
    ScaleValue,
)
from flet.utils.deprecated import deprecated_property


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
        color: Optional[ColorValue] = None,
        bgcolor: Optional[ColorValue] = None,
        border_radius: Optional[BorderRadiusValue] = None,
        semantics_label: Optional[str] = None,
        semantics_value: OptionalNumber = None,
        stop_indicator_color: Optional[ColorValue] = None,
        stop_indicator_radius: OptionalNumber = None,
        track_gap: OptionalNumber = None,
        year_2023: Optional[bool] = None,
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
        self.value = value
        self.bar_height = bar_height
        self.color = color
        self.bgcolor = bgcolor
        self.border_radius = border_radius
        self.semantics_label = semantics_label
        self.semantics_value = semantics_value
        self.stop_indicator_color = stop_indicator_color
        self.stop_indicator_radius = stop_indicator_radius
        self.track_gap = track_gap
        self.year_2023 = year_2023

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
    def color(self) -> Optional[ColorValue]:
        return self.__color

    @color.setter
    def color(self, value: Optional[ColorValue]):
        self.__color = value
        self._set_enum_attr("color", value, ColorEnums)

    # semantics_label
    @property
    def semantics_label(self) -> Optional[str]:
        return self._get_attr("semanticsLabel")

    @semantics_label.setter
    def semantics_label(self, value: Optional[str]):
        self._set_attr("semanticsLabel", value)

    # bgcolor
    @property
    def bgcolor(self) -> Optional[ColorValue]:
        return self.__bgcolor

    @bgcolor.setter
    def bgcolor(self, value: Optional[ColorValue]):
        self.__bgcolor = value
        self._set_enum_attr("bgcolor", value, ColorEnums)

    # border_radius
    @property
    def border_radius(self) -> Optional[BorderRadiusValue]:
        return self.__border_radius

    @border_radius.setter
    def border_radius(self, value: Optional[BorderRadiusValue]):
        self.__border_radius = value

    # track_gap
    @property
    def track_gap(self) -> OptionalNumber:
        return self._get_attr("trackGap", data_type="float")

    @track_gap.setter
    def track_gap(self, value: OptionalNumber):
        self._set_attr("trackGap", value)

    # year_2023
    @property
    def year_2023(self) -> Optional[bool]:
        deprecated_property(
            name="year_2023",
            version="0.27.0",
            delete_version=None,  # not known for now
            reason="Set this flag to False to opt into the 2024 Slider appearance. In the future, this flag will default to False.",
        )
        return self._get_attr("year2023", data_type="bool", def_value=True)

    @year_2023.setter
    def year_2023(self, value: Optional[bool]):
        self._set_attr("year2023", value)
        if value is not None:
            deprecated_property(
                name="year_2023",
                version="0.27.0",
                delete_version=None,  # not known for now
                reason="Set this flag to False to opt into the 2024 Slider appearance. In the future, this flag will default to False.",
            )

    # stop_indicator_color
    @property
    def stop_indicator_color(self) -> Optional[ColorValue]:
        return self.__stop_indicator_color

    @stop_indicator_color.setter
    def stop_indicator_color(self, value: Optional[ColorValue]):
        self.__stop_indicator_color = value
        self._set_enum_attr("stopIndicatorColor", value, ColorEnums)

    # stop_indicator_radius
    @property
    def stop_indicator_radius(self) -> OptionalNumber:
        return self._get_attr("stopIndicatorRadius", data_type="float")

    @stop_indicator_radius.setter
    def stop_indicator_radius(self, value: OptionalNumber):
        self._set_attr("stopIndicatorRadius", value)
