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


class PopupMenuItem(Control):
    def __init__(
        self,
        ref: Optional[Ref] = None,
        checked: Optional[bool] = None,
        icon: Optional[str] = None,
        text: Optional[str] = None,
        content: Optional[Control] = None,
        on_click=None,
        data: Any = None,
    ):
        Control.__init__(self, ref=ref)

        self.checked = checked
        self.icon = icon
        self.text = text
        self.__content: Optional[Control] = None
        self.content = content
        self.on_click = on_click
        self.data = data

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
    def checked(self) -> Optional[bool]:
        return self._get_attr("checked", data_type="bool")

    @checked.setter
    def checked(self, value: Optional[bool]):
        self._set_attr("checked", value)

    # icon
    @property
    def icon(self):
        return self._get_attr("icon")

    @icon.setter
    def icon(self, value):
        self._set_attr("icon", value)

    # text
    @property
    def text(self):
        return self._get_attr("text")

    @text.setter
    def text(self, value):
        self._set_attr("text", value)

    # content
    @property
    def content(self):
        return self.__content

    @content.setter
    def content(self, value):
        self.__content = value

    # on_click
    @property
    def on_click(self):
        return self._get_event_handler("click")

    @on_click.setter
    def on_click(self, handler):
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
        ref: Optional[Ref] = None,
        key: Optional[str] = None,
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
        #
        # PopupMenuButton-specific
        items: Optional[List[PopupMenuItem]] = None,
        icon: Optional[str] = None,
        on_cancelled=None,
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

        self.items = items
        self.icon = icon
        self.on_cancelled = on_cancelled
        self.__content: Optional[Control] = None
        self.content = content

    def _get_control_name(self):
        return "popupmenubutton"

    def _get_children(self):
        children = []
        if self.__content:
            self.__content._set_attr_internal("n", "content")
            children.append(self.__content)
        children.extend(self.__items)
        return children

    # items
    @property
    def items(self) -> Optional[List[PopupMenuItem]]:
        return self.__items

    @items.setter
    def items(self, value: Optional[List[PopupMenuItem]]):
        self.__items = value if value is not None else []

    # on_cancelled
    @property
    def on_cancelled(self):
        return self._get_event_handler("cancelled")

    @on_cancelled.setter
    def on_cancelled(self, handler):
        self._add_event_handler("cancelled", handler)

    # icon
    @property
    def icon(self):
        return self._get_attr("icon")

    @icon.setter
    def icon(self, value):
        self._set_attr("icon", value)

    # content
    @property
    def content(self) -> Optional[Control]:
        return self.__content

    @content.setter
    def content(self, value: Optional[Control]):
        self.__content = value
