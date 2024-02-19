from typing import Any, List, Optional, Union

from flet_core.border import Border
from flet_core.constrained_control import ConstrainedControl
from flet_core.control import OptionalNumber
from flet_core.navigation_bar import NavigationDestination
from flet_core.ref import Ref
from flet_core.types import (
    AnimationValue,
    BorderRadiusValue,
    OffsetValue,
    ResponsiveNumber,
    RotateValue,
    ScaleValue,
    MainAxisAlignment,
)


class GoogleNavigationBar(ConstrainedControl):
    """
    An iOS-styled bottom navigation tab bar.

    Navigation bars offer a persistent and convenient way to switch between primary destinations in an app.

    Example:

    ```
    import flet as ft

    def main(page: ft.Page):
        page.theme_mode = ft.ThemeMode.DARK
        page.title = "GoogleNavigationBar Example"
        page.navigation_bar = ft.GoogleNavigationBar(
            alignment=ft.MainAxisAlignment.CENTER,
            color=ft.colors.GREY_700,
            icon_active_color=ft.colors.WHITE,
            active_color=ft.colors.WHITE,
            bg_active_color=ft.colors.GREY_800,
            border_radius=80,
            # active_border=ft.border.all(1, ft.colors.BLUE_200),
            on_change=lambda e: print("Selected tab:", e.control.selected_index),
            destinations=[
                ft.NavigationDestination(icon=ft.icons.HOME_OUTLINED, label="Home"),
                ft.NavigationDestination(icon=ft.icons.SEARCH_OUTLINED, label="Search"),
                ft.NavigationDestination(icon=ft.icons.BOOKMARK_OUTLINE, label="Bookmark"),
                ft.NavigationDestination(icon=ft.icons.PERSON_OUTLINED, label="Person"),
            ],
        )
        page.add(ft.SafeArea(ft.Text("Hello World!")))


    ft.app(target=main)

    ```

    -----

    Online docs: https://flet.dev/docs/controls/googlenavigationbar
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
        visible: Optional[bool] = None,
        disabled: Optional[bool] = None,
        data: Any = None,
        #
        # Specific
        #
        destinations: Optional[List[NavigationDestination]] = None,
        selected_index: Optional[int] = None,
        bgcolor: Optional[str] = None,
        color: Optional[str] = None,
        active_color: Optional[str] = None,
        bg_active_color: Optional[str] = None,
        inactive_color: Optional[str] = None,
        icon_active_color: Optional[str] = None,
        border: Optional[Border] = None,
        active_border: Optional[Border] = None,
        icon_size: OptionalNumber = None,
        on_change=None,
        border_radius: BorderRadiusValue = None,
        alignment: MainAxisAlignment = MainAxisAlignment.NONE,
    ):
        ConstrainedControl.__init__(
            self,
            ref=ref,
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
            visible=visible,
            disabled=disabled,
            data=data,
        )

        self.destinations = destinations
        self.selected_index = selected_index
        self.bgcolor = bgcolor
        self.color = color
        self.active_color = active_color
        self.bg_active_color = bg_active_color
        self.inactive_color = inactive_color
        self.icon_active_color = icon_active_color
        self.border = border
        self.active_border = active_border
        self.border_radius = border_radius
        self.icon_size = icon_size
        self.on_change = on_change
        self.alignment = alignment

    def _get_control_name(self):
        return "googlenavigationbar"

    def _before_build_command(self):
        super()._before_build_command()
        self._set_attr_json("border", self.__border)
        self._set_attr_json("activeBorder", self.__active_border)
        self._set_attr_json("borderRadius", self.__border_radius)

    def _get_children(self):
        children = []
        children.extend(self.__destinations)
        return children

    # destinations
    @property
    def destinations(self) -> Optional[List[NavigationDestination]]:
        return self.__destinations

    @destinations.setter
    def destinations(self, value: Optional[List[NavigationDestination]]):
        self.__destinations = value if value is not None else []

    # border
    @property
    def border(self) -> Optional[Border]:
        return self.__border

    @border.setter
    def border(self, value: Optional[Border]):
        self.__border = value

    # active border
    @property
    def active_border(self) -> Optional[Border]:
        return self.__active_border

    @active_border.setter
    def active_border(self, value: Optional[Border]):
        self.__active_border = value

    # border_radius
    @property
    def border_radius(self) -> BorderRadiusValue:
        return self.__border_radius

    @border_radius.setter
    def border_radius(self, value: BorderRadiusValue):
        self.__border_radius = value

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

    # active_color
    @property
    def active_color(self):
        return self._get_attr("activeColor")

    @active_color.setter
    def active_color(self, value):
        self._set_attr("activeColor", value)

    # bg_active_color
    @property
    def bg_active_color(self):
        return self._get_attr("bgActiveColor")

    @bg_active_color.setter
    def bg_active_color(self, value):
        self._set_attr("bgActiveColor", value)

    # color
    @property
    def color(self):
        return self._get_attr("color")

    @color.setter
    def color(self, value):
        self._set_attr("color", value)

    # iconActiveColor
    @property
    def icon_active_color(self):
        return self._get_attr("iconActiveColor")

    @icon_active_color.setter
    def icon_active_color(self, value):
        self._set_attr("iconActiveColor", value)

    # icon_size
    @property
    def icon_size(self) -> OptionalNumber:
        return self._get_attr("iconSize")

    @icon_size.setter
    def icon_size(self, value: OptionalNumber):
        self._set_attr("iconSize", value)

    # on_change
    @property
    def on_change(self):
        return self._get_event_handler("change")

    @on_change.setter
    def on_change(self, handler):
        self._add_event_handler("change", handler)

    # alignment
    @property
    def alignment(self) -> MainAxisAlignment:
        return self.__alignment

    @alignment.setter
    def alignment(self, value: MainAxisAlignment):
        self.__alignment = value
        if isinstance(value, MainAxisAlignment):
            self._set_attr("alignment", value.value)
        else:
            self.__set_alignment(value)
