import json
from typing import Optional

from beartype import beartype

from flet import margin, padding
from flet.alignment import Alignment
from flet.constrained_control import ConstrainedControl
from flet.control import BorderStyle, Control, MarginValue, OptionalNumber, PaddingValue
from flet.ref import Ref

try:
    from typing import Literal
except:
    from typing_extensions import Literal


class Container(ConstrainedControl):
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
        # Specific
        #
        content: Control = None,
        padding: PaddingValue = None,
        margin: MarginValue = None,
        alignment: Alignment = None,
        bgcolor: str = None,
        border_color: str = None,
        border_width: OptionalNumber = None,
        border_style: BorderStyle = None,
        border_radius: OptionalNumber = None,
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

        self.content = content
        self.padding = padding
        self.margin = margin
        self.alignment = alignment
        self.bgcolor = bgcolor
        self.border_color = border_color
        self.border_width = border_width
        self.border_style = border_style
        self.border_radius = border_radius

    def _get_control_name(self):
        return "container"

    def _get_children(self):
        if self.__content == None:
            raise Exception("Container does not have any content set.")
        self.__content._set_attr_internal("n", "content")
        return [self.__content]

    # alignment
    @property
    def alignment(self):
        return self.__alignment

    @alignment.setter
    @beartype
    def alignment(self, value: Optional[Alignment]):
        self.__alignment = value
        self._set_attr("alignment", json.dumps(value, default=vars) if value else None)

    # padding
    @property
    def padding(self):
        return self.__padding

    @padding.setter
    @beartype
    def padding(self, value: PaddingValue):
        self.__padding = value
        if value and isinstance(value, (int, float)):
            value = padding.all(value)
        self._set_attr("padding", json.dumps(value, default=vars) if value else None)

    # margin
    @property
    def margin(self):
        return self.__margin

    @margin.setter
    @beartype
    def margin(self, value: MarginValue):
        self.__margin = value
        if value and isinstance(value, (int, float)):
            value = margin.all(value)
        self._set_attr("margin", json.dumps(value, default=vars) if value else None)

    # bgcolor
    @property
    def bgcolor(self):
        return self._get_attr("bgColor")

    @bgcolor.setter
    def bgcolor(self, value):
        self._set_attr("bgColor", value)

    # border_color
    @property
    def border_color(self):
        return self._get_attr("borderColor")

    @border_color.setter
    def border_color(self, value):
        self._set_attr("borderColor", value)

    # border_width
    @property
    def border_width(self) -> OptionalNumber:
        return self._get_attr("borderWidth")

    @border_width.setter
    @beartype
    def border_width(self, value: OptionalNumber):
        self._set_attr("borderWidth", value)

    # border_style
    @property
    def border_style(self):
        return self._get_attr("borderStyle")

    @border_style.setter
    @beartype
    def border_style(self, value: BorderStyle):
        self._set_attr("borderStyle", value)

    # border_radius
    @property
    def border_radius(self):
        return self._get_attr("borderRadius")

    @border_radius.setter
    def border_radius(self, value):
        self._set_attr("borderRadius", value)

    # content
    @property
    def content(self):
        return self.__content

    @content.setter
    @beartype
    def content(self, value: Optional[Control]):
        self.__content = value
