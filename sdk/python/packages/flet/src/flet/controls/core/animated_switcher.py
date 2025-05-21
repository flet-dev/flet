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
    duration: DurationValue = field(default_factory=lambda: Duration(seconds=1))
    reverse_duration: DurationValue = field(default_factory=lambda: Duration(seconds=1))
    switch_in_curve: AnimationCurve = AnimationCurve.LINEAR
    switch_out_curve: AnimationCurve = AnimationCurve.LINEAR
    transition: AnimatedSwitcherTransition = AnimatedSwitcherTransition.FADE

    def before_update(self):
        super().before_update()
        assert self.content.visible, "content must be visible"
