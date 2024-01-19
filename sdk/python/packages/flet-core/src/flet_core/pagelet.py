from typing import Any, Optional, Union

from flet_core.app_bar import AppBar
from flet_core.bottom_app_bar import BottomAppBar
from flet_core.constrained_control import ConstrainedControl
from flet_core.control import Control, OptionalNumber
from flet_core.cupertino_app_bar import CupertinoAppBar
from flet_core.cupertino_navigation_bar import CupertinoNavigationBar
from flet_core.navigation_bar import NavigationBar
from flet_core.ref import Ref
from flet_core.types import (
    AnimationValue,
    OffsetValue,
    ResponsiveNumber,
    RotateValue,
    ScaleValue,
)


class Pagelet(ConstrainedControl):
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
        ref: Optional[Ref] = None,
        width: OptionalNumber = None,
        height: OptionalNumber = None,
        left: OptionalNumber = None,
        top: OptionalNumber = None,
        right: OptionalNumber = None,
        bottom: OptionalNumber = None,
        expand: Union[None, bool, int] = None,
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
        # Specific
        #
        content: Optional[Control] = None,
        appbar: Union[AppBar, CupertinoAppBar, None] = None,
        navigation_bar: Union[NavigationBar, CupertinoNavigationBar, None] = None,
        bottom_app_bar: Optional[BottomAppBar] = None,
        bottom_sheet: Optional[Control] = None,
        bgcolor: Optional[str] = None,
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

        self.content = content
        self.appbar = appbar
        self.bgcolor = bgcolor
        self.navigation_bar = navigation_bar
        self.bottom_appbar = bottom_app_bar
        self.bottom_sheet = bottom_sheet

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
        return children

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
