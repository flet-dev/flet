from typing import Any, List, Optional

from flet_core.adaptive_control import AdaptiveControl
from flet_core.buttons import OutlinedBorder
from flet_core.control import Control, OptionalNumber
from flet_core.ref import Ref
from flet_core.types import MainAxisAlignment, PaddingValue


class AlertDialog(AdaptiveControl):
    """
    An alert dialog informs the user about situations that require acknowledgement. An alert dialog has an optional title and an optional list of actions. The title is displayed above the content and the actions are displayed below the content.

    Example:
    ```
    import flet as ft

    def main(page: ft.Page):
        page.title = "AlertDialog examples"

        dlg = ft.AlertDialog(
            title=ft.Text("Hello, you!"), on_dismiss=lambda e: print("Dialog dismissed!")
        )

        def close_dlg(e):
            dlg_modal.open = False
            page.update()

        dlg_modal = ft.AlertDialog(
            modal=True,
            title=ft.Text("Please confirm"),
            content=ft.Text("Do you really want to delete all those files?"),
            actions=[
                ft.TextButton("Yes", on_click=close_dlg),
                ft.TextButton("No", on_click=close_dlg),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
            on_dismiss=lambda e: print("Modal dialog dismissed!"),
        )

        def open_dlg(e):
            page.dialog = dlg
            dlg.open = True
            page.update()

        def open_dlg_modal(e):
            page.dialog = dlg_modal
            dlg_modal.open = True
            page.update()

        page.add(
            ft.ElevatedButton("Open dialog", on_click=open_dlg),
            ft.ElevatedButton("Open modal dialog", on_click=open_dlg_modal),
        )

    ft.app(target=main)
    ```
    -----

    Online docs: https://flet.dev/docs/controls/alertdialog
    """

    def __init__(
        self,
        modal: bool = False,
        title: Optional[Control] = None,
        content: Optional[Control] = None,
        actions: Optional[List[Control]] = None,
        bgcolor: Optional[str] = None,
        elevation: OptionalNumber = None,
        icon: Optional[Control] = None,
        open: bool = False,
        title_padding: PaddingValue = None,
        content_padding: PaddingValue = None,
        actions_padding: PaddingValue = None,
        actions_alignment: MainAxisAlignment = MainAxisAlignment.NONE,
        shape: Optional[OutlinedBorder] = None,
        inset_padding: PaddingValue = None,
        semantics_label: Optional[str] = None,
        adaptive: Optional[bool] = None,
        on_dismiss=None,
        #
        # AdaptiveControl
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

        AdaptiveControl.__init__(self, adaptive=adaptive)

        self.__title: Optional[Control] = None
        self.__icon: Optional[Control] = None
        self.__content: Optional[Control] = None
        self.__actions: List[Control] = []

        self.open = open
        self.bgcolor = bgcolor
        self.elevation = elevation
        self.icon = icon
        self.modal = modal
        self.title = title
        self.title_padding = title_padding
        self.content = content
        self.content_padding = content_padding
        self.actions = actions
        self.actions_padding = actions_padding
        self.actions_alignment = actions_alignment
        self.shape = shape
        self.inset_padding = inset_padding
        self.semantics_label = semantics_label
        self.on_dismiss = on_dismiss

    def _get_control_name(self):
        return "alertdialog"

    def before_update(self):
        super().before_update()
        self._set_attr_json("actionsPadding", self.__actions_padding)
        self._set_attr_json("contentPadding", self.__content_padding)
        self._set_attr_json("titlePadding", self.__title_padding)
        self._set_attr_json("shape", self.__shape)
        self._set_attr_json("insetPadding", self.__inset_padding)

    def _get_children(self):
        children = []
        if self.__title:
            self.__title._set_attr_internal("n", "title")
            children.append(self.__title)
        if self.__icon:
            self.__icon._set_attr_internal("n", "icon")
            children.append(self.__icon)
        if self.__content:
            self.__content._set_attr_internal("n", "content")
            children.append(self.__content)
        for action in self.__actions:
            action._set_attr_internal("n", "action")
            children.append(action)
        return children

    # open
    @property
    def open(self) -> Optional[bool]:
        return self._get_attr("open", data_type="bool", def_value=False)

    @open.setter
    def open(self, value: Optional[bool]):
        self._set_attr("open", value)

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

    # modal
    @property
    def modal(self) -> Optional[bool]:
        return self._get_attr("modal", data_type="bool", def_value=False)

    @modal.setter
    def modal(self, value: Optional[bool]):
        self._set_attr("modal", value)

    # title
    @property
    def title(self):
        return self.__title

    @title.setter
    def title(self, value):
        self.__title = value

    # icon
    @property
    def icon(self):
        return self.__icon

    @icon.setter
    def icon(self, value):
        self.__icon = value

    # title_padding
    @property
    def title_padding(self) -> PaddingValue:
        return self.__title_padding

    @title_padding.setter
    def title_padding(self, value: PaddingValue):
        self.__title_padding = value

    # content
    @property
    def content(self):
        return self.__content

    @content.setter
    def content(self, value):
        self.__content = value

    # content_padding
    @property
    def content_padding(self) -> PaddingValue:
        return self.__content_padding

    @content_padding.setter
    def content_padding(self, value: PaddingValue):
        self.__content_padding = value

    # actions
    @property
    def actions(self):
        return self.__actions

    @actions.setter
    def actions(self, value):
        self.__actions = value if value is not None else []

    # actions_padding
    @property
    def actions_padding(self) -> PaddingValue:
        return self.__actions_padding

    @actions_padding.setter
    def actions_padding(self, value: PaddingValue):
        self.__actions_padding = value

    # actions_alignment
    @property
    def actions_alignment(self) -> MainAxisAlignment:
        return self.__actions_alignment

    @actions_alignment.setter
    def actions_alignment(self, value: MainAxisAlignment):
        self.__actions_alignment = value
        self._set_attr(
            "actionsAlignment",
            value.value if isinstance(value, MainAxisAlignment) else value,
        )

    # shape
    @property
    def shape(self) -> Optional[OutlinedBorder]:
        return self.__shape

    @shape.setter
    def shape(self, value: Optional[OutlinedBorder]):
        self.__shape = value

    # inset_padding
    @property
    def inset_padding(self) -> PaddingValue:
        return self.__inset_padding

    @inset_padding.setter
    def inset_padding(self, value: PaddingValue):
        self.__inset_padding = value

    # semantics_label
    @property
    def semantics_label(self):
        return self._get_attr("semanticsLabel")

    @semantics_label.setter
    def semantics_label(self, value):
        self._set_attr("semanticsLabel", value)

    # on_dismiss
    @property
    def on_dismiss(self):
        return self._get_event_handler("dismiss")

    @on_dismiss.setter
    def on_dismiss(self, handler):
        self._add_event_handler("dismiss", handler)
