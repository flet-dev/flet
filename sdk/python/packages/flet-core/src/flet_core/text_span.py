from typing import Any, List, Optional

from flet_core.inline_span import InlineSpan
from flet_core.text_style import TextStyle


class TextSpan(InlineSpan):
    def __init__(
        self,
        text: Optional[str] = None,
        style: Optional[TextStyle] = None,
        spans: Optional[List[InlineSpan]] = None,
        # base
        ref=None,
        visible: Optional[bool] = None,
        disabled: Optional[bool] = None,
        data: Any = None,
    ):
        InlineSpan.__init__(
            self, ref=ref, visible=visible, disabled=disabled, data=data
        )

        self.text = text
        self.style = style
        self.spans = spans

    def _get_control_name(self):
        return "textspan"

    def _get_children(self):
        children = []
        children.extend(self.__spans)
        return children

    def _before_build_command(self):
        super()._before_build_command()
        self._set_attr_json("style", self.__style)

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
