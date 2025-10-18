from typing import Optional

from flet.controls.adaptive_control import AdaptiveControl
from flet.controls.base_control import control
from flet.controls.buttons import OutlinedBorder
from flet.controls.control import Control
from flet.controls.padding import PaddingValue
from flet.controls.text_style import TextStyle
from flet.controls.types import (
    ClipBehavior,
    ColorValue,
    Number,
    StrOrControl,
)


@control("AppBar")
class AppBar(AdaptiveControl):
    """
    A material design app bar.

    ```python
    ft.AppBar(
        leading=ft.Icon(ft.Icons.MENU),
        title=ft.Text("Dashboard"),
        actions=[
            ft.IconButton(ft.Icons.SEARCH),
            ft.IconButton(ft.Icons.MORE_VERT),
        ],
        bgcolor=ft.Colors.SURFACE_CONTAINER,
    )
    ```
    """

    leading: Optional[Control] = None
    """
    A control to display before the toolbar's [`title`][(c).].

    Typically an [`Icon`][flet.] or [`IconButton`][flet.] control.
    """

    leading_width: Optional[Number] = None
    """
    Defines the width of the [`leading`][(c).] control.
    """

    automatically_imply_leading: bool = True
    """
    Whether we should try to imply the [`leading`][(c).] control if it is `None`.

    - If `True` and `leading` is `None`, this app bar will automatically determine
        an appropriate leading control.
    - If `False` and `leading` is `None`, the space is allocated to the [`title`][(c).].
    - If a `leading` control is provided, this parameter has no effect.
    """

    title: Optional[StrOrControl] = None
    """
    The primary Control displayed in this app bar.

    Typically a [`Text`][flet.]
    control that contains a description of the current contents of this app.

    Note:
        If [`AppBar.adaptive=True`][(c).adaptive] and this app is opened on
        an iOS or macOS device, this [`title`][(c).] control will be
        automatically centered, independent of the value of [`center_title`][(c).].
    """

    center_title: Optional[bool] = None
    """
    Whether the [`title`][(c).] should be centered.

    Default value is defined by [`AppBarTheme.center_title`][flet.]
    """

    toolbar_height: Optional[Number] = None
    """
    Defines the height of the toolbar component of this app bar.
    """

    color: Optional[ColorValue] = None
    """
    The default color for [`Text`][flet.]
    and [`Icon`][flet.] controls within this app bar.

    Default color is defined by [`AppBarTheme.color`][flet.]
    """

    bgcolor: Optional[ColorValue] = None
    """
    The fill color to use for this app bar.

    Default color is defined by [`AppBarTheme.bgcolor`][flet.]
    """

    elevation: Optional[Number] = None
    """
    The app bar's elevation.

    Note:
        This effect is only visible when using the Material 2 design
        (when [`Theme.use_material3`][flet.] is `False`).

    Raises:
        ValueError: If it is less than `0.0`.
    """

    elevation_on_scroll: Optional[Number] = None
    """
    The elevation to be used if this app bar has something scrolled underneath it.

    Raises:
        ValueError: If it is less than `0.0`.
    """

    shadow_color: Optional[ColorValue] = None
    """
    The color of the shadow below this app bar.

    A shadow is only visible and displayed if the [`elevation`][(c).]
    is greater than zero.
    """

    clip_behavior: Optional[ClipBehavior] = None
    """
    The content will be clipped (or not) according to this option.
    """

    force_material_transparency: bool = False
    """
    Forces this app bar to be transparent (instead of Material's default type).

    This will also remove the visual display of [`bgcolor`][(c).]
    and [`elevation`][(c).], and affect other characteristics of this app bar.
    """

    secondary: bool = False
    """
    Whether this app bar is not being displayed at the top of the screen.
    """

    title_spacing: Optional[Number] = None
    """
    The spacing around [`title`][(c).] on the horizontal axis.
    It is applied even if there are
    no [`leading`][(c).] or [`actions`][(c).] controls.

    Tip:
        If you want [`title`][(c).] to take all the space available,
        set `title_spacing` to `0.0`.
    """

    exclude_header_semantics: bool = False
    """
    Whether the [`title`][(c).] should be wrapped with header
    [`Semantics`][flet.].
    """

    actions: Optional[list[Control]] = None
    """
    A list of `Control`s to display in a row after the title control.

    Typically, these controls are [`IconButton`][flet.]s
    representing common operations. For less common operations, consider using a
    [`PopupMenuButton`][flet.] as the last
    action.

    Info:
        If [`AppBar.adaptive`][(c).adaptive] is `True` and this app is opened on an
        iOS or macOS device, these `actions` will be automatically placed in a
        [`Row`][flet.].
        This is because [`CupertinoAppBar.trailing`][flet.]
        (which is the counterpart property of `actions`) takes only a single `Control`.
    """

    actions_padding: Optional[PaddingValue] = None
    """
    The padding between the [`actions`][(c).] and the end of this app bar.
    """

    toolbar_opacity: Number = 1.0
    """
    The opacity of the toolbar.

    - `0.0`: transparent
    - `1.0`: fully opaque

    Raises:
        ValueError: If it is not between `0.0` and `1.0` inclusive.
    """

    title_text_style: Optional[TextStyle] = None
    """
    The style to be used for the [`Text`][flet.] controls in the [`title`][(c).].
    """

    toolbar_text_style: Optional[TextStyle] = None
    """
    The style to be used for the [`Text`][flet.] controls in the
    app bar's [`leading`][(c).] and [`actions`][(c).].
    """

    shape: Optional[OutlinedBorder] = None
    """
    The shape of this app bar's Material as well as its shadow.
    """

    def before_update(self):
        super().before_update()
        if self.elevation is not None and self.elevation < 0:
            raise ValueError(
                f"elevation must be greater than or equal to 0, got {self.elevation}"
            )
        if self.elevation_on_scroll is not None and self.elevation_on_scroll < 0:
            raise ValueError(
                "elevation_on_scroll must be greater than or equal to 0, "
                f"got {self.elevation_on_scroll}"
            )
        if not (0 <= self.toolbar_opacity <= 1):
            raise ValueError(
                "toolbar_opacity must be between 0.0 and 1.0 inclusive, "
                f"got {self.toolbar_opacity}"
            )
