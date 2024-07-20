from typing import Any, Optional

from flet_core.control import Control
from flet_core.ref import Ref
from flet_core.types import OptionalEventCallable, DefaultOptionalEventCallable


class SelectionArea(Control):
    """
    Flet controls are not selectable by default. SelectionArea is used to enable selection for its child control.

    Example:
    ```
    import flet as ft

    def main(page: ft.Page):
        page.add(
            ft.SelectionArea(
                content=ft.Column([ft.Text("Selectable text"), ft.Text("Also selectable")])
            )
        )
        page.add(ft.Text("Not selectable"))

    ft.app(target=main)
    ```

    -----

    Online docs: https://flet.dev/docs/controls/selectionarea
    """

    def __init__(
        self,
        content: Control,
        on_change: OptionalEventCallable = None,
        #
        # Control
        #
        ref: Optional[Ref] = None,
        data: Any = None,
    ):
        Control.__init__(
            self,
            ref=ref,
            data=data,
        )

        self.content = content
        self.on_change = on_change

    def _get_control_name(self):
        return "selectionarea"

    def _get_children(self):
        self.__content._set_attr_internal("n", "content")
        return [self.__content]

    # content
    @property
    def content(self) -> Control:
        return self.__content

    @content.setter
    def content(self, value: Control):
        self.__content = value

    # on_change
    @property
    def on_change(self) -> DefaultOptionalEventCallable:
        return self._get_event_handler("change")

    @on_change.setter
    def on_change(self, handler: DefaultOptionalEventCallable):
        self._add_event_handler("change", handler)
