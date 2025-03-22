from typing import Any, List, Optional, Union

from flet.core.adaptive_control import AdaptiveControl
from flet.core.animation import AnimationValue
from flet.core.constrained_control import ConstrainedControl
from flet.core.control import Control
from flet.core.ref import Ref
from flet.core.scrollable_control import ScrollableControl
from flet.core.sliver import Sliver
from flet.core.types import (
    OffsetValue,
    OptionalNumber,
    ResponsiveNumber,
    RotateValue,
    ScaleValue,
)


class SliverGridView(ConstrainedControl, ScrollableControl, AdaptiveControl, Sliver):
    """
    A sliver that places multiple box children in a linear array along the main axis.

    -----

    Online docs: https://flet.dev/docs/controls/slivergridview
    """

    def __init__(
        self,
        controls: Optional[List[Control]] = None,
        runs_count: Optional[int] = None,
        max_extent: Optional[int] = None,
        spacing: OptionalNumber = None,
        run_spacing: OptionalNumber = None,
        child_aspect_ratio: OptionalNumber = None,
        build_controls_on_demand: Optional[bool] = None,
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
        self.runs_count = runs_count
        self.max_extent = max_extent
        self.spacing = spacing
        self.run_spacing = run_spacing
        self.child_aspect_ratio = child_aspect_ratio
        self.build_controls_on_demand = build_controls_on_demand

    def _get_control_name(self):
        return "slivergridview"

    def _get_children(self):
        return self.__controls

    # controls
    @property
    def controls(self) -> Optional[List[Control]]:
        return self.__controls

    @controls.setter
    def controls(self, value: Optional[List[Control]]):
        self.__controls = value

    # build_controls_on_demand
    @property
    def build_controls_on_demand(self) -> Optional[bool]:
        return self._get_attr("buildControlsOnDemand", data_type="bool")

    @build_controls_on_demand.setter
    def build_controls_on_demand(self, value: Optional[bool]):
        self._set_attr("buildControlsOnDemand", value)

    # runs_count
    @property
    def runs_count(self) -> Optional[int]:
        return self._get_attr("runsCount")

    @runs_count.setter
    def runs_count(self, value: Optional[int]):
        self._set_attr("runsCount", value)

    # max_extent
    @property
    def max_extent(self) -> OptionalNumber:
        return self._get_attr("maxExtent", data_type="float")

    @max_extent.setter
    def max_extent(self, value: OptionalNumber):
        self._set_attr("maxExtent", value)

    # spacing
    @property
    def spacing(self) -> OptionalNumber:
        return self._get_attr("spacing", data_type="float")

    @spacing.setter
    def spacing(self, value: OptionalNumber):
        self._set_attr("spacing", value)

    # run_spacing
    @property
    def run_spacing(self) -> OptionalNumber:
        return self._get_attr("runSpacing", data_type="float")

    @run_spacing.setter
    def run_spacing(self, value: OptionalNumber):
        self._set_attr("runSpacing", value)

    # child_aspect_ratio
    @property
    def child_aspect_ratio(self) -> OptionalNumber:
        return self._get_attr("childAspectRatio")

    @child_aspect_ratio.setter
    def child_aspect_ratio(self, value: OptionalNumber):
        self._set_attr("childAspectRatio", value)
