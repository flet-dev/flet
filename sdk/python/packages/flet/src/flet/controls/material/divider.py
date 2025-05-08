from flet.controls.base_control import control
from flet.controls.control import Control
from flet.controls.types import OptionalColorValue, OptionalNumber

__all__ = ["Divider"]


@control("Divider")
class Divider(Control):
    """
    A thin horizontal line, with padding on either side.

    In the material design language, this represents a divider.

    Online docs: https://flet.dev/docs/controls/divider
    """

    color: OptionalColorValue = None
    """
    The color to use when painting the line.
    
    If this is `None`, then the `DividerTheme.color` is used. If that is also `None`, 
    then the `Theme.divider_color` is used.
    """

    height: OptionalNumber = None
    """
    The divider's height extent. The divider itself is always drawn as a horizontal 
    line that is centered within the height specified by this value.

    If this is `None`, then the `DividerTheme.space` is used. If that is also `None`, 
    then `16.0` is used.
    """

    leading_indent: OptionalNumber = None
    """
    The amount of empty space to the leading edge of the divider.

    If this is `None`, then the `DividerTheme.leading_indent` is used. If that is also 
    `None`, then `0.0` is used.
    """

    thickness: OptionalNumber = None
    """
    The thickness of the line drawn within the divider. A divider with a thickness of 
    `0.0` is always drawn as a line with a height of exactly one device pixel.
    
    If this is `None`, then the `DividerTheme.thickness` is used. If that is also 
    `None`, then `0.0` is used.
    """

    trailing_indent: OptionalNumber = None
    """
    The amount of empty space to the trailing edge of the divider.
    
    If this is `None`, then the `DividerTheme.trailing_indent` is used. If that is also 
    `None`, then `0.0` is used.
    """

    def before_update(self):
        super().before_update()
        assert (
            self.height is None or self.height >= 0
        ), "height must be greater than or equal to 0"
        assert (
            self.thickness is None or self.thickness >= 0
        ), "thickness must be greater than or equal to 0"
        assert (
            self.leading_indent is None or self.leading_indent >= 0
        ), "leading_indent must be greater than or equal to 0"
        assert (
            self.trailing_indent is None or self.trailing_indent >= 0
        ), "trailing_indent must be greater than or equal to 0"
