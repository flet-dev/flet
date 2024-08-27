import warnings
from enum import Enum
from typing import Any, List, Optional, Union

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
    PaddingValue,
    ResponsiveNumber,
    RotateValue,
    ScaleValue,
    OptionalControlEventCallable,
)


class PopupMenuPosition(Enum):
    OVER = "over"
    UNDER = "under"


class PopupMenuItem(Control):
    def __init__(
        self,
        text: Optional[str] = None,
        icon: Optional[str] = None,
        checked: Optional[bool] = None,
        content: Optional[Control] = None,
        height: OptionalNumber = None,
        padding: PaddingValue = None,
        mouse_cursor: Optional[MouseCursor] = None,
        on_click: OptionalControlEventCallable = None,
        #
        # Control
        #
        ref: Optional[Ref] = None,
        disabled: Optional[bool] = None,
        data: Any = None,
    ):
        Control.__init__(self, ref=ref, disabled=disabled, data=data)

        self.checked = checked
        self.icon = icon
        self.text = text
        self.__content: Optional[Control] = None
        self.content = content
        self.on_click = on_click
        self.height = height
        self.padding = padding
        self.mouse_cursor = mouse_cursor

    def _get_control_name(self):
        return "popupmenuitem"

    def _get_children(self):
        children = []
        if self.__content:
            self.__content._set_attr_internal("n", "content")
            children.append(self.__content)
        return children

    # checked
    @property
    def checked(self) -> bool:
        return self._get_attr("checked", data_type="bool", def_value=False)

    @checked.setter
    def checked(self, value: Optional[bool]):
        self._set_attr("checked", value)

    # mouse_cursor
    @property
    def mouse_cursor(self) -> Optional[MouseCursor]:
        return self._get_attr("mouseCursor")

    @mouse_cursor.setter
    def mouse_cursor(self, value: Optional[MouseCursor]):
        self._set_enum_attr("mouseCursor", value, MouseCursor)

    # icon
    @property
    def icon(self) -> Optional[str]:
        return self._get_attr("icon")

    @icon.setter
    def icon(self, value: Optional[str]):
        self._set_attr("icon", value)

    # text
    @property
    def text(self) -> Optional[str]:
        return self._get_attr("text")

    @text.setter
    def text(self, value: Optional[str]):
        self._set_attr("text", value)

    # height
    @property
    def height(self) -> float:
        return self._get_attr("height", data_type="float", def_value=48.0)

    @height.setter
    def height(self, value: OptionalNumber):
        self._set_attr("height", value)

    # padding
    @property
    def padding(self) -> PaddingValue:
        return self.__padding

    @padding.setter
    def padding(self, value: PaddingValue):
        self.__padding = value

    # content
    @property
    def content(self) -> Optional[Control]:
        return self.__content

    @content.setter
    def content(self, value: Optional[Control]):
        self.__content = value

    # on_click
    @property
    def on_click(self) -> OptionalControlEventCallable:
        return self._get_event_handler("click")

    @on_click.setter
    def on_click(self, handler: OptionalControlEventCallable):
        self._add_event_handler("click", handler)


