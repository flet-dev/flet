from typing import Any, Optional

from flet.core.control import Control, OptionalNumber
from flet.core.ref import Ref
from flet.core.types import (
    ColorEnums,
    ColorValue,
    OptionalControlEventCallable,
    PaddingValue,
)


class CupertinoBottomSheet(Control):
    """
    A Cupertino version of modal bottom sheet.

    -----

    Online docs: https://flet.dev/docs/controls/cupertinobottomsheet
    """

    def __init__(
        self,
        content: Optional[Control] = None,
        open: bool = False,
        modal: bool = False,
        bgcolor: Optional[ColorValue] = None,
        height: OptionalNumber = None,
        padding: Optional[PaddingValue] = None,
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

        self.__content: Optional[Control] = None

        self.open = open
        self.modal = modal
        self.bgcolor = bgcolor
        self.height = height
        self.padding = padding
        self.content = content
        self.on_dismiss = on_dismiss

    def _get_control_name(self):
        return "cupertinobottomsheet"

    def before_update(self):
        super().before_update()
        self._set_attr_json("padding", self.__padding)

    def _get_children(self):
        children = []
        if self.__content:
            self.__content._set_attr_internal("n", "content")
            children.append(self.__content)
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

    # bgcolor
    @property
    def bgcolor(self) -> Optional[ColorValue]:
        return self.__bgcolor

    @bgcolor.setter
    def bgcolor(self, value: Optional[ColorValue]):
        self.__bgcolor = value
        self._set_enum_attr("bgColor", value, ColorEnums)

    # height
    @property
    def height(self) -> float:
        return self._get_attr("height", data_type="float", def_value=220.0)

    @height.setter
    def height(self, value: OptionalNumber):
        self._set_attr("height", value)

    # padding
    @property
    def padding(self) -> Optional[PaddingValue]:
        return self.__padding

    @padding.setter
    def padding(self, value: Optional[PaddingValue]):
        self.__padding = value

    # content
    @property
    def content(self):
        return self.__content

    @content.setter
    def content(self, value):
        self.__content = value

    # on_dismiss
    @property
    def on_dismiss(self) -> OptionalControlEventCallable:
        return self._get_event_handler("dismiss")

    @on_dismiss.setter
    def on_dismiss(self, handler: OptionalControlEventCallable):
        self._add_event_handler("dismiss", handler)
