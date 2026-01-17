from dataclasses import dataclass, field
from enum import Enum
from typing import (
    TYPE_CHECKING,
    Any,
    Callable,
    Optional,
    Protocol,
    Union,
)

from flet.controls.colors import Colors
from flet.controls.cupertino.cupertino_colors import CupertinoColors
from flet.controls.icon_data import IconData

if TYPE_CHECKING:
    from flet.controls.control import Control  # noqa
    from flet.controls.buttons import ShapeBorder


class AppView(Enum):
    """
    TBD
    """

    WEB_BROWSER = "web_browser"
    FLET_APP = "flet_app"
    FLET_APP_WEB = "flet_app_web"
    FLET_APP_HIDDEN = "flet_app_hidden"


class WebRenderer(Enum):
    """
    TBD
    """

    AUTO = "auto"
    CANVAS_KIT = "canvaskit"
    SKWASM = "skwasm"


class RouteUrlStrategy(Enum):
    """
    TBD
    """

    PATH = "path"
    HASH = "hash"


class UrlTarget(Enum):
    """
    Specifies where to open a URL.
    """

    BLANK = "blank"
    """
    Opens the URL in a new browser tab or window.
    """

    SELF = "_self"
    """
    Opens in the same browsing context (i.e., same tab).
    """

    PARENT = "_parent"
    """
    Opens in the parent frame, useful with nested iframes.
    """

    TOP = "_top"
    """
    Opens in the topmost frame, breaking out of any iframe.
    """


@dataclass
class Url:
    url: str
    """
    The url to open.
    """

    target: Optional[Union[UrlTarget, str]] = None
    """
    Where to open URL in the web mode.
    """


class FontWeight(Enum):
    """
    The thickness of the glyphs used to draw the text.
    """

    NORMAL = "normal"
    """
    The default font weight, equal to `w400`.
    """

    BOLD = "bold"
    """
    A commonly used font weight that is heavier than normal, equal to `w700`.
    """

    W_100 = "w100"
    """
    Thin, the least thick.
    """

    W_200 = "w200"
    """
    Extra-light.
    """

    W_300 = "w300"
    """
    Light.
    """

    W_400 = "w400"
    """
    Normal / regular / plain.
    """

    W_500 = "w500"
    """
    Medium.
    """

    W_600 = "w600"
    """
    Semi-bold.
    """

    W_700 = "w700"
    """
    Bold.
    """

    W_800 = "w800"
    """
    Extra-bold.
    """

    W_900 = "w900"
    """
    Black, the most thick.
    """


@dataclass
class NotchShape:
    """
    A shape with a notch in its outline.

    Typically used as the outline of a 'host' control to make a notch that
    accommodates a 'guest' control.
    e.g the [`BottomAppBar`][flet.] may have a notch to accommodate
    the [`FloatingActionButton`][flet.].

    This class is not intended to be used directly. See usable derivatives:

    - [`AutomaticNotchShape`][flet.]
    - [`CircularRectangleNotchShape`][flet.]
    """

    _type: Optional[str] = field(init=False, repr=False, compare=False, default=None)


@dataclass
class CircularRectangleNotchShape(NotchShape):
    """
    A rectangle with a smooth circular notch.
    """

    inverted: bool = False
    """
    Whether the notch should be placed at the bottom of the rectangle.
    """

    def __post_init__(self):
        self._type = "circular"


@dataclass
class AutomaticNotchShape(NotchShape):
    """
    A notch sahpe created from [`ShapeBorder`][flet.]s.
    """

    host: "ShapeBorder"
    guest: Optional["ShapeBorder"] = None

    def __post_init__(self):
        self._type = "auto"


class ResponsiveRowBreakpoint(Enum):
    """
    Breakpoint names used by [`ResponsiveRow`][flet.] and responsive
    properties such as [`Control.col`][flet.].

    To define custom breakpoints, see [`ResponsiveRow.breakpoints`][flet.].
    """

    XS = "xs"
    """
    Extra small screens. Default min width: `0` px.
    """

    SM = "sm"
    """
    Small screens. Default min width: `576` px.
    """

    MD = "md"
    """
    Medium screens. Default min width: `768` px.
    """

    LG = "lg"
    """
    Large screens. Default min width: `992` px.
    """

    XL = "xl"
    """
    Extra-large screens. Default min width: `1200` px.
    """

    XXL = "xxl"
    """
    Double extra-large screens. Default min width: `1400` px.
    """


