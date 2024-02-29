from enum import Enum
from typing import Any, Optional

from flet_core.control import Control, OptionalNumber
from flet_core.ref import Ref
from flet_core.types import MarginValue, PaddingValue


class SnackBarBehavior(Enum):
    FIXED = "fixed"
    FLOATING = "floating"


class DismissDirection(Enum):
    NONE = "none"
    VERTICAL = "vertical"
    HORIZONTAL = "horizontal"
    END_TO_START = "endToStart"
    START_TO_END = "startToEnd"
    UP = "up"
    DOWN = "down"


class SnackBar(Control):
    """
    A lightweight message with an optional action which briefly displays at the bottom of the screen.

    Example:
    ```
    import flet as ft

    class Data:
        def __init__(self) -> None:
            self.counter = 0

    d = Data()

    def main(page):

        page.snack_bar = ft.SnackBar(
            content=ft.Text("Hello, world!"),
            action="Alright!",
        )
        page.snack_bar.open = True

        def on_click(e):
            page.snack_bar = ft.SnackBar(ft.Text(f"Hello {d.counter}"))
            page.snack_bar.open = True
            d.counter += 1
            page.update()

        page.add(ft.ElevatedButton("Open SnackBar", on_click=on_click))

    ft.app(target=main)
    ```

    -----

    Online docs: https://flet.dev/docs/controls/snackbar
    """

    def __init__(
        self,
        content: Control,
        open: bool = False,
        behavior: Optional[SnackBarBehavior] = None,
        dismiss_direction: Optional[DismissDirection] = None,
        show_close_icon: Optional[bool] = False,
        action: Optional[str] = None,
        action_color: Optional[str] = None,
        close_icon_color: Optional[str] = None,
        bgcolor: Optional[str] = None,
        duration: Optional[int] = None,
        margin: MarginValue = None,
        padding: PaddingValue = None,
        width: OptionalNumber = None,
        elevation: OptionalNumber = None,
        on_action=None,
        #
        # Control
        #
        ref: Optional[Ref] = None,
        disabled: Optional[bool] = None,
        visible: Optional[bool] = None,
        data: Any = None,
    ):
        Control.__init__(
            self,
            ref=ref,
            disabled=disabled,
            visible=visible,
            data=data,
        )

        self.open = open
        self.behavior = behavior
        self.dismiss_direction = dismiss_direction
        self.show_close_icon = show_close_icon
        self.close_icon_color = close_icon_color
        self.margin = margin
        self.padding = padding
        self.width = width
        self.content = content
        self.action = action
        self.action_color = action_color
        self.bgcolor = bgcolor
        self.duration = duration
        self.elevation = elevation
        self.on_action = on_action

    def _get_control_name(self):
        return "snackbar"

    def _get_children(self):
        children = []
        if self.__content:
            self.__content._set_attr_internal("n", "content")
            children.append(self.__content)
        return children

    def before_update(self):
        super().before_update()
        self._set_attr_json("margin", self.__margin)
        self._set_attr_json("padding", self.__padding)

    # open
    @property
    def open(self) -> Optional[bool]:
        return self._get_attr("open", data_type="bool", def_value=False)

    @open.setter
    def open(self, value: Optional[bool]):
        self._set_attr("open", value)

    # show_close_icon
    @property
    def show_close_icon(self) -> Optional[bool]:
        return self._get_attr("showCloseIcon", data_type="bool", def_value=False)

    @show_close_icon.setter
    def show_close_icon(self, value: Optional[bool]):
        self._set_attr("showCloseIcon", value)

    # content
    @property
    def content(self) -> Control:
        return self.__content

    @content.setter
    def content(self, value: Control):
        self.__content = value

    # action
    @property
    def action(self):
        return self._get_attr("action")

    @action.setter
    def action(self, value):
        self._set_attr("action", value)

    # action_color
    @property
    def action_color(self):
        return self._get_attr("actionColor")

    @action_color.setter
    def action_color(self, value):
        self._set_attr("actionColor", value)

    # bgcolor
    @property
    def bgcolor(self):
        return self._get_attr("bgColor")

    @bgcolor.setter
    def bgcolor(self, value):
        self._set_attr("bgColor", value)

    # close_icon_color
    @property
    def close_icon_color(self):
        return self._get_attr("closeIconColor")

    @close_icon_color.setter
    def close_icon_color(self, value):
        self._set_attr("closeIconColor", value)

    # duration
    @property
    def duration(self) -> Optional[int]:
        return self._get_attr("duration")

    @duration.setter
    def duration(self, value: Optional[int]):
        self._set_attr("duration", value)

    # behavior
    @property
    def behavior(self) -> Optional[SnackBarBehavior]:
        return self.__behavior

    @behavior.setter
    def behavior(self, value: Optional[SnackBarBehavior]):
        self.__behavior = value
        self._set_attr(
            "behavior",
            value.value if isinstance(value, SnackBarBehavior) else value,
        )

    # dismissDirection
    @property
    def dismiss_direction(self) -> Optional[DismissDirection]:
        return self.__dismiss_direction

    @dismiss_direction.setter
    def dismiss_direction(self, value: Optional[DismissDirection]):
        self.__dismiss_direction = value
        self._set_attr(
            "dismissDirection",
            value.value if isinstance(value, DismissDirection) else value,
        )

    # padding
    @property
    def padding(self) -> PaddingValue:
        return self.__padding

    @padding.setter
    def padding(self, value: PaddingValue):
        self.__padding = value

    # margin
    @property
    def margin(self) -> MarginValue:
        return self.__margin

    @margin.setter
    def margin(self, value: MarginValue):
        self.__margin = value

    # width
    @property
    def width(self) -> OptionalNumber:
        return self._get_attr("width")

    @width.setter
    def width(self, value: OptionalNumber):
        self._set_attr("width", value)

    # elevation
    @property
    def elevation(self) -> OptionalNumber:
        return self._get_attr("elevation")

    @elevation.setter
    def elevation(self, value: OptionalNumber):
        self._set_attr("elevation", value)

    # on_action
    @property
    def on_action(self):
        return self._get_event_handler("action")

    @on_action.setter
    def on_action(self, handler):
        self._add_event_handler("action", handler)
