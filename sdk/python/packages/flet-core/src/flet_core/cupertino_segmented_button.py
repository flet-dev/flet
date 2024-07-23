from typing import Any, Optional, Union, List

from flet_core.constrained_control import ConstrainedControl
from flet_core.control import OptionalNumber, Control
from flet_core.ref import Ref
from flet_core.types import (
    AnimationValue,
    OffsetValue,
    ResponsiveNumber,
    RotateValue,
    ScaleValue,
    PaddingValue,
    OptionalEventCallable,
)


class CupertinoSegmentedButton(ConstrainedControl):
    """
    An iOS-style segmented button.

    -----

    Online docs: https://flet.dev/docs/controls/cupertinosegmentedbutton
    """

    def __init__(
        self,
        controls: List[Control],
        selected_index: Optional[int] = None,
        selected_color: Optional[str] = None,
        unselected_color: Optional[str] = None,
        border_color: Optional[str] = None,
        padding: PaddingValue = None,
        click_color: Optional[str] = None,
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
        self.controls = controls
        self.padding = padding
        self.border_color = border_color
        self.selected_index = selected_index
        self.selected_color = selected_color
        self.unselected_color = unselected_color
        self.on_change = on_change
        self.click_color = click_color

    def _get_control_name(self):
        return "cupertinosegmentedbutton"

    def _get_children(self):
        return self.__controls

    def before_update(self):
        super().before_update()
        assert (
            len(self.__controls) >= 2
        ), "CupertinoSegmentedButton must have at minimum two visible controls"

    def _before_build_command(self):
        super()._before_build_command()
        self._set_attr_json("padding", self.__padding)

    # controls
    @property
    def controls(self) -> List[Control]:
        return self.__controls

    @controls.setter
    def controls(self, value: List[Control]):
        self.__controls = value

    # border_color
    @property
    def border_color(self) -> Optional[str]:
        return self._get_attr("borderColor")

    @border_color.setter
    def border_color(self, value: Optional[str]):
        self._set_attr("borderColor", value)

    # selected_index
    @property
    def selected_index(self) -> Optional[int]:
        return self._get_attr("selectedIndex", data_type="int", def_value=0)

    @selected_index.setter
    def selected_index(self, value: Optional[int]):
        if value is not None and not (0 <= value < len(self.controls)):
            raise IndexError("selected_index out of range")
        self._set_attr("selectedIndex", value)

    # selected_color
    @property
    def selected_color(self) -> Optional[str]:
        return self._get_attr("selectedColor")

    @selected_color.setter
    def selected_color(self, value: Optional[str]):
        self._set_attr("selectedColor", value)

    # unselected_color
    @property
    def unselected_color(self) -> Optional[str]:
        return self._get_attr("unselectedColor")

    @unselected_color.setter
    def unselected_color(self, value: Optional[str]):
        self._set_attr("unselectedColor", value)

    # click_color
    @property
    def click_color(self) -> Optional[str]:
        return self._get_attr("clickColor")

    @click_color.setter
    def click_color(self, value: Optional[str]):
        self._set_attr("clickColor", value)

    # padding
    @property
    def padding(self) -> PaddingValue:
        return self.__padding

    @padding.setter
    def padding(self, value: PaddingValue):
        self.__padding = value

    # on_change
    @property
    def on_change(self) -> OptionalEventCallable:
        return self._get_event_handler("change")

    @on_change.setter
    def on_change(self, handler: OptionalEventCallable):
        self._add_event_handler("change", handler)
