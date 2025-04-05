from dataclasses import dataclass, field
from typing import Optional

from flet.core.adaptive_control import AdaptiveControl
from flet.core.alignment import Alignment
from flet.core.animation import AnimationValue
from flet.core.blur import BlurValue
from flet.core.border import Border
from flet.core.border_radius import OptionalBorderRadiusValue
from flet.core.box import (
    BoxDecoration,
    BoxShape,
    ColorFilter,
    DecorationImage,
    ShadowValue,
)
from flet.core.constrained_control import ConstrainedControl
from flet.core.control import Control, control
from flet.core.control_event import ControlEvent
from flet.core.gradients import Gradient
from flet.core.margin import OptionalMarginValue
from flet.core.padding import OptionalPaddingValue
from flet.core.theme import Theme
from flet.core.types import (
    BlendMode,
    ClipBehavior,
    Number,
    OptionalColorValue,
    OptionalControlEventCallable,
    OptionalEventCallable,
    ThemeMode,
    UrlTarget,
)

__all__ = ["Container", "ContainerTapEvent"]


@dataclass
class ContainerTapEvent(ControlEvent):
    local_x: Number = field(metadata={"data_field": "lx"})
    local_y: Number = field(metadata={"data_field": "ly"})
    global_x: Number = field(metadata={"data_field": "gx"})
    global_y: Number = field(metadata={"data_field": "gy"})


@control("Container")
class Container(ConstrainedControl, AdaptiveControl):
    """
    Container allows to decorate a control with background color and border and position it with padding, margin and alignment.

    Example:

    ```
    import flet as ft

    def main(page: ft.Page):
        page.title = "Container"

        c1 = ft.Container(
            content=ft.Text("Container with background"),
            bgcolor=ft.colors.AMBER_100,
            padding=5,
        )
        page.add(c1)

    ft.app(target=main)
    ```

    -----

    Online docs: https://flet.dev/docs/controls/container
    """

    content: Optional[Control] = None
    padding: OptionalPaddingValue = None
    margin: OptionalMarginValue = None
    alignment: Optional[Alignment] = None
    bgcolor: OptionalColorValue = None
    gradient: Optional[Gradient] = None
    blend_mode: Optional[BlendMode] = None
    border: Optional[Border] = None
    border_radius: OptionalBorderRadiusValue = None
    shape: Optional[BoxShape] = None
    clip_behavior: Optional[ClipBehavior] = None
    ink: Optional[bool] = None
    image: Optional[DecorationImage] = None
    ink_color: OptionalColorValue = None
    animate: Optional[AnimationValue] = None
    blur: Optional[BlurValue] = None
    shadow: Optional[ShadowValue] = None
    url: Optional[str] = None
    url_target: Optional[UrlTarget] = None
    theme: Optional[Theme] = None
    dark_theme: Optional[Theme] = None
    theme_mode: Optional[ThemeMode] = None
    color_filter: Optional[ColorFilter] = None
    ignore_interactions: Optional[bool] = None
    foreground_decoration: Optional[BoxDecoration] = None
    on_click: OptionalControlEventCallable = None
    on_tap_down: OptionalEventCallable[ContainerTapEvent] = None
    on_long_press: OptionalControlEventCallable = None
    on_hover: OptionalControlEventCallable = None
