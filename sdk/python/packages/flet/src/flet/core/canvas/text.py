from typing import Any, List, Optional

from flet.core.alignment import Alignment
from flet.core.canvas.shape import Shape
from flet.core.control import OptionalNumber
from flet.core.inline_span import InlineSpan
from flet.core.text_style import TextStyle
from flet.core.types import TextAlign


class Text(Shape):
    def __init__(
        self,
        x: OptionalNumber = None,
        y: OptionalNumber = None,
        text: Optional[str] = None,
        style: Optional[TextStyle] = None,
        spans: Optional[List[InlineSpan]] = None,
        alignment: Optional[Alignment] = None,
        text_align: Optional[TextAlign] = None,
        max_lines: Optional[int] = None,
        max_width: OptionalNumber = None,
        ellipsis: Optional[str] = None,
        rotate: OptionalNumber = None,
        #
        # Control
        #
        ref=None,
        visible: Optional[bool] = None,
        disabled: Optional[bool] = None,
        data: Any = None,
    ):
        Shape.__init__(self, ref=ref, visible=visible, disabled=disabled, data=data)

        self.x = x
        self.y = y
        self.text = text
        self.style = style
        self.spans = spans
        self.alignment = alignment
        self.text_align = text_align
        self.max_lines = max_lines
        self.max_width = max_width
        self.ellipsis = ellipsis
        self.rotate = rotate

    def _get_control_name(self):
        return "text"

    def _get_children(self):
        children = []
        children.extend(self.__spans)
        return children

    def before_update(self):
        super().before_update()
        self._set_attr_json("style", self.__style)
        self._set_attr_json("alignment", self.__alignment)

    # x
    @property
    def x(self) -> OptionalNumber:
        return self._get_attr("x")

    @x.setter
    def x(self, value: OptionalNumber):
        self._set_attr("x", value)

    # y
    @property
    def y(self) -> OptionalNumber:
        return self._get_attr("y")

    @y.setter
    def y(self, value: OptionalNumber):
        self._set_attr("y", value)

    # text
    @property
    def text(self) -> Optional[str]:
        return self._get_attr("text")

    @text.setter
    def text(self, value: Optional[str]):
        self._set_attr("text", value)

    # style
    @property
    def style(self) -> Optional[TextStyle]:
        return self.__style

    @style.setter
    def style(self, value: Optional[TextStyle]):
        self.__style = value

    # spans
    @property
    def spans(self) -> Optional[List[InlineSpan]]:
        return self.__spans

    @spans.setter
    def spans(self, value: Optional[List[InlineSpan]]):
        self.__spans = value if value is not None else []

    # alignment
    @property
    def alignment(self) -> Optional[Alignment]:
        return self.__alignment

    @alignment.setter
    def alignment(self, value: Optional[Alignment]):
        self.__alignment = value

    # text_align
    @property
    def text_align(self) -> Optional[TextAlign]:
        return self.__text_align

    @text_align.setter
    def text_align(self, value: Optional[TextAlign]):
        self.__text_align = value
        self._set_attr(
            "textAlign", value.value if isinstance(value, TextAlign) else value
        )

    # max_lines
    @property
    def max_lines(self) -> Optional[int]:
        return self._get_attr("maxLines")

    @max_lines.setter
    def max_lines(self, value: Optional[int]):
        self._set_attr("maxLines", value)

    # max_width
    @property
    def max_width(self) -> OptionalNumber:
        return self._get_attr("maxWidth")

    @max_width.setter
    def max_width(self, value: OptionalNumber):
        self._set_attr("maxWidth", value)

    # ellipsis
    @property
    def ellipsis(self) -> Optional[str]:
        return self._get_attr("ellipsis")

    @ellipsis.setter
    def ellipsis(self, value: Optional[str]):
        self._set_attr("ellipsis", value)

    # rotate
    @property
    def rotate(self) -> OptionalNumber:
        return self._get_attr("rotate")

    @rotate.setter
    def rotate(self, value: OptionalNumber):
        self._set_attr("rotate", value)
