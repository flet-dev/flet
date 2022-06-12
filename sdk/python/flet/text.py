from typing import Optional, Union

from beartype import beartype

from flet.constrained_control import ConstrainedControl
from flet.control import OptionalNumber, TextAlign
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


class Text(ConstrainedControl):
    def __init__(
        self,
        value: str = None,
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
        # text-specific
        #
        text_align: TextAlign = None,
        font_family: str = None,
        size: OptionalNumber = None,
        weight: FontWeight = None,
        italic: bool = None,
        style: str = None,
        max_lines: int = None,
        overflow: TextOverflow = None,
        selectable: bool = None,
        no_wrap: bool = None,
        color: str = None,
        bgcolor: str = None,
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

        self.value = value
        self.text_align = text_align
        self.font_family = font_family
        self.size = size
        self.weight = weight
        self.italic = italic
        self.no_wrap = no_wrap
        self.style = style
        self.max_lines = max_lines
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

    # font_family
    @property
    def font_family(self):
        return self._get_attr("fontFamily")

    @font_family.setter
    def font_family(self, value):
        self._set_attr("fontFamily", value)

    # size
    @property
    def size(self):
        return self._get_attr("size")

    @size.setter
    @beartype
    def size(self, value: OptionalNumber):
        self._set_attr("size", value)

    # weight
    @property
    def weight(self):
        return self._get_attr("weight")

    @weight.setter
    @beartype
    def weight(self, value: FontWeight):
        self._set_attr("weight", value)

    # style
    @property
    def style(self):
        return self._get_attr("style")

    @style.setter
    @beartype
    def style(self, value: Optional[str]):
        self._set_attr("style", value)

    # italic
    @property
    def italic(self):
        return self._get_attr("italic", data_type="bool", def_value=False)

    @italic.setter
    @beartype
    def italic(self, value: Optional[bool]):
        self._set_attr("italic", value)

    # no_wrap
    @property
    def no_wrap(self):
        return self._get_attr("italic", data_type="noWrap", def_value=False)

    @no_wrap.setter
    @beartype
    def no_wrap(self, value: Optional[bool]):
        self._set_attr("noWrap", value)

    # selectable
    @property
    def selectable(self):
        return self._get_attr("selectable", data_type="bool", def_value=False)

    @selectable.setter
    @beartype
    def selectable(self, value: Optional[bool]):
        self._set_attr("selectable", value)

    # max_lines
    @property
    def max_lines(self):
        return self._get_attr("maxLines")

    @max_lines.setter
    @beartype
    def max_lines(self, value: Optional[int]):
        self._set_attr("maxLines", value)

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
