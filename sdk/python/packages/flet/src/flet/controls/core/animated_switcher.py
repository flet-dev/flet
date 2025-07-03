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

    Raises:
        AssertionError: The [`content`][(c).] must be provided and visible.
    """

    content: Control
    """
    The content to display. When the [`content`][flet.AnimatedSwitcher.content] changes, 
    this switcher will animate the transition from the old/previous 
    [`content`][flet.AnimatedSwitcher.content] to the new one.
    """

    duration: DurationValue = field(default_factory=lambda: Duration(seconds=1))
    """
    The duration of the transition from the old [`content`][flet.AnimatedSwitcher.content]
    to the new one.
    """

    reverse_duration: DurationValue = field(default_factory=lambda: Duration(seconds=1))
    """
    The duration of the transition from the new [`content`][flet.AnimatedSwitcher.content]
    to the old one.
    """

    switch_in_curve: AnimationCurve = AnimationCurve.LINEAR
    """
    The animation curve to use when transitioning in a 
    new [`content`][flet.AnimatedSwitcher.content].
    """

    switch_out_curve: AnimationCurve = AnimationCurve.LINEAR
    """
    The animation curve to use when transitioning an old 
    [`content`][flet.AnimatedSwitcher.content] out.
    """

    transition: AnimatedSwitcherTransition = AnimatedSwitcherTransition.FADE
    """
    An animation type to transition between new and old 
    [`content`][flet.AnimatedSwitcher.content].
    """

    def before_update(self):
        super().before_update()
        assert self.content.visible, "content must be visible"