Number = Union[int, float]
ResponsiveNumber = Union[dict[Union[str, ResponsiveRowBreakpoint], Number], Number]


class MainAxisAlignment(Enum):
    """
    How the children should be placed along the main axis.
    """

    START = "start"
    """
    Place the children as close to the start of the main axis as possible.
    """

    END = "end"
    """
    Place the children as close to the end of the main axis as possible.
    """

    CENTER = "center"
    """
    Place the children as close to the middle of the main axis as possible.
    """

    SPACE_BETWEEN = "spaceBetween"
    """
    Place the free space evenly between the children.
    """

    SPACE_AROUND = "spaceAround"
    """
    Place the free space evenly between the children as well as half of that space
    before and after the first and last child.
    """

    SPACE_EVENLY = "spaceEvenly"
    """
    Place the free space evenly between the children as well as before and after the
    first and last child.
    """


class CrossAxisAlignment(Enum):
    """
    How the children should be placed along the cross axis
    """

    START = "start"
    """
    Place the children with their start edge aligned with the start side of the cross
    axis.
    """

    END = "end"
    """
    Place the children as close to the end of the cross axis as possible.
    """

    CENTER = "center"
    """
    Place the children so that their centers align with the middle of the cross axis.
    """

    STRETCH = "stretch"
    """
    Require the children to fill the cross axis.
    """

    BASELINE = "baseline"
    """
    Place the children along the cross axis such that their baselines match.
    """


class VerticalAlignment(Enum):
    """
    The vertical alignment of text within an input box.
    """

    NONE = None

    START = -1.0
    """
    Aligns the text vertically at the topmost location of the TextField.
    """

    END = 1.0
    """
    Aligns the text vertically at the bottommost location of the TextField.
    """

    CENTER = 0.0
    """
    Aligns the text vertically in the center of the TextField.
    """


class LabelPosition(Enum):
    """
    Position of label in a [`Checkbox`][flet.], [`Radio`][flet.] or
    [`Switch`][flet.]
    """

    RIGHT = "right"
    """
    The label is positioned to the right of the control.
    """

    LEFT = "left"
    """
    The label is positioned to the left of the control.
    """


class BlendMode(Enum):
    """
    See [BlendMode](https://api.flutter.dev/flutter/dart-ui/BlendMode.html) from
    Flutter documentation for blend mode examples.
    """

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
    """
    The horizontal alignment of text within an input box.
    """

    LEFT = "left"
    """
    Align the text on the left edge of the container.
    """

    RIGHT = "right"
    """
    Align the text on the right edge of the container.
    """

    CENTER = "center"
    """
    Align the text in the center of the container.
    """

    JUSTIFY = "justify"
    """
    Stretch lines of text that end with a soft line break to fill the width of the
    container.
    """

    START = "start"
    """
    Align the text on the leading edge of the container.
    """

    END = "end"
    """
    Align the text on the trailing edge of the container.
    """


class ScrollMode(Enum):
    """
    Weather scrolling is enabled and visibility of scroll bar options.
    """

    AUTO = "auto"
    """
    Scrolling is enabled and scroll bar is only shown when scrolling occurs.
    """

    ADAPTIVE = "adaptive"
    """
    Scrolling is enabled and scroll bar is always shown when running app as web or
    desktop.
    """

    ALWAYS = "always"
    """
    Scrolling is enabled and scroll bar is always shown.
    """

    HIDDEN = "hidden"
    """
    Scrolling is enabled, but scroll bar is always hidden.
    """


