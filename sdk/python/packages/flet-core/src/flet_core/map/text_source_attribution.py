from typing import Any, Optional

from flet_core.control import Control
from flet_core.ref import Ref
from flet_core.text_style import TextStyle
from flet_core.types import OptionalEventCallable


class TextSourceAttribution(Control):
    """
    A text source attribution displayed on the Map.
    For it to be displayed, it should be part of a RichAttribution.attributions list.

    -----

    Online docs: https://flet.dev/docs/controls/maptextsourceattribution
    """

    def __init__(
        self,
        text: str,
        text_style: Optional[TextStyle] = None,
        prepend_copyright: Optional[bool] = None,
        on_click: OptionalEventCallable = None,
        #
        # Control
        #
        ref: Optional[Ref] = None,
        visible: Optional[bool] = None,
        data: Any = None,
    ):

        Control.__init__(
            self,
            ref=ref,
            visible=visible,
            data=data,
        )

        self.text = text
        self.text_style = text_style
        self.prepend_copyright = prepend_copyright
        self.on_click = on_click

    def _get_control_name(self):
        return "map_text_source_attribution"

    def before_update(self):
        super().before_update()
        if isinstance(self.__text_style, TextStyle):
            self._set_attr_json("textStyle", self.__text_style)

    # text_style
    @property
    def text_style(self) -> Optional[TextStyle]:
        return self.__text_style

    @text_style.setter
    def text_style(self, value: Optional[TextStyle]):
        self.__text_style = value

    # prepend_copyright
    @property
    def prepend_copyright(self) -> Optional[bool]:
        return self._get_attr("prependCopyright", data_type="bool", def_value=True)

    @prepend_copyright.setter
    def prepend_copyright(self, value: Optional[bool]):
        self._set_attr("prependCopyright", value)

    # text
    @property
    def text(self) -> str:
        return self._get_attr("text")

    @text.setter
    def text(self, value: str):
        self._set_attr("text", value)

    # on_click
    @property
    def on_click(self) -> OptionalEventCallable:
        return self._get_event_handler("click")

    @on_click.setter
    def on_click(self, handler: OptionalEventCallable):
        self._add_event_handler("click", handler)
