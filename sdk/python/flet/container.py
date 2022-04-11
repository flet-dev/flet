from typing import List, Optional

from beartype import beartype

from flet.control import BorderStyle, Control
from flet.ref import Ref

try:
    from typing import Literal
except:
    from typing_extensions import Literal

Alignment = Literal[
    None,
    "topLeft",
    "topCenter",
    "topRight",
    "centerLeft",
    "center",
    "centerRight",
    "bottomLeft",
    "bottomCenter",
    "bottomRight",
]


class Container(Control):
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
        content: Control = None,
        alignment: Alignment = None,
        bgcolor: str = None,
        border_color: str = None,
        border_width: float = None,
        border_style: BorderStyle = None,
        border_radius: float = None,
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

        self.content = content
        self.alignment = alignment
        self.bgcolor = bgcolor
        self.border_color = border_color
        self.border_width = border_width
        self.border_style = border_style
        self.border_radius = border_radius

    def _get_control_name(self):
        return "container"

    # alignment
    @property
    def alignment(self):
        return self._get_attr("alignment")

    @alignment.setter
    @beartype
    def alignment(self, value: Alignment):
        self._set_attr("alignment", value)

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
    def border_width(self):
        return self._get_attr("borderWidth")

    @border_width.setter
    def border_width(self, value):
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

    def _get_children(self):
        if self.__content == None:
            raise Exception("Container does not have any content set.")
        return [self.__content]
