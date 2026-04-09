from typing import Annotated, Optional

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
from flet.utils.validation import V


@control("AppBar")
class AppBar(AdaptiveControl):
    """
    A material design app bar.

    Example:
    ```python
    ft.AppBar(
        leading=ft.Icon(ft.Icons.MENU),
        title=ft.Text("Dashboard"),
        bgcolor=ft.Colors.SURFACE_CONTAINER,
        actions=[
            ft.IconButton(ft.Icons.SEARCH),
            ft.IconButton(ft.Icons.MORE_VERT),
        ],
    )
    ```
    """

    leading: Optional[Control] = None
    """
    A control to display before the toolbar's :attr:`title`.

    Typically an :class:`~flet.Icon` or :class:`~flet.IconButton` control.
    """

    leading_width: Optional[Number] = None
    """
    Defines the width of the :attr:`leading` control.
    """

    automatically_imply_leading: bool = True
    """
    Whether we should try to imply the :attr:`leading` control if it is `None`.

    - If `True` and `leading` is `None`, this app bar will automatically determine
        an appropriate leading control.
    - If `False` and `leading` is `None`, the space is allocated to the :attr:`title`.
    - If a `leading` control is provided, this parameter has no effect.
    """

    title: Optional[StrOrControl] = None
    """
    The primary Control displayed in this app bar.

    Typically a :class:`~flet.Text`
    control that contains a description of the current contents of this app.

    Note:
        If :attr:`flet.AdaptiveControl.adaptive`
        and this app is opened on an iOS or macOS device,
        this :attr:`title` control will be
        automatically centered, independent of the value of :attr:`center_title`.
    """

    center_title: Optional[bool] = None
    """
    Whether the :attr:`title` should be centered.

    Default value is defined by :attr:`flet.AppBarTheme.center_title`
    """

    toolbar_height: Optional[Number] = None
    """
    Defines the height of the toolbar component of this app bar.
    """

    color: Optional[ColorValue] = None
    """
    The default color for :class:`~flet.Text`
    and :class:`~flet.Icon` controls within this app bar.

    Default color is defined by :attr:`flet.AppBarTheme.color`
    """

    bgcolor: Optional[ColorValue] = None
    """
    The fill color to use for this app bar.

    Default color is defined by :attr:`flet.AppBarTheme.bgcolor`
    """

    elevation: Annotated[
        Optional[Number],
        V.ge(0),
    ] = None
    """
    The app bar's elevation.

    Note:
        This effect is only visible when using the Material 2 design
        (when :attr:`flet.Theme.use_material3` is `False`).

    Raises:
        ValueError: If it is not greater than or equal to `0`.
    """

    elevation_on_scroll: Annotated[
        Optional[Number],
        V.ge(0),
    ] = None
    """
    The elevation to be used if this app bar has something scrolled underneath it.

    Raises:
        ValueError: If it is not greater than or equal to `0`.
    """

    shadow_color: Optional[ColorValue] = None
    """
    The color of the shadow below this app bar.

    A shadow is only visible and displayed if the :attr:`elevation`
    is greater than zero.
    """

    clip_behavior: Optional[ClipBehavior] = None
    """
    The content will be clipped (or not) according to this option.
    """

    force_material_transparency: bool = False
    """
    Forces this app bar to be transparent (instead of Material's default type).

    This will also remove the visual display of :attr:`bgcolor`
    and :attr:`elevation`, and affect other characteristics of this app bar.
    """

    secondary: bool = False
    """
    Whether this app bar is not being displayed at the top of the screen.
    """

    title_spacing: Optional[Number] = None
    """
    The spacing around :attr:`title` on the horizontal axis.
    It is applied even if there are
    no :attr:`leading` or :attr:`actions` controls.

    Tip:
        If you want :attr:`title` to take all the space available,
        set `title_spacing` to `0.0`.
    """

    exclude_header_semantics: bool = False
    """
    Whether the :attr:`title` should be wrapped with header :class:`~flet.Semantics`.
    """

    actions: Optional[list[Control]] = None
    """
    A list of `Control`s to display in a row after the title control.

    Typically, these controls are :class:`~flet.IconButton`s
    representing common operations. For less common operations, consider using a
    :class:`~flet.PopupMenuButton` as the last
    action.

    Info:
        If :attr:`flet.AdaptiveControl.adaptive` is `True`
        and this app is opened on an iOS or macOS device,
        these `actions` will be automatically placed in a
        :class:`~flet.Row`.
        This is because :attr:`flet.CupertinoAppBar.trailing`
        (which is the counterpart property of `actions`) takes only a single `Control`.
    """

    actions_padding: Optional[PaddingValue] = None
    """
    The padding between the :attr:`actions` and the end of this app bar.
    """

    toolbar_opacity: Annotated[
        Number,
        V.between(0.0, 1.0),
    ] = 1.0
    """
    The opacity of the toolbar.

    - `0.0`: transparent
    - `1.0`: fully opaque

    Raises:
        ValueError: If it is not between `0.0` and `1.0`, inclusive.
    """

    title_text_style: Optional[TextStyle] = None
    """
    The style to be used for the :class:`~flet.Text` controls in the :attr:`title`.
    """

    toolbar_text_style: Optional[TextStyle] = None
    """
    The style to be used for the :class:`~flet.Text` controls in the app bar's \
    :attr:`leading` and :attr:`actions`.
    """

    shape: Optional[OutlinedBorder] = None
    """
    The shape of this app bar's Material as well as its shadow.
    """
