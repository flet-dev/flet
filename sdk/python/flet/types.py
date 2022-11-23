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

MaterialState = Literal[
    "hovered",
    "focused",
    "pressed",
    "dragged",
    "selected",
    "scrolledUnder",
    "disabled",
    "error",
    "",
]

MainAxisAlignmentString = Literal[
    None,
    "start",
    "end",
    "center",
    "spaceBetween",
    "spaceAround",
    "spaceEvenly",
]

CrossAxisAlignmentString = Literal[
    None,
    "start",
    "end",
    "center",
    "stretch",
    "baseline",
]


class MainAxisAlignment(Enum):
    NONE = None
    START = "start"
    END = "end"
    CENTER = "center"
    SPACE_BETWEEN = "spaceBetween"
    SPACE_AROUND = "spaceAround"
    SPACE_EVENLY = "spaceEvenly"


class CrossAxisAlignment(Enum):
    NONE = None
    START = "start"
    END = "end"
    CENTER = "center"
    STRETCH = "stretch"
    BASELINE = "baseline"


LabelPositionString = Literal[None, "right", "left"]


class LabelPosition(Enum):
    NONE = None
    RIGHT = "right"
    LEFT = "left"


BlendModeString = Literal[
    "clear",
    "color",
    "colorBurn",
    "colorDodge",
    "darken",
    "difference",
    "dst",
    "dstATop",
    "dstIn",
    "dstOut",
    "dstOver",
    "exclusion",
    "hardLight",
    "hue",
    "lighten",
    "luminosity",
    "modulate",
    "multiply",
    "overlay",
    "plus",
    "saturation",
    "screen",
    "softLight",
    "src",
    "srcATop",
    "srcIn",
    "srcOut",
    "srcOver",
    "values",
    "xor",
]


class BlendMode(Enum):
    NONE = None
    CLEAR = "clear"
    COLOR = "color"
    COLOR_BURN = "colorBurn"
    COLOR_DODGE = "colorDodge"
    DARKEN = "darken"
    DIFFERENCE = "difference"
    DST = "dst"
    DST_A_TOP = "dstATop"
    DST_IN = "dstIn"
    DST_OUT = "dstOut"
    DST_OVER = "dstOver"
    EXCLUSION = "exclusion"
    HARD_LIGHT = "hardLight"
    HUE = "hue"
    LIGHTEN = "lighten"
    LUMINOSITY = "luminosity"
    MODULATE = "modulate"
    MULTIPLY = "multiply"
    OVERLAY = "overlay"
    PLUS = "plus"
    SATURATION = "saturation"
    SCREEN = "screen"
    SOFT_LIGHT = "softLight"
    SRC = "src"
    SRC_A_TOP = "srcATop"
    SRC_IN = "srcIn"
    SRC_OUT = "srcOut"
    SRC_OVER = "srcOver"
    VALUES = "values"
    XOR = "xor"
