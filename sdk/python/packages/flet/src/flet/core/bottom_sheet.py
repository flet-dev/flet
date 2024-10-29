from typing import Any, Optional

from flet.core.control import Control, OptionalNumber
from flet.core.ref import Ref
from flet.core.types import ColorEnums, ColorValue, OptionalControlEventCallable


class BottomSheet(Control):
    """
    A modal bottom sheet is an alternative to a menu or a dialog and prevents the user from interacting with the rest of the app.

    Example:
    ```
    import flet as ft


    def main(page: ft.Page):
        page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

        def handle_dismissal(e):
            page.add(ft.Text("Bottom sheet dismissed"))
        bs = ft.BottomSheet(
            on_dismiss=handle_dismissal,
            content=ft.Container(
                padding=50,
                content=ft.Column(
                    tight=True,
                    controls=[
                        ft.Text("This is bottom sheet's content!"),
                        ft.ElevatedButton("Close bottom sheet", on_click=lambda _: page.close(bs)),
                    ],
                ),
            ),
        )
        page.add(ft.ElevatedButton("Display bottom sheet", on_click=lambda _: page.open(bs)))


    ft.app(target=main)
    ```

    -----

    Online docs: https://flet.dev/docs/controls/bottomsheet
    """

    def __init__(
        self,
        content: Control,
        open: bool = False,
        elevation: OptionalNumber = None,
        bgcolor: Optional[ColorValue] = None,
        dismissible: Optional[bool] = None,
        enable_drag: Optional[bool] = None,
        show_drag_handle: Optional[bool] = None,
        use_safe_area: Optional[bool] = None,
        is_scroll_controlled: Optional[bool] = None,
        maintain_bottom_view_insets_padding: Optional[bool] = None,
        on_dismiss: OptionalControlEventCallable = None,
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
        self.elevation = elevation
        self.bgcolor = bgcolor
        self.dismissible = dismissible
        self.enable_drag = enable_drag
        self.show_drag_handle = show_drag_handle
        self.use_safe_area = use_safe_area
        self.is_scroll_controlled = is_scroll_controlled
        self.content = content
        self.maintain_bottom_view_insets_padding = maintain_bottom_view_insets_padding
        self.on_dismiss = on_dismiss

    def _get_control_name(self):
        return "bottomsheet"

    def _get_children(self):
        self.__content._set_attr_internal("n", "content")
        return [self.__content]

    def before_update(self):
        super().before_update()
        assert self.__content.visible, "content must be visible"

    # open
    @property
    def open(self) -> bool:
        return self._get_attr("open", data_type="bool", def_value=False)

    @open.setter
    def open(self, value: Optional[bool]):
        self._set_attr("open", value)

    # elevation
    @property
    def elevation(self) -> OptionalNumber:
        return self._get_attr("elevation")

    @elevation.setter
    def elevation(self, value: OptionalNumber):
        assert value is None or value >= 0, "elevation cannot be negative"
        self._set_attr("elevation", value)

    # bgcolor
    @property
    def bgcolor(self) -> Optional[ColorValue]:
        return self.__bgcolor

    @bgcolor.setter
    def bgcolor(self, value: Optional[ColorValue]):
        self.__bgcolor = value
        self._set_enum_attr("bgColor", value, ColorEnums)

    # dismissible
    @property
    def dismissible(self) -> bool:
        return self._get_attr("dismissible", data_type="bool", def_value=True)

    @dismissible.setter
    def dismissible(self, value: Optional[bool]):
        self._set_attr("dismissible", value)

    # enable_drag
    @property
    def enable_drag(self) -> bool:
        return self._get_attr("enableDrag", data_type="bool", def_value=False)

    @enable_drag.setter
    def enable_drag(self, value: Optional[bool]):
        self._set_attr("enableDrag", value)

    # show_drag_handle
    @property
    def show_drag_handle(self) -> bool:
        return self._get_attr("showDragHandle", data_type="bool", def_value=False)

    @show_drag_handle.setter
    def show_drag_handle(self, value: Optional[bool]):
        self._set_attr("showDragHandle", value)

    # use_safe_area
    @property
    def use_safe_area(self) -> bool:
        return self._get_attr("useSafeArea", data_type="bool", def_value=True)

    @use_safe_area.setter
    def use_safe_area(self, value: Optional[bool]):
        self._set_attr("useSafeArea", value)

    # is_scroll_controlled
    @property
    def is_scroll_controlled(self) -> bool:
        return self._get_attr("isScrollControlled", data_type="bool", def_value=False)

    @is_scroll_controlled.setter
    def is_scroll_controlled(self, value: Optional[bool]):
        self._set_attr("isScrollControlled", value)

    # maintain_bottom_view_insets_padding
    @property
    def maintain_bottom_view_insets_padding(self) -> bool:
        return self._get_attr(
            "maintainBottomViewInsetsPadding", data_type="bool", def_value=True
        )

    @maintain_bottom_view_insets_padding.setter
    def maintain_bottom_view_insets_padding(self, value: Optional[bool]):
        self._set_attr("maintainBottomViewInsetsPadding", value)

    # content
    @property
    def content(self) -> Control:
        return self.__content

    @content.setter
    def content(self, value: Control):
        self.__content = value

    # on_dismiss
    @property
    def on_dismiss(self) -> OptionalControlEventCallable:
        return self._get_event_handler("dismiss")

    @on_dismiss.setter
    def on_dismiss(self, handler: OptionalControlEventCallable):
        self._add_event_handler("dismiss", handler)
