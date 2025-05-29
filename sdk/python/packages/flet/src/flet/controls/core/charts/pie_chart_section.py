from typing import Optional

from flet.controls.base_control import control
from flet.controls.border import BorderSide
from flet.controls.control import Control
from flet.controls.text_style import TextStyle
from flet.controls.types import Number, OptionalColorValue, OptionalNumber


@control("s")
class PieChartSection(Control):
    value: Number
    """
    Determines how much the section should occupy. This depends on sum of all sections,
    each section should occupy (`value` / sum of all values) * `360` degrees.
    """

    radius: OptionalNumber = None
    """
    External radius of the section.
    """

    color: OptionalColorValue = None
    """
    Background [color](https://flet.dev/docs/reference/colors) of the section.
    """

    border_side: Optional[BorderSide] = None
    """
    The border around section shape.

    Value is of type [`BorderSide`](https://flet.dev/docs/reference/types/borderside).
    """

    title: Optional[str] = None
    """
    A title drawn at the center of the section. No title is drawn if `title` is empty.
    """

    title_style: Optional[TextStyle] = None
    """
    The style to draw `title` with.

    The value is an instance of [`TextStyle`](https://flet.dev/docs/reference/types/textstyle) class.
    """

    title_position: OptionalNumber = None
    """
    By default title is drawn in the middle of the section, but its position can be changed
    with `title_position` property which value must be between `0.0` (near the center) and
    `1.0`(near the outside of the pie chart).
    """

    badge_content: Optional[Control] = None
    """
    An optional `Control` drawn in the middle of a section.
    """

    badge_position: OptionalNumber = None
    """
    By default the badge is drawn in the middle of the section, but its position can be
    changed with `badge_position` property which value must be between `0.0` (near the center)
    and `1.0`(near the outside of the pie chart).
    """

