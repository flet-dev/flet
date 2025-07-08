from typing import Optional

from flet.controls.base_control import control
from flet.controls.control import Control
from flet.controls.types import ColorValue, Number

__all__ = ["Divider"]


@control("Divider")
class Divider(Control):
    """
    A thin horizontal line (divider), with padding on either side.
    """

    color: Optional[ColorValue] = None
    """
    The color to use when painting the line.

    If `None`, [`DividerTheme.color`][flet.DividerTheme.color] is used.
    If that's is also `None`, defaults to [`Theme.divider_color`][flet.Theme.divider_color].
    """

    height: Optional[Number] = None
    """
    The divider's height extent. The divider itself is always drawn as a horizontal
    line that is centered within the height specified by this value.

    If `None`, [`DividerTheme.space`][flet.DividerTheme.space] is used.
    If that's is also `None`, defaults to `16.0`.
    """

    leading_indent: Optional[Number] = None
    """
    The amount of empty space to the leading edge of the divider.

    If `None`, [`DividerTheme.leading_indent`][flet.DividerTheme.leading_indent] is used.
    If that's is also `None`, defaults to `0.0`.
    """

    thickness: Optional[Number] = None
    """
    The thickness of the line drawn within the divider. 
    
    A divider with a thickness of `0.0` is always drawn as a line with a 
    height of exactly one device pixel.

    If `None`, [`DividerTheme.thickness`][flet.DividerTheme.thickness] is used.
    If that's is also `None`, defaults to `0.0`.
    """

    trailing_indent: Optional[Number] = None
    """
    The amount of empty space to the trailing edge of the divider.

    If `None`, [`DividerTheme.trailing_indent`][flet.DividerTheme.trailing_indent] is used.
    If that's is also `None`, defaults to `0.0`.
    """

    def before_update(self):
        super().before_update()
        assert (
            self.height is None or self.height >= 0
        ), f"height must be greater than or equal to 0, got {self.height}"
        assert (
            self.thickness is None or self.thickness >= 0
        ), f"thickness must be greater than or equal to 0, got {self.thickness}"
        assert (
            self.leading_indent is None or self.leading_indent >= 0
        ), f"leading_indent must be greater than or equal to 0, got {self.leading_indent}"
        assert (
            self.trailing_indent is None or self.trailing_indent >= 0
        ), f"trailing_indent must be greater than or equal to 0, got {self.trailing_indent}"
