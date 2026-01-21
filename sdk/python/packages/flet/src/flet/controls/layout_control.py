from typing import Optional

from flet.controls.alignment import Alignment
from flet.controls.animation import AnimationValue
from flet.controls.base_control import control
from flet.controls.control import Control
from flet.controls.control_event import ControlEventHandler
from flet.controls.margin import MarginValue
from flet.controls.transform import OffsetValue, RotateValue, ScaleValue
from flet.controls.types import Number
from flet.utils import deprecated_class

__all__ = ["ConstrainedControl", "LayoutControl"]


@control(kw_only=True)
class LayoutControl(Control):
    width: Optional[Number] = None
    """
    Imposed Control width in virtual pixels.
    """

    height: Optional[Number] = None
    """
    Imposed Control height in virtual pixels.
    """

    left: Optional[Number] = None
    """
    The distance that the child's left edge is inset from the left of the stack.

    Note:
        Effective only if this control is a descendant of one of the following:
        [`Stack`][flet.] control, [`Page.overlay`][flet.] list.
    """

    top: Optional[Number] = None
    """
    The distance that the child's top edge is inset from the top of the stack.

    Note:
        Effective only if this control is a descendant of one of the following:
        [`Stack`][flet.] control, [`Page.overlay`][flet.] list.
    """

    right: Optional[Number] = None
    """
    The distance that the child's right edge is inset from the right of the stack.

    Note:
        Effective only if this control is a descendant of one of the following:
        [`Stack`][flet.] control, [`Page.overlay`][flet.] list.
    """

    bottom: Optional[Number] = None
    """
    The distance that the child's bottom edge is inset from the bottom of the stack.

    Note:
        Effective only if this control is a descendant of one of the following:
        [`Stack`][flet.] control, [`Page.overlay`][flet.] list.
    """

    align: Optional[Alignment] = None
    """
    Alignment of the control within its parent.
    """

    margin: Optional[MarginValue] = None
    """
    Sets the margin of the control.
    """

    rotate: Optional[RotateValue] = None
    """
    Transforms this control using a rotation around its center.

    The value of `rotate` property could be one of the following types:

    * `number` - a rotation in clockwise radians. Full circle `360°` is `math.pi * 2`
    radians, `90°` is `pi / 2`, `45°` is `pi / 4`, etc.
    * `Rotate` - allows to specify rotation `angle` as well as `alignment` -
    the location of rotation center.

    /// details | Example
        type: example
    For example:
    ```python
    ft.Image(
        src="https://picsum.photos/100/100",
        width=100,
        height=100,
        border_radius=5,
        rotate=Rotate(angle=0.25 * pi, alignment=ft.Alignment.CENTER_LEFT)
    )
    ```
    ///
    """

    scale: Optional[ScaleValue] = None
    """
    Scales this control along the 2D plane. Default scale factor is `1.0`,
    meaning no-scale.

    Setting this property to `0.5`, for example, makes this control twice smaller,
    while `2.0` makes it twice larger.

    Different scale multipliers can be specified for `x` and `y` axis, by setting
    `Control.scale` property to an instance of `Scale` class.
    Either `scale` or `scale_x` and `scale_y` could be specified, but not all of them.

    /// details | Example
        type: example
    ```python
    ft.Image(
        src="https://picsum.photos/100/100",
        width=100,
        height=100,
        border_radius=5,
        scale=ft.Scale(scale_x=2, scale_y=0.5)
    )
    ```
    ///
    """

    offset: Optional[OffsetValue] = None
    """
    Applies a translation transformation before painting the control.

    The translation is expressed as an `Offset` scaled to the control's size.
    So, `Offset(x=0.25, y=0)`, for example, will result in a horizontal translation
    of one quarter the width of this control.

    /// details | Example
        type: example
    The following example displays container at `0, 0` top left corner of a stack as
    transform applies `-1 * 100, -1 * 100` (`offset * control's size`) horizontal and
    vertical translations to the control:

    ```python
    import flet as ft

    def main(page: ft.Page):
        page.add(
            ft.Stack(
                width=1000,
                height=1000,
                controls=[
                    ft.Container(
                        bgcolor="red",
                        width=100,
                        height=100,
                        left=100,
                        top=100,
                        offset=ft.Offset(-1, -1),
                    )
                ],
            )
        )

    ft.run(main)
    ```
    ///
    """
    aspect_ratio: Optional[Number] = None
    """
    The aspect ratio of the control.
    It is defined as the ratio of the width to the height.
    """

    animate_opacity: Optional[AnimationValue] = None
    """
    Enables implicit animation of the [`opacity`][flet.Control.] property.

    More information [here](https://docs.flet.dev/cookbook/animations).
    """

    animate_size: Optional[AnimationValue] = None
    """
    TBD
    """

    animate_position: Optional[AnimationValue] = None
    """
    Enables implicit animation of the positioning properties
    ([`left`][flet.LayoutControl.], [`right`][flet.LayoutControl.],
    [`top`][flet.LayoutControl.] and [`bottom`][flet.LayoutControl.]).

    More information [here](https://docs.flet.dev/cookbook/animations).
    """

    animate_align: Optional[AnimationValue] = None
    """
    Enables implicit animation of the [`align`][flet.LayoutControl.] property.

    More information [here](https://docs.flet.dev/cookbook/animations).
    """

    animate_margin: Optional[AnimationValue] = None
    """
    Enables implicit animation of the [`margin`][flet.LayoutControl.] property.

    More information [here](https://docs.flet.dev/cookbook/animations).
    """

    animate_rotation: Optional[AnimationValue] = None
    """
    Enables implicit animation of the [`rotate`][flet.LayoutControl.] property.

    More information [here](https://docs.flet.dev/cookbook/animations).
    """

    animate_scale: Optional[AnimationValue] = None
    """
    Enables implicit animation of the [`scale`][flet.LayoutControl.] property.

    More information [here](https://docs.flet.dev/cookbook/animations).
    """

    animate_offset: Optional[AnimationValue] = None
    """
    Enables implicit animation of the [`offset`][flet.LayoutControl.] property.

    More information [here](https://docs.flet.dev/cookbook/animations).
    """

    on_animation_end: Optional[ControlEventHandler["LayoutControl"]] = None
    """
    Called when animation completes.

    Can be used to chain multiple animations.

    The `data` property of the event handler argument contains the name
    of the animation.

    More information [here](https://docs.flet.dev/cookbook/animations).
    """


@deprecated_class(
    reason="Inherit from LayoutControl instead.",
    version="0.80.0",
    delete_version="1.0",
)
class ConstrainedControl(LayoutControl):
    pass
