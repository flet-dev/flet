from beartype import beartype
from beartype.typing import Dict, List, Optional

from flet import Control, padding
from flet.app_bar import AppBar
from flet.control import (
    CrossAxisAlignment,
    MainAxisAlignment,
    OptionalNumber,
    PaddingValue,
    ScrollMode,
)
from flet.floating_action_button import FloatingActionButton


class View(Control):
    def __init__(self):
        Control.__init__(self)

        self.__controls = []  # page controls
        self.__appbar = None
        self.__fab = None

    def _get_control_name(self):
        return "view"

    def _get_children(self):
        children = []
        if self.__appbar:
            children.append(self.__appbar)
        if self.__fab:
            children.append(self.__fab)
        children.extend(self.__controls)
        return children

    # name
    @property
    def name(self):
        return self._get_attr("name")

    @name.setter
    @beartype
    def name(self, value: str):
        self._set_attr("name", value)

    # controls
    @property
    def controls(self):
        return self.__controls

    @controls.setter
    @beartype
    def controls(self, value: List[Control]):
        self.__controls = value or []

    # appbar
    @property
    def appbar(self):
        return self.__appbar

    @appbar.setter
    @beartype
    def appbar(self, value: Optional[AppBar]):
        self.__appbar = value

    # floating_action_button
    @property
    def floating_action_button(self):
        return self.__fab

    @floating_action_button.setter
    @beartype
    def floating_action_button(self, value: Optional[FloatingActionButton]):
        self.__fab = value

    # horizontal_alignment
    @property
    def horizontal_alignment(self):
        return self._get_attr("horizontalAlignment")

    @horizontal_alignment.setter
    @beartype
    def horizontal_alignment(self, value: CrossAxisAlignment):
        self._set_attr("horizontalAlignment", value)

    # vertical_alignment
    @property
    def vertical_alignment(self):
        return self._get_attr("verticalAlignment")

    @vertical_alignment.setter
    @beartype
    def vertical_alignment(self, value: MainAxisAlignment):
        self._set_attr("verticalAlignment", value)

    # spacing
    @property
    def spacing(self):
        return self._get_attr("spacing")

    @spacing.setter
    @beartype
    def spacing(self, value: OptionalNumber):
        self._set_attr("spacing", value)

    # padding
    @property
    def padding(self):
        return self.__padding

    @padding.setter
    @beartype
    def padding(self, value: PaddingValue):
        self.__padding = value
        if value != None and isinstance(value, (int, float)):
            value = padding.all(value)
        self._set_attr_json("padding", value)

    # bgcolor
    @property
    def bgcolor(self):
        return self._get_attr("bgcolor")

    @bgcolor.setter
    def bgcolor(self, value):
        self._set_attr("bgcolor", value)

    # scroll
    @property
    def scroll(self):
        return self.__scroll

    @scroll.setter
    @beartype
    def scroll(self, value: ScrollMode):
        self.__scroll = value
        if value == True:
            value = "auto"
        elif value == False:
            value = "none"
        self._set_attr("scroll", value)

    # auto_scroll
    @property
    def auto_scroll(self):
        return self._get_attr("autoScroll")

    @auto_scroll.setter
    @beartype
    def auto_scroll(self, value: Optional[bool]):
        self._set_attr("autoScroll", value)
