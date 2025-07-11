from typing import Optional

from flet.controls.base_control import control
from flet.controls.border import Border
from flet.controls.control import Control
from flet.controls.padding import PaddingValue
from flet.controls.types import Brightness, ColorValue, StrOrControl

__all__ = ["CupertinoAppBar"]


@control("CupertinoAppBar")
class CupertinoAppBar(Control):
    """
    An iOS-styled app bar.

    Note:
        The alignment of the [`title`][(c).] depends on whether this app bar is [`large`][(c).] or not.
        If it is `True`, the `title` is left-aligned and if it is `False` (the default),
        the `title` is centered.
    """

    leading: Optional[Control] = None
    """
    A control to display at the start of this app bar.

    Typically the leading control is an [`Icon`][flet.Icon] or an
    [`IconButton`][flet.IconButton].

    If it is `None` and [`automatically_imply_leading = True`][flet.CupertinoAppBar.automatically_imply_leading],
    an appropriate button will be automatically created.
    """

    title: Optional[StrOrControl] = None
    """
    A string or a control to display in the middle of this app bar.

    Typically a [`Text`][flet.Text].
    """

    trailing: Optional[Control] = None
    """
    A Control to place at the end of the app bar.

    Typically used for actions such as searching or editing.
    """

    bgcolor: Optional[ColorValue] = None
    """
    The fill color to use for this app bar.

    Default color is defined by current theme.
    """

    automatically_imply_leading: Optional[bool] = None
    """
    Whether we should try to imply the [`leading`][flet.CupertinoAppBar.leading]
    control if `None`.

    - If `True` and `leading` is `None`, the app bar will automatically determine an appropriate leading control.
    - If `False` and `leading` is `None`, the space is allocated to the `title`.
    - If a `leading` control is provided, this parameter has no effect.
    """

    automatically_imply_title: Optional[bool] = None
    """
    Whether we should try to imply the `title` control if `None`.

    - If True and `title` is `None`, a [`Text`][flet.Text] control containing the
      current route's title will be automatically filled in.
    - If the `title` is not `None`, this parameter has no effect.
    """

    border: Optional[Border] = None
    """
    The border of the app bar. By default, a single pixel bottom border side is
    rendered.
    """

    padding: Optional[PaddingValue] = None
    """
    Defines the padding for the contents of the app bar.

    If `None`, the app bar will adopt the following defaults:

    - vertically, contents will be sized to the same height as the app bar itself minus
      the status bar.
    - horizontally, padding will be `16` pixels according to iOS specifications unless
      the leading widget is an automatically inserted back button, in which case the
      padding will be `0`.

    Note:
        Vertical padding (`top` and `bottom`) won't change the height of this app bar.
    """

    transition_between_routes: bool = True
    """
    Determines whether the app bar transitions between routes.

    If `True`, this app bar will animate on top of route transitions when the destination
    route also contains a `CupertinoAppBar` or `CupertinoSliverAppBar` with
    `transition_between_routes` set to `True`.

    This transition also occurs during edge back swipe gestures, mimicking native iOS
    behavior.

    Note:
        When enabled, only one app bar can be present per route unless a
        `hero_tag` is specified.
    """

    previous_page_title: Optional[str] = None
    """
    Manually specify the previous route's title when automatically implying the leading back button.

    Overrides the text shown with the back chevron instead of automatically showing the
    previous route's title when [`automatically_imply_leading`][flet.CupertinoAppBar.automatically_imply_leading]
    is `True`.

    Note:
        Has no effect if `leading` is not `None` or if
        [`automatically_imply_leading`][flet.CupertinoAppBar.automatically_imply_leading] is `False`.
    """

    brightness: Optional[Brightness] = None
    """
    The brightness of the specified [`bgcolor`][flet.CupertinoAppBar.bgcolor].

    Setting this value changes the style of the system status bar. It is typically used
    to increase the contrast ratio of the system status bar over `bgcolor`.

    If `None` (the default), its value will be inferred from the relative luminance of
    the `bgcolor`.
    """

    automatic_background_visibility: Optional[bool] = None
    """
    Whether the navigation bar should appear transparent when content is scrolled under
    it.

    If `False`, the navigation bar will display its [`bgcolor`][flet.CupertinoAppBar.bgcolor].
    """

    enable_background_filter_blur: Optional[bool] = None
    """
    Whether to have a blur effect when a non-opaque [`bgcolor`][flet.CupertinoAppBar.bgcolor] is used.

    This will only be respected when
    [`automatic_background_visibility`][flet.CupertinoAppBar.automatic_background_visibility]
    is `False` or until content scrolls under the navigation bar.
    """

    large: bool = False
    """
    Whether to use a large app bar layout.

    If `True`, the title will be left-aligned and if it is `False`, the title will be
    centered.
    """