class ClipBehavior(Enum):
    """
    Different ways to clip content.

    See [Clip](https://api.flutter.dev/flutter/dart-ui/Clip.html)
    from Flutter documentation for ClipBehavior examples.
    """

    NONE = "none"
    """
    No clip at all.

    This is the default option for most widgets: if the content does not overflow the
    widget boundary, don't pay any performance cost for clipping.
    """

    ANTI_ALIAS = "antiAlias"
    """
    Clip with anti-aliasing.

    This mode has anti-aliased clipping edges, which reduces jagged edges when the clip
    shape itself has edges that are diagonal, curved, or otherwise not axis-aligned.
    """

    ANTI_ALIAS_WITH_SAVE_LAYER = "antiAliasWithSaveLayer"
    """
    Clip with anti-aliasing and saveLayer immediately following the clip.
    """

    HARD_EDGE = "hardEdge"
    """
    Clip, but do not apply anti-aliasing.

    This mode enables clipping, but curves and non-axis-aligned straight lines will be
    jagged as no effort is made to anti-alias.
    """


class ImageRepeat(Enum):
    """
    How to paint any portions of a box not covered by an image.
    """

    NO_REPEAT = "noRepeat"
    """Leave uncovered portions of the box transparent."""

    REPEAT = "repeat"
    """Repeat the image in both the x and y directions until the box is filled."""

    REPEAT_X = "repeatX"
    """Repeat the image in the x direction until the box is filled horizontally."""

    REPEAT_Y = "repeatY"
    """Repeat the image in the y direction until the box is filled vertically."""


class PagePlatform(Enum):
    """
    Supported platforms for a page, including mobile and desktop systems. Each platform
    corresponds to a specific operating system or environment.
    """

    IOS = "ios"
    ANDROID = "android"
    ANDROID_TV = "android_tv"
    MACOS = "macos"
    WINDOWS = "windows"
    LINUX = "linux"

    def is_apple(self) -> bool:
        """Whether this PagePlatform instance is an Apple (iOS or macOS) platform."""
        return self in {PagePlatform.IOS, PagePlatform.MACOS}

    def is_mobile(self) -> bool:
        """Whether this PagePlatform instance is a mobile (iOS or Android) platform."""
        return self in {PagePlatform.IOS, PagePlatform.ANDROID}

    def is_desktop(self) -> bool:
        """
        Whether this PagePlatform instance is a desktop (macOS, Windows, Linux)
        platform.
        """
        return self in {PagePlatform.MACOS, PagePlatform.WINDOWS, PagePlatform.LINUX}


class ThemeMode(Enum):
    """
    Describes which theme will be used by Flet app.
    """

    SYSTEM = "system"
    """
    Use either the light or dark theme based on what the user has selected in the
    system settings.
    """

    LIGHT = "light"
    """
    Always use the light mode regardless of system preference.
    """

    DARK = "dark"
    """
    Always use the dark mode (if available) regardless of system preference.
    """


class Brightness(Enum):
    """
    Describes the contrast of a theme or color palette.
    """

    LIGHT = "light"
    """
    The color is light and will require a dark text color to achieve readable contrast.

    For example, the color might be bright white, requiring black text.
    """

    DARK = "dark"
    """
    The color is dark and will require a light text color to achieve readable contrast.

    For example, the color might be dark grey, requiring white text.
    """


class Orientation(Enum):
    """
    Represents the layout orientation.
    """

    PORTRAIT = "portrait"
    """
    Orientation with greater height than width.
    """

    LANDSCAPE = "landscape"
    """
    Orientation with greater width than height.
    """


class DeviceOrientation(Enum):
    """
    Supported physical orientations for mobile devices.
    """

    PORTRAIT_UP = "portraitUp"
    """
    Device held upright in portrait mode.
    """

    PORTRAIT_DOWN = "portraitDown"
    """
    Device held upside-down in portrait mode.
    """

    LANDSCAPE_LEFT = "landscapeLeft"
    """
    Device rotated 90° counter-clockwise (home button or primary edge on the right).
    """

    LANDSCAPE_RIGHT = "landscapeRight"
    """
    Device rotated 90° clockwise (home button or primary edge on the left).
    """


