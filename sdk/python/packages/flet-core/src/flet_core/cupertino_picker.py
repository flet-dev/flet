from typing import Any, List, Optional, Union

from flet_core.constrained_control import ConstrainedControl
from flet_core.control import Control, OptionalNumber
from flet_core.ref import Ref
from flet_core.types import (
    AnimationValue,
    OffsetValue,
    ResponsiveNumber,
    RotateValue,
    ScaleValue,
    OptionalEventCallable,
)


class CupertinoPicker(ConstrainedControl):
    """
    An iOS-styled picker.

    -----

    Online docs: https://flet.dev/docs/controls/cupertinopicker
    """

    def __init__(
        self,
        controls: List[Control],
        item_extent: OptionalNumber = None,
        selected_index: Optional[int] = None,
        bgcolor: Optional[str] = None,
        use_magnifier: Optional[bool] = None,
        looping: Optional[bool] = None,
        magnification: OptionalNumber = None,
        squeeze: OptionalNumber = None,
        diameter_ratio: OptionalNumber = None,
        off_axis_fraction: OptionalNumber = None,
        on_change: OptionalEventCallable = None,
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

        self.squeeze = squeeze
        self.bgcolor = bgcolor
        self.on_change = on_change
        self.magnification = magnification
        self.diameter_ratio = diameter_ratio
        self.off_axis_fraction = off_axis_fraction
        self.use_magnifier = use_magnifier
        self.item_extent = item_extent
        self.controls = controls
        self.looping = looping
        self.selected_index = selected_index

    def _get_control_name(self):
        return "cupertinopicker"

    def _get_children(self):
        return self.__controls

    # squeeze
    @property
    def squeeze(self) -> OptionalNumber:
        return self._get_attr("squeeze", data_type="float", def_value=1.45)

    @squeeze.setter
    def squeeze(self, value: OptionalNumber):
        if value is not None and value <= 0:
            raise ValueError("CupertinoPicker.squeeze must be greater than 0")
        self._set_attr("squeeze", value)

    # bgcolor
    @property
    def bgcolor(self) -> Optional[str]:
        return self._get_attr("bgcolor")

    @bgcolor.setter
    def bgcolor(self, value: Optional[str]):
        self._set_attr("bgcolor", value)

    # use_magnifier
    @property
    def use_magnifier(self) -> Optional[bool]:
        return self._get_attr("useMagnifier", data_type="bool", def_value=False)

    @use_magnifier.setter
    def use_magnifier(self, value: Optional[bool]):
        self._set_attr("useMagnifier", value)

    # magnification
    @property
    def magnification(self) -> OptionalNumber:
        return self._get_attr("magnification", data_type="float", def_value=1.0)

    @magnification.setter
    def magnification(self, value: OptionalNumber):
        if value is not None and value <= 0:
            raise ValueError("CupertinoPicker.magnification must be greater than 0")
        self._set_attr("magnification", value)

    # item_extent
    @property
    def item_extent(self) -> OptionalNumber:
        return self._get_attr("itemExtent", data_type="float")

    @item_extent.setter
    def item_extent(self, value: OptionalNumber):
        assert (
            value is None or value > 0
        ), "item_extent cannot be negative or equal to 0"
        self._set_attr("itemExtent", value)

    # looping
    @property
    def looping(self) -> Optional[bool]:
        return self._get_attr("looping", data_type="bool", def_value=False)

    @looping.setter
    def looping(self, value: Optional[bool]):
        self._set_attr("looping", value)

    # selected_index
    @property
    def selected_index(self) -> Optional[int]:
        return self._get_attr("selectedIndex", data_type="int", def_value=0)

    @selected_index.setter
    def selected_index(self, value: Optional[int]):
        self._set_attr("selectedIndex", value)

    # diameter_ratio
    @property
    def diameter_ratio(self) -> OptionalNumber:
        return self._get_attr("diameterRatio", data_type="float", def_value=1.07)

    @diameter_ratio.setter
    def diameter_ratio(self, value: OptionalNumber):
        self._set_attr("diameterRatio", value)

    # off_axis_fraction
    @property
    def off_axis_fraction(self) -> OptionalNumber:
        return self._get_attr("offAxisFraction", data_type="float", def_value=0.0)

    @off_axis_fraction.setter
    def off_axis_fraction(self, value: OptionalNumber):
        self._set_attr("offAxisFraction", value)

    # controls
    @property
    def controls(self) -> List[Control]:
        return self.__controls

    @controls.setter
    def controls(self, value: Optional[List[Control]]):
        self.__controls = value if value is not None else []

    # on_change
    @property
    def on_change(self) -> OptionalEventCallable:
        return self._get_event_handler("change")

    @on_change.setter
    def on_change(self, handler: OptionalEventCallable):
        self._add_event_handler("change", handler)
