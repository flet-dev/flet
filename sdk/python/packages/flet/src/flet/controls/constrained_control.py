from typing import Optional

from flet.controls.animation import AnimationValue
from flet.controls.base_control import control
from flet.controls.control import Control
from flet.controls.transform import OffsetValue, RotateValue, ScaleValue
from flet.controls.types import OptionalControlEventCallable, OptionalNumber

__all__ = ["ConstrainedControl"]


@control(kw_only=True)
class ConstrainedControl(Control):
    key: Optional[str] = None
    width: OptionalNumber = None
    height: OptionalNumber = None
    left: OptionalNumber = None
    top: OptionalNumber = None
    right: OptionalNumber = None
    bottom: OptionalNumber = None
    rotate: Optional[RotateValue] = None
    scale: Optional[ScaleValue] = None
    offset: Optional[OffsetValue] = None
    aspect_ratio: OptionalNumber = None
    animate_opacity: Optional[AnimationValue] = None
    animate_size: Optional[AnimationValue] = None
    animate_position: Optional[AnimationValue] = None
    animate_rotation: Optional[AnimationValue] = None
    animate_scale: Optional[AnimationValue] = None
    animate_offset: Optional[AnimationValue] = None
    on_animation_end: OptionalControlEventCallable = None
