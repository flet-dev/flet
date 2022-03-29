from typing import Optional

from beartype import beartype
from flet.control import BorderColor
from flet.control import BorderRadius
from flet.control import BorderStyle
from flet.control import BorderWidth
from flet.control import Control

try:
    from typing import Literal
except:
    from typing_extensions import Literal


Align = Literal[
    None,
    "start",
    "end",
    "center",
    "space-between",
    "space-around",
    "space-evenly",
    "baseline",
    "stretch",
]


class Stack(Control):
    def __init__(
        self,
        controls=None,
        id=None,
        ref=None,
        horizontal=None,
        vertical_fill=None,
        horizontal_align: Align = None,
        vertical_align: Align = None,
        min_width=None,
        max_width=None,
        min_height=None,
        max_height=None,
        gap=None,
        wrap=None,
        bgcolor=None,
        border_style: BorderStyle = None,
        border_width: BorderWidth = None,
        border_color: BorderColor = None,
        border_radius: BorderRadius = None,
        scroll_x=None,
        scroll_y=None,
        auto_scroll=None,
        on_submit=None,
        width=None,
        height=None,
        padding=None,
        margin=None,
        visible=None,
        disabled=None,
        data=None,
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
            data=data,
        )

        self.horizontal = horizontal
        self.vertical_fill = vertical_fill
        self.horizontal_align = horizontal_align
        self.vertical_align = vertical_align
        self.min_width = min_width
        self.max_width = max_width
        self.min_height = min_height
        self.max_height = max_height
        self.gap = gap
        self.wrap = wrap
        self.bgcolor = bgcolor
        self.border_style = border_style
        self.border_width = border_width
        self.border_color = border_color
        self.border_radius = border_radius
        self.scroll_x = scroll_x
        self.scroll_y = scroll_y
        self.auto_scroll = auto_scroll
        self.on_submit = on_submit

        self.__controls = []
        if controls != None:
            for control in controls:
                self.__controls.append(control)

    def _get_control_name(self):
        return "stack"

    def clean(self):
        Control.clean(self)
        self.__controls.clear()

    # controls
    @property
    def controls(self):
        return self.__controls

    @controls.setter
    def controls(self, value):
        self.__controls = value

    # horizontal
    @property
    def horizontal(self):
        return self._get_attr("horizontal", data_type="bool", def_value=False)

    @horizontal.setter
    @beartype
    def horizontal(self, value: Optional[bool]):
        self._set_attr("horizontal", value)

    # vertical_fill
    @property
    def vertical_fill(self):
        return self._get_attr("verticalFill", data_type="bool", def_value=False)

    @vertical_fill.setter
    @beartype
    def vertical_fill(self, value: Optional[bool]):
        self._set_attr("verticalFill", value)

    # horizontal_align
    @property
    def horizontal_align(self):
        return self._get_attr("horizontalAlign")

    @horizontal_align.setter
    @beartype
    def horizontal_align(self, value: Align):
        self._set_attr("horizontalAlign", value)

    # vertical_align
    @property
    def vertical_align(self):
        return self._get_attr("verticalAlign")

    @vertical_align.setter
    @beartype
    def vertical_align(self, value: Align):
        self._set_attr("verticalAlign", value)

    # min_width
    @property
    def min_width(self):
        return self._get_attr("minWidth")

    @min_width.setter
    def min_width(self, value):
        self._set_attr("minWidth", value)

    # max_width
    @property
    def max_width(self):
        return self._get_attr("maxWidth")

    @max_width.setter
    def max_width(self, value):
        self._set_attr("maxWidth", value)

    # min_height
    @property
    def min_height(self):
        return self._get_attr("minHeight")

    @min_height.setter
    def min_height(self, value):
        self._set_attr("minHeight", value)

    # max_height
    @property
    def max_height(self):
        return self._get_attr("maxHeight")

    @max_height.setter
    def max_height(self, value):
        self._set_attr("maxHeight", value)

    # gap
    @property
    def gap(self):
        return self._get_attr("gap")

    @gap.setter
    def gap(self, value):
        self._set_attr("gap", value)

    # wrap
    @property
    def wrap(self):
        return self._get_attr("wrap", data_type="bool", def_value=False)

    @wrap.setter
    @beartype
    def wrap(self, value: Optional[bool]):
        self._set_attr("wrap", value)

    # bgcolor
    @property
    def bgcolor(self):
        return self._get_attr("bgcolor")

    @bgcolor.setter
    def bgcolor(self, value):
        self._set_attr("bgcolor", value)

    # border_style
    @property
    def border_style(self):
        return self._get_value_or_list_attr("borderStyle", " ")

    @border_style.setter
    @beartype
    def border_style(self, value: BorderStyle):
        self._set_value_or_list_attr("borderStyle", value, " ")

    # border_width
    @property
    def border_width(self):
        return self._get_value_or_list_attr("borderWidth", " ")

    @border_width.setter
    @beartype
    def border_width(self, value: BorderWidth):
        self._set_value_or_list_attr("borderWidth", value, " ")

    # border_color
    @property
    def border_color(self):
        return self._get_value_or_list_attr("borderColor", " ")

    @border_color.setter
    @beartype
    def border_color(self, value: BorderColor):
        self._set_value_or_list_attr("borderColor", value, " ")

    # border_radius
    @property
    def border_radius(self):
        return self._get_value_or_list_attr("borderRadius", " ")

    @border_radius.setter
    @beartype
    def border_radius(self, value: BorderRadius):
        self._set_value_or_list_attr("borderRadius", value, " ")

    # scroll_x
    @property
    def scroll_x(self):
        return self._get_attr("scrollx", data_type="bool", def_value=False)

    @scroll_x.setter
    @beartype
    def scroll_x(self, value: Optional[bool]):
        self._set_attr("scrollx", value)

    # scroll_y
    @property
    def scroll_y(self):
        return self._get_attr("scrolly", data_type="bool", def_value=False)

    @scroll_y.setter
    @beartype
    def scroll_y(self, value: Optional[bool]):
        self._set_attr("scrolly", value)

    # auto_scroll
    @property
    def auto_scroll(self):
        return self._get_attr("autoscroll", data_type="bool", def_value=False)

    @auto_scroll.setter
    @beartype
    def auto_scroll(self, value: Optional[bool]):
        self._set_attr("autoscroll", value)

    # on_submit
    @property
    def on_submit(self):
        return self._get_event_handler("submit")

    @on_submit.setter
    def on_submit(self, handler):
        self._add_event_handler("submit", handler)
        if handler != None:
            self._set_attr("onsubmit", True)
        else:
            self._set_attr("onsubmit", None)

    def _get_children(self):
        return self.__controls
