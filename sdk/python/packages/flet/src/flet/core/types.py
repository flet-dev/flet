from dataclasses import dataclass
from datetime import date, datetime
from enum import Enum
from typing import Any, Callable, Dict, List, Optional, Protocol, Tuple, TypeVar, Union

from flet.core.border_radius import BorderRadius
from flet.core.colors import Colors
from flet.core.control_event import ControlEvent
from flet.core.cupertino_colors import CupertinoColors
from flet.core.cupertino_icons import CupertinoIcons
from flet.core.event import Event
from flet.core.icons import Icons
from flet.core.margin import Margin
from flet.core.padding import Padding
from flet.core.transform import Offset, Rotate, Scale

WEB_BROWSER = "web_browser"
FLET_APP = "flet_app"
FLET_APP_WEB = "flet_app_web"
FLET_APP_HIDDEN = "flet_app_hidden"


class AppView(Enum):
    WEB_BROWSER = "web_browser"
    FLET_APP = "flet_app"
    FLET_APP_WEB = "flet_app_web"
    FLET_APP_HIDDEN = "flet_app_hidden"


class WindowEventType(Enum):
    CLOSE = "close"
    FOCUS = "focus"
    BLUR = "blur"
    HIDE = "hide"
    SHOW = "show"
    MAXIMIZE = "maximize"
    UNMAXIMIZE = "unmaximize"
    MINIMIZE = "minimize"
    RESTORE = "restore"
    RESIZE = "resize"
    RESIZED = "resized"
    MOVE = "move"
    MOVED = "moved"
    LEAVE_FULL_SCREEN = "leave-full-screen"
    ENTER_FULL_SCREEN = "enter-full-screen"


class WebRenderer(Enum):
    AUTO = "auto"
    HTML = "html"
    CANVAS_KIT = "canvaskit"


class UrlTarget(Enum):
    BLANK = "blank"
    SELF = "_self"
    PARENT = "_parent"
    TOP = "_top"


PaddingValue = Union[int, float, Padding]

MarginValue = Union[int, float, Margin]

BorderRadiusValue = Union[int, float, BorderRadius]

RotateValue = Union[int, float, Rotate]

ScaleValue = Union[int, float, Scale]

OffsetValue = Union[Offset, Tuple[Union[float, int], Union[float, int]]]


@dataclass
class Duration:
    microseconds: int = 0
    milliseconds: int = 0
    seconds: int = 0
    minutes: int = 0
    hours: int = 0
    days: int = 0


DurationValue = Union[int, Duration]


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


class NotchShape(Enum):
    AUTO = "auto"
    CIRCULAR = "circular"


Number = Union[int, float]
ResponsiveNumber = Union[Dict[str, Number], Number]
OptionalNumber = Optional[Number]

# str type alias
OptionalString = Optional[str]


class ControlState(Enum):
    HOVERED = "hovered"
    FOCUSED = "focused"
    PRESSED = "pressed"
    DRAGGED = "dragged"
    SELECTED = "selected"
    SCROLLED_UNDER = "scrolledUnder"
    DISABLED = "disabled"
    ERROR = "error"
    DEFAULT = "default"


class MainAxisAlignment(Enum):
    START = "start"
    END = "end"
    CENTER = "center"
    SPACE_BETWEEN = "spaceBetween"
    SPACE_AROUND = "spaceAround"
    SPACE_EVENLY = "spaceEvenly"


class CrossAxisAlignment(Enum):
    START = "start"
    END = "end"
    CENTER = "center"
    STRETCH = "stretch"
    BASELINE = "baseline"


class VerticalAlignment(Enum):
    NONE = None
    START = -1.0
    END = 1.0
    CENTER = 0.0


class TabAlignment(Enum):
    START = "start"
    START_OFFSET = "startOffset"
    FILL = "fill"
    CENTER = "center"


class LabelPosition(Enum):
    RIGHT = "right"
    LEFT = "left"


class BlendMode(Enum):
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


class TextAlign(Enum):
    LEFT = "left"
    RIGHT = "right"
    CENTER = "center"
    JUSTIFY = "justify"
    START = "start"
    END = "end"


class ScrollMode(Enum):
    AUTO = "auto"
    ADAPTIVE = "adaptive"
    ALWAYS = "always"
    HIDDEN = "hidden"


class ClipBehavior(Enum):
    NONE = "none"
    ANTI_ALIAS = "antiAlias"
    ANTI_ALIAS_WITH_SAVE_LAYER = "antiAliasWithSaveLayer"
    HARD_EDGE = "hardEdge"


class ImageFit(Enum):
    NONE = "none"
    CONTAIN = "contain"
    COVER = "cover"
    FILL = "fill"
    FIT_HEIGHT = "fitHeight"
    FIT_WIDTH = "fitWidth"
    SCALE_DOWN = "scaleDown"


class ImageRepeat(Enum):
    NO_REPEAT = "noRepeat"
    REPEAT = "repeat"
    REPEAT_X = "repeatX"
    REPEAT_Y = "repeatY"


class PagePlatform(Enum):
    IOS = "ios"
    ANDROID = "android"
    ANDROID_TV = "android_tv"
    MACOS = "macos"
    WINDOWS = "windows"
    LINUX = "linux"


