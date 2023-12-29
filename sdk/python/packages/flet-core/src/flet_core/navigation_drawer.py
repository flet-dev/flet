from typing import Any, List, Optional

from flet_core.buttons import OutlinedBorder
from flet_core.control import Control, OptionalNumber
from flet_core.ref import Ref
from flet_core.types import PaddingValue


class NavigationDrawerDestination(Control):
    """
    Displays an icon with a label, for use in NavigationDrawer destinations.

    """

    def __init__(
        self,
        ref: Optional[Ref] = None,
        # bgcolor: Optional[str] = None,
        icon: Optional[str] = None,
        icon_content: Optional[Control] = None,
        label: Optional[str] = None,
        selected_icon: Optional[str] = None,
        selected_icon_content: Optional[Control] = None,
    ):
        Control.__init__(self, ref=ref)
        self.label = label
        # self.bgcolor = bgcolor
        self.icon = icon
        self.__icon_content: Optional[Control] = None
        self.icon_content = icon_content
        self.selected_icon = selected_icon
        self.__selected_icon_content: Optional[Control] = None
        self.selected_icon_content = selected_icon_content

    def _get_control_name(self):
        return "navigationdrawerdestination"

    def _get_children(self):
        children = []
        if self.__icon_content:
            self.__icon_content._set_attr_internal("n", "icon_content")
            children.append(self.__icon_content)
        if self.__selected_icon_content:
            self.__selected_icon_content._set_attr_internal(
                "n", "selected_icon_content"
            )
            children.append(self.__selected_icon_content)
        return children

    # # bgcolor
    # @property
    # def bgcolor(self):
    #     return self._get_attr("bgColor")

    # @bgcolor.setter
    # def bgcolor(self, value):
    #     self._set_attr("bgColor", value)

    # icon
    @property
    def icon(self):
        return self._get_attr("icon")

    @icon.setter
    def icon(self, value):
        self._set_attr("icon", value)

    # icon_content
    @property
    def icon_content(self) -> Optional[Control]:
        return self.__icon_content

    @icon_content.setter
    def icon_content(self, value: Optional[Control]):
        self.__icon_content = value

    # selected_icon
    @property
    def selected_icon(self):
        return self._get_attr("selectedIcon")

    @selected_icon.setter
    def selected_icon(self, value):
        self._set_attr("selectedIcon", value)

    # selected_icon_content
    @property
    def selected_icon_content(self) -> Optional[Control]:
        return self.__selected_icon_content

    @selected_icon_content.setter
    def selected_icon_content(self, value: Optional[Control]):
        self.__selected_icon_content = value

    # label
    @property
    def label(self):
        return self._get_attr("label")

    @label.setter
    def label(self, value):
        self._set_attr("label", value)


