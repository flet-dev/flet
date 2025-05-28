from typing import Optional

from flet.controls.animation import AnimationValue
from flet.controls.base_control import control
from flet.controls.control import Control
from flet.controls.transform import OffsetValue, RotateValue, ScaleValue
from flet.controls.types import OptionalControlEventCallable, OptionalNumber

__all__ = ["ConstrainedControl"]


@control(kw_only=True)
class ConstrainedControl(Control):
    scroll_key: Optional[str] = None
    """"""

    width: OptionalNumber = None
    """Imposed Control width in virtual pixels."""

    height: OptionalNumber = None
    """Imposed Control height in virtual pixels."""

    left: OptionalNumber = None
    """
    The distance that the child's left edge is inset from the left of it's parent.
    Effective inside the following only: `Stack`, `Page.overlay` 
    """

    top: OptionalNumber = None
    """
    The distance that the child's top edge is inset from the top of it's parent.
    Effective inside the following only: `Stack`, `Page.overlay` 
    """

    right: OptionalNumber = None
    """
    The distance that the child's right edge is inset from the right of it's parent.
    Effective inside the following only: `Stack`, `Page.overlay` 
    """

    bottom: OptionalNumber = None
    """
    The distance that the child's bottom edge is inset from the bottom of it's parent.
    Effective inside the following only: `Stack`, `Page.overlay` 
    """

    rotate: Optional[RotateValue] = None
    """
    Applies a rotation transform to the control around its center.

    The `rotate` value can be:
        - A number: Specifies the rotation in clockwise radians. For reference:
            • Full circle (360°) = `2 * math.pi`
            • 90° = `math.pi / 2`
            • 45° = `math.pi / 4`
        - A `Rotate` object: Allows specifying both the rotation angle 
        and the alignment (i.e., the pivot point for rotation).
    """

    scale: Optional[ScaleValue] = None
    """
    Scale control along the 2D plane. 
    
    The value of this property can be a number or an instance of `Scale` class.
    
    Default scale factor is `1.0` - control is not scaled. 
    `0.5` - the control is twice smaller, `2.0` - the control is twice larger.
    """

    offset: Optional[OffsetValue] = None
    """
    Applies a translation transform to the control before it is painted.

    The translation is specified as an `Offset`, where each component is scaled relative to the control's size. 
    For example, an `Offset(x=0.25, y=0)` translates the control horizontally by 25% of its width.

    Example:
        If the control is placed at (0, 0) in a `Stack` and has a size of 100x100, an `offset` of (-1, -1) moves the control 
        left and up by 100 pixels, effectively positioning it at (-100, -100).
    """

    aspect_ratio: OptionalNumber = None
    """
    The aspect ratio of the control.
    """

    animate_opacity: Optional[AnimationValue] = None
    """"""

    animate_size: Optional[AnimationValue] = None
    """"""

    animate_position: Optional[AnimationValue] = None
    """"""

    animate_rotation: Optional[AnimationValue] = None
    """"""

    animate_scale: Optional[AnimationValue] = None
    """"""

    animate_offset: Optional[AnimationValue] = None
    """"""

    on_animation_end: OptionalControlEventCallable = None
    """"""

