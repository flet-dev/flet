from typing import Any, List, Optional

from flet_core.control import Control, OptionalNumber
from flet_core.ref import Ref
from flet_core.text_style import TextStyle
from flet_core.types import (
    PaddingValue,
    MarginValue,
    OptionalControlEventCallable,
)


class Banner(Control):
    """
    A banner displays an important, succinct message, and provides actions for users to address (or dismiss the banner). A user action is required for it to be dismissed.

    Banners are displayed at the top of the screen, below a top app bar. They are persistent and non-modal, allowing the user to either ignore them or interact with them at any time.

    Example:
    ```
    import flet as ft


    def main(page):
        page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

        def close_banner(e):
            page.close(banner)
            page.add(ft.Text("Action clicked: " + e.control.text))

        action_button_style = ft.ButtonStyle(color=ft.colors.BLUE)
        banner = ft.Banner(
            bgcolor=ft.colors.AMBER_100,
            leading=ft.Icon(ft.icons.WARNING_AMBER_ROUNDED, color=ft.colors.AMBER, size=40),
            content=ft.Text(
                value="Oops, there were some errors while trying to delete the file. What would you like me to do?",
                color=ft.colors.BLACK,
            ),
            actions=[
                ft.TextButton(text="Retry", style=action_button_style, on_click=close_banner),
                ft.TextButton(text="Ignore", style=action_button_style, on_click=close_banner),
                ft.TextButton(text="Cancel", style=action_button_style, on_click=close_banner),
            ],
        )

        page.add(ft.ElevatedButton("Show Banner", on_click=lambda e: page.open(banner)))


    ft.app(main)
    ```

    -----

    Online docs: https://flet.dev/docs/controls/banner
    """

    def __init__(
        self,
        content: Control,
        actions: List[Control],
        open: bool = False,
        leading: Optional[Control] = None,
        leading_padding: Optional[PaddingValue] = None,
        content_padding: Optional[PaddingValue] = None,
        force_actions_below: Optional[bool] = None,
        bgcolor: Optional[str] = None,
        surface_tint_color: Optional[str] = None,
        shadow_color: Optional[str] = None,
        divider_color: Optional[str] = None,
        elevation: OptionalNumber = None,
        margin: MarginValue = None,
        content_text_style: Optional[TextStyle] = None,
        on_visible: OptionalControlEventCallable = None,
        #
        # Control
        #
        ref: Optional[Ref] = None,
        disabled: Optional[bool] = None,
        visible: Optional[bool] = None,
        data: Any = None,
    ):

        Control.__init__(
            self,
            ref=ref,
            disabled=disabled,
            visible=visible,
            data=data,
        )

        self.open = open
        self.leading = leading
        self.leading_padding = leading_padding
        self.content = content
        self.content_padding = content_padding
        self.actions = actions
        self.force_actions_below = force_actions_below
        self.bgcolor = bgcolor
        self.surface_tint_color = surface_tint_color
        self.shadow_color = shadow_color
        self.divider_color = divider_color
        self.elevation = elevation
        self.margin = margin
        self.content_text_style = content_text_style
        self.on_visible = on_visible

    def _get_control_name(self):
        return "banner"

    def before_update(self):
        super().before_update()
        assert self.__content.visible, "content must be visible"
        assert any(
            a.visible for a in self.__actions
        ), "actions must contain at minimum one visible action Control"

        self._set_attr_json("contentPadding", self.__content_padding)
        self._set_attr_json("leadingPadding", self.__leading_padding)
        self._set_attr_json("margin", self.__margin)
        if isinstance(self.__content_text_style, TextStyle):
            self._set_attr_json("contentTextStyle", self.__content_text_style)

    def _get_children(self):
        self.__content._set_attr_internal("n", "content")
        for action in self.__actions:
            action._set_attr_internal("n", "action")
        children = [self.__content] + self.__actions
        if self.__leading:
            self.__leading._set_attr_internal("n", "leading")
            children.append(self.__leading)
        return children

    # open
    @property
    def open(self) -> bool:
        return self._get_attr("open", data_type="bool", def_value=False)

    @open.setter
    def open(self, value: Optional[bool]):
        self._set_attr("open", value)

    # modal
    @property
    def modal(self) -> bool:
        return self._get_attr("modal", data_type="bool", def_value=False)

    @modal.setter
    def modal(self, value: Optional[bool]):
        self._set_attr("modal", value)

    # leading
    @property
    def leading(self) -> Optional[Control]:
        return self.__leading

    @leading.setter
    def leading(self, value: Optional[Control]):
        self.__leading = value

    # leading_padding
    @property
    def leading_padding(self) -> PaddingValue:
        return self.__leading_padding

    @leading_padding.setter
    def leading_padding(self, value: PaddingValue):
        self.__leading_padding = value

    # content
    @property
    def content(self) -> Control:
        return self.__content

    @content.setter
    def content(self, value: Control):
        self.__content = value

    # content_padding
    @property
    def content_padding(self) -> PaddingValue:
        return self.__content_padding

    @content_padding.setter
    def content_padding(self, value: PaddingValue):
        self.__content_padding = value

    # margin
    @property
    def margin(self) -> MarginValue:
        return self.__margin

    @margin.setter
    def margin(self, value: MarginValue):
        self.__margin = value

    # actions
    @property
    def actions(self) -> List[Control]:
        return self.__actions

    @actions.setter
    def actions(self, value: List[Control]):
        self.__actions = value

    # force_actions_below
    @property
    def force_actions_below(self) -> bool:
        return self._get_attr("forceActionsBelow", data_type="bool", def_value=False)

    @force_actions_below.setter
    def force_actions_below(self, value: Optional[bool]):
        self._set_attr("forceActionsBelow", value)

    # bgcolor
    @property
    def bgcolor(self) -> Optional[str]:
        return self._get_attr("bgColor")

    @bgcolor.setter
    def bgcolor(self, value: Optional[str]):
        self._set_attr("bgColor", value)

    # content_text_style
    @property
    def content_text_style(self) -> Optional[TextStyle]:
        return self.__content_text_style

    @content_text_style.setter
    def content_text_style(self, value: Optional[TextStyle]):
        self.__content_text_style = value

    # shadow_color
    @property
    def shadow_color(self) -> Optional[str]:
        return self._get_attr("shadowColor")

    @shadow_color.setter
    def shadow_color(self, value: Optional[str]):
        self._set_attr("shadowColor", value)

    # surface_tint_color
    @property
    def surface_tint_color(self) -> Optional[str]:
        return self._get_attr("surfaceTintColor")

    @surface_tint_color.setter
    def surface_tint_color(self, value: Optional[str]):
        self._set_attr("surfaceTintColor", value)

    # divider_color
    @property
    def divider_color(self) -> Optional[str]:
        return self._get_attr("dividerColor")

    @divider_color.setter
    def divider_color(self, value: Optional[str]):
        self._set_attr("dividerColor", value)

    # elevation
    @property
    def elevation(self) -> OptionalNumber:
        return self._get_attr("elevation", data_type="float")

    @elevation.setter
    def elevation(self, value: OptionalNumber):
        assert value is None or value >= 0, "elevation_on_scroll cannot be negative"
        self._set_attr("elevation", value)

    # on_visible
    @property
    def on_visible(self) -> OptionalControlEventCallable:
        return self._get_event_handler("visible")

    @on_visible.setter
    def on_visible(self, handler: OptionalControlEventCallable):
        self._add_event_handler("visible", handler)
