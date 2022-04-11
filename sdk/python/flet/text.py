from typing import Optional

from beartype import beartype

from flet.control import Control, TextAlign, TextSize

try:
    from typing import Literal
except:
    from typing_extensions import Literal


VerticalAlign = Literal[None, "top", "center", "bottom"]


class Text(Control):
    def __init__(
        self,
        value=None,
        id=None,
        ref=None,
        markdown=None,
        align: TextAlign = None,
        vertical_align: VerticalAlign = None,
        size: TextSize = None,
        bold=None,
        italic=None,
        pre=None,
        nowrap=None,
        block=None,
        color=None,
        bgcolor=None,
        width=None,
        height=None,
        padding=None,
        margin=None,
        visible=None,
        disabled=None,
    ):

        Control.__init__(
            self,
            id=id,
            ref=ref,
            width=width,
            height=height,
            padding=padding,
            margin=margin,
            visible=visible,
            disabled=disabled,
        )

        self.value = value
        self.markdown = markdown
        self.align = align
        self.vertical_align = vertical_align
        self.size = size
        self.bold = bold
        self.italic = italic
        self.pre = pre
        self.nowrap = nowrap
        self.block = block
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

    # markdown
    @property
    def markdown(self):
        return self._get_attr("markdown", data_type="bool", def_value=False)

    @markdown.setter
    @beartype
    def markdown(self, value: Optional[bool]):
        self._set_attr("markdown", value)

    # align
    @property
    def align(self):
        return self._get_attr("align")

    @align.setter
    @beartype
    def align(self, value: TextAlign):
        self._set_attr("align", value)

    # vertical_align
    @property
    def vertical_align(self):
        return self._get_attr("verticalAlign")

    @vertical_align.setter
    @beartype
    def vertical_align(self, value: VerticalAlign):
        self._set_attr("verticalAlign", value)

    # size
    @property
    def size(self):
        return self._get_attr("size")

    @size.setter
    @beartype
    def size(self, value: TextSize):
        self._set_attr("size", value)

    # bold
    @property
    def bold(self):
        return self._get_attr("bold", data_type="bool", def_value=False)

    @bold.setter
    @beartype
    def bold(self, value: Optional[bool]):
        self._set_attr("bold", value)

    # italic
    @property
    def italic(self):
        return self._get_attr("italic", data_type="bool", def_value=False)

    @italic.setter
    @beartype
    def italic(self, value: Optional[bool]):
        self._set_attr("italic", value)

    # pre
    @property
    def pre(self):
        return self._get_attr("pre", data_type="bool", def_value=False)

    @pre.setter
    @beartype
    def pre(self, value: Optional[bool]):
        self._set_attr("pre", value)

    # nowrap
    @property
    def nowrap(self):
        return self._get_attr("nowrap", data_type="bool", def_value=False)

    @nowrap.setter
    @beartype
    def nowrap(self, value: Optional[bool]):
        self._set_attr("nowrap", value)

    # block
    @property
    def block(self):
        return self._get_attr("block", data_type="bool", def_value=False)

    @block.setter
    @beartype
    def block(self, value: Optional[bool]):
        self._set_attr("block", value)

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
