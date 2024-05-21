from enum import Enum
from typing import Any, Optional

from flet_core.buttons import OutlinedBorder
from flet_core.control import Control, OptionalNumber
from flet_core.ref import Ref
from flet_core.types import MarginValue, PaddingValue, ClipBehavior


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
        shape: Optional[OutlinedBorder] = None,
        clip_behavior: Optional[ClipBehavior] = None,
        action_overflow_threshold: OptionalNumber = None,
        on_action=None,
        on_visible=None,
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
        self.on_visible = on_visible
        self.shape = shape
        self.clip_behavior = clip_behavior
        self.action_overflow_threshold = action_overflow_threshold

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
        self._set_attr_json("shape", self.__shape)
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
    def action(self) -> Optional[str]:
        return self._get_attr("action")

    @action.setter
    def action(self, value: Optional[str]):
        self._set_attr("action", value)

    # action_color
    @property
    def action_color(self) -> Optional[str]:
        return self._get_attr("actionColor")

    @action_color.setter
    def action_color(self, value: Optional[str]):
        self._set_attr("actionColor", value)

    # bgcolor
    @property
    def bgcolor(self) -> Optional[str]:
        return self._get_attr("bgColor")

    @bgcolor.setter
    def bgcolor(self, value: Optional[str]):
        self._set_attr("bgColor", value)

    # close_icon_color
    @property
    def close_icon_color(self) -> Optional[str]:
        return self._get_attr("closeIconColor")

    @close_icon_color.setter
    def close_icon_color(self, value: Optional[str]):
        self._set_attr("closeIconColor", value)

    # duration
    @property
    def duration(self) -> Optional[int]:
        return self._get_attr("duration", data_type="int")

    @duration.setter
    def duration(self, value: Optional[int]):
        self._set_attr("duration", value)

    # action_overflow_threshold
    @property
    def action_overflow_threshold(self) -> OptionalNumber:
        return self._get_attr("actionOverflowThreshold", data_type="float")

    @action_overflow_threshold.setter
    def action_overflow_threshold(self, value: OptionalNumber):
        self._set_attr("actionOverflowThreshold", value)

    # behavior
    @property
    def behavior(self) -> Optional[SnackBarBehavior]:
        return self.__behavior

    @behavior.setter
    def behavior(self, value: Optional[SnackBarBehavior]):
        self.__behavior = value
        self._set_attr("behavior", value, SnackBarBehavior)

    # dismissDirection
    @property
    def dismiss_direction(self) -> Optional[DismissDirection]:
        return self.__dismiss_direction

    @dismiss_direction.setter
    def dismiss_direction(self, value: Optional[DismissDirection]):
        self.__dismiss_direction = value
        self._set_enum_attr("dismissDirection", value, DismissDirection)

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
        return self._get_attr("width", data_type="float")

    @width.setter
    def width(self, value: OptionalNumber):
        self._set_attr("width", value)

    # elevation
    @property
    def elevation(self) -> OptionalNumber:
        return self._get_attr("elevation", data_type="float")

    @elevation.setter
    def elevation(self, value: OptionalNumber):
        self._set_attr("elevation", value)

    # clip_behavior
    @property
    def clip_behavior(self) -> Optional[ClipBehavior]:
        return self.__clip_behavior

    @clip_behavior.setter
    def clip_behavior(self, value: Optional[ClipBehavior]):
        self.__clip_behavior = value
        self._set_attr(
            "clipBehavior", value.value if isinstance(value, ClipBehavior) else value
        )

    # shape
    @property
    def shape(self) -> Optional[OutlinedBorder]:
        return self.__shape

    @shape.setter
    def shape(self, value: Optional[OutlinedBorder]):
        self.__shape = value

    # on_action
    @property
    def on_action(self):
        return self._get_event_handler("action")

    @on_action.setter
    def on_action(self, handler):
        self._add_event_handler("action", handler)

    # on_visible
    @property
    def on_visible(self):
        return self._get_event_handler("visible")

    @on_visible.setter
    def on_visible(self, handler):
        self._add_event_handler("visible", handler)
