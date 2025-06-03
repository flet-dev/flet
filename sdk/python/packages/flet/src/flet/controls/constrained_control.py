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
    """
    Transforms control using a rotation around the center.

    The value of `rotate` property could be one of the following types:

    * `number` - a rotation in clockwise radians. Full circle `360°` is `math.pi * 2` 
    radians, `90°` is `pi / 2`, `45°` is `pi / 4`, etc.
    * `transform.Rotate` - allows to specify rotation `angle` as well as `alignment` - 
    the location of rotation center.

    For example:

    ```python
    ft.Image(
        src="https://picsum.photos/100/100",
        width=100,
        height=100,
        border_radius=5,
        rotate=Rotate(angle=0.25 * pi, alignment=ft.Alignment.center_left())
    )
    ```
    """
    
    scale: Optional[ScaleValue] = None
    """
    Scale control along the 2D plane. Default scale factor is `1.0` - control is not 
    scaled. `0.5` - the control is twice smaller, `2.0` - the control is twice larger.

    Different scale multipliers can be specified for `x` and `y` axis, but setting 
    `Control.scale` property to an instance of `transform.Scale` class.

    Either `scale` or `scale_x` and `scale_y` could be specified, but not all of them, 
    for example:

    ```python
    ft.Image(
        src="https://picsum.photos/100/100",
        width=100,
        height=100,
        border_radius=5,
        scale=Scale(scale_x=2, scale_y=0.5)
    )
    ```
    """
    
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
