from typing import Optional

from flet.controls.base_control import control
from flet.controls.control import Control
from flet.controls.types import ColorValue, Number

__all__ = ["Divider"]


@control("Divider")
class Divider(Control):
    """
    A thin horizontal line (divider), with padding on either side.

    Raises:
        ValueError: If [`height`][(c).] is negative.
        ValueError: If [`thickness`][(c).] is negative.
        ValueError: If [`leading_indent`][(c).] is negative.
        ValueError: If [`trailing_indent`][(c).] is negative.
    """

    color: Optional[ColorValue] = None
    """
    The color to use when painting the line.

    If `None`, [`DividerTheme.color`][flet.] is used.
    """

    height: Optional[Number] = None
    """
    The divider's height extent. The divider itself is always drawn as a horizontal
    line that is centered within the height specified by this value.

    If `None`, [`DividerTheme.space`][flet.] is used.
    If that's is also `None`, defaults to `16.0`.
    """

    leading_indent: Optional[Number] = None
    """
    The amount of empty space to the leading edge of the divider.

    If `None`, [`DividerTheme.leading_indent`][flet.] is used.
    If that's is also `None`, defaults to `0.0`.
    """

    thickness: Optional[Number] = None
    """
    The thickness of the line drawn within the divider.

    A divider with a thickness of `0.0` is always drawn as a line with a
    height of exactly one device pixel.

    If `None`, [`DividerTheme.thickness`][flet.] is used.
    If that is also `None`, defaults to `0.0`.
    """

    trailing_indent: Optional[Number] = None
    """
    The amount of empty space to the trailing edge of the divider.

    If `None`, [`DividerTheme.trailing_indent`][flet.] is used.
    If that is also `None`, defaults to `0.0`.
    """

    def before_update(self):
        super().before_update()
        if self.height is not None and self.height < 0:
            raise ValueError(
                f"height must be greater than or equal to 0, got {self.height}"
            )
        if self.thickness is not None and self.thickness < 0:
            raise ValueError(
                f"thickness must be greater than or equal to 0, got {self.thickness}"
            )
        if self.leading_indent is not None and self.leading_indent < 0:
            raise ValueError(
                f"leading_indent must be greater than or equal to 0, "
                f"got {self.leading_indent}"
            )
        if self.trailing_indent is not None and self.trailing_indent < 0:
            raise ValueError(
                f"trailing_indent must be greater than or equal to 0, "
                f"got {self.trailing_indent}"
            )
