from enum import Enum
from typing import Dict, Union

from flet_core.animation import Animation
from flet_core.border_radius import BorderRadius
from flet_core.margin import Margin
from flet_core.padding import Padding
from flet_core.transform import Offset, Rotate, Scale

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

FontWeightString = Literal[
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


class FontWeight(Enum):
    NORMAL = "normal"
    BOLD = "bold"
    W_100 = "w100"
    W_200 = "w200"
    W_300 = "w300"
    W_400 = "w400"
    W_500 = "w500"
    W_600 = "w600"
    W_700 = "w700"
    W_800 = "w800"
    W_900 = "w900"


class BoxShape(Enum):
    RECTANGLE = "rectangle"
    CIRCLE = "circle"


ResponsiveNumber = Union[Dict[str, Union[int, float]], int, float]


class MaterialState(Enum):
    HOVERED = "hovered"
    FOCUSED = "focused"
    PRESSED = "pressed"
    DRAGGED = "dragged"
    SELECTED = "selected"
    SCROLLED_UNDER = "scrolledUnder"
    DISABLED = "disabled"
    ERROR = "error"
    DEFAULT = ""


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


TextAlignString = Literal[None, "left", "right", "center", "justify", "start", "end"]


class TextAlign(Enum):
    NONE = None
    LEFT = "left"
    RIGHT = "right"
    CENTER = "center"
    JUSTIFY = "justify"
    START = "start"
    END = "end"


ScrollModeString = Literal[
    None, True, False, "none", "auto", "adaptive", "always", "hidden"
]


class ScrollMode(Enum):
    AUTO = "auto"
    ADAPTIVE = "adaptive"
    ALWAYS = "always"
    HIDDEN = "hidden"


ClipBehaviorString = Literal[
    None, "none", "antiAlias", "antiAliasWithSaveLayer", "hardEdge"
]


class ClipBehavior(Enum):
    NONE = "none"
    ANTI_ALIAS = "antiAlias"
    ANTI_ALIAS_WITH_SAVE_LAYER = "antiAliasWithSaveLayer"
    HARD_EDGE = "hardEdge"


ImageFitString = Literal[
    None, "none", "contain", "cover", "fill", "fitHeight", "fitWidth", "scaleDown"
]


class ImageFit(Enum):
    NONE = "none"
    CONTAIN = "contain"
    COVER = "cover"
    FILL = "fill"
    FIT_HEIGHT = "fitHeight"
    FIT_WIDTH = "fitWidth"
    SCALE_DOWN = "scaleDown"


ImageRepeatString = Literal[None, "noRepeat", "repeat", "repeatX", "repeatY"]


class ImageRepeat(Enum):
    NO_REPEAT = "noRepeat"
    REPEAT = "repeat"
    REPEAT_X = "repeatX"
    REPEAT_Y = "repeatY"


PageDesignString = Literal[None, "material", "cupertino", "fluent", "macos", "adaptive"]


class PageDesignLanguage(Enum):
    MATERIAL = "material"
    CUPERTINO = "cupertino"
    FLUENT = "fluent"
    MACOS = "macos"
    ADAPTIVE = "adaptive"


ThemeModeString = Literal[None, "system", "light", "dark"]


class ThemeMode(Enum):
    SYSTEM = "system"
    LIGHT = "light"
    DARK = "dark"
