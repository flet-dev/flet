from typing import Optional, Union

from beartype import beartype

from flet import padding
from flet.constrained_control import ConstrainedControl
from flet.control import Control, InputBorder, OptionalNumber, PaddingValue
from flet.ref import Ref


class FormFieldControl(ConstrainedControl):
    def __init__(
        self,
        ref: Ref = None,
        width: OptionalNumber = None,
        height: OptionalNumber = None,
        expand: Union[bool, int] = None,
        opacity: OptionalNumber = None,
        tooltip: str = None,
        visible: bool = None,
        disabled: bool = None,
        data: any = None,
        #
        # FormField specific
        #
        label: str = None,
        icon: str = None,
        border: InputBorder = None,
        content_padding: PaddingValue = None,
        filled: bool = None,
        hint_text: str = None,
        helper_text: str = None,
        counter_text: str = None,
        error_text: str = None,
        prefix: Control = None,
        prefix_icon: str = None,
        prefix_text: str = None,
        suffix: Control = None,
        suffix_icon: str = None,
        suffix_text: str = None,
    ):
        ConstrainedControl.__init__(
            self,
            ref=ref,
            width=width,
            height=height,
            expand=expand,
            opacity=opacity,
            tooltip=tooltip,
            visible=visible,
            disabled=disabled,
            data=data,
        )

        self.__prefix: Control = None
        self.__suffix: Control = None

        self.label = label
        self.icon = icon
        self.border = border
        self.content_padding = content_padding
        self.filled = filled
        self.hint_text = hint_text
        self.helper_text = helper_text
        self.counter_text = counter_text
        self.error_text = error_text
        self.prefix = prefix
        self.prefix_icon = prefix_icon
        self.prefix_text = prefix_text
        self.suffix = suffix
        self.suffix_icon = suffix_icon
        self.suffix_text = suffix_text

    def _get_children(self):
        children = []
        if self.__prefix:
            self.__prefix._set_attr_internal("n", "prefix")
            children.append(self.__prefix)
        if self.__suffix:
            self.__suffix._set_attr_internal("n", "suffix")
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

    # content_padding
    @property
    def content_padding(self):
        return self.__content_padding

    @content_padding.setter
    @beartype
    def content_padding(self, value: PaddingValue):
        self.__content_padding = value
        if value and isinstance(value, (int, float)):
            value = padding.all(value)
        self._set_attr_json("contentPadding", value)

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

    # prefix_icon
    @property
    def prefix_icon(self):
        return self._get_attr("prefixIcon")

    @prefix_icon.setter
    def prefix_icon(self, value):
        self._set_attr("prefixIcon", value)

    # prefix_text
    @property
    def prefix_text(self):
        return self._get_attr("prefixText")

    @prefix_text.setter
    def prefix_text(self, value):
        self._set_attr("prefixText", value)

    # suffix
    @property
    def suffix(self):
        return self.__suffix

    @suffix.setter
    def suffix(self, value):
        self.__suffix = value

    # suffix_icon
    @property
    def suffix_icon(self):
        return self._get_attr("suffixIcon")

    @suffix_icon.setter
    def suffix_icon(self, value):
        self._set_attr("suffixIcon", value)

    # suffix_text
    @property
    def suffix_text(self):
        return self._get_attr("suffixText")

    @suffix_text.setter
    def suffix_text(self, value):
        self._set_attr("suffixText", value)
