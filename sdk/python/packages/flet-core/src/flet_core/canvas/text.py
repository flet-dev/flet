from typing import Any, List, Optional

from flet_core.alignment import Alignment
from flet_core.canvas.shape import Shape
from flet_core.control import OptionalNumber
from flet_core.painting import Paint
from flet_core.text_span import TextSpan
from flet_core.text_style import TextStyle
from flet_core.types import OffsetValue, TextAlign, TextAlignString


class Text(Shape):
    def __init__(
        self,
        text: Optional[str] = None,
        style: Optional[TextStyle] = None,
        spans: Optional[List[TextSpan]] = None,
        offset: OffsetValue = None,
        alignment: Optional[Alignment] = None,
        text_align: TextAlign = TextAlign.NONE,
        max_lines: Optional[int] = None,
        max_width: OptionalNumber = None,
        ellipsis: Optional[str] = None,
        rotate: OptionalNumber = None,
        # base
        ref=None,
        visible: Optional[bool] = None,
        disabled: Optional[bool] = None,
        data: Any = None,
    ):
        Shape.__init__(self, ref=ref, visible=visible, disabled=disabled, data=data)

        self.text = text
        self.style = style
        self.spans = spans
        self.offset = offset
        self.alignment = alignment
        self.text_align = text_align
        self.max_lines = max_lines
        self.max_width = max_width
        self.ellipsis = ellipsis
        self.rotate = rotate

    def _get_control_name(self):
        return "text"

    def _before_build_command(self):
        super()._before_build_command()
        self._set_attr_json("style", self.__style)
        self._set_attr_json("spans", self.__spans)
        self._set_attr_json("offset", self.__offset)
        self._set_attr_json("alignment", self.__alignment)

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
    def spans(self) -> Optional[List[TextSpan]]:
        return self.__spans

    @spans.setter
    def spans(self, value: Optional[List[TextSpan]]):
        self.__spans = value if value is not None else []

    # offset
    @property
    def offset(self) -> OffsetValue:
        return self.__offset

    @offset.setter
    def offset(self, value: OffsetValue):
        self.__offset = value

    # alignment
    @property
    def alignment(self) -> Optional[Alignment]:
        return self.__alignment

    @alignment.setter
    def alignment(self, value: Optional[Alignment]):
        self.__alignment = value

    # text_align
    @property
    def text_align(self) -> TextAlign:
        return self.__text_align

    @text_align.setter
    def text_align(self, value: TextAlign):
        self.__text_align = value
        if isinstance(value, TextAlign):
            self._set_attr("textAlign", value.value)
        else:
            self.__set_text_align(value)

    def __set_text_align(self, value: TextAlignString):
        self._set_attr("textAlign", value)

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
