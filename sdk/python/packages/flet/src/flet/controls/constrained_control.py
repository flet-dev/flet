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
    width: OptionalNumber = None
    """
    Imposed Control width in virtual pixels.
    """
    
    height: OptionalNumber = None
    """
    Imposed Control height in virtual pixels.
    """
    
    left: OptionalNumber = None
    """
    Effective inside [`Stack`](/docs/controls/stack) only. The distance that the 
    child's left edge is inset from the left of the stack.
    """
    
    top: OptionalNumber = None
    """
    Effective inside [`Stack`](/docs/controls/stack) only. The distance that the 
    child's top edge is inset from the top of the stack.
    """

    right: OptionalNumber = None
    """
    Effective inside [`Stack`](/docs/controls/stack) only. The distance that the 
    child's right edge is inset from the right of the stack.
    """

    bottom: OptionalNumber = None
    """
    Effective inside [`Stack`](/docs/controls/stack) only. The distance that the 
    child's bottom edge is inset from the bottom of the stack.
    """

    rotate: Optional[RotateValue] = None
    scale: Optional[ScaleValue] = None
    offset: Optional[OffsetValue] = None
    """
    Applies a translation transformation before painting the control.

    The translation is expressed as a `transform.Offset` scaled to the control's size. 
    For example, an `Offset` with a `x` of `0.25` will result in a horizontal 
    translation of one quarter the width of the control.

    The following example displays container at `0, 0` top left corner of a stack as 
    transform applies `-1 * 100, -1 * 100` (`offset * control_size`) horizontal and 
    vertical translations to the control:

    ```python
    import flet as ft

    def main(page: ft.Page):

        page.add(
            ft.Stack(
                [
                    ft.Container(
                        bgcolor="red",
                        width=100,
                        height=100,
                        left=100,
                        top=100,
                        offset=ft.transform.Offset(-1, -1),
                    )
                ],
                width=1000,
                height=1000,
            )
        )

    ft.run(main)
    ```
    """
    aspect_ratio: OptionalNumber = None
    animate_opacity: Optional[AnimationValue] = None
    animate_size: Optional[AnimationValue] = None
    animate_position: Optional[AnimationValue] = None
    animate_rotation: Optional[AnimationValue] = None
    animate_scale: Optional[AnimationValue] = None
    animate_offset: Optional[AnimationValue] = None
    on_animation_end: OptionalControlEventCallable = None
