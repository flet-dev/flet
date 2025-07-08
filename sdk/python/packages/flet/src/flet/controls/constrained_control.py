from typing import Optional

from flet.controls.animation import AnimationValue
from flet.controls.base_control import control
from flet.controls.control import Control
from flet.controls.control_event import OptionalControlEventHandler
from flet.controls.transform import OffsetValue, RotateValue, ScaleValue
from flet.controls.types import OptionalNumber

__all__ = ["ConstrainedControl"]


@control(kw_only=True)
class ConstrainedControl(Control):
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
    Effective inside [`Stack`](https://flet.dev/docs/controls/stack) only. The distance 
    that the child's left edge is inset from the left of the stack.
    """

    top: OptionalNumber = None
    """
    Effective inside [`Stack`](https://flet.dev/docs/controls/stack) only. The distance 
    that the child's top edge is inset from the top of the stack.
    """

    right: OptionalNumber = None
    """
    Effective inside [`Stack`](https://flet.dev/docs/controls/stack) only. The distance 
    that the child's right edge is inset from the right of the stack.
    """

    bottom: OptionalNumber = None
    """
    Effective inside [`Stack`](https://flet.dev/docs/controls/stack) only. The distance 
    that the child's bottom edge is inset from the bottom of the stack.
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
        rotate=Rotate(angle=0.25 * pi, alignment=ft.Alignment.CENTER_LEFT)
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
    """
    TBD
    """

    animate_opacity: Optional[AnimationValue] = None
    """
    Setting control's `animate_opacity` to either `True`, number or an instance of 
    `animation.Animation` class enables implicit animation of [`Control.opacity`](https://flet.dev/docs/controls#opacity) 
    property.

    <img src="https://flet.dev/img/docs/getting-started/animations/animate-opacity.gif" 
    className="screenshot-20" />

    ```python
    import flet as ft

    def main(page: ft.Page):

        c = ft.Container(
            width=150,
            height=150,
            bgcolor="blue",
            border_radius=10,
            animate_opacity=300,
        )

        def animate_opacity(e):
            c.opacity = 0 if c.opacity == 1 else 1
            c.update()

        page.add(
            c,
            ft.ElevatedButton(
                "Animate opacity",
                on_click=animate_opacity,
            ),
        )

    ft.app(main)
    ```
    """

    animate_size: Optional[AnimationValue] = None
    """
    TBD
    """

    animate_position: Optional[AnimationValue] = None
    """
    Setting control's `animate_position` to either `True`, number or an instance of 
    `animation.Animation` class (see above) enables implicit animation of [Control's 
    `left`, `top`, `right` and `bottom` properties](https://flet.dev/docs/controls#left).

    Please note Control position works inside `Stack` control only.

    <img src="https://flet.dev/img/docs/getting-started/animations/animate-position.gif" 
    className="screenshot-30" />

    ```python
    import flet as ft

    def main(page: ft.Page):

        c1 = ft.Container(width=50, height=50, bgcolor="red", animate_position=1000)

        c2 = ft.Container(
            width=50, height=50, bgcolor="green", top=60, left=0, animate_position=500
        )

        c3 = ft.Container(
            width=50, height=50, bgcolor="blue", top=120, left=0, animate_position=1000
        )

        def animate_container(e):
            c1.top = 20
            c1.left = 200
            c2.top = 100
            c2.left = 40
            c3.top = 180
            c3.left = 100
            page.update()

        page.add(
            ft.Stack([c1, c2, c3], height=250),
            ft.ElevatedButton("Animate!", on_click=animate_container),
        )

    ft.run(main)
    ```
    """

    animate_rotation: Optional[AnimationValue] = None
    """
    Setting control's `animate_rotation` to either `True`, number or an instance of 
    `animation.Animation` class enables implicit animation of [`Control.rotate`](https://flet.dev/docs/controls#rotate) 
    property.

    <img src="https://flet.dev/img/docs/getting-started/animations/animate-rotation.gif" 
    className="screenshot-20" />

    ```python
    from math import pi
    import flet as ft

    def main(page: ft.Page):

        c = ft.Container(
            width=100,
            height=70,
            bgcolor="blue",
            border_radius=5,
            rotate=ft.transform.Rotate(0, alignment=ft.Alignment.CENTER),
            animate_rotation=ft.animation.Animation(300, ft.AnimationCurve.BOUNCE_OUT),
        )

        def animate(e):
            c.rotate.angle += pi / 2
            page.update()

        page.vertical_alignment = ft.MainAxisAlignment.CENTER
        page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
        page.spacing = 30
        page.add(
            c,
            ft.ElevatedButton("Animate!", on_click=animate),
        )

    ft.run(main)
    ```
    """

    animate_scale: Optional[AnimationValue] = None
    """
    Setting control's `animate_scale` to either `True`, number or an instance of 
    `animation.Animation` class enables implicit animation of [`Control.scale`](https://flet.dev/docs/controls#scale) 
    property.

    <img src="https://flet.dev/img/docs/getting-started/animations/animate-scale.gif" 
    className="screenshot-20" />

    ```python
    import flet as ft

    def main(page: ft.Page):

        c = ft.Container(
            width=100,
            height=100,
            bgcolor="blue",
            border_radius=5,
            scale=ft.transform.Scale(scale=1),
            animate_scale=ft.animation.Animation(600, ft.AnimationCurve.BOUNCE_OUT),
        )

        def animate(e):
            c.scale = 2
            page.update()

        page.vertical_alignment = ft.MainAxisAlignment.CENTER
        page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
        page.spacing = 30
        page.add(
            c,
            ft.ElevatedButton("Animate!", on_click=animate),
        )

    ft.run(main)
    ```
    """

    animate_offset: Optional[AnimationValue] = None
    """
    Setting control's `animate_offset` to either `True`, number or an instance of 
    `animation.Animation` class enables implicit animation of `Control.offset` property.

    `offset` property is an instance of `transform.Offset` class which specifies 
    horizontal `x` and vertical `y` offset of a control scaled to control's size. 
    For example, an offset `transform.Offset(-0.25, 0)` will result in a horizontal 
    translation of one quarter the width of the control.

    Offset animation is used for various sliding effects:

    <img src="https://flet.dev/img/docs/getting-started/animations/animate-offset.gif" 
    className="screenshot-20" />

    ```python
    import flet as ft

    def main(page: ft.Page):

        c = ft.Container(
            width=150,
            height=150,
            bgcolor="blue",
            border_radius=10,
            offset=ft.transform.Offset(-2, 0),
            animate_offset=ft.animation.Animation(1000),
        )

        def animate(e):
            c.offset = ft.transform.Offset(0, 0)
            c.update()

        page.add(
            c,
            ft.ElevatedButton("Reveal!", on_click=animate),
        )

    ft.run(main)
    ```
    """

    on_animation_end: OptionalControlEventHandler["ConstrainedControl"] = None
    """
    All controls with `animate_*` properties have `on_animation_end` event handler 
    which is called when animation complete and can be used to chain multiple 
    animations.

    Event's object `data` field contains the name of animation:

    * `opacity`
    * `rotation`
    * `scale`
    * `offset`
    * `position`
    * `container`

    For example:

    ```python
    c = ft.Container(
            ft.Text("Animate me!"),
            # ...
            animate=ft.animation.Animation(1000, "bounceOut"),
            on_animation_end=lambda e: print("Container animation end:", e.data)
        )
    ```
    """