class FloatingActionButtonLocation(Enum):
    """
    Defines a position for the [`FloatingActionButton`][flet.].

    See [FloatingActionButtonLocation](https://api.flutter.dev/flutter/material/FloatingActionButtonLocation-class.html)
    from Flutter documentation for placement location examples.
    """

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
    """
    States that an application can be in once it is running.
    """

    SHOW = "show"
    """
    The application is shown.

    On mobile platforms, this is usually just before the application replaces another
    application in the foreground.

    On desktop platforms, this is just before the application is shown after being
    minimized or otherwise made to show at least one view of the application.

    On the web, this is just before a window (or tab) is shown.
    """

    RESUME = "resume"
    """
    The application gains input focus. Indicates that the application is entering a
    state where it is visible, active, and accepting user input.
    """

    HIDE = "hide"
    """
    The application is hidden.

    On mobile platforms, this is usually just before the application is replaced by
    another application in the foreground.

    On desktop platforms, this is just before the application is hidden by being
    minimized or otherwise hiding all views of the application.

    On the web, this is just before a window (or tab) is hidden.
    """

    INACTIVE = "inactive"
    """
    The application loses input focus.

    On mobile platforms, this can be during a phone call or when a system dialog is
    visible.

    On desktop platforms, this is when all views in an application have lost input
    focus but at least one view of the application is still visible.

    On the web, this is when the window (or tab) has lost input focus.
    """

    PAUSE = "pause"
    """
    The application is paused.

    On mobile platforms, this happens right before the application is replaced by
    another application.

    On desktop platforms and the web, this function is not called.
    """

    DETACH = "detach"
    """
    The application has exited, and detached all host views from the engine.

    This callback is only called on iOS and Android.
    """

    RESTART = "restart"
    """
    The application is resumed after being paused.

    On mobile platforms, this happens just before this application takes over as the
    active application.

    On desktop platforms and the web, this function is not called.
    """


