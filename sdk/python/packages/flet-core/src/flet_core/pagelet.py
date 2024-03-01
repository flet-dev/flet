from typing import Any, Optional, Union

from flet_core.adaptive_control import AdaptiveControl
from flet_core.app_bar import AppBar
from flet_core.bottom_app_bar import BottomAppBar
from flet_core.constrained_control import ConstrainedControl
from flet_core.control import Control, OptionalNumber
from flet_core.cupertino_app_bar import CupertinoAppBar
from flet_core.cupertino_navigation_bar import CupertinoNavigationBar
from flet_core.floating_action_button import FloatingActionButton
from flet_core.navigation_bar import NavigationBar
from flet_core.navigation_drawer import NavigationDrawer
from flet_core.ref import Ref
from flet_core.types import (
    AnimationValue,
    FloatingActionButtonLocation,
    OffsetValue,
    ResponsiveNumber,
    RotateValue,
    ScaleValue,
)
from flet_core.utils import deprecated


class Pagelet(ConstrainedControl, AdaptiveControl):
    """
        Pagelet implements the basic Material Design visual layout structure.

        Use it for projects that require "page within a page" layouts with its own AppBar, BottomBar, Drawer, such as demos and galleries.

        Example:
        ```
    import flet as ft


    def main(page: ft.Page):
        page.add(
            ft.Pagelet(
                appbar=ft.CupertinoAppBar(middle=ft.Text("AppBar title")),
                content=ft.Text("This is pagelet"),
            )
        )


    ft.app(target=main)
        ```

        -----

        Online docs: https://flet.dev/docs/controls/pagelet
    """

    def __init__(
        self,
        content: Optional[Control] = None,
        appbar: Union[AppBar, CupertinoAppBar, None] = None,
        navigation_bar: Union[NavigationBar, CupertinoNavigationBar, None] = None,
        bottom_app_bar: Optional[BottomAppBar] = None,
        bottom_sheet: Optional[Control] = None,
        drawer: Optional[NavigationDrawer] = None,
        end_drawer: Optional[NavigationDrawer] = None,
        floating_action_button: Optional[FloatingActionButton] = None,
        floating_action_button_location: Union[
            FloatingActionButtonLocation, OffsetValue
        ] = None,
        bgcolor: Optional[str] = None,
        #
        # ConstrainedControl
        #
        ref: Optional[Ref] = None,
        width: OptionalNumber = None,
        height: OptionalNumber = None,
        left: OptionalNumber = None,
        top: OptionalNumber = None,
        right: OptionalNumber = None,
        bottom: OptionalNumber = None,
        expand: Union[None, bool, int] = None,
        expand_loose: Optional[bool] = None,
        col: Optional[ResponsiveNumber] = None,
        opacity: OptionalNumber = None,
        rotate: RotateValue = None,
        scale: ScaleValue = None,
        offset: OffsetValue = None,
        aspect_ratio: OptionalNumber = None,
        animate_opacity: AnimationValue = None,
        animate_size: AnimationValue = None,
        animate_position: AnimationValue = None,
        animate_rotation: AnimationValue = None,
        animate_scale: AnimationValue = None,
        animate_offset: AnimationValue = None,
        on_animation_end=None,
        tooltip: Optional[str] = None,
        visible: Optional[bool] = None,
        disabled: Optional[bool] = None,
        data: Any = None,
        key: Optional[str] = None,
        #
        # AdaptiveControl
        #
        adaptive: Optional[bool] = None,
    ):
        ConstrainedControl.__init__(
            self,
            ref=ref,
            key=key,
            width=width,
            height=height,
            left=left,
            top=top,
            right=right,
            bottom=bottom,
            expand=expand,
            expand_loose=expand_loose,
            col=col,
            opacity=opacity,
            rotate=rotate,
            scale=scale,
            offset=offset,
            aspect_ratio=aspect_ratio,
            animate_opacity=animate_opacity,
            animate_size=animate_size,
            animate_position=animate_position,
            animate_rotation=animate_rotation,
            animate_scale=animate_scale,
            animate_offset=animate_offset,
            on_animation_end=on_animation_end,
            tooltip=tooltip,
            visible=visible,
            disabled=disabled,
            data=data,
        )

        AdaptiveControl.__init__(self, adaptive=adaptive)

        self.content = content
        self.appbar = appbar
        self.bgcolor = bgcolor
        self.navigation_bar = navigation_bar
        self.bottom_appbar = bottom_app_bar
        self.bottom_sheet = bottom_sheet
        self.drawer = drawer
        self.end_drawer = end_drawer
        self.floating_action_button = floating_action_button
        self.floating_action_button_location = floating_action_button_location

    def _get_control_name(self):
        return "pagelet"

    def _get_children(self):
        children = []
        if self.__appbar:
            self.__appbar._set_attr_internal("n", "appbar")
            children.append(self.__appbar)
        if self.__content:
            self.__content._set_attr_internal("n", "content")
            children.append(self.__content)
        if self.__navigation_bar:
            self.__navigation_bar._set_attr_internal("n", "navigationbar")
            children.append(self.__navigation_bar)
        if self.__bottom_appbar:
            self.__bottom_appbar._set_attr_internal("n", "bottomappbar")
            children.append(self.__bottom_appbar)
        if self.__bottom_sheet:
            self.__bottom_sheet._set_attr_internal("n", "bottomsheet")
            children.append(self.__bottom_sheet)
        if self.__drawer:
            self.__drawer._set_attr_internal("n", "drawer")
            children.append(self.__drawer)
        if self.__end_drawer:
            self.__end_drawer._set_attr_internal("n", "enddrawer")
            children.append(self.__end_drawer)
        if self.__floating_action_button:
            self.__floating_action_button._set_attr_internal(
                "n", "floatingactionbutton"
            )
            children.append(self.__floating_action_button)
        return children

    # Drawer
    #
    def show_drawer(self, drawer: NavigationDrawer):
        self.drawer = drawer
        self.drawer.open = True
        self.update()

    @deprecated(
        reason="Use show_drawer() method instead.",
        version="0.21.0",
        delete_version="1.0",
    )
    async def show_drawer_async(self, drawer: NavigationDrawer):
        self.show_drawer(drawer)

    def close_drawer(self):
        if self.drawer is not None:
            self.drawer.open = False
            self.update()

    @deprecated(
        reason="Use close_end_drawer() method instead.",
        version="0.21.0",
        delete_version="1.0",
    )
    async def close_drawer_async(self):
        self.close_end_drawer()

    # End_drawer
    #
    def show_end_drawer(self, end_drawer: NavigationDrawer):
        self.end_drawer = end_drawer
        self.end_drawer.open = True
        self.update()

    @deprecated(
        reason="Use show_end_drawer() method instead.",
        version="0.21.0",
        delete_version="1.0",
    )
    async def show_end_drawer_async(self, end_drawer: NavigationDrawer):
        self.show_end_drawer(end_drawer)

    def close_end_drawer(self):
        if self.end_drawer is not None:
            self.end_drawer.open = False
            self.update()

    @deprecated(
        reason="Use close_end_drawer() method instead.",
        version="0.21.0",
        delete_version="1.0",
    )
    async def close_end_drawer_async(self):
        self.close_end_drawer()

    # appbar
    @property
    def appbar(self) -> Union[AppBar, CupertinoAppBar, None]:
        return self.__appbar

    @appbar.setter
    def appbar(self, value: Union[AppBar, CupertinoAppBar, None]):
        self.__appbar = value

    # content
    @property
    def content(self) -> Optional[Control]:
        return self.__content

    @content.setter
    def content(self, value: Optional[Control]):
        self.__content = value

    # bgcolor
    @property
    def bgcolor(self):
        return self._get_attr("bgcolor")

    @bgcolor.setter
    def bgcolor(self, value):
        self._set_attr("bgcolor", value)

    # bottom_appbar
    @property
    def bottom_appbar(self) -> Optional[BottomAppBar]:
        return self.__bottom_appbar

    @bottom_appbar.setter
    def bottom_appbar(self, value: Optional[BottomAppBar]):
        self.__bottom_appbar = value

    # navigation_bar
    @property
    def navigation_bar(self) -> Union[NavigationBar, CupertinoNavigationBar, None]:
        return self.__navigation_bar

    @navigation_bar.setter
    def navigation_bar(
        self,
        value: Union[NavigationBar, CupertinoNavigationBar, None],
    ):
        self.__navigation_bar = value

    # bottom_sheet
    @property
    def bottom_sheet(self) -> Optional[Control]:
        return self.__bottom_sheet

    @bottom_sheet.setter
    def bottom_sheet(
        self,
        value: Optional[Control],
    ):
        self.__bottom_sheet = value

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

    # floating_action_button
    @property
    def floating_action_button(self) -> Optional[FloatingActionButton]:
        return self.__floating_action_button

    @floating_action_button.setter
    def floating_action_button(self, value: Optional[FloatingActionButton]):
        self.__floating_action_button = value

    # floating_action_button_location
    @property
    def floating_action_button_location(
        self,
    ) -> Union[FloatingActionButtonLocation, OffsetValue]:
        return self.__floating_action_button_location

    @floating_action_button_location.setter
    def floating_action_button_location(
        self, value: Union[FloatingActionButtonLocation, OffsetValue]
    ):
        self.__floating_action_button_location = value
        self._set_attr(
            "floatingActionButtonLocation",
            value.value if isinstance(value, FloatingActionButtonLocation) else value,
        )
