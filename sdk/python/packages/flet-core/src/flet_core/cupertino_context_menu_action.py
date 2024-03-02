from typing import Any, Optional

from flet_core.adaptive_control import AdaptiveControl
from flet_core.control import Control
from flet_core.ref import Ref


class CupertinoContextMenuAction(AdaptiveControl):
    """
    An action that can be added to a CupertinoContextMenu.

    -----

    Online docs: https://flet.dev/docs/controls/cupertinocontextmenuaction
    """

    def __init__(
        self,
        content: Optional[Control] = None,
        text: Optional[str] = None,
        trailing_icon: Optional[str] = None,
        default: Optional[bool] = None,
        destructive: Optional[bool] = None,
        on_click=None,
        #
        # Control
        #
        ref: Optional[Ref] = None,
        disabled: Optional[bool] = None,
        visible: Optional[bool] = None,
        data: Any = None,
        adaptive: Optional[bool] = False,
    ):
        Control.__init__(
            self,
            ref=ref,
            disabled=disabled,
            visible=visible,
            data=data,
        )

        AdaptiveControl.__init__(self, adaptive=adaptive)

        self.default = default
        self.destructive = destructive
        self.content = content
        self.trailing_icon = trailing_icon
        self.on_click = on_click
        self.text = text

    def _get_control_name(self):
        return "cupertinocontextmenuaction"

    def _get_children(self):
        return [self.__content] if self.__content else []

    # default
    @property
    def default(self) -> Optional[bool]:
        return self._get_attr("default", data_type="bool", def_value=False)

    @default.setter
    def default(self, value: Optional[bool]):
        self._set_attr("default", value)

    # destructive
    @property
    def destructive(self) -> Optional[bool]:
        return self._get_attr("destructive", data_type="bool", def_value=False)

    @destructive.setter
    def destructive(self, value: Optional[bool]):
        self._set_attr("destructive", value)

    # trailing_icon
    @property
    def trailing_icon(self) -> Optional[str]:
        return self._get_attr("trailingIcon")

    @trailing_icon.setter
    def trailing_icon(self, value: Optional[str]):
        self._set_attr("trailingIcon", value)

    # text
    @property
    def text(self) -> Optional[str]:
        return self._get_attr("text")

    @text.setter
    def text(self, value: Optional[str]):
        self._set_attr("text", value)

    # content
    @property
    def content(self) -> Optional[Control]:
        return self.__content

    @content.setter
    def content(self, value: Optional[Control]):
        self.__content = value

    # on_click
    @property
    def on_click(self):
        return self._get_event_handler("click")

    @on_click.setter
    def on_click(self, handler):
        self._add_event_handler("click", handler)