class ThemeMode(Enum):
    SYSTEM = "system"
    LIGHT = "light"
    DARK = "dark"


class Brightness(Enum):
    LIGHT = "light"
    DARK = "dark"


class Orientation(Enum):
    PORTRAIT = "portrait"
    LANDSCAPE = "landscape"


class FloatingActionButtonLocation(Enum):
    CENTER_DOCKED = "centerDocked"
    CENTER_FLOAT = "centerFloat"
    CENTER_TOP = "centerTop"
    END_CONTAINED = "endContained"
    END_DOCKED = "endDocked"
    END_FLOAT = "endFloat"
    END_TOP = "endTop"
    MINI_CENTER_DOCKED = "miniCenterDocked"
    MINI_CENTER_FLOAT = "miniCenterFloat"
    MINI_CENTER_TOP = "miniCenterTop"
    MINI_END_DOCKED = "miniEndDocked"
    MINI_END_FLOAT = "miniEndFloat"
    MINI_END_TOP = "miniEndTop"
    MINI_START_DOCKED = "miniStartDocked"
    MINI_START_FLOAT = "miniStartFloat"
    MINI_START_TOP = "miniStartTop"
    START_DOCKED = "startDocked"
    START_FLOAT = "startFloat"
    START_TOP = "startTop"


class AppLifecycleState(Enum):
    SHOW = "show"
    RESUME = "resume"
    HIDE = "hide"
    INACTIVE = "inactive"
    PAUSE = "pause"
    DETACH = "detach"
    RESTART = "restart"


class MouseCursor(Enum):
    ALIAS = "alias"
    ALL_SCROLL = "allScroll"
    BASIC = "basic"
    CELL = "cell"
    CLICK = "click"
    CONTEXT_MENU = "contextMenu"
    COPY = "copy"
    DISAPPEARING = "disappearing"
    FORBIDDEN = "forbidden"
    GRAB = "grab"
    GRABBING = "grabbing"
    HELP = "help"
    MOVE = "move"
    NO_DROP = "noDrop"
    NONE = "none"
    PRECISE = "precise"
    PROGRESS = "progress"
    RESIZE_COLUMN = "resizeColumn"
    RESIZE_DOWN = "resizeDown"
    RESIZE_DOWN_LEFT = "resizeDownLeft"
    RESIZE_DOWN_RIGHT = "resizeDownRight"
    RESIZE_LEFT = "resizeLeft"
    RESIZE_LEFT_RIGHT = "resizeLeftRight"
    RESIZE_RIGHT = "resizeRight"
    RESIZE_ROW = "resizeRow"
    RESIZE_UP = "resizeUp"
    RESIZE_UP_DOWN = "resizeUpDown"
    RESIZE_UP_LEFT = "resizeUpLeft"
    RESIZE_UP_LEFT_DOWN_RIGHT = "resizeUpLeftDownRight"
    RESIZE_UP_RIGHT = "resizeUpRight"
    RESIZE_UP_RIGHT_DOWN_LEFT = "resizeUpRightDownLeft"
    TEXT = "text"
    VERTICAL_TEXT = "verticalText"
    WAIT = "wait"
    ZOOM_IN = "zoomIn"
    ZOOM_OUT = "zoomOut"


class PointerDeviceType(Enum):
    TOUCH = "touch"
    MOUSE = "mouse"
    STYLUS = "stylus"
    INVERTED_STYLUS = "invertedStylus"
    TRACKPAD = "trackpad"
    UNKNOWN = "unknown"


class StrokeCap(Enum):
    ROUND = "round"
    SQUARE = "square"
    BUTT = "butt"


class StrokeJoin(Enum):
    MITER = "miter"
    ROUND = "round"
    BEVEL = "bevel"


class VisualDensity(Enum):
    STANDARD = "standard"
    COMPACT = "compact"
    COMFORTABLE = "comfortable"
    ADAPTIVE_PLATFORM_DENSITY = "adaptivePlatformDensity"


@dataclass
class Locale:
    language_code: Optional[str] = None
    country_code: Optional[str] = None
    script_code: Optional[str] = None


@dataclass
class LocaleConfiguration:
    supported_locales: Optional[List[Locale]] = None
    current_locale: Optional[Locale] = None


# Events
ControlEventType = TypeVar("ControlEventType", bound=ControlEvent)
EventType = TypeVar("EventType", bound=Event)
OptionalEventCallable = Optional[Callable[[EventType], Any]]
OptionalControlEventCallable = Optional[Callable[[ControlEvent], Any]]


class OnFocusEvent(ControlEvent):
    def __init__(self, e: ControlEvent):
        super().__init__(e.target, e.name, e.data, e.control, e.page)
        self.primary: bool = bool(e.data)


# Colors
ColorEnums = (Colors, CupertinoColors)
ColorValue = Union[str, Colors, CupertinoColors]

# Icons
IconEnums = (Icons, CupertinoIcons)
IconValue = Union[str, Icons, CupertinoIcons]
IconValueOrControl = Union[IconValue, "Control"]

# ControlState
T = TypeVar("T")
ControlStateValue = Union[None, T, Dict[ControlState, T]]

# DateTime
DateTimeValue = Union[datetime, date]

# Wrapper
Wrapper = Callable[..., Any]


# Protocols
class SupportsStr(Protocol):
    def __str__(self) -> str:
        ...