class PopupMenuButton(ConstrainedControl):
    """
    An icon button which displays a menu when clicked.

    Example:
    ```
    import flet as ft

    def main(page: ft.Page):
        def check_item_clicked(e):
            e.control.checked = not e.control.checked
            page.update()

        pb = ft.PopupMenuButton(
            items=[
                ft.PopupMenuItem(text="Item 1"),
                ft.PopupMenuItem(icon=ft.icons.POWER_INPUT, text="Check power"),
                ft.PopupMenuItem(
                    content=ft.Row(
                        [
                            ft.Icon(ft.icons.HOURGLASS_TOP_OUTLINED),
                            ft.Text("Item with a custom content"),
                        ]
                    ),
                    on_click=lambda _: print("Button with a custom content clicked!"),
                ),
                ft.PopupMenuItem(),  # divider
                ft.PopupMenuItem(
                    text="Checked item", checked=False, on_click=check_item_clicked
                ),
            ]
        )
        page.add(pb)

    ft.app(target=main)
    ```

    -----

    Online docs: https://flet.dev/docs/controls/popupmenubutton
    """

    def __init__(
        self,
        content: Optional[Control] = None,
        items: Optional[List[PopupMenuItem]] = None,
        icon: Optional[str] = None,
        bgcolor: Optional[str] = None,
        icon_color: Optional[str] = None,
        shadow_color: Optional[str] = None,
        surface_tint_color: Optional[str] = None,
        icon_size: OptionalNumber = None,
        splash_radius: OptionalNumber = None,
        elevation: OptionalNumber = None,
        menu_position: Optional[PopupMenuPosition] = None,
        clip_behavior: Optional[ClipBehavior] = None,
        enable_feedback: Optional[bool] = None,
        shape: Optional[OutlinedBorder] = None,
        padding: PaddingValue = None,
        on_cancelled: OptionalControlEventCallable = None,
        on_open: OptionalControlEventCallable = None,
        on_cancel: OptionalControlEventCallable = None,
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

        self.items = items
        self.icon = icon
        self.on_cancel = on_cancel
        self.on_cancelled = on_cancelled
        self.on_open = on_open
        self.shape = shape
        self.padding = padding
        self.clip_behavior = clip_behavior
        self.bgcolor = bgcolor
        self.icon_color = icon_color
        self.shadow_color = shadow_color
        self.surface_tint_color = surface_tint_color
        self.splash_radius = splash_radius
        self.icon_size = icon_size
        self.elevation = elevation
        self.enable_feedback = enable_feedback
        self.__content: Optional[Control] = None
        self.content = content
        self.menu_position = menu_position

    def _get_control_name(self):
        return "popupmenubutton"

    def _get_children(self):
        children = []
        if self.__content:
            self.__content._set_attr_internal("n", "content")
            children.append(self.__content)
        return children + self.__items

    def before_update(self):
        super().before_update()
        self._set_attr_json("shape", self.__shape)
        self._set_attr_json("padding", self.__padding)

    # items
    @property
    def items(self) -> Optional[List[PopupMenuItem]]:
        return self.__items

    @items.setter
    def items(self, value: Optional[List[PopupMenuItem]]):
        self.__items = value if value is not None else []

    # shape
    @property
    def shape(self) -> Optional[OutlinedBorder]:
        return self.__shape

    @shape.setter
    def shape(self, value: Optional[OutlinedBorder]):
        self.__shape = value

    # padding
    @property
    def padding(self) -> PaddingValue:
        return self.__padding

    @padding.setter
    def padding(self, value: PaddingValue):
        self.__padding = value

    # icon
    @property
    def icon(self) -> Optional[str]:
        return self._get_attr("icon")

    @icon.setter
    def icon(self, value: Optional[str]):
        self._set_attr("icon", value)

    # icon_color
    @property
    def icon_color(self) -> Optional[str]:
        return self._get_attr("iconColor")

    @icon_color.setter
    def icon_color(self, value: Optional[str]):
        self._set_attr("iconColor", value)

    # bgcolor
    @property
    def bgcolor(self) -> Optional[str]:
        return self._get_attr("bgcolor")

    @bgcolor.setter
    def bgcolor(self, value: Optional[str]):
        self._set_attr("bgcolor", value)

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

    # icon_size
    @property
    def icon_size(self) -> OptionalNumber:
        return self._get_attr("iconSize", data_type="float")

    @icon_size.setter
    def icon_size(self, value: OptionalNumber):
        self._set_attr("iconSize", value)

    # enable_feedback
    @property
    def enable_feedback(self) -> bool:
        return self._get_attr("enableFeedback", data_type="bool", def_value=True)

    @enable_feedback.setter
    def enable_feedback(self, value: Optional[bool]):
        self._set_attr("enableFeedback", value)

    # elevation
    @property
    def elevation(self) -> float:
        return self._get_attr("elevation", data_type="float", def_value=8.0)

    @elevation.setter
    def elevation(self, value: OptionalNumber):
        self._set_attr("elevation", value)

    # splash_radius
    @property
    def splash_radius(self) -> OptionalNumber:
        return self._get_attr("splashRadius", data_type="float")

    @splash_radius.setter
    def splash_radius(self, value: OptionalNumber):
        self._set_attr("splashRadius", value)

    # content
    @property
    def content(self) -> Optional[Control]:
        return self.__content

    @content.setter
    def content(self, value: Optional[Control]):
        self.__content = value

    # menu_position
    @property
    def menu_position(self) -> PopupMenuPosition:
        return self.__menu_position

    @menu_position.setter
    def menu_position(self, value: PopupMenuPosition):
        self.__menu_position = value
        self._set_enum_attr("menuPosition", value, PopupMenuPosition)

    # clip_behavior
    @property
    def clip_behavior(self) -> ClipBehavior:
        return self.__clip_behavior

    @clip_behavior.setter
    def clip_behavior(self, value: ClipBehavior):
        self.__clip_behavior = value
        self._set_enum_attr("clipBehavior", value, ClipBehavior)

    # on_cancel
    @property
    def on_cancel(self) -> OptionalControlEventCallable:
        return self._get_event_handler("cancel")

    @on_cancel.setter
    def on_cancel(self, handler: OptionalControlEventCallable):
        self._add_event_handler("cancel", handler)

    # on_cancelled
    @property
    def on_cancelled(self) -> OptionalControlEventCallable:
        warnings.warn(
            f"on_cancelled is deprecated/renamed since version 0.22.0 "
            f"and will be removed in version 0.26.0. Use on_cancel instead.",
            category=DeprecationWarning,
            stacklevel=2,
        )
        return self._get_event_handler("cancelled")

    @on_cancelled.setter
    def on_cancelled(self, handler: OptionalControlEventCallable):
        self._add_event_handler("cancelled", handler)
        if handler is not None:
            warnings.warn(
                f"on_cancelled is deprecated/renamed since version 0.22.0 "
                f"and will be removed in version 0.26.0. Use on_cancel instead.",
                category=DeprecationWarning,
                stacklevel=2,
            )

    # on_open
    @property
    def on_open(self) -> OptionalControlEventCallable:
        return self._get_event_handler("open")

    @on_open.setter
    def on_open(self, handler: OptionalControlEventCallable):
        self._add_event_handler("open", handler)
