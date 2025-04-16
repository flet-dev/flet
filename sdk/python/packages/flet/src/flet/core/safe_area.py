from typing import Any, Optional, Union

from flet.core.adaptive_control import AdaptiveControl
from flet.core.animation import AnimationValue
from flet.core.badge import BadgeValue
from flet.core.constrained_control import ConstrainedControl
from flet.core.control import Control, OptionalNumber
from flet.core.ref import Ref
from flet.core.tooltip import TooltipValue
from flet.core.types import (
    OffsetValue,
    OptionalControlEventCallable,
    PaddingValue,
    ResponsiveNumber,
    RotateValue,
    ScaleValue,
)


class SafeArea(ConstrainedControl, AdaptiveControl):
    def __init__(
        self,
        content: Control,
        left: Optional[bool] = None,
        top: Optional[bool] = None,
        right: Optional[bool] = None,
        bottom: Optional[bool] = None,
        maintain_bottom_view_padding: Optional[bool] = None,
        minimum_padding: Optional[PaddingValue] = None,
        #
        # ConstrainedControl
        #
        ref: Optional[Ref] = None,
        key: Optional[str] = None,
        width: OptionalNumber = None,
        height: OptionalNumber = None,
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
        rtl: Optional[bool] = None,
        #
        # Adaptive
        #
        adaptive: Optional[bool] = None,
    ):
        ConstrainedControl.__init__(
            self,
            ref=ref,
            key=key,
            width=width,
            height=height,
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
            rtl=rtl,
        )

        AdaptiveControl.__init__(self, adaptive=adaptive)

        self.content = content
        self.left = left
        self.top = top
        self.right = right
        self.bottom = bottom
        self.maintain_bottom_view_padding = maintain_bottom_view_padding
        self.minimum_padding = minimum_padding

    def _get_control_name(self):
        return "safearea"

    def before_update(self):
        super().before_update()
        assert self.__content.visible, "content must be visible"
        self._set_attr_json("minimumPadding", self.__minimum_padding)

    def _get_children(self):
        self.__content._set_attr_internal("n", "content")
        return [self.__content]

    # left
    @property
    def left(self) -> bool:
        return self._get_attr("left", data_type="bool", def_value=True)

    @left.setter
    def left(self, value: Optional[bool]):
        self._set_attr("left", value)

    # top
    @property
    def top(self) -> bool:
        return self._get_attr("top", data_type="bool", def_value=True)

    @top.setter
    def top(self, value: Optional[bool]):
        self._set_attr("top", value)

    # right
    @property
    def right(self) -> bool:
        return self._get_attr("right", data_type="bool", def_value=True)

    @right.setter
    def right(self, value: Optional[bool]):
        self._set_attr("right", value)

    # bottom
    @property
    def bottom(self) -> bool:
        return self._get_attr("bottom", data_type="bool", def_value=True)

    @bottom.setter
    def bottom(self, value: Optional[bool]):
        self._set_attr("bottom", value)

    # maintain_bottom_view_padding
    @property
    def maintain_bottom_view_padding(self) -> bool:
        return self._get_attr(
            "maintainBottomViewPadding", data_type="bool", def_value=False
        )

    @maintain_bottom_view_padding.setter
    def maintain_bottom_view_padding(self, value: Optional[bool]):
        self._set_attr("maintainBottomViewPadding", value)

    # content
    @property
    def content(self) -> Control:
        return self.__content

    @content.setter
    def content(self, value: Control):
        self.__content = value

    # minimum_padding
    @property
    def minimum_padding(self) -> Optional[PaddingValue]:
        return self.__minimum_padding

    @minimum_padding.setter
    def minimum_padding(self, value: Optional[PaddingValue]):
        self.__minimum_padding = value
