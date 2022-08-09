from typing import Union

from flet.animation import Animation
from flet.border_radius import BorderRadius
from flet.margin import Margin
from flet.padding import Padding
from flet.transform import Offset, Rotate, Scale

PaddingValue = Union[None, int, float, Padding]

MarginValue = Union[None, int, float, Margin]

BorderRadiusValue = Union[None, int, float, BorderRadius]

RotateValue = Union[None, int, float, Rotate]

ScaleValue = Union[None, int, float, Scale]

OffsetValue = Union[None, Offset]

AnimationValue = Union[None, bool, int, Animation]
