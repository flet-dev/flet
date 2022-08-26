from typing import Any, List, Optional, Union

from beartype import beartype

from flet.constrained_control import ConstrainedControl
from flet.control import Control, OptionalNumber
from flet.ref import Ref
from flet.types import AnimationValue, OffsetValue, RotateValue, ScaleValue

try:
    from typing import Literal
except:
    from typing_extensions import Literal

ClipBehavior = Literal[None, "none", "antiAlias", "antiAliasWithSaveLayer", "hardEdge"]


class Stack(ConstrainedControl):
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
        visible: Optional[bool] = None,
        disabled: Optional[bool] = None,
        data: Any = None,
        #
        # Stack-specific
        #
        clip_behavior: ClipBehavior = None,
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
        self.__controls = value or []

    # clip_behavior
    @property
    def clip_behavior(self) -> Optional[ClipBehavior]:
        return self._get_attr("clipBehavior")

    @clip_behavior.setter
    @beartype
    def clip_behavior(self, value: Optional[ClipBehavior]):
        self._set_attr("clipBehavior", value)
