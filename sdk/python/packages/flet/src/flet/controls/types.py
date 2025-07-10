from dataclasses import dataclass
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
from flet.controls.cupertino.cupertino_icons import CupertinoIcons
from flet.controls.material.icons import Icons

if TYPE_CHECKING:
    from flet.controls.control import Control  # noqa


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
    TBD
    """
    BLANK = "blank"
    SELF = "_self"
    PARENT = "_parent"
    TOP = "_top"


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


class NotchShape(Enum):
    """
    A shape with a notch in its outline.
    """
    AUTO = "auto"
    """
    A NotchShape created with continuous rectangle border.
    """
    CIRCULAR = "circular"
    """
    A rectangle with a smooth circular notch.
    """


class ResponsiveRowBreakpoint(Enum):
    """
    Breakpoints for responsive design.
    """

    XS = "xs"
    SM = "sm"
    MD = "md"
    LG = "lg"
    XL = "xl"
    XXL = "xxl"


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


class TabAlignment(Enum):
    """
    Defines how tabs are aligned horizontally in a [`Tabs`][flet.Tabs].
    """

    START = "start"
    """
    If `Tabs.scrollable` is `True`, tabs are aligned to the start of the `Tabs`. 
    Otherwise throws an exception.
    """

    START_OFFSET = "startOffset"
    """
    If `Tabs.scrollable` is `True`, tabs are aligned to the start of the `Tabs` with an 
    offset of 52.0 pixels. Otherwise throws an exception.
    """

    FILL = "fill"
    """
    If `Tabs.scrollable` is `False`, tabs are stretched to fill the `Tabs`. Otherwise 
    throws an exception.
    """
    
    CENTER = "center"
    """
    Tabs are aligned to the center of the `Tabs`.
    """


class LabelPosition(Enum):
    """
    Position of label in a [`Checkbox`][flet.Checkbox], [`Radio`][flet.Radio] or 
    [`Switch`][flet.Switch]
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
    Different ways to clip content. See [Clip](https://api.flutter.dev/flutter/dart-ui/Clip.html) 
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
    supported_locales: Optional[list[Locale]] = None
    current_locale: Optional[Locale] = None


# Colors
ColorValue = Union[str, Colors, CupertinoColors]
"""Type alias for color values.

Represents a color and can be:
- a string (representing a color name or hex value),
- a material color from the [`Colors`][flet.Colors] enum,
- or a Cupertino color from the [`CupertinoColors`][flet.CupertinoColors] enum.

<img src="/img/docs/colors/color_palettes.png"className="screenshot-100" />

### Hex value

Hex value should be in format `#aarrggbb` (`0xaarrggbb`) or `#rrggbb` (`0xeeggbb`). 
In case `aa` ([opacity](/docs/reference/colors#color-opacity)) is omitted, it is set to `ff` (not transparent).

```
>>> Container(bgcolor='#ff0000')
```

[Live example](https://flet-controls-gallery.fly.dev/colors/controlcolors)

### Named colors

Named colors are the Material Design [theme colors](https://m3.material.io/styles/color/the-color-system/color-roles) 
and [colors palettes](https://m2.material.io/design/color/the-color-system.html#color-usage-and-palettes). 
They can either be set with a string value or using the `Colors` or `CupertinoColors` enums.

```python
>>> Container(bgcolor=ft.Colors.YELLOW)
>>> Container(bgcolor='yellow')
```

#### Theme colors

<img src="/img/docs/colors/theme_colors.png"className="screenshot-100" />

[Live Example](https://flet-controls-gallery.fly.dev/colors/themecolors)

There are 30 named theme colors in [`Theme.color_scheme`][flet.Theme.color_scheme] that are 
generated based on the [`Theme.color_scheme_seed`][flet.Theme.color_scheme_seed] property, 
which defaults to `Colors.BLUE`.

```
# example for generating page theme colors based on the seed color
page.theme = Theme(color_scheme_seed=ft.Colors.GREEN)
page.update()
```

Any of the 30 colors can be overridden, in which case they will have an absolute value 
that will not be dependent on the seed color.
```
page.theme = ft.Theme(
    color_scheme=ft.ColorScheme(
        primary=ft.Colors.GREEN,
        primary_container=ft.Colors.GREEN_200
    ),
)
```

<img src="/img/docs/colors/theme_colors_green.png"className="screenshot-100" />

Theme colors define fallback colors for most of Flet controls.

#### Color palettes

<img src="/img/docs/colors/color_palettes_2.png"className="screenshot-100" />

[Live example](https://flet-controls-gallery.fly.dev/colors/colorspalettes)

Originally created by Material Design in 2014, color palettes are comprised of colors designed 
to work together harmoniously. 

Color swatches (palettes) consist of different shades of a certain color. 
Most swatches have shades from `100` to `900` in increments of one hundred, plus the color `50`. 
The smaller the number, the more pale the color. The greater the number, the darker the color. 
The accent swatches (e.g. `redAccent`) only have the values `100`, `200`, `400`, and `700`.

In addition, a series of blacks and whites with common opacities are available. 
For example, `black54` is a pure black with 54% opacity.

Palette colors can be used for setting individual controls color property or as a 
seed color for generating Theme colors.

## Color opacity

You can specify opacity for any color (hex value or named) using `with_opacity` method. 
Opacity value should be between `0.0` (completely transparent) and `1.0` (not transparent).

```python
color = ft.Colors.with_opacity(0.5, ft.Colors.PRIMARY)
color = ft.Colors.with_opacity(0.5, '#ff6666')
```

Another way to specify opacity for string value:

```python
color = "surface,0.5"
```

For hex value, you can specify `aa` channel with values between `00` and `ff`, for example:

```python
color = "#7fff6666"
``` 

## Defining colors for Flet controls

Most Flet controls have default colors defined by the `color_scheme` that can be 
overridden on different levels.

[Live example](https://flet-controls-gallery.fly.dev/colors/controlcolors)

<img src="/img/docs/colors/colors_fallback.svg"className="screenshot-80" />

### Control level

If the color is defined on the control level, it will be used.

```python
c = ft.Container(width=100, height=100, bgcolor=ft.Colors.GREEN_200)
```

Not every Flet control has a color property that can be set on the control level. 
For example, `FilledButton` always has a default "primary" color defined by the nearest 
ancestor's `theme`.

### Control Theme level

For `ScrollBar` (used in scrollable controls: `Page`, `View`, `Column`, `Row`, `ListView` 
and `GridView`), `Tabs` and `Text` controls, Flet will check if the [nearest anscestor](/blog/scrolling-controls-and-theming#nested-themes) 
theme has [ScrollBar Theme](/blog/scrolling-controls-and-theming#scrollbar-theme), [Tabs theme](/blog/scrolling-controls-and-theming#tabs-theming) or [Text theme](/blog/scrolling-controls-and-theming#text-theming) specified.

Note:
    If you need to change theme for a particular ScrollBar, Text or Tabs control, you can wrap 
    this control in a Container and customize `scrollbar_theme`, `text_theme` or `tabs_theme` 
    for this Container `theme`.

### Theme level

Flet will check for the nearest ancestor that has `theme` defined, which is of type 
[`Theme`][flet.Theme], and will take color from its [`color_scheme`][flet.Theme.color_scheme]. 

/// details | Example
    type: example
In the example below, the nearest anscestor for the [`FilledButton`][flet.FilledButton]
is [`Container`][flet.Container], and the `primary` color that is used for the button 
will be taken from [`Container.theme`][flet.Container.theme].

```python
import flet as ft

def main(page: ft.Page):          
    page.add(
        ft.Container(
            width=200,
            height=200,
            border=ft.border.all(1, ft.Colors.BLACK),
            theme=ft.Theme(color_scheme=ft.ColorScheme(primary=ft.Colors.YELLOW))
            content=ft.FilledButton("Primary color"),
        )
    )

ft.run(main)   
```

If control's color property, control-specific theme or nearest ancestor's theme is not 
specified, the nearest ancestor will be the [`Page`][flet.Page] and the colors from its 
[`theme.color_scheme`][flet.Page.theme] will be used.  
///
"""

# Icons
IconValue = Union[str, Icons, CupertinoIcons]
"""Type alias for icon values.

Represents an icon and can be:
- a string (icon name),
- a material icon from the [`Icons`][flet.Icons] enum,
- or a Cupertino icon from the `[CupertinoIcons`][flet.CupertinoIcons] enum.

/// details | Example
    type: example

```python
>>> import flet as ft
>>> ft.Icons.ABC
>>> ft.CupertinoIcons.BACK
>>> ft.Icons.random()
>>> ft.CupertinoIcons.random()
>>> ft.Icons.random(exclude=[ft.Icons.FAVORITE, ft.Icons.SCHOOL], weights={ft.Icons.SCHOOL: 150, ft.Icons.ADJUST: 5})
>>> ft.CupertinoIcons.random(exclude=[ft.CupertinoIcons.CAMERA, ft.CupertinoIcons.TABLE], weights={ft.CupertinoIcons.TABLE: 150, ft.CupertinoIcons.PENCIL: 5})
```
///
"""
IconValueOrControl = Union[IconValue, "Control"]

# Content
StrOrControl = Union[str, "Control"]
"""
Type alias for string or control values.

Represents a string or a control and can be:
- a string, which will be converted internally into a [`Text`][flet.Text] control,
- or a control.

"""

# Wrapper
Wrapper = Callable[..., Any]


# Protocols
class SupportsStr(Protocol):
    def __str__(self) -> str: ...
