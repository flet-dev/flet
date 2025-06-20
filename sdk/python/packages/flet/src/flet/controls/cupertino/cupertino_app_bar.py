from typing import Optional

from flet.controls.base_control import control
from flet.controls.border import Border
from flet.controls.control import Control
from flet.controls.padding import OptionalPaddingValue
from flet.controls.types import Brightness, OptionalColorValue, StrOrControl

__all__ = ["CupertinoAppBar"]


@control("CupertinoAppBar")
class CupertinoAppBar(Control):
    """
    An iOS-styled application bar.

    Online docs: https://flet.dev/docs/controls/cupertinoappbar
    """

    leading: Optional[Control] = None
    """
    A `Control` to display at the start of this app bar. Typically the leading control 
    is an [`Icon`](https://flet.dev/docs/controls/icon) or an 
    [`IconButton`](https://flet.dev/docs/controls/iconbutton).

    If `None` and `automatically_imply_leading = True`, an appropriate button will be 
    automatically created.
    """

    middle: Optional[StrOrControl] = None
    """
    A `Control` to display in the middle of this app bar. Typically a 
    [`Text`](https://flet.dev/docs/controls/text) or a segmented control.
    """

    title: Optional[StrOrControl] = None
    """
    TBD
    """

    trailing: Optional[Control] = None
    """
    A Control to place at the end of the app bar. Normally additional actions taken on 
    the page such as a search or edit function.
    """

    bgcolor: OptionalColorValue = None
    """
    The fill [color](https://flet.dev/docs/reference/colors) to use for an AppBar. 
    Default color is defined by current theme.
    """

    automatically_imply_leading: Optional[bool] = None
    """
    Controls whether we should try to imply the leading control if None.

    If `True` and `leading` is null, automatically try to deduce what the leading 
    widget should be. If `False` and `leading` is None, leading space is given to 
    title. If leading widget is not None, this parameter has no effect.
    """

    automatically_imply_middle: Optional[bool] = None
    """
    Controls whether we should try to imply the middle control if None.

    If `True` and `middle` is null, automatically fill in a Text control with the 
    current route's title. If middle control is not None, this parameter has no effect.
    """

    automatically_imply_title: Optional[bool] = None
    """
    TBD
    """

    border: Optional[Border] = None
    """
    The border of the app bar. By default, a single pixel bottom border side is 
    rendered.

    Value is of type 
    [`Border`](https://flet.dev/docs/reference/types/border).
    """

    padding: OptionalPaddingValue = None
    """
    Defines the padding for the contents of the app bar.

    Padding is an instance of 
    [`Padding`](https://flet.dev/docs/reference/types/padding) class.

    If `None`, the app bar will adopt the following defaults:

    - vertically, contents will be sized to the same height as the app bar itself minus 
      the status bar.
    - horizontally, padding will be `16` pixels according to iOS specifications unless 
      the leading widget is an automatically inserted back button, in which case the 
      padding will be `0`.

    Vertical padding won't change the height of the app bar.
    """

    transition_between_routes: Optional[bool] = None
    """
    TBD
    """

    previous_page_title: Optional[str] = None
    """
    TBD
    """

    brightness: Optional[Brightness] = None
    """
    The brightness of the specified `bgcolor`.

    Setting this value changes the style of the system status bar. It is typically used 
    to increase the contrast ratio of the system status bar over `bgcolor`.

    If `None` (the default), its value will be inferred from the relative luminance of 
    the `bgcolor`.

    Value is of type 
    [`Brightness`](https://flet.dev/docs/reference/types/brightness).
    """

    automatic_background_visibility: Optional[bool] = None
    """
    Whether the navigation bar should appear transparent when content is scrolled under 
    it.

    If `False`, the navigation bar will display its `bgcolor`.

    Defaults to `True`.
    """

    enable_background_filter_blur: Optional[bool] = None
    """
    Whether to have a blur effect when a non-opaque `bgcolor` is used.

    This will only be respected when `automatic_background_visibility` is `False` or 
    until content scrolls under the navbar.

    Defaults to `True`.
    """

    large: Optional[bool] = None
    """
    TBD
    """
