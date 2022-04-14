from typing import Optional

from beartype import beartype

from flet.constrained_control import ConstrainedControl
from flet.control import Control, InputBorder, OptionalNumber
from flet.ref import Ref


class FormFieldControl(ConstrainedControl):
    def __init__(
        self,
        ref: Ref = None,
        width: OptionalNumber = None,
        height: OptionalNumber = None,
        expand: int = None,
        opacity: OptionalNumber = None,
        visible: bool = None,
        disabled: bool = None,
        data: any = None,
        #
        # FormField specific
        #
        label: str = None,
        icon: str = None,
        border: InputBorder = None,
        filled: bool = None,
        hint_text: str = None,
        helper_text: str = None,
        counter_text: str = None,
        error_text: str = None,
        prefix: Control = None,
        suffix: Control = None,
    ):
        ConstrainedControl.__init__(
            self,
            ref=ref,
            width=width,
            height=height,
            expand=expand,
            opacity=opacity,
            visible=visible,
            disabled=disabled,
            data=data,
        )

        self.__prefix: Control = None
        self.__suffix: Control = None

        self.label = label
        self.icon = icon
        self.border = border
        self.filled = filled
        self.hint_text = hint_text
        self.helper_text = helper_text
        self.counter_text = counter_text
        self.error_text = error_text
        self.prefix = prefix
        self.suffix = suffix

    def _get_children(self):
        children = []
        if self.__prefix:
            self.__prefix._set_attr_internal("n", "prefix")
            children.append(self.__prefix)
        if self.__suffix:
            self.__suffix._set_attr_internal("n", "prefix")
            children.append(self.__suffix)
        return children

    # label
    @property
    def label(self):
        return self._get_attr("label")

    @label.setter
    def label(self, value):
        self._set_attr("label", value)

    # icon
    @property
    def icon(self):
        return self._get_attr("icon")

    @icon.setter
    def icon(self, value):
        self._set_attr("icon", value)

    # border
    @property
    def border(self):
        return self._get_attr("border")

    @border.setter
    @beartype
    def border(self, value: InputBorder):
        self._set_attr("border", value)

    # filled
    @property
    def filled(self):
        return self._get_attr("filled")

    @filled.setter
    def filled(self, value: Optional[bool]):
        self._set_attr("filled", value)

    # hint_text
    @property
    def hint_text(self):
        return self._get_attr("hintText")

    @hint_text.setter
    def hint_text(self, value):
        self._set_attr("hintText", value)

    # helper_text
    @property
    def helper_text(self):
        return self._get_attr("helperText")

    @helper_text.setter
    def helper_text(self, value):
        self._set_attr("helperText", value)

    # counter_text
    @property
    def counter_text(self):
        return self._get_attr("counterText")

    @counter_text.setter
    def counter_text(self, value):
        self._set_attr("counterText", value)

    # error_text
    @property
    def error_text(self):
        return self._get_attr("errorText")

    @error_text.setter
    def error_text(self, value):
        self._set_attr("errorText", value)

    # prefix
    @property
    def prefix(self):
        return self.__prefix

    @prefix.setter
    def prefix(self, value):
        self.__prefix = value

    # suffix
    @property
    def suffix(self):
        return self.__suffix

    @suffix.setter
    def suffix(self, value):
        self.__suffix = value
