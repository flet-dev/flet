from typing import List, Optional

from flet.controls.alignment import Alignment
from flet.controls.control import control
from flet.controls.core.canvas.shape import Shape
from flet.controls.core.text_span import TextSpan
from flet.controls.text_style import TextStyle
from flet.controls.types import OptionalNumber, TextAlign

__all__ = ["Text"]


@control("Text")
class Text(Shape):
    x: OptionalNumber = None
    y: OptionalNumber = None
    text: Optional[str] = None
    style: Optional[TextStyle] = None
    spans: Optional[List[TextSpan]] = None
    alignment: Optional[Alignment] = None
    text_align: Optional[TextAlign] = None
    max_lines: Optional[int] = None
    max_width: OptionalNumber = None
    ellipsis: Optional[str] = None
    rotate: OptionalNumber = None
