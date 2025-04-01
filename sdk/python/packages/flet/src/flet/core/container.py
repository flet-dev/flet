from dataclasses import dataclass
from typing import List, Optional, Tuple, Union

from flet.core.adaptive_control import AdaptiveControl
from flet.core.alignment import Alignment
from flet.core.animation import AnimationValue
from flet.core.blur import Blur
from flet.core.border import Border
from flet.core.box import (
    BoxDecoration,
    BoxShadow,
    BoxShape,
    ColorFilter,
    DecorationImage,
)
from flet.core.constrained_control import ConstrainedControl
from flet.core.control import Control, control
from flet.core.control_event import ControlEvent
from flet.core.gradients import Gradient
from flet.core.theme import Theme
from flet.core.types import (
    BlendMode,
    BorderRadiusValue,
    ClipBehavior,
    ColorValue,
    MarginValue,
    OptionalControlEventCallable,
    OptionalEventCallable,
    PaddingValue,
    ThemeMode,
    UrlTarget,
)


@dataclass
class ContainerTapEvent(ControlEvent):
    local_x: float
    local_y: float
    global_x: float
    global_y: float


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
    padding: Optional[PaddingValue] = None
    margin: Optional[MarginValue] = None
    alignment: Optional[Alignment] = None
    bgcolor: Optional[ColorValue] = None
    gradient: Optional[Gradient] = None
    blend_mode: Optional[BlendMode] = None
    border: Optional[Border] = None
    border_radius: Optional[BorderRadiusValue] = None
    shape: Optional[BoxShape] = None
    clip_behavior: Optional[ClipBehavior] = None
    ink: Optional[bool] = None
    image: Optional[DecorationImage] = None
    ink_color: Optional[ColorValue] = None
    animate: Optional[AnimationValue] = None
    blur: Optional[
        Union[float, int, Tuple[Union[float, int], Union[float, int]], Blur]
    ] = None
    shadow: Optional[Union[BoxShadow, List[BoxShadow]]] = None
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