class NavigationDrawer(Control):
    """
    Material Design Navigation Drawer component.

    Navigation Drawer is a panel slides in horizontally from the left or right edge of a page to show primary destinations in an app.

    Example:

    ```
    import flet as ft


    def main(page: ft.Page):
        def item_selected_left(e):
            print(e.control.selected_index)

        page.drawer = ft.NavigationDrawer(
            elevation=40,
            indicator_color=ft.colors.GREEN_200,
            indicator_shape=ft.StadiumBorder(),
            shadow_color=ft.colors.GREEN_900,
            surface_tint_color=ft.colors.GREEN,
            selected_index=-1,
            on_change=item_selected_left,
            controls=[
                ft.Container(height=12),
                ft.NavigationDrawerDestination(
                    label="Item 1",
                    icon=ft.icons.ABC,
                    selected_icon_content=ft.Icon(ft.icons.ACCESS_ALARM),
                ),
                ft.Divider(thickness=2),
                ft.NavigationDrawerDestination(
                    icon_content=ft.Icon(ft.icons.MAIL),
                    label="Item 2",
                    selected_icon=ft.icons.PHISHING,
                ),
                ft.NavigationDrawerDestination(
                    icon_content=ft.Icon(ft.icons.PHONE),
                    label="Item 3",
                    selected_icon=ft.icons.PHISHING,
                ),
            ],
        )

        end_drawer = ft.NavigationDrawer(
            controls=[
                ft.NavigationDrawerDestination(
                    icon=ft.icons.ADD_TO_HOME_SCREEN_SHARP, label="Item 1"
                ),
                ft.NavigationDrawerDestination(icon=ft.icons.ADD_COMMENT, label="Item 2"),
            ],
        )

        def show_drawer(e):
            page.drawer.open = True
            page.drawer.update()

        def show_end_drawer(e):
            page.show_end_drawer(end_drawer)

        page.add(
            ft.Row(
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                controls=[
                    ft.ElevatedButton("Show drawer", on_click=show_drawer),
                    ft.ElevatedButton("Show end drawer", on_click=show_end_drawer),
                ],
            )
        )


    ft.app(main)

    ```

    -----

    Online docs: https://flet.dev/docs/controls/navigationdrawer
    """

    def __init__(
        self,
        ref: Optional[Ref] = None,
        disabled: Optional[bool] = None,
        visible: Optional[bool] = None,
        data: Any = None,
        #
        # NavigationDrawer-specific
        #
        open: bool = False,
        controls: Optional[List[Control]] = None,
        selected_index: Optional[int] = None,
        bgcolor: Optional[str] = None,
        elevation: OptionalNumber = None,
        indicator_color: Optional[str] = None,
        indicator_shape: Optional[OutlinedBorder] = None,
        shadow_color: Optional[str] = None,
        surface_tint_color: Optional[str] = None,
        tile_padding: PaddingValue = None,
        on_change=None,
        on_dismiss=None,
    ):
        Control.__init__(
            self,
            ref=ref,
            visible=visible,
            disabled=disabled,
            data=data,
        )

        self.open = open
        self.controls = controls
        self.selected_index = selected_index
        self.bgcolor = bgcolor
        self.elevation = elevation
        self.indicator_color = indicator_color
        self.indicator_shape = indicator_shape
        self.shadow_color = shadow_color
        self.surface_tint_color = surface_tint_color
        self.tile_padding = tile_padding

        self.on_change = on_change
        self.on_dismiss = on_dismiss

    def _get_control_name(self):
        return "navigationdrawer"

    def _before_build_command(self):
        super()._before_build_command()
        self._set_attr_json("indicatorShape", self.__indicator_shape)
        self._set_attr_json("tilePadding", self.__tile_padding)

    def _get_children(self):
        children = []
        children.extend(self.__controls)
        return children

    # open
    @property
    def open(self) -> Optional[bool]:
        return self._get_attr("open", data_type="bool", def_value=False)

    @open.setter
    def open(self, value: Optional[bool]):
        self._set_attr("open", value)

    # controls
    @property
    def controls(self) -> Optional[List[Control]]:
        return self.__controls

    @controls.setter
    def controls(self, value: Optional[List[Control]]):
        self.__controls = value if value is not None else []

    # selected_index
    @property
    def selected_index(self) -> Optional[int]:
        return self._get_attr("selectedIndex", data_type="int", def_value=0)

    @selected_index.setter
    def selected_index(self, value: Optional[int]):
        self._set_attr("selectedIndex", value)

    # bgcolor
    @property
    def bgcolor(self):
        return self._get_attr("bgcolor")

    @bgcolor.setter
    def bgcolor(self, value):
        self._set_attr("bgcolor", value)

    # elevation
    @property
    def elevation(self) -> OptionalNumber:
        return self._get_attr("elevation")

    @elevation.setter
    def elevation(self, value: OptionalNumber):
        self._set_attr("elevation", value)

    # indicator_color
    @property
    def indicator_color(self):
        return self._get_attr("indicatorColor")

    @indicator_color.setter
    def indicator_color(self, value):
        self._set_attr("indicatorColor", value)

    # indicator_shape
    @property
    def indicator_shape(self) -> Optional[OutlinedBorder]:
        return self.__indicator_shape

    @indicator_shape.setter
    def indicator_shape(self, value: Optional[OutlinedBorder]):
        self.__indicator_shape = value

    # shadow_color
    @property
    def shadow_color(self):
        return self._get_attr("shadowColor")

    @shadow_color.setter
    def shadow_color(self, value):
        self._set_attr("shadowColor", value)

    # surface_tint_color
    @property
    def surface_tint_color(self):
        return self._get_attr("surfaceTintColor")

    @surface_tint_color.setter
    def surface_tint_color(self, value):
        self._set_attr("surfaceTintColor", value)

    # tile_padding
    @property
    def tile_padding(self) -> PaddingValue:
        return self.__tile_padding

    @tile_padding.setter
    def tile_padding(self, value: PaddingValue):
        self.__tile_padding = value

    # on_change
    @property
    def on_change(self):
        return self._get_event_handler("change")

    @on_change.setter
    def on_change(self, handler):
        self._add_event_handler("change", handler)

    # on_dismiss
    @property
    def on_dismiss(self):
        return self._get_event_handler("dismiss")

    @on_dismiss.setter
    def on_dismiss(self, handler):
        self._add_event_handler("dismiss", handler)
