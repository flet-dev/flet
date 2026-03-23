from dataclasses import dataclass, field
from typing import Optional

from flet.controls.alignment import Alignment
from flet.controls.animation import AnimationValue
from flet.controls.base_control import control
from flet.controls.control import Control
from flet.controls.control_event import (
    ControlEventHandler,
    Event,
    EventControlType,
    EventHandler,
)
from flet.controls.margin import MarginValue
from flet.controls.transform import (
    Flip,
    OffsetValue,
    RotateValue,
    ScaleValue,
    Transform,
)
from flet.controls.types import Number
from flet.utils import deprecated_class

__all__ = ["ConstrainedControl", "LayoutControl", "LayoutSizeChangeEvent"]


@dataclass
class LayoutSizeChangeEvent(Event[EventControlType]):
    """
    Event fired when a control's rendered size changes after layout.
    """

    width: float = field(metadata={"data_field": "w"})
    """
    Width of the control after layout.
    """

    height: float = field(metadata={"data_field": "h"})
    """
    Height of the control after layout.
    """


@control(kw_only=True)
class LayoutControl(Control):
    """
    Base class for visual controls that participate in page layout.

    `LayoutControl` extends :class:`~flet.Control` with common visual layout
    capabilities, including:

    - explicit sizing (:attr:`width`, :attr:`height`, :attr:`aspect_ratio`);
    - absolute positioning (:attr:`left`, [`top`], :attr:`right`, :attr:`bottom`);
    - parent-space placement (:attr:`align`, :attr:`margin`);
    - 2D transforms (:attr:`rotate`, :attr:`scale`, :attr:`offset`,
      :attr:`flip`, :attr:`transform`);
    - implicit animations for those properties (`animate_*`);
    - layout/animation lifecycle events (:attr:`on_size_change`,
      :attr:`on_animation_end`).

    Use `LayoutControl` as the base for custom visual controls rendered on
    the page surface. For popup controls, use :class:`~flet.DialogControl`;
    for non-visual integrations, use :class:`~flet.Service`.
    """

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
        :class:`~flet.Stack` control, :attr:`flet.Page.overlay` list.
    """

    top: Optional[Number] = None
    """
    The distance that the child's top edge is inset from the top of the stack.

    Note:
        Effective only if this control is a descendant of one of the following:
        :class:`~flet.Stack` control, :attr:`flet.Page.overlay` list.
    """

    right: Optional[Number] = None
    """
    The distance that the child's right edge is inset from the right of the stack.

    Note:
        Effective only if this control is a descendant of one of the following:
        :class:`~flet.Stack` control, :attr:`flet.Page.overlay` list.
    """

    bottom: Optional[Number] = None
    """
    The distance that the child's bottom edge is inset from the bottom of the stack.

    Note:
        Effective only if this control is a descendant of one of the following:
        :class:`~flet.Stack` control, :attr:`flet.Page.overlay` list.
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

    Example:
        ```python
        ft.Image(
            src="https://picsum.photos/100/100",
            width=100,
            height=100,
            border_radius=5,
            rotate=Rotate(angle=0.25 * pi, alignment=ft.Alignment.CENTER_LEFT)
        )
        ```
    """

    scale: Optional[ScaleValue] = None
    """
    Scales this control along the 2D plane. Default scale factor is `1.0`, meaning \
    no-scale.

    Setting this property to `0.5`, for example, makes this control twice smaller,
    while `2.0` makes it twice larger.

    Different scale multipliers can be specified for `x` and `y` axis, by setting
    `Control.scale` property to an instance of `Scale` class.
    Either `scale` or `scale_x` and `scale_y` could be specified, but not all of them.

    Example:
        ```python
        ft.Image(
            src="https://picsum.photos/100/100",
            width=100,
            height=100,
            border_radius=5,
            scale=ft.Scale(scale_x=2, scale_y=0.5)
        )
        ```
    """

    offset: Optional[OffsetValue] = None
    """
    Applies a translation transformation before painting the control.

    The translation is expressed as an `Offset` scaled to the control's size.
    So, `Offset(x=0.25, y=0)`, for example, will result in a horizontal translation
    of one quarter the width of this control.

    Example
        The following example displays container at `0, 0` top left corner of a stack
        as transform applies `-1 * 100, -1 * 100` (`offset * control's size`)
        horizontal and vertical translations to the control:

        ```python
        import flet as ft

        def main(page: ft.Page):
            page.add(
                ft.Stack(
                    width=1000,
                    height=1000,
                    controls=[
                        ft.Container(
                            bgcolor=ft.Colors.RED,
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
    """

    flip: Optional[Flip] = None
    """
    Flips this control horizontally and/or vertically.

    Set to an instance of :class:`~flet.Flip` to mirror across x-axis, y-axis, or both.
    """

    transform: Optional[Transform] = None
    """
    Applies a generic matrix transform to this control.

    Set to an instance of :class:`~flet.Transform` with a recorded
    :class:`~flet.Matrix4` to describe arbitrary transform sequences.
    """
    aspect_ratio: Optional[Number] = None
    """
    The aspect ratio of the control.
    It is defined as the ratio of :attr:`width` to :attr:`height`.

    Note:
        In current implementation, if :attr:`aspect_ratio` is set, :attr:`width`
        and :attr:`height` on the same control are ignored for final rendered size.
    """

    animate_opacity: Optional[AnimationValue] = None
    """
    Enables implicit animation of the :attr:`~flet.Control.opacity` property.

    More information [here](https://flet.dev/docs/cookbook/animations).
    """

    animate_size: Optional[AnimationValue] = None
    """
    TBD
    """

    animate_position: Optional[AnimationValue] = None
    """
    Enables implicit animation of the positioning properties \
    (:attr:`~flet.LayoutControl.left`, :attr:`~flet.LayoutControl.right`, \
    :attr:`~flet.LayoutControl.top` and :attr:`~flet.LayoutControl.bottom`).

    More information [here](https://flet.dev/docs/cookbook/animations).
    """

    animate_align: Optional[AnimationValue] = None
    """
    Enables implicit animation of the :attr:`~flet.LayoutControl.align` property.

    More information [here](https://flet.dev/docs/cookbook/animations).
    """

    animate_margin: Optional[AnimationValue] = None
    """
    Enables implicit animation of the :attr:`~flet.LayoutControl.margin` property.

    More information [here](https://flet.dev/docs/cookbook/animations).
    """

    animate_rotation: Optional[AnimationValue] = None
    """
    Enables implicit animation of the :attr:`~flet.LayoutControl.rotate` property.

    More information [here](https://flet.dev/docs/cookbook/animations).
    """

    animate_scale: Optional[AnimationValue] = None
    """
    Enables implicit animation of the :attr:`~flet.LayoutControl.scale` property.

    More information [here](https://flet.dev/docs/cookbook/animations).
    """

    animate_offset: Optional[AnimationValue] = None
    """
    Enables implicit animation of the :attr:`~flet.LayoutControl.offset` property.

    More information [here](https://flet.dev/docs/cookbook/animations).
    """

    size_change_interval: int = 10
    """
    Sampling interval in milliseconds for :attr:`on_size_change` event.

    Setting to `0` calls :attr:`on_size_change` immediately
    on every change.
    """

    on_size_change: Optional[EventHandler[LayoutSizeChangeEvent["LayoutControl"]]] = (
        None
    )
    """
    Called when the size of this control changes.

    :attr:`size_change_interval` defines how often this event is called.
    """

    on_animation_end: Optional[ControlEventHandler["LayoutControl"]] = None
    """
    Called when animation completes.

    Can be used to chain multiple animations.

    The `data` property of the event handler argument contains the name
    of the animation.

    More information [here](https://flet.dev/docs/cookbook/animations).
    """


@deprecated_class(
    reason="Inherit from LayoutControl instead.",
    version="0.80.0",
    delete_version="1.0",
)
class ConstrainedControl(LayoutControl):
    pass
