import dataclasses
from dataclasses import field
from typing import Optional
from enum import Enum

from flet_core.types import AnimationCurve

try:
    from typing import Literal
except ImportError:
    from typing_extensions import Literal


@dataclasses.dataclass
class Animation:
    duration: int = field(default=1)
    curve: Optional[AnimationCurve] = field(default=None)


def implicit(duration: int, curve: Optional[AnimationCurve] = None):
    return Animation(duration=duration, curve=curve)
