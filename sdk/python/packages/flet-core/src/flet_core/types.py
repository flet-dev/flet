from enum import Enum
from typing import Dict, Tuple, Union, Type, TypeVar, Optional

from flet_core.animation import Animation
from flet_core.border_radius import BorderRadius
from flet_core.margin import Margin
from flet_core.padding import Padding
from flet_core.transform import Offset, Rotate, Scale

try:
    from typing import Literal
except ImportError:
    from typing_extensions import Literal

try:
    from enum import StrEnum
except ImportError:
    class StrEnum(str, Enum):
        value: str


T = TypeVar('T', bound=StrEnum)
R = TypeVar('R')


def get_valid_enum(cls_enum: Type[T], value: Union[T, str, None], default: R) -> Union[T, R]:
    if isinstance(value, cls_enum):
        return value
    return cls_enum.__dict__['_value2member_map_'].get(value, default)

def get_non_default_value(
        enum: Optional[StrEnum], default: Optional[StrEnum], spare_value: R = None,
    ) -> Union[str, None, R]:
    if enum == default:
        return spare_value
    return enum if enum is None else enum.value

WEB_BROWSER = "web_browser"
FLET_APP = "flet_app"
FLET_APP_WEB = "flet_app_web"
FLET_APP_HIDDEN = "flet_app_hidden"


class AppView(Enum):
    WEB_BROWSER = "web_browser"
    FLET_APP = "flet_app"
    FLET_APP_WEB = "flet_app_web"
    FLET_APP_HIDDEN = "flet_app_hidden"


class WebRenderer(Enum):
    AUTO = "auto"
    HTML = "html"
    CANVAS_KIT = "canvaskit"

PaddingValue = Union[None, int, float, Padding]

MarginValue = Union[None, int, float, Margin]

BorderRadiusValue = Union[None, int, float, BorderRadius]

RotateValue = Union[None, int, float, Rotate]

ScaleValue = Union[None, int, float, Scale]

OffsetValue = Union[None, Offset, Tuple[Union[float, int], Union[float, int]]]

AnimationValue = Union[None, bool, int, Animation]


class AnimatedSwitcherTransition(StrEnum):
    FADE = "fade"
    ROTATION = "rotation"
    SCALE = "scale"


class FontWeight(StrEnum):
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


class BoxShape(StrEnum):
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


class MainAxisAlignment(StrEnum):
    START = "start"
    END = "end"
    CENTER = "center"
    SPACE_BETWEEN = "spaceBetween"
    SPACE_AROUND = "spaceAround"
    SPACE_EVENLY = "spaceEvenly"


class CrossAxisAlignment(StrEnum):
    START = "start"
    END = "end"
    CENTER = "center"
    STRETCH = "stretch"
    BASELINE = "baseline"


class LabelPosition(StrEnum):
    RIGHT = "right"
    LEFT = "left"


class BlendMode(StrEnum):
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


class TextAlign(StrEnum):
    LEFT = "left"
    RIGHT = "right"
    CENTER = "center"
    JUSTIFY = "justify"
    START = "start"
    END = "end"


class ScrollMode(StrEnum):
    AUTO = "auto"
    ADAPTIVE = "adaptive"
    ALWAYS = "always"
    HIDDEN = "hidden"


class ClipBehavior(StrEnum):
    NONE = "none"
    ANTI_ALIAS = "antiAlias"
    ANTI_ALIAS_WITH_SAVE_LAYER = "antiAliasWithSaveLayer"
    HARD_EDGE = "hardEdge"


class ImageFit(StrEnum):
    NONE = "none"
    CONTAIN = "contain"
    COVER = "cover"
    FILL = "fill"
    FIT_HEIGHT = "fitHeight"
    FIT_WIDTH = "fitWidth"
    SCALE_DOWN = "scaleDown"


class ImageRepeat(StrEnum):
    NO_REPEAT = "noRepeat"
    REPEAT = "repeat"
    REPEAT_X = "repeatX"
    REPEAT_Y = "repeatY"


class PageDesignLanguage(StrEnum):
    MATERIAL = "material"
    CUPERTINO = "cupertino"
    FLUENT = "fluent"
    MACOS = "macos"
    ADAPTIVE = "adaptive"


class ThemeMode(StrEnum):
    SYSTEM = "system"
    LIGHT = "light"
    DARK = "dark"
