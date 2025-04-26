from dataclasses import field
from enum import Enum

from flet.controls.animation import AnimationCurve
from flet.controls.base_control import control
from flet.controls.constrained_control import ConstrainedControl
from flet.controls.control import Control
from flet.controls.duration import Duration, DurationValue

__all__ = ["AnimatedSwitcher", "AnimatedSwitcherTransition"]


class AnimatedSwitcherTransition(Enum):
    FADE = "fade"
    ROTATION = "rotation"
    SCALE = "scale"


@control("AnimatedSwitcher")
class AnimatedSwitcher(ConstrainedControl):
    """
    A control that by default does a cross-fade between a new control and the control previously set on the AnimatedSwitcher as a `content`.

    Example:
    ```
    import flet as ft

    def main(page: ft.Page):

        c1 = ft.Container(
            ft.Text("Hello!", style=ft.TextThemeStyle.HEADLINE_MEDIUM),
            alignment=ft.Alignment.center(),
            width=200,
            height=200,
            bgcolor=ft.colors.GREEN,
        )
        c2 = ft.Container(
            ft.Text("Bye!", size=50),
            alignment=ft.Alignment.center(),
            width=200,
            height=200,
            bgcolor=ft.colors.YELLOW,
        )
        c = ft.AnimatedSwitcher(
            content=c1,
            transition=ft.AnimatedSwitcherTransition.SCALE,
            duration=500,
            reverse_duration=100,
            switch_in_curve=ft.AnimationCurve.BOUNCE_OUT,
            switch_out_curve=ft.AnimationCurve.BOUNCE_IN,
        )

        def animate(e):
            c.content = c2 if c.content == c1 else c1
            c.update()

        page.add(
            c,
            ft.ElevatedButton("Animate!", on_click=animate),
        )

    ft.app(target=main)
    ```

    -----

    Online docs: https://flet.dev/docs/controls/animatedswitcher
    """

    content: Control
    duration: DurationValue = field(default_factory=lambda: Duration(seconds=1))
    reverse_duration: DurationValue = field(default_factory=lambda: Duration(seconds=1))
    switch_in_curve: AnimationCurve = AnimationCurve.LINEAR
    switch_out_curve: AnimationCurve = AnimationCurve.LINEAR
    transition: AnimatedSwitcherTransition = AnimatedSwitcherTransition.FADE

    def before_update(self):
        super().before_update()
        assert self.content.visible, "content must be visible"
