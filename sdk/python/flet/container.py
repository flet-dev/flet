from typing import Optional, Union

from beartype import beartype

from flet.alignment import Alignment
from flet.border import Border
from flet.constrained_control import ConstrainedControl
from flet.control import Control, OptionalNumber
from flet.gradients import Gradient
from flet.ref import Ref
from flet.types import BorderRadiusValue, MarginValue, PaddingValue

try:
    from typing import Literal
except:
    from typing_extensions import Literal


class Container(ConstrainedControl):
    def __init__(
        self,
        content: Control = None,
        ref: Ref = None,
        width: OptionalNumber = None,
        height: OptionalNumber = None,
        left: OptionalNumber = None,
        top: OptionalNumber = None,
        right: OptionalNumber = None,
        bottom: OptionalNumber = None,
        expand: Union[bool, int] = None,
        opacity: OptionalNumber = None,
        tooltip: str = None,
        visible: bool = None,
        disabled: bool = None,
        data: any = None,
        #
        # Specific
        #
        padding: PaddingValue = None,
        margin: MarginValue = None,
        alignment: Alignment = None,
        bgcolor: str = None,
        gradient: Gradient = None,
        border: Border = None,
        border_radius: BorderRadiusValue = None,
        ink: bool = None,
        on_click=None,
        on_long_press=None,
    ):
        ConstrainedControl.__init__(
            self,
            ref=ref,
            width=width,
            height=height,
            left=left,
            top=top,
            right=right,
            bottom=bottom,
            expand=expand,
            opacity=opacity,
            tooltip=tooltip,
            visible=visible,
            disabled=disabled,
            data=data,
        )

        self.content = content
        self.padding = padding
        self.margin = margin
        self.alignment = alignment
        self.bgcolor = bgcolor
        self.gradient = gradient
        self.border = border
        self.border_radius = border_radius
        self.ink = ink
        self.on_click = on_click
        self.on_long_press = on_long_press

    def _get_control_name(self):
        return "container"

    def _before_build_command(self):
        self._set_attr_json("borderRadius", self.__border_radius)
        self._set_attr_json("border", self.__border)
        self._set_attr_json("margin", self.__margin)
        self._set_attr_json("padding", self.__padding)
        self._set_attr_json("alignment", self.__alignment)
        self._set_attr_json("gradient", self.__gradient)

    def _get_children(self):
        children = []
        if self.__content != None:
            self.__content._set_attr_internal("n", "content")
            children.append(self.__content)
        return children

    # alignment
    @property
    def alignment(self):
        return self.__alignment

    @alignment.setter
    @beartype
    def alignment(self, value: Optional[Alignment]):
        self.__alignment = value

    # padding
    @property
    def padding(self):
        return self.__padding

    @padding.setter
    @beartype
    def padding(self, value: PaddingValue):
        self.__padding = value

    # margin
    @property
    def margin(self):
        return self.__margin

    @margin.setter
    @beartype
    def margin(self, value: MarginValue):
        self.__margin = value

    # bgcolor
    @property
    def bgcolor(self):
        return self._get_attr("bgColor")

    @bgcolor.setter
    def bgcolor(self, value):
        self._set_attr("bgColor", value)

    # gradient
    @property
    def gradient(self):
        return self.__gradient

    @gradient.setter
    @beartype
    def gradient(self, value: Optional[Gradient]):
        self.__gradient = value

    # border
    @property
    def border(self):
        return self.__border

    @border.setter
    @beartype
    def border(self, value: Optional[Border]):
        self.__border = value

    # border_radius
    @property
    def border_radius(self):
        return self.__border_radius

    @border_radius.setter
    @beartype
    def border_radius(self, value: BorderRadiusValue):
        self.__border_radius = value

    # content
    @property
    def content(self):
        return self.__content

    @content.setter
    @beartype
    def content(self, value: Optional[Control]):
        self.__content = value

    # ink
    @property
    def ink(self):
        return self._get_attr("ink", data_type="bool", def_value=False)

    @ink.setter
    @beartype
    def ink(self, value: Optional[bool]):
        self._set_attr("ink", value)

    # on_click
    @property
    def on_click(self):
        return self._get_event_handler("click")

    @on_click.setter
    def on_click(self, handler):
        self._add_event_handler("click", handler)
        if handler != None:
            self._set_attr("onclick", True)
        else:
            self._set_attr("onclick", None)

    # on_long_press
    @property
    def on_long_press(self):
        return self._get_event_handler("long_press")

    @on_long_press.setter
    def on_long_press(self, handler):
        self._add_event_handler("long_press", handler)
        if handler != None:
            self._set_attr("onLongPress", True)
        else:
            self._set_attr("onLongPress", None)
