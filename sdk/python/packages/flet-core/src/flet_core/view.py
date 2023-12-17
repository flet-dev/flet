from typing import Any, List, Optional, Union

from flet_core import Control
from flet_core.app_bar import AppBar
from flet_core.bottom_app_bar import BottomAppBar
from flet_core.control import OptionalNumber
from flet_core.floating_action_button import (
    FloatingActionButton,
    FloatingActionButtonLocation,
)
from flet_core.navigation_bar import NavigationBar
from flet_core.cupertino_navigation_bar import CupertinoNavigationBar
from flet_core.navigation_drawer import NavigationDrawer
from flet_core.scrollable_control import ScrollableControl
from flet_core.types import (
    CrossAxisAlignment,
    CrossAxisAlignmentString,
    MainAxisAlignment,
    MainAxisAlignmentString,
    PaddingValue,
    ScrollMode,
)


class View(ScrollableControl):
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
        bottom_appbar: Optional[BottomAppBar] = None,
        floating_action_button: Optional[FloatingActionButton] = None,
        floating_action_button_location: Optional[FloatingActionButtonLocation] = None,
        navigation_bar: Union[NavigationBar, CupertinoNavigationBar, None] = None,
        drawer: Optional[NavigationDrawer] = None,
        end_drawer: Optional[NavigationDrawer] = None,
        vertical_alignment: MainAxisAlignment = MainAxisAlignment.NONE,
        horizontal_alignment: CrossAxisAlignment = CrossAxisAlignment.NONE,
        spacing: OptionalNumber = None,
        padding: PaddingValue = None,
        bgcolor: Optional[str] = None,
        #
        # ScrollableControl specific
        #
        scroll: Optional[ScrollMode] = None,
        auto_scroll: Optional[bool] = None,
        fullscreen_dialog: Optional[bool] = None,
        on_scroll_interval: OptionalNumber = None,
        on_scroll: Any = None,
    ):
        Control.__init__(self)

        ScrollableControl.__init__(
            self,
            scroll=scroll,
            auto_scroll=auto_scroll,
            on_scroll_interval=on_scroll_interval,
            on_scroll=on_scroll,
        )

        self.controls = controls if controls is not None else []
        self.route = route
        self.appbar = appbar
        self.bottom_appbar = bottom_appbar
        self.navigation_bar = navigation_bar
        self.drawer = drawer
        self.end_drawer = end_drawer
        self.floating_action_button = floating_action_button
        self.floating_action_button_location = floating_action_button_location
        self.vertical_alignment = vertical_alignment
        self.horizontal_alignment = horizontal_alignment
        self.spacing = spacing
        self.padding = padding
        self.bgcolor = bgcolor
        self.scroll = scroll
        self.auto_scroll = auto_scroll
        self.fullscreen_dialog = fullscreen_dialog

    def _get_control_name(self):
        return "view"

    def _before_build_command(self):
        super()._before_build_command()
        self._set_attr_json("padding", self.__padding)

    def _get_children(self):
        children = []
        if self.__appbar:
            children.append(self.__appbar)
        if self.__bottom_appbar:
            children.append(self.__bottom_appbar)
        if self.__fab:
            children.append(self.__fab)
        if self.__navigation_bar:
            children.append(self.__navigation_bar)
        if self.__drawer:
            self.__drawer._set_attr_internal("n", "start")
            children.append(self.__drawer)
        if self.__end_drawer:
            self.__end_drawer._set_attr_internal("n", "end")
            children.append(self.__end_drawer)
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

    # bottom_appbar
    @property
    def bottom_appbar(self) -> Optional[BottomAppBar]:
        return self.__bottom_appbar

    @bottom_appbar.setter
    def bottom_appbar(self, value: Optional[BottomAppBar]):
        self.__bottom_appbar = value

    # floating_action_button
    @property
    def floating_action_button(self) -> Optional[FloatingActionButton]:
        return self.__fab

    @floating_action_button.setter
    def floating_action_button(self, value: Optional[FloatingActionButton]):
        self.__fab = value

    # floating_action_button_location
    @property
    def floating_action_button_location(self) -> FloatingActionButtonLocation:
        return self.__floating_action_button_location

    @floating_action_button_location.setter
    def floating_action_button_location(self, value: FloatingActionButtonLocation):
        self.__floating_action_button_location = value
        self._set_attr(
            "floatingActionButtonLocation",
            value.value if isinstance(value, FloatingActionButtonLocation) else value,
        )

    # navigation_bar
    @property
    def navigation_bar(self) -> Union[NavigationBar, CupertinoNavigationBar, None]:
        return self.__navigation_bar

    @navigation_bar.setter
    def navigation_bar(self, value: Union[NavigationBar, CupertinoNavigationBar, None]):
        self.__navigation_bar = value

    # drawer
    @property
    def drawer(self) -> Optional[NavigationDrawer]:
        return self.__drawer

    @drawer.setter
    def drawer(self, value: Optional[NavigationDrawer]):
        self.__drawer = value

    # end_drawer
    @property
    def end_drawer(self) -> Optional[NavigationDrawer]:
        return self.__end_drawer

    @end_drawer.setter
    def end_drawer(self, value: Optional[NavigationDrawer]):
        self.__end_drawer = value

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

    # fullscreen_dialog
    @property
    def fullscreen_dialog(self) -> Optional[bool]:
        return self._get_attr("fullscreenDialog", data_type="bool", def_value=False)

    @fullscreen_dialog.setter
    def fullscreen_dialog(self, value: Optional[bool]):
        self._set_attr("fullscreenDialog", value)
