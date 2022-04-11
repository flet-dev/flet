from typing import Optional

from beartype import beartype

from flet.control import Control, InputBorder
from flet.ref import Ref

try:
    from typing import Literal
except:
    from typing_extensions import Literal


class FormField(Control):
    def __init__(
        self,
        id: str = None,
        ref: Ref = None,
        width: float = None,
        height: float = None,
        padding: float = None,
        margin: float = None,
        expand: int = None,
        opacity: float = None,
        visible: bool = None,
        disabled: bool = None,
        data: any = None,
        #
        # Specific
        #
        label: str = None,
        icon: str = None,
        border: InputBorder = None,
        filled: bool = None,
        hint_text: str = None,
        helper_text: str = None,
        counter_text: str = None,
        error_text: str = None,
        prefix_icon: str = None,
        prefix_text: str = None,
        suffix_icon: str = None,
        suffix_text: str = None,
    ):
        Control.__init__(
            self,
            id=id,
            ref=ref,
            width=width,
            height=height,
            padding=padding,
            margin=margin,
            expand=expand,
            opacity=opacity,
            visible=visible,
            disabled=disabled,
            data=data,
        )

        self.label = label
        self.icon = icon
        self.border = border
        self.filled = filled
        self.hint_text = hint_text
        self.helper_text = helper_text
        self.counter_text = counter_text
        self.error_text = error_text
        self.prefix_icon = prefix_icon
        self.prefix_text = prefix_text
        self.suffix_icon = suffix_icon
        self.suffix_text = suffix_text

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