class MouseCursor(Enum):
    """
    Various mouse cursor types that represent different operations or states.
    """

    ALIAS = "alias"
    """
    A cursor indicating that the current operation will create an alias of, or a
    shortcut of the item. Typically the shape of an arrow with a shortcut icon at the
    corner.
    """

    ALL_SCROLL = "allScroll"
    """
    A cursor indicating scrolling in any direction. Typically the shape of a dot
    surrounded by 4 arrows.
    """

    BASIC = "basic"
    """
    The platform-dependent basic cursor. Typically the shape of an arrow.
    """

    CELL = "cell"
    """
    A cursor indicating selectable table cells. Typically the shape of a hollow plus
    sign.
    """

    CLICK = "click"
    """
    A cursor that emphasizes an element being clickable, such as a hyperlink.
    Typically the shape of a pointing hand.
    """

    CONTEXT_MENU = "contextMenu"
    """
    A cursor indicating somewhere the user can trigger a context menu. Typically the
    shape of an arrow with a small menu at the corner.
    """

    COPY = "copy"
    """
    A cursor indicating that the current operation will copy the item. Typically the
    shape of an arrow with a boxed plus sign at the corner.
    """

    DISAPPEARING = "disappearing"
    """
    A cursor indicating that the current operation will result in the disappearance of
    the item. Typically the shape of an arrow with a cloud of smoke at the corner.
    """

    FORBIDDEN = "forbidden"
    """
    A cursor indicating an operation that will not be carried out.
    Typically the shape of a circle with a diagonal line.
    """

    GRAB = "grab"
    """
    A cursor indicating something that can be dragged. Typically the shape of an open
    hand.
    """

    GRABBING = "grabbing"
    """
    A cursor indicating something that is being dragged. Typically the shape of a
    closed hand.
    """

    HELP = "help"
    """
    A cursor indicating help information. Typically the shape of a question mark, or an
    arrow therewith.
    """

    MOVE = "move"
    """
    A cursor indicating moving something. Typically the shape of four-way arrow.
    """

    NO_DROP = "noDrop"
    """
    A cursor indicating somewhere that the current item may not be dropped.
    Typically the shape of a hand with a forbidden sign at the corner.
    """

    NONE = "none"
    """
    Hide the cursor.
    """

    PRECISE = "precise"
    """
    A cursor indicating precise selection, such as selecting a pixel in a bitmap.
    Typically the shape of a crosshair.
    """

    PROGRESS = "progress"
    """
    A cursor indicating the status that the program is busy but can still be interacted
    with. Typically the shape of an arrow with an hourglass or a watch at the corner.
    """

    RESIZE_COLUMN = "resizeColumn"
    """
    A cursor indicating resizing a column, or an item horizontally. Typically the shape
    of arrows pointing left and right with a vertical bar separating them.
    """

    RESIZE_DOWN = "resizeDown"
    """
    A cursor indicating resizing an object from its bottom edge. Typically the shape of
    an arrow pointing down.
    """

    RESIZE_DOWN_LEFT = "resizeDownLeft"
    """
    A cursor indicating resizing an object from its bottom-left corner. Typically the
    shape of an arrow pointing lower left.
    """

    RESIZE_DOWN_RIGHT = "resizeDownRight"
    """
    A cursor indicating resizing an object from its bottom-right corner. Typically the
    shape of an arrow pointing lower right.
    """

    RESIZE_LEFT = "resizeLeft"
    """
    A cursor indicating resizing an object from its left edge. Typically the shape of
    an arrow pointing left.
    """

    RESIZE_LEFT_RIGHT = "resizeLeftRight"
    """
    A cursor indicating resizing an object bidirectionally from its left or right edge.
    Typically the shape of a bidirectional arrow pointing left and right.
    """

    RESIZE_RIGHT = "resizeRight"
    """
    A cursor indicating resizing an object from its right edge. Typically the shape of
    an arrow pointing right.
    """

    RESIZE_ROW = "resizeRow"
    """
    A cursor indicating resizing a row, or an item vertically. Typically the shape of
    arrows pointing up and down with a horizontal bar separating them.
    """

    RESIZE_UP = "resizeUp"
    """
    A cursor indicating resizing an object from its top edge. Typically the shape of an
    arrow pointing up.
    """

    RESIZE_UP_DOWN = "resizeUpDown"
    """
    A cursor indicating resizing an object bidirectionally from its top or bottom edge.
    Typically the shape of a bidirectional arrow pointing up and down.
    """

    RESIZE_UP_LEFT = "resizeUpLeft"
    """
    A cursor indicating resizing an object from its top-left corner. Typically the
    shape of an arrow pointing upper left.
    """

    RESIZE_UP_LEFT_DOWN_RIGHT = "resizeUpLeftDownRight"
    """
    A cursor indicating resizing an object bidirectionally from its top left or bottom
    right corner. Typically the shape of a bidirectional arrow pointing upper left and
    lower right.
    """

    RESIZE_UP_RIGHT = "resizeUpRight"
    """
    A cursor indicating resizing an object from its top-right corner. Typically the
    shape of an arrow pointing upper right.
    """

    RESIZE_UP_RIGHT_DOWN_LEFT = "resizeUpRightDownLeft"
    """
    A cursor indicating resizing an object bidirectionally from its top right or bottom
    left corner. Typically the shape of a bidirectional arrow pointing upper right and
    lower left.
    """

    TEXT = "text"
    """
    A cursor indicating selectable text. Typically the shape of a capital I.
    """

    VERTICAL_TEXT = "verticalText"
    """
    A cursor indicating selectable vertical text. Typically the shape of a capital I
    rotated to be horizontal.
    """

    WAIT = "wait"
    """
    A cursor indicating the status that the program is busy and therefore can not be
    interacted with. Typically the shape of an hourglass or a watch.

    This cursor is not available as a system cursor on macOS. Although macOS displays a
    "spinning ball" cursor when busy, it's handled by the OS and not exposed for
    applications to choose.
    """

    ZOOM_IN = "zoomIn"
    """
    A cursor indicating zooming in. Typically a magnifying glass with a plus sign.
    """

    ZOOM_OUT = "zoomOut"
    """
    A cursor indicating zooming out. Typically a magnifying glass with a minus sign.
    """


