import time
from typing import Any, Dict, List, Optional, Union, Sequence

from flet_core.border import BorderSide
from flet_core.buttons import OutlinedBorder
from flet_core.constrained_control import ConstrainedControl
from flet_core.control import Control
from flet_core.ref import Ref
from flet_core.text_style import TextStyle
from flet_core.textfield import KeyboardType, TextCapitalization
from flet_core.tooltip import TooltipValue
from flet_core.types import (
    AnimationValue,
    ControlState,
    OffsetValue,
    OptionalNumber,
    ResponsiveNumber,
    RotateValue,
    ScaleValue,
    OptionalControlEventCallable,
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
        controls: Optional[Sequence[Control]] = None,
        value: Optional[str] = None,
        bar_leading: Optional[Control] = None,
        bar_trailing: Optional[List[Control]] = None,
        bar_hint_text: Optional[str] = None,
        bar_bgcolor: Union[None, str, Dict[ControlState, str]] = None,
        bar_overlay_color: Union[None, str, Dict[ControlState, str]] = None,
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
        capitalization: Optional[TextCapitalization] = None,
        full_screen: Optional[bool] = None,
        keyboard_type: Optional[KeyboardType] = None,
        view_surface_tint_color: Optional[str] = None,
        autofocus: Optional[bool] = None,
        on_tap: OptionalControlEventCallable = None,
        on_submit: OptionalControlEventCallable = None,
        on_change: OptionalControlEventCallable = None,
        on_focus: OptionalControlEventCallable = None,
        on_blur: OptionalControlEventCallable = None,
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
        on_animation_end: OptionalControlEventCallable = None,
        tooltip: TooltipValue = None,
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
        self.on_focus = on_focus
        self.on_blur = on_blur
        self.on_tap = on_tap
        self.on_submit = on_submit
        self.on_change = on_change
        self.keyboard_type = keyboard_type
        self.view_surface_tint_color = view_surface_tint_color
        self.autofocus = autofocus

    def _get_control_name(self):
        return "searchbar"

    def before_update(self):
        super().before_update()
        self._set_attr_json("barBgcolor", self.__bar_bgcolor)
        self._set_attr_json("barOverlayColor", self.__bar_overlay_color)
        self._set_attr_json("viewShape", self.__view_shape)
        if isinstance(self.__view_header_text_style, TextStyle):
            self._set_attr_json("viewHeaderTextStyle", self.__view_header_text_style)
        if isinstance(self.__view_hint_text_style, TextStyle):
            self._set_attr_json("viewHintTextStyle", self.__view_hint_text_style)
        if isinstance(self.__view_side, BorderSide):
            self._set_attr_json("viewSide", self.__view_side)

    def _get_children(self):
        children = []
        if self.__bar_leading:
            self.__bar_leading._set_attr_internal("n", "barLeading")
            children.append(self.__bar_leading)
        if self.__view_leading:
            self.__view_leading._set_attr_internal("n", "viewLeading")
            children.append(self.__view_leading)
        for i in self.__bar_trailing:
            i._set_attr_internal("n", "barTrailing")
            children.append(i)
        for i in self.__view_trailing:
            i._set_attr_internal("n", "viewTrailing")
            children.append(i)
        for i in self.__controls:
            i._set_attr_internal("n", "controls")
            children.append(i)
        return children

    # Public methods
    def focus(self):
        self._set_attr_json("focus", str(time.time()))
        self.update()

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
        delete_version="0.26.0",
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
        delete_version="0.26.0",
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
        self.__bar_trailing = value if value is not None else []

    # bar_bgcolor
    @property
    def bar_bgcolor(self) -> Union[None, str, Dict[ControlState, str]]:
        return self.__bar_bgcolor

    @bar_bgcolor.setter
    def bar_bgcolor(self, value: Union[None, str, Dict[ControlState, str]]):
        self.__bar_bgcolor = value

    # bar_overlay_color
    @property
    def bar_overlay_color(self) -> Union[None, str, Dict[ControlState, str]]:
        return self.__bar_overlay_color

    @bar_overlay_color.setter
    def bar_overlay_color(self, value: Union[None, str, Dict[ControlState, str]]):
        self.__bar_overlay_color = value

    # view_leading
    @property
    def view_leading(self) -> Optional[Control]:
        return self.__view_leading

    @view_leading.setter
    def view_leading(self, value: Optional[Control]):
        self.__view_leading = value

    # view_surface_tint_color
    @property
    def view_surface_tint_color(self) -> Optional[str]:
        return self._get_attr("viewSurfaceTintColor")

    @view_surface_tint_color.setter
    def view_surface_tint_color(self, value: Optional[str]):
        self._set_attr("viewSurfaceTintColor", value)

    # autofocus
    @property
    def autofocus(self) -> bool:
        return self._get_attr("autofocus", data_type="bool", def_value=False)

    @autofocus.setter
    def autofocus(self, value: Optional[bool]):
        self._set_attr("autofocus", value)

    # view_trailing
    @property
    def view_trailing(self) -> Optional[List[Control]]:
        return self.__view_trailing

    @view_trailing.setter
    def view_trailing(self, value: Optional[List[Control]]):
        self.__view_trailing = value if value is not None else []

    # view_elevation
    @property
    def view_elevation(self) -> OptionalNumber:
        return self._get_attr("viewElevation")

    @view_elevation.setter
    def view_elevation(self, value: OptionalNumber):
        self._set_attr("viewElevation", value)

    # view_bgcolor
    @property
    def view_bgcolor(self) -> Optional[str]:
        return self._get_attr("viewBgcolor")

    @view_bgcolor.setter
    def view_bgcolor(self, value: Optional[str]):
        self._set_attr("viewBgcolor", value)

    # divider_color
    @property
    def divider_color(self) -> Optional[str]:
        return self._get_attr("dividerColor")

    @divider_color.setter
    def divider_color(self, value: Optional[str]):
        self._set_attr("dividerColor", value)

    # bar_hint_text
    @property
    def bar_hint_text(self) -> Optional[str]:
        return self._get_attr("barHintText")

    @bar_hint_text.setter
    def bar_hint_text(self, value: Optional[str]):
        self._set_attr("barHintText", value)

    # view_hint_text
    @property
    def view_hint_text(self) -> Optional[str]:
        return self._get_attr("viewHintText")

    @view_hint_text.setter
    def view_hint_text(self, value: Optional[str]):
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
    def full_screen(self) -> bool:
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
        self._set_enum_attr("capitalization", value, TextCapitalization)

    # keyboard_type
    @property
    def keyboard_type(self) -> KeyboardType:
        return self.__keyboard_type

    @keyboard_type.setter
    def keyboard_type(self, value: KeyboardType):
        self.__keyboard_type = value
        self._set_enum_attr("keyboardType", value, KeyboardType)

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
    def controls(self, value: Optional[Sequence[Control]]):
        self.__controls = list(value) if value is not None else []

    # value
    @property
    def value(self) -> Optional[str]:
        return self._get_attr("value", def_value="")

    @value.setter
    def value(self, value: Optional[str]):
        self._set_attr("value", value)

    # on_change
    @property
    def on_change(self) -> OptionalControlEventCallable:
        return self._get_event_handler("change")

    @on_change.setter
    def on_change(self, handler: OptionalControlEventCallable):
        self._add_event_handler("change", handler)
        self._set_attr("onchange", True if handler is not None else None)

    # on_focus
    @property
    def on_focus(self) -> OptionalControlEventCallable:
        return self._get_event_handler("focus")

    @on_focus.setter
    def on_focus(self, handler: OptionalControlEventCallable):
        self._add_event_handler("focus", handler)

    # on_blur
    @property
    def on_blur(self) -> OptionalControlEventCallable:
        return self._get_event_handler("blur")

    @on_blur.setter
    def on_blur(self, handler: OptionalControlEventCallable):
        self._add_event_handler("blur", handler)

    # on_tap
    @property
    def on_tap(self) -> OptionalControlEventCallable:
        return self._get_event_handler("tap")

    @on_tap.setter
    def on_tap(self, handler: OptionalControlEventCallable):
        self._add_event_handler("tap", handler)
        self._set_attr("ontap", True if handler is not None else None)

    # on_submit
    @property
    def on_submit(self) -> OptionalControlEventCallable:
        return self._get_event_handler("submit")

    @on_submit.setter
    def on_submit(self, handler: OptionalControlEventCallable):
        self._add_event_handler("submit", handler)
        self._set_attr("onsubmit", True if handler is not None else None)
