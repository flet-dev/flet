from typing import Optional

from flet.controls.adaptive_control import AdaptiveControl
from flet.controls.alignment import Alignment
from flet.controls.animation import AnimationValue
from flet.controls.base_control import control
from flet.controls.blur import BlurValue
from flet.controls.border import Border
from flet.controls.border_radius import OptionalBorderRadiusValue
from flet.controls.box import (
    BoxDecoration,
    BoxShape,
    ColorFilter,
    DecorationImage,
    ShadowValue,
)
from flet.controls.constrained_control import ConstrainedControl
from flet.controls.control import Control
from flet.controls.control_event import (
    OptionalControlEventHandler,
    OptionalEventHandler,
)
from flet.controls.events import TapEvent
from flet.controls.gradients import Gradient
from flet.controls.margin import OptionalMarginValue
from flet.controls.padding import OptionalPaddingValue
from flet.controls.theme import Theme
from flet.controls.types import (
    BlendMode,
    ClipBehavior,
    OptionalColorValue,
    ThemeMode,
    UrlTarget,
)

__all__ = ["Container"]


@control("Container")
class Container(ConstrainedControl, AdaptiveControl):
    """
    Container allows to decorate a control with background color and border and
    position it with padding, margin and alignment.

    <img src="https://flet.dev/img/docs/controls/container/container-diagram.png"
    className="screenshot-50" />

    Online docs: https://flet.dev/docs/controls/container
    """

    content: Optional[Control] = None
    """
    A child Control contained by the container.
    """

    padding: OptionalPaddingValue = None
    """
    Empty space to inscribe inside a container decoration (background, border). The 
    child control is placed inside this padding.

    Value is of type [`Padding`](https://flet.dev/docs/reference/types/padding) or a 
    number.
    """

    margin: OptionalMarginValue = None
    """
    Empty space to surround the decoration and child control.

    Value is of type [`Margin`](https://flet.dev/docs/reference/types/margin) class or 
    a number.
    """

    alignment: Optional[Alignment] = None
    """
    Align the child control within the container.

    Value is of type [`Alignment`](https://flet.dev/docs/reference/types/alignment).
    """

    bgcolor: OptionalColorValue = None
    """
    Defines the background [color](https://flet.dev/docs/reference/colors) of the 
    container.
    """

    gradient: Optional[Gradient] = None
    """
    Defines the gradient background of the container.

    Value is of type [`Gradient`](https://flet.dev/docs/reference/types/gradient).
    """

    blend_mode: Optional[BlendMode] = None
    """
    The blend mode applied to the `color` or `gradient` background of the container. 

    Value is of type [`BlendMode`](https://flet.dev/docs/reference/types/blendmode) and 
    defaults to `BlendMode.MODULATE`.
    """

    border: Optional[Border] = None
    """
    A border to draw above the background color.

    Value is of type [`Border`](https://flet.dev/docs/reference/types/border).
    """

    border_radius: OptionalBorderRadiusValue = None
    """
    If specified, the corners of the container are rounded by this radius.

    Value is of type [`BorderRadius`](https://flet.dev/docs/reference/types/borderradius).
    """

    shape: Optional[BoxShape] = None
    """
    Sets the shape of the container.

    Value is of type [`BoxShape`](https://flet.dev/docs/reference/types/boxshape) and 
    defaults to `BoxShape.RECTANGLE`.
    """

    clip_behavior: Optional[ClipBehavior] = None
    """
    The content will be clipped (or not) according to this option.

    Value is of type [`ClipBehavior`](https://flet.dev/docs/reference/types/clipbehavior) 
    and defaults to `ClipBehavior.ANTI_ALIAS` if `border_radius` is not `None`; 
    otherwise `ClipBehavior.NONE`.
    """

    ink: bool = False
    """
    `True` to produce ink ripples effect when user clicks the container.

    Defaults to `False`.
    """

    image: Optional[DecorationImage] = None
    """
    An image to paint above the `bgcolor` or `gradient`. If `shape=BoxShape.CIRCLE` 
    then this image is clipped to the circle's boundary; if `border_radius` is not 
    `None` then the image is clipped to the given radii.

    Value is of type [`DecorationImage`](https://flet.dev/docs/reference/types/decorationimage).
    """

    ink_color: OptionalColorValue = None
    """
    The splash [color](https://flet.dev/docs/reference/colors) of the ink response.
    """

    animate: Optional[AnimationValue] = None
    """
    Enables container "implicit" animation that gradually changes its values over a 
    period of time.

    Value is of type [`AnimationValue`](https://flet.dev/docs/reference/types/animationvalue).
    """

    blur: Optional[BlurValue] = None
    """
    Applies Gaussian blur effect under the container.

    The value of this property could be one of the following:

    * **a number** - specifies the same value for horizontal and vertical sigmas, e.g. 
    `10`.
    * **a tuple** - specifies separate values for horizontal and vertical sigmas, e.g. 
    `(10, 1)`.
    * **an instance of [`Blur`](https://flet.dev/docs/reference/types/blur)**

    For example:

    ```python
    ft.Stack(
        [
            ft.Container(
                content=ft.Text("Hello"),
                image_src="https://picsum.photos/100/100",
                width=100,
                height=100,
            ),
            ft.Container(
                width=50,
                height=50,
                blur=10,
                bgcolor="#44CCCC00",
            ),
            ft.Container(
                width=50,
                height=50,
                left=10,
                top=60,
                blur=(0, 10),
            ),
            ft.Container(
                top=10,
                left=60,
                blur=ft.Blur(10, 0, ft.BlurTileMode.MIRROR),
                width=50,
                height=50,
                bgcolor="#44CCCCCC",
                border=ft.border.all(2, ft.Colors.BLACK),
            ),
        ]
    )
    ```
    """

    shadow: Optional[ShadowValue] = None
    """
    Shadows cast by the container.

    Value is of type [`BoxShadow`](https://flet.dev/docs/reference/types/boxshadow) or 
    a `List[BoxShadow]`.
    """

    url: Optional[str] = None
    """
    The URL to open when the container is clicked. If provided, `on_click` event is 
    fired after that.
    """

    url_target: Optional[UrlTarget] = None
    """
    Where to open URL in the web mode.

    Value is of type [`UrlTarget`](https://flet.dev/docs/reference/types/urltarget) and 
    defaults to `UrlTarget.BLANK`.
    """

    theme: Optional[Theme] = None
    """
    Allows setting a nested `theme` for all controls inside the container and down the 
    tree.

    Value is of type [`Theme`](https://flet.dev/docs/cookbook/theming).

    **Usage example**

    ```python
    import flet as ft

    def main(page: ft.Page):
        # Yellow page theme with SYSTEM (default) mode
        page.theme = ft.Theme(
            color_scheme_seed=ft.Colors.YELLOW,
        )

        page.add(
            # Page theme
            ft.Container(
                content=ft.ElevatedButton("Page theme button"),
                bgcolor=ft.Colors.SURFACE_CONTAINER_HIGHEST,
                padding=20,
                width=300,
            ),

            # Inherited theme with primary color overridden
            ft.Container(
                theme=ft.Theme(color_scheme=ft.ColorScheme(primary=ft.Colors.PINK)),
                content=ft.ElevatedButton("Inherited theme button"),
                bgcolor=ft.Colors.SURFACE_CONTAINER_HIGHEST,
                padding=20,
                width=300,
            ),
            
            # Unique always DARK theme
            ft.Container(
                theme=ft.Theme(color_scheme_seed=ft.Colors.INDIGO),
                theme_mode=ft.ThemeMode.DARK,
                content=ft.ElevatedButton("Unique theme button"),
                bgcolor=ft.Colors.SURFACE_CONTAINER_HIGHEST,
                padding=20,
                width=300,
            ),
        )

    ft.app(main)
    ```
    """

    dark_theme: Optional[Theme] = None
    """
    Allows setting a nested `theme` to be used when in dark theme mode for all controls 
    inside the container and down the tree.

    Value is of type [`Theme`](https://flet.dev/docs/cookbook/theming).
    """

    theme_mode: Optional[ThemeMode] = None
    """
    Setting `theme_mode` "resets" parent theme and creates a new, unique scheme for all 
    controls inside the container. Otherwise the styles defined in container's `theme` 
    property override corresponding styles from the parent, inherited theme.

    Value is of type [`ThemeMode`](https://flet.dev/docs/reference/types/thememode) and 
    defaults to `ThemeMode.SYSTEM`.
    """

    color_filter: Optional[ColorFilter] = None
    """
    Applies a color filter to the container.

    Value is of type [`ColorFilter`](https://flet.dev/docs/reference/types/colorfilter).
    """

    ignore_interactions: bool = False
    """
    Whether to ignore all interactions with this container and its descendants.

    Defaults to `False`.
    """

    foreground_decoration: Optional[BoxDecoration] = None
    """
    The foreground decoration.

    Value is of type [`BoxDecoration`](https://flet.dev/docs/reference/types/boxdecoration).
    """

    on_click: OptionalControlEventHandler["Container"] = None
    """
    Fires when a user clicks the container. Will not be fired on long press.
    """

    on_tap_down: OptionalEventHandler[TapEvent["Container"]] = None
    """
    Fires when a user clicks the container with or without a long press.

    Event handler argument is of type [`TapEvent`](https://flet.dev/docs/reference/types/tapevent).

    Info:
        If `ink` is `True`, `e` will be plain `ControlEvent` with empty `data` instead of 
        `ContainerTapEvent`.

    A simple usage example:

    ```python
    import flet as ft

    def main(page: ft.Page):
        page.vertical_alignment = ft.MainAxisAlignment.CENTER
        page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

        def on_long_press(e):
            print("on long press")
            page.add(ft.Text("on_long_press triggered"))

        def on_click(e):
            print("on click")
            page.add(ft.Text("on_click triggered"))

        def on_tap_down(e: ft.ContainerTapEvent):
            print("on tap down", e.local_x, e.local_y)
            page.add(ft.Text("on_tap_down triggered"))

        c = ft.Container(
            bgcolor=ft.Colors.RED,
            content=ft.Text("Test Long Press"),
            height=100,
            width=100,
            on_click=on_click,
            on_long_press=on_long_press,
            on_tap_down=on_tap_down,
        )
        
        page.add(c)

    ft.app(main)
    ```
    """

    on_long_press: OptionalControlEventHandler["Container"] = None
    """
    Fires when the container is long-pressed.
    """

    on_hover: OptionalControlEventHandler["Container"] = None
    """
    Fires when a mouse pointer enters or exists the container area. `data` property of 
    event object contains `true` (string) when cursor enters and `false` when it exits.

    A simple example of a container changing its background color on mouse hover:

    ```python
    import flet as ft

    def main(page: ft.Page):
        def on_hover(e):
            e.control.bgcolor = "blue" if e.data == True else "red"
            e.control.update()

        page.add(
            ft.Container(
                width=100, 
                height=100, 
                bgcolor="red", 
                ink=False, 
                on_hover=on_hover,
            )
        )

    ft.app(main)
    ```
    """
