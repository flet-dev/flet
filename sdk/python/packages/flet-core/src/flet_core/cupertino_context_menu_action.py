from typing import Any, Optional

from flet_core.adaptive_control import AdaptiveControl
from flet_core.control import Control
from flet_core.ref import Ref
from flet_core.types import OptionalControlEventCallable


class CupertinoContextMenuAction(AdaptiveControl):
    """
    An action that can be added to a CupertinoContextMenu.

    -----

    Online docs: https://flet.dev/docs/controls/cupertinocontextmenuaction
    """

    def __init__(
        self,
        text: Optional[str] = None,
        content: Optional[Control] = None,
        is_default_action: Optional[bool] = None,
        is_destructive_action: Optional[bool] = None,
        trailing_icon: Optional[str] = None,
        on_click: OptionalControlEventCallable = None,
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

        self.is_default_action = is_default_action
        self.is_destructive_action = is_destructive_action
        self.content = content
        self.trailing_icon = trailing_icon
        self.on_click = on_click
        self.text = text

    def _get_control_name(self):
        return "cupertinocontextmenuaction"

    def _get_children(self):
        return [self.__content] if self.__content else []

    # is_default_action
    @property
    def is_default_action(self) -> bool:
        return self._get_attr("isDefaultAction", data_type="bool", def_value=False)

    @is_default_action.setter
    def is_default_action(self, value: Optional[bool]):
        self._set_attr("isDefaultAction", value)

    # is_destructive_action
    @property
    def is_destructive_action(self) -> bool:
        return self._get_attr("isDestructiveAction", data_type="bool", def_value=False)

    @is_destructive_action.setter
    def is_destructive_action(self, value: Optional[bool]):
        self._set_attr("isDestructiveAction", value)

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
    def on_click(self) -> OptionalControlEventCallable:
        return self._get_event_handler("click")

    @on_click.setter
    def on_click(self, handler: OptionalControlEventCallable):
        self._add_event_handler("click", handler)
