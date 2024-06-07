from typing import Any, List, Optional, Union

from flet_core.adaptive_control import AdaptiveControl
from flet_core.constrained_control import ConstrainedControl
from flet_core.control import Control, OptionalNumber
from flet_core.ref import Ref
from flet_core.scrollable_control import ScrollableControl
from flet_core.types import (
    AnimationValue,
    OffsetValue,
    PaddingValue,
    ResponsiveNumber,
    RotateValue,
    ScaleValue,
    ClipBehavior,
)


class SliverListView(ConstrainedControl, ScrollableControl, AdaptiveControl):
    """
    A scrollable list of controls arranged linearly.

    -----

    Online docs: https://flet.dev/docs/controls/sliverlistview
    """

    def __init__(
        self,
        controls: Optional[List[Control]] = None,
        horizontal: Optional[bool] = None,
        spacing: OptionalNumber = None,
        divider_thickness: OptionalNumber = None,
        padding: PaddingValue = None,
        clip_behavior: Optional[ClipBehavior] = None,
        cache_extent: OptionalNumber = None,
        #
        # ScrollableControl specific
        #
        on_scroll_interval: OptionalNumber = None,
        on_scroll: Any = None,
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
        )

        AdaptiveControl.__init__(self, adaptive=adaptive)

        self.controls = controls
        self.horizontal = horizontal
        self.spacing = spacing
        self.divider_thickness = divider_thickness
        self.padding = padding
        self.clip_behavior = clip_behavior
        self.cache_extent = cache_extent

    def _get_control_name(self):
        return "sliver_list_view"

    def before_update(self):
        super().before_update()
        self._set_attr_json("padding", self.__padding)

    def _get_children(self):
        return self.__controls

    def clean(self):
        super().clean()
        self.__controls.clear()

    # horizontal
    @property
    def horizontal(self) -> Optional[bool]:
        return self._get_attr("horizontal")

    @horizontal.setter
    def horizontal(self, value: Optional[bool]):
        self._set_attr("horizontal", value)

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

    # cache_extent
    @property
    def cache_extent(self) -> OptionalNumber:
        return self._get_attr("cacheExtent", data_type="float")

    @cache_extent.setter
    def cache_extent(self, value: OptionalNumber):
        self._set_attr("cacheExtent", value)

    # padding
    @property
    def padding(self) -> PaddingValue:
        return self.__padding

    @padding.setter
    def padding(self, value: PaddingValue):
        self.__padding = value

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
