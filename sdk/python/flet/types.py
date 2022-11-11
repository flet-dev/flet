from enum import Enum
from typing import Union

from beartype.typing import Dict

from flet.animation import Animation
from flet.border_radius import BorderRadius
from flet.margin import Margin
from flet.padding import Padding
from flet.transform import Offset, Rotate, Scale

try:
    from typing import Literal
except ImportError:
    from typing_extensions import Literal


PaddingValue = Union[None, int, float, Padding]

MarginValue = Union[None, int, float, Margin]

BorderRadiusValue = Union[None, int, float, BorderRadius]

RotateValue = Union[None, int, float, Rotate]

ScaleValue = Union[None, int, float, Scale]

OffsetValue = Union[None, Offset]

AnimationValue = Union[None, bool, int, Animation]

FontWeight = Literal[
    None,
    "normal",
    "bold",
    "w100",
    "w200",
    "w300",
    "w400",
    "w500",
    "w600",
    "w700",
    "w800",
    "w900",
]


class BoxShape(Enum):
    RECTANGLE = "rectangle"
    CIRCLE = "circle"


ResponsiveNumber = Union[Dict[str, Union[int, float]], int, float]
