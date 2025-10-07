from dataclasses import field
from enum import Enum

from flet.controls.animation import AnimationCurve
from flet.controls.base_control import control
from flet.controls.control import Control
from flet.controls.duration import Duration, DurationValue
from flet.controls.layout_control import LayoutControl

__all__ = ["AnimatedSwitcher", "AnimatedSwitcherTransition"]


class AnimatedSwitcherTransition(Enum):
    FADE = "fade"
    ROTATION = "rotation"
    SCALE = "scale"


@control("AnimatedSwitcher")
class AnimatedSwitcher(LayoutControl):
    """
    Used to switch between controls with an animation.
    """

    content: Control
    """
    The content to display.

    When it changes, this switcher will animate the transition from the old/previous
    `content` to the new one.

    Raises:
        ValueError: If [`content`][(c).] is not visible.
    """

    duration: DurationValue = field(default_factory=lambda: Duration(seconds=1))
    """
    The duration of the transition from the old [`content`][(c).] to the new one.
    """

    reverse_duration: DurationValue = field(default_factory=lambda: Duration(seconds=1))
    """
    The duration of the transition from the new [`content`][(c).] to the old one.
    """

    switch_in_curve: AnimationCurve = AnimationCurve.LINEAR
    """
    The animation curve to use when transitioning in a new [`content`][(c).].
    """

    switch_out_curve: AnimationCurve = AnimationCurve.LINEAR
    """
    The animation curve to use when transitioning an old [`content`][(c).] out.
    """

    transition: AnimatedSwitcherTransition = AnimatedSwitcherTransition.FADE
    """
    An animation type to transition between new and old [`content`][(c).].
    """

    def before_update(self):
        super().before_update()
        if not self.content.visible:
            raise ValueError("content must be visible")
