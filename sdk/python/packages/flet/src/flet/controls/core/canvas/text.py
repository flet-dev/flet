from typing import Optional

from flet.controls.alignment import Alignment
from flet.controls.base_control import control
from flet.controls.core.canvas.shape import Shape
from flet.controls.core.text_span import TextSpan
from flet.controls.text_style import TextStyle
from flet.controls.types import OptionalNumber, TextAlign

__all__ = ["Text"]


@control("Text")
class Text(Shape):
    """
    Draws `text` with `style` in the given point (`x`, `y`).
    """

    x: OptionalNumber = None
    """
    The x-axis coordinate of the text's `alignment` point.
    """

    y: OptionalNumber = None
    """
    The y-axis coordinate of the text's `alignment` point.
    """

    text: Optional[str] = None
    """
    The text to draw.
    """

    style: Optional[TextStyle] = None
    """
    A text style to draw `text` and `spans` with. The value is the instance of
    [`TextStyle`](https://flet.dev/docs/reference/types/textstyle) class.
    """

    spans: Optional[list[TextSpan]] = None
    """
    The list of [`TextSpan`](https://flet.dev/docs/reference/types/textspan)
    objects to build a rich text paragraph.
    """

    alignment: Optional[Alignment] = None
    """
    A point within a text rectangle to determine its position and rotation center.

    Value is of type [`Alignment`](https://flet.dev/docs/reference/types/alignment)
    and defaults to `alignment.top_left`.
    """

    text_align: Optional[TextAlign] = None
    """
    Text horizontal align.

    Value is of type [`TextAlign`](https://flet.dev/docs/reference/types/textalign)
    and defaults to `TextAlign.LEFT`.
    """

    max_lines: Optional[int] = None
    """
    The maximum number of lines painted. Lines beyond this number are silently
    dropped. For example, if `max_lines = 1`, then only one line is rendered.
    If `max_lines = None`, but `ellipsis != None`, then lines after the first one
    that overflows the width constraints are dropped.
    """

    max_width: OptionalNumber = None
    """
    The maximum width of the painted text.

    Defaults to `None` - infinity.
    """

    ellipsis: Optional[str] = None
    """
    String used to ellipsize overflowing text.
    """

    rotate: OptionalNumber = None
    """
    Text rotation in radians. Text is rotated around the point determined by
    `alignment`. See code examples above.
    ```
    """  

