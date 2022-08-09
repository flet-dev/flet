import dataclasses
from dataclasses import field
from typing import Optional

try:
    from typing import Literal
except:
    from typing_extensions import Literal

Curve = Literal[
    "bounceIn",
    "bounceInOut",
    "bounceOut",
    "decelerate",
    "ease",
    "easeIn",
    "easeInBack",
    "easeInCirc",
    "easeInCubic",
    "easeInExpo",
    "easeInOut",
    "easeInOutBack",
    "easeInOutCirc",
    "easeInOutCubic",
    "easeInOutCubicEmphasized",
    "easeInOutExpo",
    "easeInOutQuad",
    "easeInOutQuart",
    "easeInOutQuint",
    "easeInOutSine",
    "easeInQuad",
    "easeInQuart",
    "easeInQuint",
    "easeInSine",
    "easeInToLinear",
    "easeOut",
    "easeOutBack",
    "easeOutCirc",
    "easeOutCubic",
    "easeOutExpo",
    "easeOutQuad",
    "easeOutQuart",
    "easeOutQuint",
    "easeOutSine",
    "elasticIn",
    "elasticInOut",
    "elasticOut",
    "fastLinearToSlowEaseIn",
    "fastOutSlowIn",
    "linear",
    "linearToEaseOut",
    "slowMiddle",
]

TransitionValue = Literal["fade", "rotation", "scale"]


@dataclasses.dataclass
class Animation:
    duration: int = field(default=1)
    curve: Optional[Curve] = field(default=None)


def implicit(duration: int, curve: Optional[Curve] = None):
    return Animation(duration=duration, curve=curve)
