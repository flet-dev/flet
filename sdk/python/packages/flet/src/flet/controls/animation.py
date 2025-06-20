from dataclasses import dataclass, field
from enum import Enum
from typing import Optional, Union

from flet.controls.duration import OptionalDurationValue, DurationValue, Duration

__all__ = [
    "Animation",
    "AnimationCurve",
    "AnimationStyle",
    "AnimationValue",
    "OptionalAnimation",
    "OptionalAnimationCurve",
    "OptionalAnimationStyle",
    "OptionalAnimationValue",
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


@dataclass
class AnimationStyle:
    duration: OptionalDurationValue = None
    """
    The duration of the animation.

    Value is of type [`DurationValue`](https://flet.dev/docs/reference/types/aliases#durationvalue).
    """

    reverse_duration: OptionalDurationValue = None
    """
    The duration of the reverse animation.

    Value is of type [`DurationValue`](https://flet.dev/docs/reference/types/aliases#durationvalue).
    """

    curve: "OptionalAnimationCurve" = None
    """
    The curve to use for the animation.

    Value is of type [`AnimationCurve`](https://flet.dev/docs/reference/types/animationcurve).
    """

    reverse_curve: "OptionalAnimationCurve" = None
    """
    The curve to use for the reverse animation.

    Value is of type [`AnimationCurve`](https://flet.dev/docs/reference/types/animationcurve).
    """
    

AnimationValue = Union[bool, int, Animation]
OptionalAnimationValue = Optional[AnimationValue]
OptionalAnimationStyle = Optional[AnimationStyle]
OptionalAnimation = Optional[Animation]
OptionalAnimationCurve = Optional[AnimationCurve]
