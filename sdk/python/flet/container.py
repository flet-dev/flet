from typing import List, Literal, Optional

from beartype import beartype

from flet.control import BorderStyle, Control
from flet.ref import Ref

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
        control: Control = None,
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
            alignment=alignment,
            bgcolor=bgcolor,
            border_color=border_color,
            border_width=border_width,
            border_style=border_style,
            border_radius=border_radius,
        )

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

    # control
    @property
    def property(self):
        return self.__control

    @property.setter
    def controls(self, value):
        self.__control = value

    def _get_children(self):
        if self.__control == None:
            raise Exception("Container does not have a child control set.")
        return [self.__control]
