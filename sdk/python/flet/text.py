from typing import Optional

from beartype import beartype

from flet.control import Control, TextAlign, TextSize
from flet.ref import Ref

try:
    from typing import Literal
except:
    from typing_extensions import Literal

FontWeight = Literal[
    None,
    "normal",
    "bold",
    "w100",
    "w200",
    "w300",
    "w400",
    "w500",
    "w600",
    "w700",
    "w800",
    "w900",
]

TextOverflow = Literal[None, "clip", "ellipsis", "fade", "visible"]

VerticalAlign = Literal[None, "top", "center", "bottom"]


class Text(Control):
    def __init__(
        self,
        value: str = None,
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
        # text-specific
        #
        text_align: TextAlign = None,
        size: float = None,
        weight: FontWeight = None,
        italic: bool = None,
        themeStyle: str = None,
        overflow: TextOverflow = None,
        selectable: bool = None,
        color=None,
        bgcolor=None,
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

        self.value = value
        self.text_align = text_align
        self.size = size
        self.weight = weight
        self.italic = italic
        self.themeStyle = themeStyle
        self.overflow = overflow
        self.selectable = selectable
        self.color = color
        self.bgcolor = bgcolor

    def _get_control_name(self):
        return "text"

    # value
    @property
    def value(self):
        return self._get_attr("value")

    @value.setter
    def value(self, value):
        self._set_attr("value", value)

    # text_align
    @property
    def text_align(self):
        return self._get_attr("textAlign")

    @text_align.setter
    @beartype
    def text_align(self, value: TextAlign):
        self._set_attr("textAlign", value)

    # size
    @property
    def size(self):
        return self._get_attr("size")

    @size.setter
    @beartype
    def size(self, value: Optional[float]):
        self._set_attr("size", value)

    # weight
    @property
    def weight(self):
        return self._get_attr("weight")

    @weight.setter
    @beartype
    def weight(self, value: FontWeight):
        self._set_attr("weight", value)

    # theme_style
    @property
    def theme_style(self):
        return self._get_attr("themeStyle")

    @theme_style.setter
    @beartype
    def theme_style(self, value: Optional[str]):
        self._set_attr("themeStyle", value)

    # italic
    @property
    def italic(self):
        return self._get_attr("italic", data_type="bool", def_value=False)

    @italic.setter
    @beartype
    def italic(self, value: Optional[bool]):
        self._set_attr("italic", value)

    # selectable
    @property
    def selectable(self):
        return self._get_attr("selectable", data_type="bool", def_value=False)

    @selectable.setter
    @beartype
    def selectable(self, value: Optional[bool]):
        self._set_attr("v", value)

    # overflow
    @property
    def overflow(self):
        return self._get_attr("overflow")

    @overflow.setter
    @beartype
    def overflow(self, value: TextOverflow):
        self._set_attr("overflow", value)

    # color
    @property
    def color(self):
        return self._get_attr("color")

    @color.setter
    def color(self, value):
        self._set_attr("color", value)

    # bgcolor
    @property
    def bgcolor(self):
        return self._get_attr("bgcolor")

    @bgcolor.setter
    def bgcolor(self, value):
        self._set_attr("bgcolor", value)
