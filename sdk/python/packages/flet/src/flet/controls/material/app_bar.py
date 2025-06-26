from typing import Optional

from flet.controls.adaptive_control import AdaptiveControl
from flet.controls.base_control import control
from flet.controls.buttons import OutlinedBorder
from flet.controls.control import Control
from flet.controls.text_style import TextStyle
from flet.controls.types import (
    ClipBehavior,
    Number,
    OptionalColorValue,
    OptionalNumber,
    StrOrControl,
)


@control("AppBar")
class AppBar(AdaptiveControl):
    """
    A material design app bar.

    Online docs: https://flet.dev/docs/controls/appbar
    """

    leading: Optional[Control] = None
    """
    A `Control` to display before the toolbar's title.

    Typically the leading control is an [`Icon`](https://flet.dev/docs/controls/icon) 
    or an [`IconButton`](https://flet.dev/docs/controls/iconbutton).

    Value is of type `Control`.
    """

    leading_width: OptionalNumber = None
    """
    Defines the width of leading control.

    Value is of type [`OptionalNumber`](https://flet.dev/docs/reference/types/aliases#optionalnumber) 
    and defaults to `56.0`.
    """

    automatically_imply_leading: bool = True
    """
    Controls whether we should try to imply the leading widget if null.

    If `True` and `leading` is null, automatically try to deduce what the leading 
    widget should be. If `False` and `leading` is null, leading space is given to 
    title. If leading widget is not null, this parameter has no effect.

    Value is of type `bool`.
    """

    title: Optional[StrOrControl] = None
    """
    The primary `Control` displayed in the app bar. Typically a [`Text`](https://flet.dev/docs/controls/text) 
    control that contains a description of the current contents of the app.

    **Note** that, if `AppBar.adaptive=True` and the app is opened on an iOS or macOS 
    device, this control will be automatically centered.

    Value is of type `Control`.
    """

    center_title: bool = False
    """
    Whether the title should be centered.

    Value is of type `bool` and defaults to `False`.
    """

    toolbar_height: OptionalNumber = None
    """
    Defines the height of the toolbar component of an AppBar.

    Value is of type [`OptionalNumber`](https://flet.dev/docs/reference/types/aliases#optionalnumber) 
    and defaults to `56.0`.
    """

    color: OptionalColorValue = None
    """
    The default [color](https://flet.dev/docs/reference/colors) for `Text` and `Icon` 
    controls within the app bar. Default color is defined by current theme.
    """

    bgcolor: OptionalColorValue = None
    """
    The fill [color](https://flet.dev/docs/reference/colors) to use for an AppBar. 
    Default color is defined by current theme.
    """

    elevation: OptionalNumber = None
    """
    The app bar's elevation.

    Note: This effect is only visible when using the Material 2 design 
    (`Theme.use_material3=False`).

    Value is of type [`OptionalNumber`](https://flet.dev/docs/reference/types/aliases#optionalnumber) 
    and defaults to `4`.
    """

    elevation_on_scroll: OptionalNumber = None
    """
    The elevation to be used if this app bar has something scrolled underneath it.

    Value is of type [`OptionalNumber`](https://flet.dev/docs/reference/types/aliases#optionalnumber).
    """

    shadow_color: OptionalColorValue = None
    """
    The [color](https://flet.dev/docs/reference/colors) of the shadow below the app bar.

    A shadow is only visible and displayed if the `elevation` is greater than zero.
    """

    surface_tint_color: OptionalColorValue = None
    """
    The color of the surface tint overlay applied to the app bar's `bgcolor` to 
    indicate elevation.

    By default, no overlay will be applied.
    """

    clip_behavior: Optional[ClipBehavior] = None
    """
    The content will be clipped (or not) according to this option.

    Value is of type [`ClipBehavior`](https://flet.dev/docs/reference/types/clipbehavior).
    """

    force_material_transparency: bool = False
    """
    Forces the app bar to be transparent (instead of Material's default type).

    This will also remove the visual display of `bgcolor` and `elevation`, and affect 
    other characteristics of this app bar.

    Value is of type `bool`.
    """

    is_secondary: bool = False
    """
    Whether this app bar is not being displayed at the top of the screen.

    Value is of type `bool` and defaults to `False`.
    """

    title_spacing: OptionalNumber = None
    """
    The spacing around `title` on the horizontal axis. It is applied even if there are 
    no `leading` or `actions` controls.

    If you want `title` to take all the space available, set this value to `0.0`.

    Value is of type [`OptionalNumber`](https://flet.dev/docs/reference/types/aliases#optionalnumber).
    """

    exclude_header_semantics: bool = False
    """
    Whether the `title` should be wrapped with header [`Semantics`](https://flet.dev/docs/controls/semantics).

    Value is of type `bool` and defaults to `False`.
    """

    actions: Optional[list[Control]] = None
    """
    A list of `Control`s to display in a row after the title control.

    Typically these controls are [`IconButtons`](https://flet.dev/docs/controls/iconbutton) 
    representing common operations. For less common operations, consider using a 
    [`PopupMenuButton`](https://flet.dev/docs/controls/popupmenubutton) as the last 
    action.

    **Note** that, if `AppBar.adaptive=True` and the app is opened on an iOS or macOS 
    device, only the first element of this list will be used. This is because the 
    `CupertinoAppBar`(which will be used on those two platforms) only accepts one - 
    trailing - action control.
    """

    toolbar_opacity: Number = 1.0
    """
    The opacity of the toolbar. Value ranges from `0.0` (transparent) to `1.0` (fully 
    opaque).

    Value is of type [`OptionalNumber`](https://flet.dev/docs/reference/types/aliases#optionalnumber) 
    and defaults to `1.0`.
    """

    title_text_style: Optional[TextStyle] = None
    """
    The style to be used for the `Text` controls in the `title`.

    Value is of type [`TextStyle`](https://flet.dev/docs/reference/types/textstyle).
    """

    toolbar_text_style: Optional[TextStyle] = None
    """
    The style to be used for the `Text` controls in the app bar's `leading` and 
    `actions` (but not `title`).

    Value is of type [`TextStyle`](https://flet.dev/docs/reference/types/textstyle).
    """

    shape: Optional[OutlinedBorder] = None
    """
    The shape of the app bar's Material as well as its shadow.

    Value is of type [`OutlinedBorder`](https://flet.dev/docs/reference/types/outlinedborder).
    """

    def before_update(self):
        super().before_update()
        assert (
            self.elevation is None or self.elevation >= 0
        ), "elevation cannot be negative"
        assert (
            self.elevation_on_scroll is None or self.elevation_on_scroll >= 0
        ), "elevation_on_scroll cannot be negative"
