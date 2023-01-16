from typing import List, Optional

from flet_core import Control
from flet_core.app_bar import AppBar
from flet_core.control import OptionalNumber
from flet_core.floating_action_button import FloatingActionButton
from flet_core.navigation_bar import NavigationBar
from flet_core.types import (
    CrossAxisAlignment,
    CrossAxisAlignmentString,
    MainAxisAlignment,
    MainAxisAlignmentString,
    PaddingValue,
    ScrollMode,
    ScrollModeString,
)


class View(Control):
    """
    View is the top most container for all other controls.

    A root view is automatically created when a new user session started. From layout perspective the View represents a `Column`(https://flet.dev/docs/controls/column/) control, so it has a similar behavior and shares same properties.

    -----

    Online docs: https://flet.dev/docs/controls/view
    """

    def __init__(
        self,
        route: Optional[str] = None,
        controls: Optional[List[Control]] = None,
        appbar: Optional[AppBar] = None,
        floating_action_button: Optional[FloatingActionButton] = None,
        navigation_bar: Optional[NavigationBar] = None,
        vertical_alignment: MainAxisAlignment = MainAxisAlignment.NONE,
        horizontal_alignment: CrossAxisAlignment = CrossAxisAlignment.NONE,
        spacing: OptionalNumber = None,
        padding: PaddingValue = None,
        bgcolor: Optional[str] = None,
        scroll: Optional[ScrollMode] = None,
        auto_scroll: Optional[bool] = None,
    ):
        Control.__init__(self)

        self.controls = controls if controls is not None else []
        self.route = route
        self.appbar = appbar
        self.navigation_bar = navigation_bar
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
        super()._before_build_command()
        self._set_attr_json("padding", self.__padding)

    def _get_children(self):
        children = []
        if self.__appbar:
            children.append(self.__appbar)
        if self.__fab:
            children.append(self.__fab)
        if self.__navigation_bar:
            children.append(self.__navigation_bar)
        children.extend(self.__controls)
        return children

    # route
    @property
    def route(self):
        return self._get_attr("route")

    @route.setter
    def route(self, value):
        self._set_attr("route", value)

    # controls
    @property
    def controls(self) -> List[Control]:
        return self.__controls

    @controls.setter
    def controls(self, value: List[Control]):
        self.__controls = value

    # appbar
    @property
    def appbar(self) -> Optional[AppBar]:
        return self.__appbar

    @appbar.setter
    def appbar(self, value: Optional[AppBar]):
        self.__appbar = value

    # floating_action_button
    @property
    def floating_action_button(self) -> Optional[FloatingActionButton]:
        return self.__fab

    @floating_action_button.setter
    def floating_action_button(self, value: Optional[FloatingActionButton]):
        self.__fab = value

    # navigation_bar
    @property
    def navigation_bar(self) -> Optional[NavigationBar]:
        return self.__navigation_bar

    @navigation_bar.setter
    def navigation_bar(self, value: Optional[NavigationBar]):
        self.__navigation_bar = value

    # horizontal_alignment
    @property
    def horizontal_alignment(self) -> CrossAxisAlignment:
        return self.__horizontal_alignment

    @horizontal_alignment.setter
    def horizontal_alignment(self, value: CrossAxisAlignment):
        self.__horizontal_alignment = value
        if isinstance(value, CrossAxisAlignment):
            self._set_attr("horizontalAlignment", value.value)
        else:
            self.__set_horizontal_alignment(value)

    def __set_horizontal_alignment(self, value: CrossAxisAlignmentString):
        self._set_attr("horizontalAlignment", value)

    # vertical_alignment
    @property
    def vertical_alignment(self) -> MainAxisAlignment:
        return self.__vertical_alignment

    @vertical_alignment.setter
    def vertical_alignment(self, value: MainAxisAlignment):
        self.__vertical_alignment = value
        if isinstance(value, MainAxisAlignment):
            self._set_attr("verticalAlignment", value.value)
        else:
            self.__set_vertical_alignment(value)

    def __set_vertical_alignment(self, value: MainAxisAlignmentString):
        self._set_attr("verticalAlignment", value)

    # spacing
    @property
    def spacing(self) -> OptionalNumber:
        return self._get_attr("spacing")

    @spacing.setter
    def spacing(self, value: OptionalNumber):
        self._set_attr("spacing", value)

    # padding
    @property
    def padding(self) -> PaddingValue:
        return self.__padding

    @padding.setter
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
    def scroll(self) -> Optional[ScrollMode]:
        return self.__scroll

    @scroll.setter
    def scroll(self, value: Optional[ScrollMode]):
        self.__scroll = value
        if isinstance(value, ScrollMode):
            self._set_attr("scroll", value.value)
        else:
            self.__set_scroll(value)

    def __set_scroll(self, value: Optional[ScrollModeString]):
        if value == True:
            value = "auto"
        elif value == False:
            value = None
        self._set_attr("scroll", value)

    # auto_scroll
    @property
    def auto_scroll(self) -> Optional[bool]:
        return self._get_attr("autoScroll")

    @auto_scroll.setter
    def auto_scroll(self, value: Optional[bool]):
        self._set_attr("autoScroll", value)
