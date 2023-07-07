from typing import Any, Optional, Union

from flet_core.constrained_control import ConstrainedControl
from flet_core.control import Control, OptionalNumber
from flet_core.ref import Ref
from flet_core.types import (
    AnimationValue,
    OffsetValue,
    PaddingValue,
    ResponsiveNumber,
    RotateValue,
    ScaleValue,
)


class SafeArea(ConstrainedControl):
    def __init__(
        self,
        content: Optional[Control] = None,
        ref: Optional[Ref] = None,
        width: OptionalNumber = None,
        height: OptionalNumber = None,
        expand: Union[None, bool, int] = None,
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
        tooltip: Optional[str] = None,
        visible: Optional[bool] = None,
        disabled: Optional[bool] = None,
        data: Any = None,
        #
        # Specific
        #
        key: Optional[str] = None,
        left: Optional[bool] = None,
        top: Optional[bool] = None,
        right: Optional[bool] = None,
        bottom: Optional[bool] = None,
        maintain_bottom_view_padding: Optional[bool] = None,
        minimum: PaddingValue = None,
    ):
        ConstrainedControl.__init__(
            self,
            ref=ref,
            key=key,
            width=width,
            height=height,
            expand=expand,
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

        self.content = content
        self.left = left
        self.top = top
        self.right = right
        self.bottom = bottom
        self.maintain_bottom_view_padding = maintain_bottom_view_padding
        self.minimum = minimum

    def _get_control_name(self):
        return "safearea"

    def _before_build_command(self):
        super()._before_build_command()
        self._set_attr_json("minimum", self.__minimum)

    def _get_children(self):
        children = []
        if self.__content is not None:
            self.__content._set_attr_internal("n", "content")
            children.append(self.__content)
        return children

    # left
    @property
    def left(self) -> Optional[bool]:
        return self._get_attr("left", data_type="bool", def_value=True)

    @left.setter
    def left(self, value: Optional[bool]):
        self._set_attr("left", value)

    # top
    @property
    def top(self) -> Optional[bool]:
        return self._get_attr("top", data_type="bool", def_value=True)

    @top.setter
    def top(self, value: Optional[bool]):
        self._set_attr("top", value)

    # right
    @property
    def right(self) -> Optional[bool]:
        return self._get_attr("right", data_type="bool", def_value=True)

    @right.setter
    def right(self, value: Optional[bool]):
        self._set_attr("right", value)

    # bottom
    @property
    def bottom(self) -> Optional[bool]:
        return self._get_attr("bottom", data_type="bool", def_value=True)

    @bottom.setter
    def bottom(self, value: Optional[bool]):
        self._set_attr("bottom", value)

    # maintain_bottom_view_padding
    @property
    def maintain_bottom_view_padding(self) -> Optional[bool]:
        return self._get_attr(
            "maintainBottomViewPadding", data_type="bool", def_value=False
        )

    @maintain_bottom_view_padding.setter
    def maintain_bottom_view_padding(self, value: Optional[bool]):
        self._set_attr("maintainBottomViewPadding", value)

    # content
    @property
    def content(self) -> Optional[Control]:
        return self.__content

    @content.setter
    def content(self, value: Optional[Control]):
        self.__content = value

    # minimum
    @property
    def minimum(self) -> PaddingValue:
        return self.__minimum

    @minimum.setter
    def minimum(self, value: PaddingValue):
        self.__minimum = value
