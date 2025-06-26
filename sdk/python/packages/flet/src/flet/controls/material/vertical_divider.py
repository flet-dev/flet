from flet.controls.base_control import control
from flet.controls.control import Control
from flet.controls.types import OptionalColorValue, OptionalNumber

__all__ = ["VerticalDivider"]


@control("VerticalDivider")
class VerticalDivider(Control):
    """
    A thin vertical line, with padding on either side.

    In the material design language, this represents a divider.

    Online docs: https://flet.dev/docs/controls/verticaldivider
    """

    width: OptionalNumber = None
    """
    The divider's width. The divider itself is always drawn as a vertical line
    that is centered within the width specified by this value.

    Defaults to `16.0`.
    """

    thickness: OptionalNumber = None
    """
    The thickness of the line drawn within the divider.

    A divider with a thickness of `0.0` is always drawn as a line with a width of
    exactly one device pixel.

    Defaults to `0.0`.
    """

    color: OptionalColorValue = None
    """
    The [color](https://flet.dev/docs/reference/colors) to use when painting the
    line.
    """

    leading_indent: OptionalNumber = None
    """
    The amount of empty space to the leading edge of the divider.

    Defaults to `0.0`.
    """

    trailing_indent: OptionalNumber = None
    """
    The amount of empty space to the trailing edge of the divider.

    Defaults to `0.0`.
    """

    def before_update(self):
        super().before_update()
        assert (
            self.width is None or self.width >= 0
        ), "width must be greater than or equal to 0"
        assert (
            self.thickness is None or self.thickness >= 0
        ), "thickness must be greater than or equal to 0"
        assert (
            self.leading_indent is None or self.leading_indent >= 0
        ), "leading_indent must be greater than or equal to 0"
        assert (
            self.trailing_indent is None or self.trailing_indent >= 0
        ), "trailing_indent must be greater than or equal to 0"
