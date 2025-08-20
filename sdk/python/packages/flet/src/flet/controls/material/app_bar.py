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

    Raises:
        AssertionError: If [`elevation`][(c).] or [`elevation_on_scroll`][(c).] is negative.
        AssertionError: If [`toolbar_opacity`][(c).] is not between `0.0` and `1.0` inclusive.
    """  # noqa: E501

    leading: Optional[Control] = None
    """
    A control to display before the toolbar's [`title`][flet.AppBar.title].

    Typically an [`Icon`][flet.Icon] or [`IconButton`][flet.IconButton] control.
    """

    leading_width: Optional[Number] = None
    """
    Defines the width of the [`leading`][flet.AppBar.leading] control.
    """

    automatically_imply_leading: bool = True
    """
    Whether we should try to imply the [`leading`][flet.AppBar.leading] control
    if it is `None`.

    - If `True` and `leading` is `None`, this app bar will automatically determine
      an appropriate leading control.
    - If `False` and `leading` is `None`, the space is allocated to the
      [`title`][flet.AppBar.title].
    - If a `leading` control is provided, this parameter has no effect.
    """

    title: Optional[StrOrControl] = None
    """
    The primary Control displayed in this app bar.

    Typically a [`Text`][flet.Text]
    control that contains a description of the current contents of this app.

    Note:
        If [`AppBar.adaptive=True`][flet.AppBar.adaptive] and this app is opened on
        an iOS or macOS device, this [`title`][flet.AppBar.title] control will be
        automatically centered, independent of the value of
        [`center_title`][flet.AppBar.center_title].
    """

    center_title: Optional[bool] = None
    """
    Whether the [`title`][flet.AppBar.title] should be centered.

    Default value is defined by [`AppBarTheme.center_title`][flet.AppBarTheme.center_title]
    """  # noqa: E501

    toolbar_height: Optional[Number] = None
    """
    Defines the height of the toolbar component of this app bar.
    """

    color: Optional[ColorValue] = None
    """
    The default color for [`Text`][flet.Text]
    and [`Icon`][flet.Icon] controls within this app bar.

    Default color is defined by [`AppBarTheme.color`][flet.AppBarTheme.color]
    """

    bgcolor: Optional[ColorValue] = None
    """
    The fill color to use for this app bar.

    Default color is defined by [`AppBarTheme.bgcolor`][flet.AppBarTheme.bgcolor]
    """

    elevation: Optional[Number] = None
    """
    The app bar's elevation.

    Note:
        This effect is only visible when using the Material 2 design
        (when [`Theme.use_material3 = False`][flet.Theme.use_material3]).
    """

    elevation_on_scroll: Optional[Number] = None
    """
    The elevation to be used if this app bar has something scrolled underneath it.
    """

    shadow_color: Optional[ColorValue] = None
    """
    The color of the shadow below this app bar.

    A shadow is only visible and displayed if the [`elevation`][flet.AppBar.elevation]
    is greater than zero.
    """

    clip_behavior: Optional[ClipBehavior] = None
    """
    The content will be clipped (or not) according to this option.
    """

    force_material_transparency: bool = False
    """
    Forces this app bar to be transparent (instead of Material's default type).

    This will also remove the visual display of [`bgcolor`][flet.AppBar.bgcolor]
    and [`elevation`][flet.AppBar.elevation], and affect
    other characteristics of this app bar.
    """

    secondary: bool = False
    """
    Whether this app bar is not being displayed at the top of the screen.
    """

    title_spacing: Optional[Number] = None
    """
    The spacing around [`title`][flet.AppBar.title] on the horizontal axis.
    It is applied even if there are
    no [`leading`][flet.AppBar.leading] or [`actions`][flet.AppBar.actions] controls.

    Tip:
        If you want [`title`][flet.AppBar.title] to take all the space available,
        set this value to `0.0`.
    """

    exclude_header_semantics: bool = False
    """
    Whether the [`title`][flet.AppBar.title] should be wrapped with header
    [`Semantics`][flet.Semantics].
    """

    actions: Optional[list[Control]] = None
    """
    A list of `Control`s to display in a row after the title control.

    Typically, these controls are [`IconButton`][flet.IconButton]s
    representing common operations. For less common operations, consider using a
    [`PopupMenuButton`][flet.PopupMenuButton] as the last
    action.

    Info:
        If [`AppBar.adaptive=True`][flet.AppBar.adaptive] and this app is opened on an
        iOS or macOS device, these `actions` will be automatically placed in a
        [`Row`][flet.Row].
        This is because [`CupertinoAppBar.trailing`][flet.CupertinoAppBar.trailing]
        (which is the counterpart property of `actions`) takes only a single `Control`.
    """

    actions_padding: Optional[PaddingValue] = None
    """
    The padding between the [`actions`][flet.AppBar.actions]
    and the end of this app bar.
    """

    toolbar_opacity: Number = 1.0
    """
    The opacity of the toolbar.

    Note:
        Must be in the range `0.0` (transparent) to `1.0` (fully opaque).
    """

    title_text_style: Optional[TextStyle] = None
    """
    The style to be used for the [`Text`][flet.Text] controls in the
    [`title`][flet.AppBar.title].
    """

    toolbar_text_style: Optional[TextStyle] = None
    """
    The style to be used for the [`Text`][flet.Text] controls in the
    app bar's [`leading`][flet.AppBar.leading] and [`actions`][flet.AppBar.actions].
    """

    shape: Optional[OutlinedBorder] = None
    """
    The shape of this app bar's Material as well as its shadow.
    """

    def before_update(self):
        super().before_update()
        assert self.elevation is None or self.elevation >= 0, (
            f"elevation must be greater than or equal to 0, got {self.elevation}"
        )
        assert self.elevation_on_scroll is None or self.elevation_on_scroll >= 0, (
            "elevation_on_scroll must be greater than or equal to 0, "
            f"got {self.elevation_on_scroll}"
        )
        assert 0 <= self.toolbar_opacity <= 1, (
            "toolbar_opacity must be between 0.0 and 1.0 inclusive, "
            f"got {self.toolbar_opacity}"
        )
