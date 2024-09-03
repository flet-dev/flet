from typing import Any, List, Optional

from flet_core.inline_span import InlineSpan
from flet_core.text_style import TextStyle
from flet_core.types import (
    UrlTarget,
    OptionalControlEventCallable,
)


class TextSpan(InlineSpan):
    def __init__(
        self,
        text: Optional[str] = None,
        style: Optional[TextStyle] = None,
        spans: Optional[List[InlineSpan]] = None,
        url: Optional[str] = None,
        url_target: Optional[UrlTarget] = None,
        on_click: OptionalControlEventCallable = None,
        on_enter: OptionalControlEventCallable = None,
        on_exit: OptionalControlEventCallable = None,
        #
        # Control
        #
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
        self.url = url
        self.url_target = url_target
        self.on_click = on_click
        self.on_enter = on_enter
        self.on_exit = on_exit

    def _get_control_name(self):
        return "textspan"

    def _get_children(self):
        return self.__spans

    def before_update(self):
        super().before_update()
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
    def spans(self) -> List[InlineSpan]:
        return self.__spans

    @spans.setter
    def spans(self, value: Optional[List[InlineSpan]]):
        self.__spans = value if value is not None else []

    # url
    @property
    def url(self) -> Optional[str]:
        return self._get_attr("url")

    @url.setter
    def url(self, value: Optional[str]):
        self._set_attr("url", value)

    # url_target
    @property
    def url_target(self) -> Optional[UrlTarget]:
        return self.__url_target

    @url_target.setter
    def url_target(self, value: Optional[UrlTarget]):
        self.__url_target = value
        self._set_enum_attr("urlTarget", value, UrlTarget)

    # on_click
    @property
    def on_click(self) -> OptionalControlEventCallable:
        return self._get_event_handler("click")

    @on_click.setter
    def on_click(self, handler: OptionalControlEventCallable):
        self._add_event_handler("click", handler)
        self._set_attr("onClick", True if handler is not None else None)

    # on_enter
    @property
    def on_enter(self) -> OptionalControlEventCallable:
        return self._get_event_handler("enter")

    @on_enter.setter
    def on_enter(self, handler: OptionalControlEventCallable):
        self._add_event_handler("enter", handler)
        self._set_attr("onEnter", True if handler is not None else None)

    # on_exit
    @property
    def on_exit(self) -> OptionalControlEventCallable:
        return self._get_event_handler("exit")

    @on_exit.setter
    def on_exit(self, handler: OptionalControlEventCallable):
        self._add_event_handler("exit", handler)
        self._set_attr("onExit", True if handler is not None else None)
