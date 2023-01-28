from typing import Any, List, Optional, Union

from flet_core.constrained_control import ConstrainedControl
from flet_core.control import Control, OptionalNumber
from flet_core.ref import Ref
from flet_core.types import (
    AnimationValue,
    OffsetValue,
    ResponsiveNumber,
    RotateValue,
    ScaleValue,
)


class Tab(Control):
    def __init__(
        self,
        text: Optional[str] = None,
        content: Optional[Control] = None,
        tab_content: Optional[Control] = None,
        ref: Optional[Ref] = None,
        icon: Optional[str] = None,
    ):
        Control.__init__(self, ref=ref)
        self.text = text
        self.icon = icon
        self.__content: Optional[Control] = None
        self.content = content
        self.__tab_content: Optional[Control] = None
        self.tab_content = tab_content

    def _get_control_name(self):
        return "tab"

    def _get_children(self):
        children = []
        if self.__tab_content:
            self.__tab_content._set_attr_internal("n", "tab_content")
            children.append(self.__tab_content)
        if self.__content:
            self.__content._set_attr_internal("n", "content")
            children.append(self.__content)
        return children

    # text
    @property
    def text(self):
        return self._get_attr("text")

    @text.setter
    def text(self, value):
        self._set_attr("text", value)

    # icon
    @property
    def icon(self):
        return self._get_attr("icon")

    @icon.setter
    def icon(self, value):
        self._set_attr("icon", value)

    # tab_content
    @property
    def tab_content(self):
        return self.__tab_content

    @tab_content.setter
    def tab_content(self, value):
        self.__tab_content = value

    # content
    @property
    def content(self):
        return self.__content

    @content.setter
    def content(self, value):
        self.__content = value


class Tabs(ConstrainedControl):
    """
    The Tabs control is used for navigating frequently accessed, distinct content categories. Tabs allow for navigation between two or more content views and relies on text headers to articulate the different sections of content.

    Example:
    ```
    import flet as ft


    def main(page: ft.Page):

        t = ft.Tabs(
            selected_index=1,
            animation_duration=300,
            tabs=[
                ft.Tab(
                    text="Tab 1",
                    content=ft.Container(
                        content=ft.Text("This is Tab 1"), alignment=ft.alignment.center
                    ),
                ),
                ft.Tab(
                    tab_content=ft.Icon(ft.icons.SEARCH),
                    content=ft.Text("This is Tab 2"),
                ),
                ft.Tab(
                    text="Tab 3",
                    icon=ft.icons.SETTINGS,
                    content=ft.Text("This is Tab 3"),
                ),
            ],
            expand=1,
        )

        page.add(t)


    ft.app(target=main)

    ```

    -----

    Online docs: https://flet.dev/docs/controls/tabs
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
        visible: Optional[bool] = None,
        disabled: Optional[bool] = None,
        data: Any = None,
        #
        # Tabs-specific
        tabs: Optional[List[Tab]] = None,
        selected_index: Optional[int] = None,
        scrollable: Optional[bool] = None,
        animation_duration: Optional[int] = None,
        on_change=None,
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

        self.tabs = tabs
        self.selected_index = selected_index
        self.scrollable = scrollable
        self.animation_duration = animation_duration
        self.on_change = on_change

    def _get_control_name(self):
        return "tabs"

    def _get_children(self):
        return self.__tabs

    # tabs
    @property
    def tabs(self) -> Optional[List[Tab]]:
        return self.__tabs

    @tabs.setter
    def tabs(self, value: Optional[List[Tab]]):
        self.__tabs = value if value is not None else []

    # on_change
    @property
    def on_change(self):
        return self._get_event_handler("change")

    @on_change.setter
    def on_change(self, handler):
        self._add_event_handler("change", handler)

    # selected_index
    @property
    def selected_index(self) -> Optional[int]:
        return self._get_attr("selectedIndex", data_type="int", def_value=0)

    @selected_index.setter
    def selected_index(self, value: Optional[int]):
        self._set_attr("selectedIndex", value)

    # scrollable
    @property
    def scrollable(self) -> Optional[bool]:
        return self._get_attr("scrollable", data_type="bool", def_value=True)

    @scrollable.setter
    def scrollable(self, value: Optional[bool]):
        self._set_attr("scrollable", value)

    # animation_duration
    @property
    def animation_duration(self) -> Optional[int]:
        return self._get_attr("animationDuration")

    @animation_duration.setter
    def animation_duration(self, value: Optional[int]):
        self._set_attr("animationDuration", value)
