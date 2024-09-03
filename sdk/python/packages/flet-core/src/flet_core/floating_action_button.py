from typing import Any, Optional, Union

from flet_core.buttons import OutlinedBorder
from flet_core.constrained_control import ConstrainedControl
from flet_core.control import Control, OptionalNumber
from flet_core.ref import Ref
from flet_core.tooltip import TooltipValue
from flet_core.types import (
    AnimationValue,
    ClipBehavior,
    MouseCursor,
    OffsetValue,
    ResponsiveNumber,
    RotateValue,
    ScaleValue,
    UrlTarget,
    OptionalControlEventCallable,
)


class FloatingActionButton(ConstrainedControl):
    """
    A floating action button is a circular icon button that hovers over content to promote a primary action in the application. Floating action button is usually set to `page.floating_action_button`, but can also be added as a regular control at any place on a page.

    Example:
    ```
    import flet as ft

    def main(page: ft.Page):
        page.title = "Floating Action Button"
        page.theme_mode = ft.ThemeMode.LIGHT
        page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
        page.auto_scroll = True
        page.scroll = ft.ScrollMode.HIDDEN
        page.appbar = ft.AppBar(
            title=ft.Text(
                "Floating Action Button", weight=ft.FontWeight.BOLD, color=ft.colors.BLACK87
            ),
            bgcolor=ft.colors.BLUE,
            center_title=True,
            actions=[
                ft.IconButton(ft.icons.MENU, tooltip="Menu", icon_color=ft.colors.BLACK87)
            ],
            color=ft.colors.WHITE,
        )

        # keeps track of the number of tiles already added
        page.count = 0

        def fab_pressed(e):
            page.add(ft.ListTile(title=ft.Text(f"Tile {page.count}")))
            page.show_snack_bar(
                ft.SnackBar(ft.Text("Tile was added successfully!"), open=True)
            )
            page.count += 1

        page.floating_action_button = ft.FloatingActionButton(
            icon=ft.icons.ADD, on_click=fab_pressed, bgcolor=ft.colors.LIME_300
        )
        page.add(ft.Text("Press the FAB to add a tile!"))

    ft.app(target=main)
    ```

    -----

    Online docs: https://flet.dev/docs/controls/floatingactionbutton
    """

    def __init__(
        self,
        text: Optional[str] = None,
        icon: Optional[str] = None,
        bgcolor: Optional[str] = None,
        content: Optional[Control] = None,
        shape: Optional[OutlinedBorder] = None,
        autofocus: Optional[bool] = None,
        mini: Optional[bool] = None,
        foreground_color: Optional[str] = None,
        focus_color: Optional[str] = None,
        clip_behavior: Optional[ClipBehavior] = None,
        elevation: OptionalNumber = None,
        disabled_elevation: OptionalNumber = None,
        focus_elevation: OptionalNumber = None,
        highlight_elevation: OptionalNumber = None,
        hover_elevation: OptionalNumber = None,
        enable_feedback: Optional[bool] = None,
        url: Optional[str] = None,
        url_target: Optional[UrlTarget] = None,
        mouse_cursor: Optional[MouseCursor] = None,
        on_click: OptionalControlEventCallable = None,
        #
        # ConstrainedControl
        #
        ref: Optional[Ref] = None,
        key: Optional[str] = None,
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
        tooltip: TooltipValue = None,
        visible: Optional[bool] = None,
        disabled: Optional[bool] = None,
        data: Any = None,
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

        self.text = text
        self.icon = icon
        self.bgcolor = bgcolor
        self.content = content
        self.autofocus = autofocus
        self.shape = shape
        self.mini = mini
        self.url = url
        self.url_target = url_target
        self.on_click = on_click
        self.foreground_color = foreground_color
        self.focus_color = focus_color
        self.clip_behavior = clip_behavior
        self.elevation = elevation
        self.disabled_elevation = disabled_elevation
        self.focus_elevation = focus_elevation
        self.highlight_elevation = highlight_elevation
        self.hover_elevation = hover_elevation
        self.enable_feedback = enable_feedback
        self.mouse_cursor = mouse_cursor

    def _get_control_name(self):
        return "floatingactionbutton"

    def before_update(self):
        super().before_update()
        assert (
            self.text or self.icon or (self.__content and self.__content.visible)
        ), "at minimum, text, icon or a visible content must be provided"
        self._set_attr_json("shape", self.__shape)

    def _get_children(self):
        if self.__content is None:
            return []
        self.__content._set_attr_internal("n", "content")
        return [self.__content]

    # text
    @property
    def text(self) -> Optional[str]:
        return self._get_attr("text")

    @text.setter
    def text(self, value: Optional[str]):
        self._set_attr("text", value)

    # icon
    @property
    def icon(self) -> Optional[str]:
        return self._get_attr("icon")

    @icon.setter
    def icon(self, value: Optional[str]):
        self._set_attr("icon", value)

    # bgcolor
    @property
    def bgcolor(self) -> Optional[str]:
        return self._get_attr("bgcolor")

    @bgcolor.setter
    def bgcolor(self, value: Optional[str]):
        self._set_attr("bgcolor", value)

    # url
    @property
    def url(self) -> Optional[str]:
        return self._get_attr("url")

    @url.setter
    def url(self, value: Optional[str]):
        self._set_attr("url", value)

    # url_target
    @property
    def url_target(self) -> Optional[UrlTarget]:
        return self.__url_target

    @url_target.setter
    def url_target(self, value: Optional[UrlTarget]):
        self.__url_target = value
        self._set_enum_attr("urlTarget", value, UrlTarget)

    # mouse_cursor
    @property
    def mouse_cursor(self) -> Optional[MouseCursor]:
        return self.__mouse_cursor

    @mouse_cursor.setter
    def mouse_cursor(self, value: Optional[MouseCursor]):
        self.__mouse_cursor = value
        self._set_enum_attr("mouseCursor", value, MouseCursor)

    # on_click
    @property
    def on_click(self) -> OptionalControlEventCallable:
        return self._get_event_handler("click")

    @on_click.setter
    def on_click(self, handler: OptionalControlEventCallable):
        self._add_event_handler("click", handler)

    # content
    @property
    def content(self) -> Optional[Control]:
        return self.__content

    @content.setter
    def content(self, value: Optional[Control]):
        self.__content = value

    # autofocus
    @property
    def autofocus(self) -> bool:
        return self._get_attr("autofocus", data_type="bool", def_value=False)

    @autofocus.setter
    def autofocus(self, value: Optional[bool]):
        self._set_attr("autofocus", value)

    # shape
    @property
    def shape(self) -> Optional[OutlinedBorder]:
        return self.__shape

    @shape.setter
    def shape(self, value: Optional[OutlinedBorder]):
        self.__shape = value

    # mini
    @property
    def mini(self) -> bool:
        return self._get_attr("mini", data_type="bool", def_value=False)

    @mini.setter
    def mini(self, value: Optional[bool]):
        self._set_attr("mini", value)

    # elevation
    @property
    def elevation(self) -> OptionalNumber:
        return self._get_attr("elevation", data_type="float")

    @elevation.setter
    def elevation(self, value: OptionalNumber):
        assert value is None or value >= 0, "elevation cannot be negative"
        self._set_attr("elevation", value)

    # disabled_elevation
    @property
    def disabled_elevation(self) -> OptionalNumber:
        return self._get_attr("disabledElevation", data_type="float")

    @disabled_elevation.setter
    def disabled_elevation(self, value: OptionalNumber):
        assert value is None or value >= 0, "disabled_elevation cannot be negative"
        self._set_attr("disabledElevation", value)

    # enable_feedback
    @property
    def enable_feedback(self) -> bool:
        return self._get_attr("enableFeedback", data_type="bool", def_value=True)

    @enable_feedback.setter
    def enable_feedback(self, value: Optional[bool]):
        self._set_attr("enableFeedback", value)

    # focus_color
    @property
    def focus_color(self) -> Optional[str]:
        return self._get_attr("focusColor")

    @focus_color.setter
    def focus_color(self, value: Optional[str]):
        self._set_attr("focusColor", value)

    # focus_elevation
    @property
    def focus_elevation(self) -> OptionalNumber:
        return self._get_attr("focusElevation", data_type="float")

    @focus_elevation.setter
    def focus_elevation(self, value: OptionalNumber):
        assert value is None or value >= 0, "focus_elevation cannot be negative"
        self._set_attr("focusElevation", value)

    # foreground_color
    @property
    def foreground_color(self) -> Optional[str]:
        return self._get_attr("foregroundColor")

    @foreground_color.setter
    def foreground_color(self, value: Optional[str]):
        self._set_attr("foregroundColor", value)

    # highlight_elevation
    @property
    def highlight_elevation(self) -> OptionalNumber:
        return self._get_attr("highlightElevation", data_type="float")

    @highlight_elevation.setter
    def highlight_elevation(self, value: OptionalNumber):
        assert value is None or value >= 0, "highlight_elevation cannot be negative"
        self._set_attr("highlightElevation", value)

    # hover_elevation
    @property
    def hover_elevation(self) -> OptionalNumber:
        return self._get_attr("hoverElevation", data_type="float")

    @hover_elevation.setter
    def hover_elevation(self, value: OptionalNumber):
        assert value is None or value >= 0, "hover_elevation cannot be negative"
        self._set_attr("hoverElevation", value)

    # clip_behavior
    @property
    def clip_behavior(self) -> Optional[ClipBehavior]:
        return self.__clip_behavior

    @clip_behavior.setter
    def clip_behavior(self, value: Optional[ClipBehavior]):
        self.__clip_behavior = value
        self._set_enum_attr("clipBehavior", value, ClipBehavior)
