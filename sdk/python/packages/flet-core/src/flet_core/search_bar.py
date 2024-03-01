import time
from typing import Any, Dict, List, Optional, Union

from flet_core import BorderSide, OutlinedBorder
from flet_core.constrained_control import ConstrainedControl
from flet_core.control import Control, OptionalNumber
from flet_core.ref import Ref
from flet_core.text_style import TextStyle
from flet_core.textfield import TextCapitalization
from flet_core.types import (
    AnimationValue,
    MaterialState,
    OffsetValue,
    ResponsiveNumber,
    RotateValue,
    ScaleValue,
)
from flet_core.utils import deprecated


class SearchBar(ConstrainedControl):
    """
    Manages a "search view" route that allows the user to select one of the suggested completions for a search query.

    -----

    Online docs: https://flet.dev/docs/controls/searchbar
    """

    def __init__(
        self,
        controls: Optional[List[Control]] = None,
        value: Optional[str] = None,
        bar_leading: Optional[Control] = None,
        bar_trailing: Optional[List[Control]] = None,
        bar_hint_text: Optional[str] = None,
        bar_bgcolor: Union[None, str, Dict[MaterialState, str]] = None,
        bar_overlay_color: Union[None, str, Dict[MaterialState, str]] = None,
        view_leading: Optional[Control] = None,
        view_trailing: Optional[List[Control]] = None,
        view_elevation: OptionalNumber = None,
        view_bgcolor: Optional[str] = None,
        view_hint_text: Optional[str] = None,
        view_side: Optional[BorderSide] = None,
        view_shape: Optional[OutlinedBorder] = None,
        view_header_text_style: Optional[TextStyle] = None,
        view_hint_text_style: Optional[TextStyle] = None,
        divider_color: Optional[str] = None,
        full_screen: Optional[bool] = None,
        capitalization: TextCapitalization = TextCapitalization.NONE,
        on_tap=None,
        on_submit=None,
        on_change=None,
        #
        # ConstrainedControl
        #
        ref: Optional[Ref] = None,
        key: Optional[str] = None,
        width: OptionalNumber = None,
        height: OptionalNumber = None,
        expand: Union[None, bool, int] = None,
        expand_loose: Optional[bool] = None,
        col: Optional[ResponsiveNumber] = None,
        opacity: OptionalNumber = None,
        rotate: RotateValue = None,
        scale: ScaleValue = None,
        offset: OffsetValue = None,
        aspect_ratio: OptionalNumber = None,
        animate_opacity: AnimationValue = None,
        animate_size: AnimationValue = None,
        animate_position: AnimationValue = None,
        animate_rotation: AnimationValue = None,
        animate_scale: AnimationValue = None,
        animate_offset: AnimationValue = None,
        on_animation_end=None,
        tooltip: Optional[str] = None,
        visible: Optional[bool] = None,
        disabled: Optional[bool] = None,
        data: Any = None,
    ):
        ConstrainedControl.__init__(
            self,
            ref=ref,
            key=key,
            width=width,
            height=height,
            expand=expand,
            expand_loose=expand_loose,
            col=col,
            opacity=opacity,
            rotate=rotate,
            scale=scale,
            offset=offset,
            aspect_ratio=aspect_ratio,
            animate_opacity=animate_opacity,
            animate_size=animate_size,
            animate_position=animate_position,
            animate_rotation=animate_rotation,
            animate_scale=animate_scale,
            animate_offset=animate_offset,
            on_animation_end=on_animation_end,
            tooltip=tooltip,
            visible=visible,
            disabled=disabled,
            data=data,
        )

        self.value = value
        self.controls = controls
        self.bar_leading = bar_leading
        self.bar_trailing = bar_trailing
        self.bar_hint_text = bar_hint_text
        self.bar_bgcolor = bar_bgcolor
        self.bar_overlay_color = bar_overlay_color
        self.view_leading = view_leading
        self.view_trailing = view_trailing
        self.view_elevation = view_elevation
        self.view_bgcolor = view_bgcolor
        self.view_hint_text = view_hint_text
        self.view_side = view_side
        self.view_shape = view_shape
        self.view_header_text_style = view_header_text_style
        self.view_hint_text_style = view_hint_text_style
        self.divider_color = divider_color
        self.full_screen = full_screen
        self.capitalization = capitalization
        self.on_tap = on_tap
        self.on_submit = on_submit
        self.on_change = on_change

    def _get_control_name(self):
        return "searchbar"

    def before_update(self):
        super().before_update()
        self._set_attr_json("barBgcolor", self.__bar_bgcolor)
        self._set_attr_json("barOverlayColor", self.__bar_overlay_color)
        self._set_attr_json("viewShape", self.__view_shape)
        self._set_attr_json("viewHeaderTextStyle", self.__view_header_text_style)
        self._set_attr_json("viewHintTextStyle", self.__view_hint_text_style)
        self._set_attr_json("viewSide", self.__view_side)

    def _get_children(self):
        children = []
        if self.__bar_leading:
            self.__bar_leading._set_attr_internal("n", "barLeading")
            children.append(self.__bar_leading)
        if self.__view_leading:
            self.__view_leading._set_attr_internal("n", "viewLeading")
            children.append(self.__view_leading)
        if self.__bar_trailing:
            for i in self.__bar_trailing:
                i._set_attr_internal("n", "barTrailing")
                children.append(i)
        if self.__view_trailing:
            for i in self.__view_trailing:
                i._set_attr_internal("n", "viewTrailing")
                children.append(i)
        if self.__controls:
            for i in self.__controls:
                i._set_attr_internal("n", "controls")
                children.append(i)
        return children

    def open_view(self):
        m = {
            "n": "openView",
            "i": str(time.time()),
            "p": {},
        }
        self._set_attr_json("method", m)
        self.update()

    @deprecated(
        reason="Use open_view() method instead.",
        version="0.21.0",
        delete_version="1.0",
    )
    async def open_view_async(self):
        self.open_view()

    def close_view(self, text: str = ""):
        m = {
            "n": "closeView",
            "i": str(time.time()),
            "p": {"text": text},
        }
        self.value = text
        self._set_attr_json("method", m)
        self.update()

    @deprecated(
        reason="Use close_view() method instead.",
        version="0.21.0",
        delete_version="1.0",
    )
    async def close_view_async(self, text: str = ""):
        self.close_view(text=text)

    # bar_leading
    @property
    def bar_leading(self) -> Optional[Control]:
        return self.__bar_leading

    @bar_leading.setter
    def bar_leading(self, value: Optional[Control]):
        self.__bar_leading = value

    # bar_trailing
    @property
    def bar_trailing(self) -> Optional[List[Control]]:
        return self.__bar_trailing

    @bar_trailing.setter
    def bar_trailing(self, value: Optional[List[Control]]):
        self.__bar_trailing = value

    # bar_bgcolor
    @property
    def bar_bgcolor(self) -> Union[None, str, Dict[MaterialState, str]]:
        return self.__bar_bgcolor

    @bar_bgcolor.setter
    def bar_bgcolor(self, value: Union[None, str, Dict[MaterialState, str]]):
        self.__bar_bgcolor = value

    # bar_overlay_color
    @property
    def bar_overlay_color(self) -> Union[None, str, Dict[MaterialState, str]]:
        return self.__bar_overlay_color

    @bar_overlay_color.setter
    def bar_overlay_color(self, value: Union[None, str, Dict[MaterialState, str]]):
        self.__bar_overlay_color = value

    # view_leading
    @property
    def view_leading(self) -> Optional[Control]:
        return self.__view_leading

    @view_leading.setter
    def view_leading(self, value: Optional[Control]):
        self.__view_leading = value

    # view_trailing
    @property
    def view_trailing(self) -> Optional[List[Control]]:
        return self.__view_trailing

    @view_trailing.setter
    def view_trailing(self, value: Optional[List[Control]]):
        self.__view_trailing = value

    # view_elevation
    @property
    def view_elevation(self) -> OptionalNumber:
        return self._get_attr("viewElevation")

    @view_elevation.setter
    def view_elevation(self, value: OptionalNumber):
        self._set_attr("viewElevation", value)

    # view_bgcolor
    @property
    def view_bgcolor(self):
        return self._get_attr("viewBgcolor")

    @view_bgcolor.setter
    def view_bgcolor(self, value):
        self._set_attr("viewBgcolor", value)

    # divider_color
    @property
    def divider_color(self):
        return self._get_attr("dividerColor")

    @divider_color.setter
    def divider_color(self, value):
        self._set_attr("dividerColor", value)

    # bar_hint_text
    @property
    def bar_hint_text(self):
        return self._get_attr("barHintText")

    @bar_hint_text.setter
    def bar_hint_text(self, value):
        self._set_attr("barHintText", value)

    # view_hint_text
    @property
    def view_hint_text(self):
        return self._get_attr("viewHintText")

    @view_hint_text.setter
    def view_hint_text(self, value):
        self._set_attr("viewHintText", value)

    # view_shape
    @property
    def view_shape(self) -> Optional[OutlinedBorder]:
        return self.__view_shape

    @view_shape.setter
    def view_shape(self, value: Optional[OutlinedBorder]):
        self.__view_shape = value

    # view_side
    @property
    def view_side(self) -> Optional[BorderSide]:
        return self.__view_side

    @view_side.setter
    def view_side(self, value: Optional[BorderSide]):
        self.__view_side = value

    # full_screen
    @property
    def full_screen(self) -> Optional[bool]:
        return self._get_attr("fullScreen", data_type="bool", def_value=False)

    @full_screen.setter
    def full_screen(self, value: Optional[bool]):
        self._set_attr("fullScreen", value)

    # capitalization
    @property
    def capitalization(self) -> TextCapitalization:
        return self.__capitalization

    @capitalization.setter
    def capitalization(self, value: TextCapitalization):
        self.__capitalization = value
        self._set_attr(
            "capitalization",
            value.value if isinstance(value, TextCapitalization) else value,
        )

    # view_header_text_style
    @property
    def view_header_text_style(self):
        return self.__view_header_text_style

    @view_header_text_style.setter
    def view_header_text_style(self, value: Optional[TextStyle]):
        self.__view_header_text_style = value

    # view_hint_text_style
    @property
    def view_hint_text_style(self):
        return self.__view_hint_text_style

    @view_hint_text_style.setter
    def view_hint_text_style(self, value: Optional[TextStyle]):
        self.__view_hint_text_style = value

    # controls
    @property
    def controls(self):
        return self.__controls

    @controls.setter
    def controls(self, value: Optional[List[Control]]):
        self.__controls = value if value is not None else []

    # value
    @property
    def value(self) -> Optional[str]:
        return self._get_attr("value", def_value="")

    @value.setter
    def value(self, value: Optional[str]):
        self._set_attr("value", value)

    # on_change
    @property
    def on_change(self):
        return self._get_event_handler("change")

    @on_change.setter
    def on_change(self, handler):
        self._add_event_handler("change", handler)
        self._set_attr("onchange", True if handler is not None else None)

    # on_tap
    @property
    def on_tap(self):
        return self._get_event_handler("tap")

    @on_tap.setter
    def on_tap(self, handler):
        self._add_event_handler("tap", handler)
        self._set_attr("ontap", True if handler is not None else None)

    # on_submit
    @property
    def on_submit(self):
        return self._get_event_handler("submit")

    @on_submit.setter
    def on_submit(self, handler):
        self._add_event_handler("submit", handler)
        self._set_attr("onsubmit", True if handler is not None else None)
