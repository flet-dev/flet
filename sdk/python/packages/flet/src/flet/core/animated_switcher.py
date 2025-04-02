from enum import Enum
from typing import Optional

from flet.core.animation import AnimationCurve
from flet.core.constrained_control import ConstrainedControl
from flet.core.control import Control, control

try:
    from typing import Literal
except ImportError:
    from typing_extensions import Literal
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
            alignment=ft.alignment.center,
            width=200,
            height=200,
            bgcolor=ft.colors.GREEN,
        )
        c2 = ft.Container(
            ft.Text("Bye!", size=50),
            alignment=ft.alignment.center,
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
    duration: Optional[int] = None
    reverse_duration: Optional[int] = None
    switch_in_curve: Optional[AnimationCurve] = None
    switch_out_curve: Optional[AnimationCurve] = None
    transition: Optional[AnimatedSwitcherTransition] = None

    def before_update(self):
        super().before_update()
        assert self.content.visible, "content must be visible"
