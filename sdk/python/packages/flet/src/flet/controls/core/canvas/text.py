from dataclasses import field
from typing import Optional

from flet.controls.alignment import Alignment
from flet.controls.base_control import control
from flet.controls.core.canvas.shape import Shape
from flet.controls.core.text_span import TextSpan
from flet.controls.text_style import TextStyle
from flet.controls.types import Number, TextAlign

__all__ = ["Text"]


@control("Text")
class Text(Shape):
    """
    Draws [`value`][(c).] with [`style`][(c).] at
    the given ([`x`][(c).], [`y`][(c).]) point.
    """

    x: Number
    """
    The x-axis coordinate of the text's `alignment` point.
    """

    y: Number
    """
    The y-axis coordinate of the text's `alignment` point.
    """

    value: Optional[str] = None
    """
    The text to draw.
    """

    style: Optional[TextStyle] = None
    """
    A text style to draw `text` and `spans` with.
    """

    spans: Optional[list[TextSpan]] = None
    """
    The list of [`TextSpan`][flet.]
    objects to build a rich text paragraph.
    """

    alignment: Alignment = field(default_factory=lambda: Alignment.TOP_LEFT)
    """
    A point within a text rectangle to determine its position and rotation center.
    """

    text_align: TextAlign = TextAlign.START
    """
    Text horizontal align.
    """

    max_lines: Optional[int] = None
    """
    The maximum number of lines painted. Lines beyond this number are silently
    dropped. For example, if `max_lines = 1`, then only one line is rendered.
    If `max_lines = None`, but `ellipsis != None`, then lines after the first one
    that overflows the width constraints are dropped.
    """

    max_width: Optional[Number] = None
    """
    The maximum width of the painted text.

    Defaults to `None` - infinity.
    """

    ellipsis: Optional[str] = None
    """
    String used to ellipsize overflowing text.
    """

    rotate: Number = 0
    """
    The rotation of this text in radians. Text is rotated around the point determined by
    `alignment`.
    """
