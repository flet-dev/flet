from typing import Any, List, Optional, Union

from flet.core.adaptive_control import AdaptiveControl
from flet.core.animation import AnimationValue
from flet.core.constrained_control import ConstrainedControl
from flet.core.control import Control
from flet.core.ref import Ref
from flet.core.scrollable_control import ScrollableControl
from flet.core.sliver import Sliver
from flet.core.types import (
    ClipBehavior,
    OffsetValue,
    OptionalNumber,
    ResponsiveNumber,
    RotateValue,
    ScaleValue,
)


class SliverListView(ConstrainedControl, ScrollableControl, AdaptiveControl, Sliver):
    """
    A sliver that places multiple box children in a linear array along the main axis.

    -----

    Online docs: https://flet.dev/docs/controls/sliverlistview
    """

    def __init__(
        self,
        controls: Optional[List[Control]] = None,
        spacing: OptionalNumber = None,
        divider_thickness: OptionalNumber = None,
        #
        # ScrollableControl
        #
        on_scroll_interval: OptionalNumber = None,
        on_scroll: Any = None,
        reverse: Optional[bool] = None,
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
        on_animation_end=None,
        visible: Optional[bool] = None,
        disabled: Optional[bool] = None,
        data: Any = None,
        #
        # AdaptiveControl
        #
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
            visible=visible,
            disabled=disabled,
            data=data,
        )

        ScrollableControl.__init__(
            self,
            on_scroll_interval=on_scroll_interval,
            on_scroll=on_scroll,
            reverse=reverse,
        )

        AdaptiveControl.__init__(self, adaptive=adaptive)

        self.controls = controls
        self.spacing = spacing
        self.divider_thickness = divider_thickness

    def _get_control_name(self):
        return "sliverlistview"

    def before_update(self):
        super().before_update()

    def _get_children(self):
        return self.__controls

    # spacing
    @property
    def spacing(self) -> OptionalNumber:
        return self._get_attr("spacing", data_type="float")

    @spacing.setter
    def spacing(self, value: OptionalNumber):
        self._set_attr("spacing", value)

    # divider_thickness
    @property
    def divider_thickness(self) -> OptionalNumber:
        return self._get_attr("dividerThickness")

    @divider_thickness.setter
    def divider_thickness(self, value: OptionalNumber):
        self._set_attr("dividerThickness", value)

    # controls
    @property
    def controls(self) -> List[Control]:
        return self.__controls

    @controls.setter
    def controls(self, value: List[Control]):
        self.__controls = value if value is not None else []

    # clip_behavior
    @property
    def clip_behavior(self) -> Optional[ClipBehavior]:
        return self.__clip_behavior

    @clip_behavior.setter
    def clip_behavior(self, value: Optional[ClipBehavior]):
        self.__clip_behavior = value
        self._set_enum_attr("clipBehavior", value, ClipBehavior)
