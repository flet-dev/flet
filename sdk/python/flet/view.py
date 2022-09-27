from beartype import beartype
from beartype.typing import List, Optional

from flet import Control
from flet.app_bar import AppBar
from flet.control import (
    CrossAxisAlignment,
    MainAxisAlignment,
    OptionalNumber,
    ScrollMode,
)
from flet.floating_action_button import FloatingActionButton
from flet.types import PaddingValue


class View(Control):
    def __init__(
        self,
        route: Optional[str] = None,
        controls: Optional[List[Control]] = None,
        appbar: Optional[AppBar] = None,
        floating_action_button: Optional[FloatingActionButton] = None,
        vertical_alignment: MainAxisAlignment = None,
        horizontal_alignment: CrossAxisAlignment = None,
        spacing: OptionalNumber = None,
        padding: PaddingValue = None,
        bgcolor: Optional[str] = None,
        scroll: ScrollMode = None,
        auto_scroll: Optional[bool] = None,
    ):
        Control.__init__(self)

        self.controls = controls or []
        self.route = route
        self.appbar = appbar
        self.floating_action_button = floating_action_button
        self.vertical_alignment = vertical_alignment
        self.horizontal_alignment = horizontal_alignment
        self.spacing = spacing
        self.padding = padding
        self.bgcolor = bgcolor
        self.scroll = scroll
        self.auto_scroll = auto_scroll

    def _get_control_name(self):
        return "view"

    def _before_build_command(self):
        self._set_attr_json("padding", self.__padding)

    def _get_children(self):
        children = []
        if self.__appbar:
            children.append(self.__appbar)
        if self.__fab:
            children.append(self.__fab)
        children.extend(self.__controls)
        return children

    # route
    @property
    def route(self):
        return self._get_attr("route")

    @route.setter
    @beartype
    def route(self, value):
        self._set_attr("route", value)

    # controls
    @property
    def controls(self) -> List[Control]:
        return self.__controls

    @controls.setter
    @beartype
    def controls(self, value: List[Control]):
        self.__controls = value

    # appbar
    @property
    def appbar(self) -> Optional[AppBar]:
        return self.__appbar

    @appbar.setter
    @beartype
    def appbar(self, value: Optional[AppBar]):
        self.__appbar = value

    # floating_action_button
    @property
    def floating_action_button(self) -> Optional[FloatingActionButton]:
        return self.__fab

    @floating_action_button.setter
    @beartype
    def floating_action_button(self, value: Optional[FloatingActionButton]):
        self.__fab = value

    # horizontal_alignment
    @property
    def horizontal_alignment(self) -> CrossAxisAlignment:
        return self._get_attr("horizontalAlignment")

    @horizontal_alignment.setter
    @beartype
    def horizontal_alignment(self, value: CrossAxisAlignment):
        self._set_attr("horizontalAlignment", value)

    # vertical_alignment
    @property
    def vertical_alignment(self) -> MainAxisAlignment:
        return self._get_attr("verticalAlignment")

    @vertical_alignment.setter
    @beartype
    def vertical_alignment(self, value: MainAxisAlignment):
        self._set_attr("verticalAlignment", value)

    # spacing
    @property
    def spacing(self) -> OptionalNumber:
        return self._get_attr("spacing")

    @spacing.setter
    @beartype
    def spacing(self, value: OptionalNumber):
        self._set_attr("spacing", value)

    # padding
    @property
    def padding(self) -> PaddingValue:
        return self.__padding

    @padding.setter
    @beartype
    def padding(self, value: PaddingValue):
        self.__padding = value

    # bgcolor
    @property
    def bgcolor(self):
        return self._get_attr("bgcolor")

    @bgcolor.setter
    def bgcolor(self, value):
        self._set_attr("bgcolor", value)

    # scroll
    @property
    def scroll(self) -> ScrollMode:
        return self.__scroll

    @scroll.setter
    @beartype
    def scroll(self, value: ScrollMode):
        self.__scroll: ScrollMode = value
        if value == True:
            value = "auto"
        elif value == False:
            value = "none"
        self._set_attr("scroll", value)

    # auto_scroll
    @property
    def auto_scroll(self) -> Optional[bool]:
        return self._get_attr("autoScroll")

    @auto_scroll.setter
    @beartype
    def auto_scroll(self, value: Optional[bool]):
        self._set_attr("autoScroll", value)
