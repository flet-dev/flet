from typing import Any, Optional, Union

from flet_core.constrained_control import ConstrainedControl
from flet_core.control import Control, OptionalNumber
from flet_core.gradients import Gradient
from flet_core.ref import Ref
from flet_core.types import (
    AnimationValue,
    BlendMode,
    BorderRadiusValue,
    OffsetValue,
    ResponsiveNumber,
    RotateValue,
    ScaleValue,
)


class ShaderMask(ConstrainedControl):
    """
    A control that applies a mask generated by a shader to its child.

    For example, ShaderMask can be used to gradually fade out the edge of a child by using a `LinearGradient` mask.

    Example:
    ```
    import flet as ft

    def main(page: ft.Page):
        page.add(
            ft.Row(
                [
                    ft.ShaderMask(
                        ft.Image(src="https://picsum.photos/100/200?2"),
                        blend_mode=ft.BlendMode.DST_IN,
                        shader=ft.LinearGradient(
                            begin=ft.alignment.top_center,
                            end=ft.alignment.bottom_center,
                            colors=[ft.colors.BLACK, ft.colors.TRANSPARENT],
                            stops=[0.5, 1.0],
                        ),
                        border_radius=10,
                    ),
                ]
            )
        )

    ft.app(target=main)
    ```

    -----

    Online docs: https://flet.dev/docs/controls/shadermask
    """

    def __init__(
        self,
        content: Optional[Control] = None,
        blend_mode: Optional[BlendMode] = None,
        shader: Optional[Gradient] = None,
        border_radius: BorderRadiusValue = None,
        #
        # ConstrainedControl
        #
        ref: Optional[Ref] = None,
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
        tooltip: Optional[str] = None,
        visible: Optional[bool] = None,
        disabled: Optional[bool] = None,
        data: Any = None,
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

        self.content = content
        self.blend_mode = blend_mode
        self.shader = shader
        self.border_radius = border_radius

    def _get_control_name(self):
        return "shadermask"

    def before_update(self):
        super().before_update()
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
    def content(self, value: Optional[Control]):
        self.__content = value

    # blend_mode
    @property
    def blend_mode(self) -> Optional[BlendMode]:
        return self.__blend_mode

    @blend_mode.setter
    def blend_mode(self, value: Optional[BlendMode]):
        self.__blend_mode = value
        self._set_enum_attr("blendMode", value, BlendMode)

    # shader
    @property
    def shader(self) -> Optional[Gradient]:
        return self.__shader

    @shader.setter
    def shader(self, value: Optional[Gradient]):
        self.__shader = value

    # border_radius
    @property
    def border_radius(self) -> BorderRadiusValue:
        return self.__border_radius

    @border_radius.setter
    def border_radius(self, value: BorderRadiusValue):
        self.__border_radius = value
