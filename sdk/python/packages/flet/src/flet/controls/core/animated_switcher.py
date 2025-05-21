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
    A control that by default does a cross-fade between a new control and the control
    previously set on the AnimatedSwitcher as a `content`.

    Online docs: https://flet.dev/docs/controls/animatedswitcher
    """

    content: Control
    """
    The content to display. When the `content` changes, the AnimatedSwitcher will
    animate the transition from the old `content` to the new one.

    Value is of type `Control`.
    """

    duration: DurationValue = field(default_factory=lambda: Duration(seconds=1))
    """
    The duration, in milliseconds, of the transition from the old `content` value
    to the new one.

    Value is of type `int` defaults to `1000` milliseconds.
    """

    reverse_duration: DurationValue = field(default_factory=lambda: Duration(seconds=1))
    """
    The duration, in milliseconds, of the transition from the new `content` value
    to the old one.

    Value is of type `int` and defaults to `1000` milliseconds.
    """

    switch_in_curve: AnimationCurve = AnimationCurve.LINEAR
    """
    The animation curve to use when transitioning in a new `content`.

    Value is of type
    [`AnimationCurve`](https://flet.dev/docs/reference/types/animationcurve) and 
    defaults to [`AnimationCurve.LINEAR`](https://flet.dev/docs/reference/types/animationcurve).
    """

    switch_out_curve: AnimationCurve = AnimationCurve.LINEAR
    """
    The animation curve to use when transitioning a previous `content` out.

    Value is of type
    [`AnimationCurve`](https://flet.dev/docs/reference/types/animationcurve) and 
    defaults to [`AnimationCurve.LINEAR`](https://flet.dev/docs/reference/types/animationcurve).
    """

    transition: AnimatedSwitcherTransition = AnimatedSwitcherTransition.FADE
    """
    An animation type to transition between new and old `content`.

    Value is of type
    [`AnimatedSwitcherTransition`](https://flet.dev/docs/reference/types/animatedswitchertransition)
    and defaults to
    [`AnimatedSwitcherTransition.FADE`](https://flet.dev/docs/reference/types/animatedswitchertransition).
    """

    def before_update(self):
        super().before_update()
        assert self.content.visible, "content must be visible"