class PointerDeviceType(Enum):
    """
    The kind of pointer device.
    """

    TOUCH = "touch"
    """
    A touch-based pointer device.
    """

    MOUSE = "mouse"
    """
    A mouse-based pointer device.
    """

    STYLUS = "stylus"
    """
    A pointer device with a stylus.
    """

    INVERTED_STYLUS = "invertedStylus"
    """
    A pointer device with a stylus that has been inverted.
    """

    TRACKPAD = "trackpad"
    """
    Gestures from a trackpad.
    """

    UNKNOWN = "unknown"
    """
    An unknown pointer device.
    """


class StrokeCap(Enum):
    """
    Styles to use for line endings.
    """

    ROUND = "round"
    """
    Begin and end contours with a semi-circle extension.
    """

    SQUARE = "square"
    """
    Begin and end contours with a half square extension.
    """

    BUTT = "butt"
    """
    Begin and end contours with a flat edge and no extension.
    """


class StrokeJoin(Enum):
    """
    Styles to use for line segment joins.
    """

    MITER = "miter"
    """
    Joins between line segments form sharp corners.
    """

    ROUND = "round"
    """
    Joins between line segments are semi-circular.
    """

    BEVEL = "bevel"
    """
    Joins between line segments connect the corners of the butt ends of the line
    segments to give a beveled appearance.
    """


class VisualDensity(Enum):
    """
    Defines the visual density of user interface components.
    """

    STANDARD = "standard"
    """
    The default/standard profile for visual density.

    This default value represents a visual density that is less dense than
    either [`COMFORTABLE`][(c).] or [`COMPACT`][(c).], and corresponds to
    density values of zero in both axes.
    """

    COMPACT = "compact"
    """
    The profile for a "compact" interpretation of visual density.

    Individual components will interpret the density value independently, making
    themselves more visually dense than [`STANDARD`][(c).] and [`COMFORTABLE`][(c).] to
    different degrees based on the Material Design specification of the
    [`COMFORTABLE`][(c).] setting for their particular use case.

    It corresponds to a density value of `-2` in both axes.
    """

    COMFORTABLE = "comfortable"
    """
    The profile for a "comfortable" interpretation of visual density.

    Individual
    components will interpret the density value independently, making themselves more
    visually dense than [`STANDARD`][(c).] and less dense than [`COMPACT`][(c).]
    to different degrees based on the Material Design specification of the
    comfortable setting for their particular use case.

    It corresponds to a density value of `-1` in both axes.
    """

    ADAPTIVE_PLATFORM_DENSITY = "adaptivePlatformDensity"
    """
    Visual density that is adaptive based on the given platform.

    For desktop platforms, this returns [`COMPACT`][(c).], and for other platforms,
    it returns a default-constructed visual density.
    """


@dataclass
class Locale:
    """
    An identifier used to select a user's language and formatting preferences.
    """

    language_code: str = "und"
    """
    The primary language subtag/code of the locale, e.g `en` for English.

    Its value is case-sensitive and must be a registered subtag in the
    [IANA Language Subtag Registry](https://www.iana.org/assignments/language-subtag-registry/language-subtag-registry)
    with the type "language". If you use a deprecated subtag, it will be internally
    modified to its “Preferred-Value”, if it has one. For example: `Locale("he")`
    and `Locale("iw")` are equal, and both have the `language_code="he”`,
    because `iw` is a deprecated language subtag which has been replaced by `he`.

    When there is no language subtag, this parameter should be set
    to `"und"` (the default), which represents an undefined language code.
    """

    country_code: Optional[str] = None
    """
    The country code or region subtag of the locale, e.g `US` for the United States.

    Its value is case-sensitive and must be a registered subtag in the
    [IANA Language Subtag Registry](https://www.iana.org/assignments/language-subtag-registry/language-subtag-registry)
    with the type "region". If you use a deprecated subtag, it will be internally
    modified to its “Preferred-Value”, if it has one. For example: `Locale("de", "DE")`
    and `Locale("de", "DD")` are equal, and both have the `country_code="DE”`,
    because `DD` is a deprecated region subtag which has been replaced by `DE`.

    Locales may also be defined without this, to specify a generic fallback for a
    particular script.
    """  # noqa: E501

    script_code: Optional[str] = None
    """
    The script code/subtag of the locale, e.g. `Hant` for Traditional Chinese
    or `Hans` for Simplified Chinese. It is especially recommended to set this property
    explicitly for languages with more than one script.

    Its value must be a valid Unicode Language Identifier script subtag as listed in
    [Unicode CLDR supplemental data](https://github.com/unicode-org/cldr/blob/master/common/validity/script.xml).
    """  # noqa: E501

    def __post_init__(self):
        if self.language_code == "":
            raise ValueError("language_code cannot be empty")


