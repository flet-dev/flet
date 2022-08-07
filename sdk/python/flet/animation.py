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


@dataclasses.dataclass
class Animation:
    duration_ms: int = field(default=1)
    curve: Optional[Curve] = field(default=None)


def implicit(duration_ms: int, curve: Optional[Curve] = None):
    return Animation(duration_ms=duration_ms, curve=curve)
