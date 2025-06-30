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
    Used to switch between controls with an animation.
    """

    content: Control
    """
    The content to display. When the `content` changes, the AnimatedSwitcher will
    animate the transition from the old `content` to the new one.
    """

    duration: DurationValue = field(default_factory=lambda: Duration(seconds=1))
    """
    The duration, in milliseconds, of the transition from the old `content` value
    to the new one.
    """

    reverse_duration: DurationValue = field(default_factory=lambda: Duration(seconds=1))
    """
    The duration, in milliseconds, of the transition from the new `content` value
    to the old one.
    """

    switch_in_curve: AnimationCurve = AnimationCurve.LINEAR
    """
    The animation curve to use when transitioning in a new `content`.
    """

    switch_out_curve: AnimationCurve = AnimationCurve.LINEAR
    """
    The animation curve to use when transitioning a previous `content` out.
    """

    transition: AnimatedSwitcherTransition = AnimatedSwitcherTransition.FADE
    """
    An animation type to transition between new and old `content`.
    """

    def before_update(self):
        super().before_update()
        assert self.content.visible, "content must be visible"