@dataclass
class LocaleConfiguration:
    """
    Represents the configuration for supported locales and the current locale.
    """

    supported_locales: list[Locale] = field(
        default_factory=lambda: [Locale("en", "US")]
    )
    """
    A list of locales that the application supports for localization.

    Note:
        - Locales unsupported/invalid are ignored.
        - Order matters: Locale resolution is performed by progressively relaxing
            specificity until a match is found. Matching is attempted in the following
            priority order:

            1. language + script + country
            2. language + script
            3. language + country
            4. language only
            5. country only (only if no language-based match is found)

            When multiple supported locales match at the same priority level,
            the first matching locale in `supported_locales` is selected.
            If no supported locale matches at any level, the first entry in
            `supported_locales` is used as the final fallback.
        - For languages with multiple scripts or regional variants, include locales in
            increasing order of specificity: language-only → language+script →
            language+script+country. Defining all of these variants is not strictly
            required, but doing so greatly improves locale resolution and reduces
            ambiguous matches. Omitting intermediate fallbacks can lead to incorrect
            script or regional selection in edge cases—for example, a Simplified
            Chinese user in Taiwan (`zh_Hans_TW`) may incorrectly resolve to
            Traditional Chinese if `zh_Hans` and `zh_Hans_CN` are not present.

    Example: Full Chinese support for CN (Mainland China), TW (Taiwan), and HK (Hong Kong)
        ```python
        supported_locales = [
            # Generic Chinese (fallback for all Chinese variants)
            Locale(language_code="zh"),

            # Script-level variants
            Locale(language_code="zh", script_code="Hans"),  # Simplified Chinese zh_Hans
            Locale(language_code="zh", script_code="Hant"),  # Traditional Chinese zh_Hant

            # Region-specific variants
            Locale(language_code="zh", script_code="Hans", country_code="CN"),  # zh_Hans_CN
            Locale(language_code="zh", script_code="Hant", country_code="TW"),  # zh_Hant_TW
            Locale(language_code="zh", script_code="Hant", country_code="HK"),  # zh_Hant_HK
        ]
        ```
    """  # noqa: E501

    current_locale: Optional[Locale] = None
    """
    The current locale.

    Note:
        - Must be an item of [`supported_locales`][(c).] to take effect.
        - If `None` or invalid/unsupported, the first supported locale in
            [`supported_locales`][(c).] is used.
    """

    def __post_init__(self) -> None:
        if not self.supported_locales:
            raise ValueError(
                "supported_locales must contain at least one locale, "
                "as the first entry is used as the final fallback."
            )


# Colors
ColorValue = Union[str, Colors, CupertinoColors]
"""Type alias for color values.

Represents a color and can be:
- a string (representing a color name or hex value),
- a material color from the [`Colors`][flet.] enum,
- or a Cupertino color from the [`CupertinoColors`][flet.] enum.

More information [here](https://docs.flet.dev/cookbook/cookbook/cookbook/colors).
"""

# Icons
IconDataOrControl = Union[IconData, "Control"]

# Content
StrOrControl = Union[str, "Control"]
"""
Type alias for string or control values.

Represents a string or a control and can be:
- a string, which will be converted internally into a [`Text`][flet.] control,
- or a control.
"""

# Wrapper
Wrapper = Callable[..., Any]


# Protocols
class SupportsStr(Protocol):
    def __str__(self) -> str: ...
