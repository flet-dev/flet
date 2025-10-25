from dataclasses import dataclass, field
from enum import Enum
from typing import Optional, Union

from flet.controls.duration import Duration, DurationValue

__all__ = [
    "Animation",
    "AnimationCurve",
    "AnimationStyle",
    "AnimationValue",
]


class AnimationCurve(Enum):
    BOUNCE_IN = "bounceIn"
    BOUNCE_IN_OUT = "bounceInOut"
    BOUNCE_OUT = "bounceOut"
    DECELERATE = "decelerate"
    EASE = "ease"
    EASE_IN = "easeIn"
    EASE_IN_BACK = "easeInBack"
    EASE_IN_CIRC = "easeInCirc"
    EASE_IN_CUBIC = "easeInCubic"
    EASE_IN_EXPO = "easeInExpo"
    EASE_IN_OUT = "easeInOut"
    EASE_IN_OUT_BACK = "easeInOutBack"
    EASE_IN_OUT_CIRC = "easeInOutCirc"
    EASE_IN_OUT_CUBIC = "easeInOutCubic"
    EASE_IN_OUT_CUBIC_EMPHASIZED = "easeInOutCubicEmphasized"
    EASE_IN_OUT_EXPO = "easeInOutExpo"
    EASE_IN_OUT_QUAD = "easeInOutQuad"
    EASE_IN_OUT_QUART = "easeInOutQuart"
    EASE_IN_OUT_QUINT = "easeInOutQuint"
    EASE_IN_OUT_SINE = "easeInOutSine"
    EASE_IN_QUAD = "easeInQuad"
    EASE_IN_QUART = "easeInQuart"
    EASE_IN_QUINT = "easeInQuint"
    EASE_IN_SINE = "easeInSine"
    EASE_IN_TO_LINEAR = "easeInToLinear"
    EASE_OUT = "easeOut"
    EASE_OUT_BACK = "easeOutBack"
    EASE_OUT_CIRC = "easeOutCirc"
    EASE_OUT_CUBIC = "easeOutCubic"
    EASE_OUT_EXPO = "easeOutExpo"
    EASE_OUT_QUAD = "easeOutQuad"
    EASE_OUT_QUART = "easeOutQuart"
    EASE_OUT_QUINT = "easeOutQuint"
    EASE_OUT_SINE = "easeOutSine"
    ELASTIC_IN = "elasticIn"
    ELASTIC_IN_OUT = "elasticInOut"
    ELASTIC_OUT = "elasticOut"
    FAST_LINEAR_TO_SLOW_EASE_IN = "fastLinearToSlowEaseIn"
    FAST_OUT_SLOWIN = "fastOutSlowIn"
    LINEAR = "linear"
    LINEAR_TO_EASE_OUT = "linearToEaseOut"
    SLOW_MIDDLE = "slowMiddle"


@dataclass
class Animation:
    duration: DurationValue = field(default_factory=lambda: Duration())
    """
    The duration of the animation.
    """

    curve: AnimationCurve = AnimationCurve.LINEAR
    """
    The curve to use for the animation.
    """

    def copy(
        self,
        *,
        duration: Optional[DurationValue] = None,
        curve: Optional[AnimationCurve] = None,
    ) -> "Animation":
        """
        Returns a copy of this object with the specified properties overridden.
        """
        return Animation(
            duration=duration if duration is not None else self.duration,
            curve=curve if curve is not None else self.curve,
        )


@dataclass
class AnimationStyle:
    """
    Used to override the default parameters of an animation.

    Note:
        If [`duration`][(c).] and [`reverse_duration`][(c).] are set to
        [`Duration()`][flet.Duration], the corresponding animation will be disabled.
        See [`no_animation()`][(c).no_animation] method for a convenient way to create
        such an instance.
    """

    duration: Optional[DurationValue] = None
    """
    The duration of the animation.
    """

    reverse_duration: Optional[DurationValue] = None
    """
    The duration of the reverse animation.
    """

    curve: Optional[AnimationCurve] = None
    """
    The curve to use for the animation.
    """

    reverse_curve: Optional[AnimationCurve] = None
    """
    The curve to use for the reverse animation.
    """

    @staticmethod
    def no_animation() -> "AnimationStyle":
        """
        Creates an instance of `AnimationStyle` with no animation.
        """
        return AnimationStyle(
            duration=Duration(),
            reverse_duration=Duration(),
        )

    def copy(
        self,
        *,
        duration: Optional[DurationValue] = None,
        reverse_duration: Optional[DurationValue] = None,
        curve: Optional[AnimationCurve] = None,
        reverse_curve: Optional[AnimationCurve] = None,
    ) -> "AnimationStyle":
        """
        Returns a copy of this object with the specified properties overridden.
        """
        return AnimationStyle(
            duration=duration if duration is not None else self.duration,
            reverse_duration=reverse_duration
            if reverse_duration is not None
            else self.reverse_duration,
            curve=curve if curve is not None else self.curve,
            reverse_curve=reverse_curve
            if reverse_curve is not None
            else self.reverse_curve,
        )


AnimationValue = Union[bool, int, Animation]
