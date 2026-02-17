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
    """
    Animation curves.
    """

    BOUNCE_IN = "bounceIn"
    """
    Easing that enters with a bounce effect.
    """

    BOUNCE_IN_OUT = "bounceInOut"
    """
    Easing that bounces both at the beginning and the end.
    """

    BOUNCE_OUT = "bounceOut"
    """
    Easing that exits with a bounce effect.
    """

    DECELERATE = "decelerate"
    """
    Starts quickly, then slows down toward the end.
    """

    EASE = "ease"
    """
    Standard symmetric ease-in/ease-out curve.
    """

    EASE_IN = "easeIn"
    """
    Starts slowly and accelerates.
    """

    EASE_IN_BACK = "easeInBack"
    """
    Ease-in curve with a slight initial backward overshoot.
    """

    EASE_IN_CIRC = "easeInCirc"
    """
    Circular ease-in curve.
    """

    EASE_IN_CUBIC = "easeInCubic"
    """
    Cubic ease-in curve.
    """

    EASE_IN_EXPO = "easeInExpo"
    """
    Exponential ease-in curve.
    """

    EASE_IN_OUT = "easeInOut"
    """
    Symmetric ease-in/ease-out curve.
    """

    EASE_IN_OUT_BACK = "easeInOutBack"
    """
    Ease-in/ease-out curve with overshoot near both ends.
    """

    EASE_IN_OUT_CIRC = "easeInOutCirc"
    """
    Circular ease-in/ease-out curve.
    """

    EASE_IN_OUT_CUBIC = "easeInOutCubic"
    """
    Cubic ease-in/ease-out curve.
    """

    EASE_IN_OUT_CUBIC_EMPHASIZED = "easeInOutCubicEmphasized"
    """
    Material 3 emphasized cubic ease-in/ease-out curve.
    """

    EASE_IN_OUT_EXPO = "easeInOutExpo"
    """
    Exponential ease-in/ease-out curve.
    """

    EASE_IN_OUT_QUAD = "easeInOutQuad"
    """
    Quadratic ease-in/ease-out curve.
    """

    EASE_IN_OUT_QUART = "easeInOutQuart"
    """
    Quartic ease-in/ease-out curve.
    """

    EASE_IN_OUT_QUINT = "easeInOutQuint"
    """
    Quintic ease-in/ease-out curve.
    """

    EASE_IN_OUT_SINE = "easeInOutSine"
    """
    Sinusoidal ease-in/ease-out curve.
    """

    EASE_IN_QUAD = "easeInQuad"
    """
    Quadratic ease-in curve.
    """

    EASE_IN_QUART = "easeInQuart"
    """
    Quartic ease-in curve.
    """

    EASE_IN_QUINT = "easeInQuint"
    """
    Quintic ease-in curve.
    """

    EASE_IN_SINE = "easeInSine"
    """
    Sinusoidal ease-in curve.
    """

    EASE_IN_TO_LINEAR = "easeInToLinear"
    """
    Transitions from ease-in motion into linear motion.
    """

    EASE_OUT = "easeOut"
    """
    Starts quickly and decelerates to the end.
    """

    EASE_OUT_BACK = "easeOutBack"
    """
    Ease-out curve with trailing overshoot.
    """

    EASE_OUT_CIRC = "easeOutCirc"
    """
    Circular ease-out curve.
    """

    EASE_OUT_CUBIC = "easeOutCubic"
    """
    Cubic ease-out curve.
    """

    EASE_OUT_EXPO = "easeOutExpo"
    """
    Exponential ease-out curve.
    """

    EASE_OUT_QUAD = "easeOutQuad"
    """
    Quadratic ease-out curve.
    """

    EASE_OUT_QUART = "easeOutQuart"
    """
    Quartic ease-out curve.
    """

    EASE_OUT_QUINT = "easeOutQuint"
    """
    Quintic ease-out curve.
    """

    EASE_OUT_SINE = "easeOutSine"
    """
    Sinusoidal ease-out curve.
    """

    ELASTIC_IN = "elasticIn"
    """
    Elastic spring-like ease-in curve.
    """

    ELASTIC_IN_OUT = "elasticInOut"
    """
    Elastic spring-like ease-in/ease-out curve.
    """

    ELASTIC_OUT = "elasticOut"
    """
    Elastic spring-like ease-out curve.
    """

    FAST_LINEAR_TO_SLOW_EASE_IN = "fastLinearToSlowEaseIn"
    """
    Starts linear and then eases into a slower end.
    """

    FAST_OUT_SLOWIN = "fastOutSlowIn"
    """
    Material motion curve: quick start, gentle finish.
    """

    LINEAR = "linear"
    """
    Constant speed with no easing.
    """

    LINEAR_TO_EASE_OUT = "linearToEaseOut"
    """
    Starts linear and transitions to an ease-out tail.
    """

    SLOW_MIDDLE = "slowMiddle"
    """
    Slows in the middle section of the animation.
    """


@dataclass
class Animation:
    """
    Explicit animation configuration for animatable control properties.

    Properties that accept animation usually also support shorthand values via
    [`AnimationValue`][flet.]:
    - `True`: enables a default `1000ms` [`LINEAR`][flet.AnimationCurve.] animation.
    - `int`: interpreted as animation duration in milliseconds with a linear curve.
    """

    duration: DurationValue = field(default_factory=lambda: Duration())
    """
    The duration of the animation.

    If provided as an integer, it is considered/assumed to be in milliseconds.
    For more control and flexibility, use [`Duration`][flet.] instead.
    """

    curve: AnimationCurve = AnimationCurve.LINEAR
    """
    Easing curve that shapes interpolation over time.
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
"""Type alias for animation configuration values.

Represents animation input as either:
- `True` or `False` to enable or disable animation,
- an `int` duration in milliseconds,
- or an explicit [`Animation`][flet.] configuration.
"""
