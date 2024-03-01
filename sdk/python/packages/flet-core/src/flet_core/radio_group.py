from typing import Any, Optional

from flet_core.control import Control, OptionalNumber
from flet_core.ref import Ref


class RadioGroup(Control):
    """
    Radio buttons let people select a single option from two or more choices.

    Example:
    ```
    import flet as ft

    def main(page):
    def button_clicked(e):
        t.value = f"Your favorite color is:  {cg.value}"
        page.update()

    t = ft.Text()
    b = ft.ElevatedButton(text='Submit', on_click=button_clicked)
    cg = ft.RadioGroup(content=ft.Column([
        ft.Radio(value="red", label="Red"),
        ft.Radio(value="green", label="Green"),
        ft.Radio(value="blue", label="Blue")]))

    page.add(ft.Text("Select your favorite color:"), cg, b, t)

    ft.app(target=main)
    ```

    -----

    Online docs: https://flet.dev/docs/controls/radio
    """

    def __init__(
        self,
        content: Optional[Control] = None,
        value: Optional[str] = None,
        on_change=None,
        #
        # Control
        #
        ref: Optional[Ref] = None,
        opacity: OptionalNumber = None,
        visible: Optional[bool] = None,
        disabled: Optional[bool] = None,
        data: Any = None,
    ):

        Control.__init__(
            self,
            ref=ref,
            opacity=opacity,
            visible=visible,
            disabled=disabled,
            data=data,
        )

        self.content = content
        self.value = value
        self.on_change = on_change

    def _get_control_name(self):
        return "radiogroup"

    def _get_children(self):
        if self.__content is None:
            return []
        self.__content._set_attr_internal("n", "content")
        return [self.__content]

    # value
    @property
    def value(self) -> Optional[str]:
        return self._get_attr("value")

    @value.setter
    def value(self, value: Optional[str]):
        self._set_attr("value", value)

    # content
    @property
    def content(self) -> Optional[Control]:
        return self.__content

    @content.setter
    def content(self, value: Optional[Control]):
        self.__content = value

    # on_change
    @property
    def on_change(self):
        return self._get_event_handler("change")

    @on_change.setter
    def on_change(self, handler):
        self._add_event_handler("change", handler)
