from typing import Any, List, Optional, Union

from flet_core.border import Border
from flet_core.constrained_control import ConstrainedControl
from flet_core.navigation_bar import NavigationBarDestination
from flet_core.ref import Ref
from flet_core.types import (
    AnimationValue,
    OffsetValue,
    OptionalNumber,
    ResponsiveNumber,
    RotateValue,
    ScaleValue,
    OptionalControlEventCallable,
)


class CupertinoNavigationBar(ConstrainedControl):
    """
    An iOS-styled bottom navigation tab bar.

    Navigation bars offer a persistent and convenient way to switch between primary destinations in an app.

    Example:

    ```
    import flet as ft

    def main(page: ft.Page):
        page.title = "CupertinoNavigationBar Example"
        page.navigation_bar = ft.CupertinoNavigationBar(
            bgcolor=ft.colors.AMBER_100,
            inactive_color=ft.colors.GREY,
            active_color=ft.colors.BLACK,
            on_change=lambda e: print("Selected tab:", e.control.selected_index),
            destinations=[
                ft.NavigationBarDestination(icon=ft.icons.EXPLORE, label="Explore"),
                ft.NavigationBarDestination(icon=ft.icons.COMMUTE, label="Commute"),
                ft.NavigationBarDestination(
                    icon=ft.icons.BOOKMARK_BORDER,
                    selected_icon=ft.icons.BOOKMARK,
                    label="Explore",
                ),
            ]
        )
        page.add(ft.SafeArea(ft.Text("Body!")))


    ft.app(target=main)
    ```

    -----

    Online docs: https://flet.dev/docs/controls/cupertinonavigationbar
    """

    def __init__(
        self,
        destinations: Optional[List[NavigationBarDestination]] = None,
        selected_index: Optional[int] = None,
        bgcolor: Optional[str] = None,
        active_color: Optional[str] = None,
        inactive_color: Optional[str] = None,
        border: Optional[Border] = None,
        icon_size: OptionalNumber = None,
        on_change: OptionalControlEventCallable = None,
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
        on_animation_end: OptionalControlEventCallable = None,
        visible: Optional[bool] = None,
        disabled: Optional[bool] = None,
        data: Any = None,
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
        self.active_color = active_color
        self.inactive_color = inactive_color
        self.border = border
        self.icon_size = icon_size
        self.on_change = on_change

    def _get_control_name(self):
        return "cupertinonavigationbar"

    def before_update(self) -> None:
        super().before_update()
        self._set_attr_json("border", self.__border)

    def _get_children(self):
        return self.__destinations

    # destinations
    @property
    def destinations(self) -> Optional[List[NavigationBarDestination]]:
        return self.__destinations

    @destinations.setter
    def destinations(self, value: Optional[List[NavigationBarDestination]]):
        self.__destinations = value if value else []

    # border
    @property
    def border(self) -> Optional[Border]:
        return self.__border

    @border.setter
    def border(self, value: Optional[Border]):
        self.__border = value

    # selected_index
    @property
    def selected_index(self) -> int:
        return self._get_attr("selectedIndex", data_type="int", def_value=0)

    @selected_index.setter
    def selected_index(self, value: Optional[int]):
        self._set_attr("selectedIndex", value)

    # bgcolor
    @property
    def bgcolor(self) -> Optional[str]:
        return self._get_attr("bgcolor")

    @bgcolor.setter
    def bgcolor(self, value: Optional[str]):
        self._set_attr("bgcolor", value)

    # active_color
    @property
    def active_color(self) -> Optional[str]:
        return self._get_attr("activeColor")

    @active_color.setter
    def active_color(self, value: Optional[str]):
        self._set_attr("activeColor", value)

    # inactive_color
    @property
    def inactive_color(self) -> Optional[str]:
        return self._get_attr("inactiveColor")

    @inactive_color.setter
    def inactive_color(self, value: Optional[str]):
        self._set_attr("inactiveColor", value)

    # icon_size
    @property
    def icon_size(self) -> OptionalNumber:
        return self._get_attr("iconSize")

    @icon_size.setter
    def icon_size(self, value: OptionalNumber):
        self._set_attr("iconSize", value)

    # on_change
    @property
    def on_change(self) -> OptionalControlEventCallable:
        return self._get_event_handler("change")

    @on_change.setter
    def on_change(self, handler: OptionalControlEventCallable):
        self._add_event_handler("change", handler)
