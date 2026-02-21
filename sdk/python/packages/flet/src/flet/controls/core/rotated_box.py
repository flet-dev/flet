from typing import Optional

from flet.controls.base_control import control
from flet.controls.control import Control
from flet.controls.layout_control import LayoutControl

__all__ = ["RotatedBox"]


@control("RotatedBox")
class RotatedBox(LayoutControl):
    """
    Rotates its [`content`][(c).] by an integral number of quarter turns.

    Unlike [`LayoutControl.rotate`][flet.LayoutControl.rotate] (which uses
    `Transform.rotate` and applies the rotation only at paint time),
    `RotatedBox` applies the rotation before layout. This means the control's
    rotated dimensions participate in layout and can affect surrounding
    controls.
    """

    quarter_turns: int = 0
    """
    The number of clockwise quarter turns.

    For example, `1` rotates by 90 degrees, `2` by 180 degrees.
    """

    content: Optional[Control] = None
    """
    The `Control` to rotate.
    """
