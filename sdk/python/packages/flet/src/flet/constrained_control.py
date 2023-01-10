from typing import Any, Optional, Union

from beartype import beartype

from flet.control import Control, OptionalNumber
from flet.ref import Ref
from flet.types import (
    AnimationValue,
    OffsetValue,
    ResponsiveNumber,
    RotateValue,
    ScaleValue,
)


class ConstrainedControl(Control):
    def __init__(
        self,
        ref: Optional[Ref] = None,
        expand: Union[None, bool, int] = None,
        col: Optional[ResponsiveNumber] = None,
        opacity: OptionalNumber = None,
        tooltip: Optional[str] = None,
        visible: Optional[bool] = None,
        disabled: Optional[bool] = None,
        data: Any = None,
        #
        # ConstrainedControl specific
        #
        width: OptionalNumber = None,
        height: OptionalNumber = None,
        left: OptionalNumber = None,
        top: OptionalNumber = None,
        right: OptionalNumber = None,
        bottom: OptionalNumber = None,
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
    ):
        Control.__init__(
            self,
            ref=ref,
            expand=expand,
            col=col,
            opacity=opacity,
            tooltip=tooltip,
            visible=visible,
            disabled=disabled,
            data=data,
        )

        self.width = width
        self.height = height
        self.left = left
        self.top = top
        self.right = right
        self.bottom = bottom
        self.scale = scale
        self.rotate = rotate
        self.offset = offset
        self.aspect_ratio = aspect_ratio
        self.animate_opacity = animate_opacity
        self.animate_size = animate_size
        self.animate_position = animate_position
        self.animate_rotation = animate_rotation
        self.animate_scale = animate_scale
        self.animate_offset = animate_offset
        self.on_animation_end = on_animation_end

    def _before_build_command(self):
        super()._before_build_command()
        self._set_attr_json("rotate", self.__rotate)
        self._set_attr_json("scale", self.__scale)
        self._set_attr_json("offset", self.__offset)
        self._set_attr_json("animateOpacity", self.__animate_opacity)
        self._set_attr_json("animateSize", self.__animate_size)
        self._set_attr_json("animatePosition", self.__animate_position)
        self._set_attr_json("animateRotation", self.__animate_rotation)
        self._set_attr_json("animateScale", self.__animate_scale)
        self._set_attr_json("animateOffset", self.__animate_offset)

    # width
    @property
    def width(self) -> OptionalNumber:
        """
        Control width.
        """
        return self._get_attr("width")

    @width.setter
    @beartype
    def width(self, value: OptionalNumber):
        self._set_attr("width", value)

    # height
    @property
    def height(self) -> OptionalNumber:
        return self._get_attr("height")

    @height.setter
    @beartype
    def height(self, value: OptionalNumber):
        self._set_attr("height", value)

    # left
    @property
    def left(self) -> OptionalNumber:
        return self._get_attr("left")

    @left.setter
    @beartype
    def left(self, value: OptionalNumber):
        self._set_attr("left", value)

    # top
    @property
    def top(self) -> OptionalNumber:
        return self._get_attr("top")

    @top.setter
    @beartype
    def top(self, value: OptionalNumber):
        self._set_attr("top", value)

    # right
    @property
    def right(self) -> OptionalNumber:
        return self._get_attr("right")

    @right.setter
    @beartype
    def right(self, value: OptionalNumber):
        self._set_attr("right", value)

    # bottom
    @property
    def bottom(self) -> OptionalNumber:
        return self._get_attr("bottom")

    @bottom.setter
    @beartype
    def bottom(self, value: OptionalNumber):
        self._set_attr("bottom", value)

    # rotate
    @property
    def rotate(self) -> RotateValue:
        return self.__rotate

    @rotate.setter
    @beartype
    def rotate(self, value: RotateValue):
        self.__rotate = value

    # scale
    @property
    def scale(self) -> ScaleValue:
        return self.__scale

    @scale.setter
    @beartype
    def scale(self, value: ScaleValue):
        self.__scale = value

    # offset
    @property
    def offset(self) -> OffsetValue:
        return self.__offset

    @offset.setter
    @beartype
    def offset(self, value: OffsetValue):
        self.__offset = value

    # aspect_ratio
    @property
    def aspect_ratio(self) -> OptionalNumber:
        return self._get_attr("aspectRatio")

    @aspect_ratio.setter
    @beartype
    def aspect_ratio(self, value: OptionalNumber):
        self._set_attr("aspectRatio", value)

    # animate_opacity
    @property
    def animate_opacity(self) -> AnimationValue:
        return self.__animate_opacity

    @animate_opacity.setter
    @beartype
    def animate_opacity(self, value: AnimationValue):
        self.__animate_opacity = value

    # animate_size
    @property
    def animate_size(self) -> AnimationValue:
        return self.__animate_size

    @animate_size.setter
    @beartype
    def animate_size(self, value: AnimationValue):
        self.__animate_size = value

    # animate_position
    @property
    def animate_position(self) -> AnimationValue:
        return self.__animate_position

    @animate_position.setter
    @beartype
    def animate_position(self, value: AnimationValue):
        self.__animate_position = value

    # animate_rotation
    @property
    def animate_rotation(self) -> AnimationValue:
        return self.__animate_rotation

    @animate_rotation.setter
    @beartype
    def animate_rotation(self, value: AnimationValue):
        self.__animate_rotation = value

    # animate_scale
    @property
    def animate_scale(self) -> AnimationValue:
        return self.__animate_scale

    @animate_scale.setter
    @beartype
    def animate_scale(self, value: AnimationValue):
        self.__animate_scale = value

    # animate_offset
    @property
    def animate_offset(self) -> AnimationValue:
        return self.__animate_offset

    @animate_offset.setter
    @beartype
    def animate_offset(self, value: AnimationValue):
        self.__animate_offset = value

    # on_animation_end
    @property
    def on_animation_end(self):
        return self._get_event_handler("animation_end")

    @on_animation_end.setter
    def on_animation_end(self, handler):
        self._add_event_handler("animation_end", handler)
        if handler is not None:
            self._set_attr("onAnimationEnd", True)
        else:
            self._set_attr("onAnimationEnd", None)
