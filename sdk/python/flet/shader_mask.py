from typing import Any, Optional, Union

from beartype import beartype

from flet.constrained_control import ConstrainedControl
from flet.control import BlendMode, Control, OptionalNumber
from flet.gradients import Gradient
from flet.ref import Ref
from flet.types import (
    AnimationValue,
    BorderRadiusValue,
    OffsetValue,
    RotateValue,
    ScaleValue,
)


class ShaderMask(ConstrainedControl):
    def __init__(
        self,
        content: Optional[Control] = None,
        ref: Optional[Ref] = None,
        width: OptionalNumber = None,
        height: OptionalNumber = None,
        left: OptionalNumber = None,
        top: OptionalNumber = None,
        right: OptionalNumber = None,
        bottom: OptionalNumber = None,
        expand: Union[None, bool, int] = None,
        opacity: OptionalNumber = None,
        rotate: RotateValue = None,
        scale: ScaleValue = None,
        offset: OffsetValue = None,
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
        blend_mode: Optional[BlendMode] = None,
        shader: Optional[Gradient] = None,
        border_radius: BorderRadiusValue = None,
    ):
        ConstrainedControl.__init__(
            self,
            ref=ref,
            width=width,
            height=height,
            left=left,
            top=top,
            right=right,
            bottom=bottom,
            expand=expand,
            opacity=opacity,
            rotate=rotate,
            scale=scale,
            offset=offset,
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
        self.blend_mode = blend_mode
        self.shader = shader
        self.border_radius = border_radius

    def _get_control_name(self):
        return "shadermask"

    def _before_build_command(self):
        super()._before_build_command()
        self._set_attr_json("shader", self.__shader)
        self._set_attr_json("borderRadius", self.__border_radius)

    def _get_children(self):
        children = []
        if self.__content is not None:
            self.__content._set_attr_internal("n", "content")
            children.append(self.__content)
        return children

    # content
    @property
    def content(self) -> Optional[Control]:
        return self.__content

    @content.setter
    @beartype
    def content(self, value: Optional[Control]):
        self.__content = value

    # blend_mode
    @property
    def blend_mode(self) -> Optional[BlendMode]:
        return self._get_attr("blendMode")

    @blend_mode.setter
    @beartype
    def blend_mode(self, value: Optional[BlendMode]):
        self._set_attr("blendMode", value)

    # shader
    @property
    def shader(self) -> Optional[Gradient]:
        return self.__shader

    @shader.setter
    @beartype
    def shader(self, value: Optional[Gradient]):
        self.__shader = value

    # border_radius
    @property
    def border_radius(self) -> BorderRadiusValue:
        return self.__border_radius

    @border_radius.setter
    @beartype
    def border_radius(self, value: BorderRadiusValue):
        self.__border_radius = value
