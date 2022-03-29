from typing import Optional

from beartype import beartype

from flet.control import Control

try:
    from typing import Literal
except:
    from typing_extensions import Literal


class SplitStack(Control):
    def __init__(
        self,
        controls=None,
        id=None,
        ref=None,
        horizontal=None,
        gutter_size=None,
        gutter_color=None,
        gutter_hover_color=None,
        gutter_drag_color=None,
        on_resize=None,
        width=None,
        height=None,
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
            visible=visible,
            disabled=disabled,
            data=data,
        )

        self.horizontal = horizontal
        self.gutter_size = gutter_size
        self.gutter_color = gutter_color
        self.gutter_hover_color = gutter_hover_color
        self.gutter_drag_color = gutter_drag_color
        self.on_resize = on_resize

        self.__controls = []
        if controls != None:
            for control in controls:
                self.__controls.append(control)

    def _get_control_name(self):
        return "splitstack"

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

    # gutter_size
    @property
    def gutter_size(self):
        return self._get_attr("guttersize")

    @gutter_size.setter
    @beartype
    def gutter_size(self, value: Optional[int]):
        self._set_attr("guttersize", value)

    # gutter_color
    @property
    def gutter_color(self):
        return self._get_attr("guttercolor")

    @gutter_color.setter
    def gutter_color(self, value):
        self._set_attr("guttercolor", value)

    # gutter_hover_color
    @property
    def gutter_hover_color(self):
        return self._get_attr("gutterhovercolor")

    @gutter_hover_color.setter
    def gutter_hover_color(self, value):
        self._set_attr("gutterhovercolor", value)

    # gutter_drag_color
    @property
    def gutter_drag_color(self):
        return self._get_attr("gutterdragcolor")

    @gutter_drag_color.setter
    def gutter_drag_color(self, value):
        self._set_attr("gutterdragcolor", value)

    def _get_children(self):
        return self.__controls

    # on_resize
    @property
    def on_resize(self):
        return self._get_event_handler("resize")

    @on_resize.setter
    def on_resize(self, handler):
        self._add_event_handler("resize", handler)
