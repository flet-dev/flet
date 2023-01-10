from typing import Any, List, Optional, Union

from flet_core.constrained_control import ConstrainedControl
from flet_core.control import Control, OptionalNumber
from flet_core.ref import Ref
from flet_core.types import (
    AnimationValue,
    ClipBehavior,
    ClipBehaviorString,
    OffsetValue,
    ResponsiveNumber,
    RotateValue,
    ScaleValue,
)

try:
    from typing import Literal
except ImportError:
    from typing_extensions import Literal


class Stack(ConstrainedControl):
    """
    A control that positions its children on top of each other.

    This control is useful if you want to overlap several children in a simple way, for example having some text and an image, overlaid with a gradient and a button attached to the bottom.

    Stack is also useful if you want to implement implicit animations (https://flet.dev/docs/guides/python/animations/) that require knowing absolute position of a target value.

    Example:

    ```
    import flet as ft

    def main(page: ft.Page):
        st = ft.Stack(
            controls=[
                ft.Image(
                    src=f"https://picsum.photos/300/300",
                    width=300,
                    height=300,
                    fit=ft.ImageFit.CONTAIN,
                ),
                ft.Row(
                    controls=[
                        ft.Text(
                            "Image title",
                            color="white",
                            size=40,
                            weight="bold",
                            opacity=0.5,
                        )
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
            ],
            width=300,
            height=300,
        )

        page.add(st)

    ft.app(target=main)
    ```

    -----

    Online docs: https://flet.dev/docs/controls/stack
    """

    def __init__(
        self,
        controls: Optional[List[Control]] = None,
        ref: Optional[Ref] = None,
        width: OptionalNumber = None,
        height: OptionalNumber = None,
        left: OptionalNumber = None,
        top: OptionalNumber = None,
        right: OptionalNumber = None,
        bottom: OptionalNumber = None,
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
        visible: Optional[bool] = None,
        disabled: Optional[bool] = None,
        data: Any = None,
        #
        # Stack-specific
        #
        clip_behavior: Optional[ClipBehavior] = None,
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

        self.__controls: List[Control] = []
        self.controls = controls
        self.clip_behavior = clip_behavior

    def _get_control_name(self):
        return "stack"

    def _get_children(self):
        return self.__controls

    # controls
    @property
    def controls(self):
        return self.__controls

    @controls.setter
    def controls(self, value):
        self.__controls = value if value is not None else []

    # clip_behavior
    @property
    def clip_behavior(self) -> Optional[ClipBehavior]:
        return self.__clip_behavior

    @clip_behavior.setter
    def clip_behavior(self, value: Optional[ClipBehavior]):
        self.__clip_behavior = value
        if isinstance(value, ClipBehavior):
            self._set_attr("clipBehavior", value.value)
        else:
            self.__set_clip_behavior(value)

    def __set_clip_behavior(self, value: Optional[ClipBehaviorString]):
        self._set_attr("clipBehavior", value)
