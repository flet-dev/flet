from enum import Enum
from typing import Any, List, Optional, Union

from flet.core.adaptive_control import AdaptiveControl
from flet.core.animation import AnimationValue
from flet.core.badge import BadgeValue
from flet.core.constrained_control import ConstrainedControl
from flet.core.control import Control
from flet.core.ref import Ref
from flet.core.tooltip import TooltipValue
from flet.core.types import (
    OffsetValue,
    OptionalControlEventCallable,
    OptionalNumber,
    PaddingValue,
    ResponsiveNumber,
    RotateValue,
    ScaleValue,
)


class CollapseMode(Enum):
    PARALLAX = "parallax"
    PIN = "pin"
    NONE = "none"


class StretchMode(Enum):
    ZOOM_BACKGROUND = "zoomBackground"
    BLUR_BACKGROUND = "blurBackground"
    FADE_TITLE = "fadeTitle"


class FlexibleSpaceBar(ConstrainedControl, AdaptiveControl):
    """
    A flexible space bar.

    -----

    Online docs: https://flet.dev/docs/controls/flexiblespacebar
    """

    def __init__(
        self,
        title: Optional[Control] = None,
        background: Optional[Control] = None,
        center_title: Optional[bool] = None,
        expanded_title_scale: OptionalNumber = None,
        tile_padding: Optional[PaddingValue] = None,
        collapse_mode: Optional[CollapseMode] = None,
        stretch_mode: Optional[List[StretchMode]] = None,
        #
        # ConstrainedControl and AdaptiveControl
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
            tooltip=tooltip,
            badge=badge,
            visible=visible,
            disabled=disabled,
            data=data,
        )

        AdaptiveControl.__init__(self, adaptive=adaptive)

        self.title = title
        self.background = background
        self.center_title = center_title
        self.expanded_title_scale = expanded_title_scale
        self.tile_padding = tile_padding
        self.collapse_mode = collapse_mode
        self.stretch_mode = stretch_mode

    def _get_control_name(self):
        return "flexiblespacebar"

    def before_update(self):
        super().before_update()
        self._set_attr_json("tilePadding", self.__tile_padding)
        self._set_attr_json("stretchMode", self.__stretch_mode)

    def _get_children(self):
        children = []
        if self.__title:
            self.__title._set_attr_internal("n", "title")
            children.append(self.__title)
        if self.__background:
            self.__background._set_attr_internal("n", "background")
            children.append(self.__background)
        return children

    # background
    @property
    def background(self) -> Optional[Control]:
        return self.__background

    @background.setter
    def background(self, value: Optional[Control]):
        self.__background = value

    # title
    @property
    def title(self) -> Optional[Control]:
        return self.__title

    @title.setter
    def title(self, value: Optional[Control]):
        self.__title = value

    # center_title
    @property
    def center_title(self) -> bool:
        return self._get_attr("centerTitle", data_type="bool", def_value=False)

    @center_title.setter
    def center_title(self, value: Optional[bool]):
        self._set_attr("centerTitle", value)

    # expanded_title_scale
    @property
    def expanded_title_scale(self) -> OptionalNumber:
        return self._get_attr("expandedTitleScale", data_type="float")

    @expanded_title_scale.setter
    def expanded_title_scale(self, value: OptionalNumber):
        self._set_attr("expandedTitleScale", value)

    # tile_padding
    @property
    def tile_padding(self) -> Optional[PaddingValue]:
        return self.__tile_padding

    @tile_padding.setter
    def tile_padding(self, value: Optional[PaddingValue]):
        self.__tile_padding = value

    # collapse_mode
    @property
    def collapse_mode(self) -> Optional[CollapseMode]:
        return self.__collapse_mode

    @collapse_mode.setter
    def collapse_mode(self, value: Optional[CollapseMode]):
        self.__collapse_mode = value
        self._set_enum_attr("collapseMode", value, CollapseMode)

    # stretch_mode
    @property
    def stretch_mode(self) -> Optional[List[StretchMode]]:
        return self.__stretch_mode

    @stretch_mode.setter
    def stretch_mode(self, value: Optional[List[StretchMode]]):
        self.__stretch_mode = value
