import time
from typing import Any, Dict, List, Optional, Sequence, Union

from flet.core.animation import AnimationValue
from flet.core.badge import BadgeValue
from flet.core.border import BorderSide
from flet.core.box import BoxConstraints
from flet.core.buttons import OutlinedBorder
from flet.core.constrained_control import ConstrainedControl
from flet.core.control import Control
from flet.core.ref import Ref
from flet.core.text_style import TextStyle
from flet.core.textfield import KeyboardType, TextCapitalization
from flet.core.tooltip import TooltipValue
from flet.core.types import (
    ColorEnums,
    ColorValue,
    ControlState,
    ControlStateValue,
    Number,
    OffsetValue,
    OptionalControlEventCallable,
    OptionalNumber,
    PaddingValue,
    ResponsiveNumber,
    RotateValue,
    ScaleValue,
)


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
        bar_bgcolor: ControlStateValue[ColorValue] = None,
        bar_overlay_color: ControlStateValue[ColorValue] = None,
        bar_shadow_color: ControlStateValue[ColorValue] = None,
        bar_surface_tint_color: ControlStateValue[ColorValue] = None,
        bar_elevation: ControlStateValue[OptionalNumber] = None,
        bar_border_side: ControlStateValue[BorderSide] = None,
        bar_shape: ControlStateValue[OutlinedBorder] = None,
        bar_text_style: ControlStateValue[TextStyle] = None,
        bar_hint_text_style: ControlStateValue[TextStyle] = None,
        bar_padding: ControlStateValue[PaddingValue] = None,
        bar_scroll_padding: Optional[PaddingValue] = None,
        view_leading: Optional[Control] = None,
        view_trailing: Optional[List[Control]] = None,
        view_elevation: OptionalNumber = None,
        view_bgcolor: Optional[ColorValue] = None,
        view_hint_text: Optional[str] = None,
        view_side: Optional[BorderSide] = None,
        view_shape: Optional[OutlinedBorder] = None,
        view_header_text_style: Optional[TextStyle] = None,
        view_hint_text_style: Optional[TextStyle] = None,
        view_size_constraints: Optional[BoxConstraints] = None,
        view_header_height: OptionalNumber = None,
        divider_color: Optional[ColorValue] = None,
        capitalization: Optional[TextCapitalization] = None,
        full_screen: Optional[bool] = None,
        keyboard_type: Optional[KeyboardType] = None,
        view_surface_tint_color: Optional[ColorValue] = None,
        autofocus: Optional[bool] = None,
        on_tap: OptionalControlEventCallable = None,
        on_tap_outside_bar: OptionalControlEventCallable = None,
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
        rotate: Optional[RotateValue] = None,
        scale: Optional[ScaleValue] = None,
        offset: Optional[OffsetValue] = None,
        aspect_ratio: OptionalNumber = None,
        animate_opacity: Optional[AnimationValue] = None,
        animate_size: Optional[AnimationValue] = None,
        animate_position: Optional[AnimationValue] = None,
        animate_rotation: Optional[AnimationValue] = None,
        animate_scale: Optional[AnimationValue] = None,
        animate_offset: Optional[AnimationValue] = None,
        on_animation_end: OptionalControlEventCallable = None,
        tooltip: Optional[TooltipValue] = None,
        badge: Optional[BadgeValue] = None,
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
            badge=badge,
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
        self.on_tap_outside_bar = on_tap_outside_bar
        self.keyboard_type = keyboard_type
        self.view_surface_tint_color = view_surface_tint_color
        self.autofocus = autofocus
        self.view_header_height = view_header_height
        self.view_size_constraints = view_size_constraints
        self.bar_surface_tint_color = bar_surface_tint_color
        self.bar_elevation = bar_elevation
        self.bar_border_side = bar_border_side
        self.bar_shape = bar_shape
        self.bar_text_style = bar_text_style
        self.bar_hint_text_style = bar_hint_text_style
        self.bar_padding = bar_padding
        self.bar_scroll_padding = bar_scroll_padding
        self.bar_shadow_color = bar_shadow_color

    def _get_control_name(self):
        return "searchbar"

    def __contains__(self, item):
        return item in self.__controls

    def before_update(self):
        super().before_update()
        self._set_attr_json("barBgcolor", self.__bar_bgcolor, wrap_attr_dict=True)
        self._set_attr_json(
            "barOverlayColor", self.__bar_overlay_color, wrap_attr_dict=True
        )
        self._set_attr_json(
            "barHintTextStyle", self.__bar_hint_text_style, wrap_attr_dict=True
        )
        self._set_attr_json(
            "barSurfaceTintColor", self.__bar_surface_tint_color, wrap_attr_dict=True
        )
        self._set_attr_json("barElevation", self.__bar_elevation, wrap_attr_dict=True)
        self._set_attr_json(
            "barBorderSide", self.__bar_border_side, wrap_attr_dict=True
        )
        self._set_attr_json("barShape", self.__bar_shape, wrap_attr_dict=True)
        self._set_attr_json("barTextStyle", self.__bar_text_style, wrap_attr_dict=True)
        self._set_attr_json("barPadding", self.__bar_padding, wrap_attr_dict=True)
        self._set_attr_json(
            "barShadowColor", self.__bar_shadow_color, wrap_attr_dict=True
        )
        self._set_attr_json("viewShape", self.__view_shape)
        self._set_attr_json("viewHeaderTextStyle", self.__view_header_text_style)
        self._set_attr_json("viewHintTextStyle", self.__view_hint_text_style)
        self._set_attr_json("viewSide", self.__view_side)
        self._set_attr_json("viewSizeConstraints", self.__view_size_constraints)
        self._set_attr_json("barScrollPadding", self.__bar_scroll_padding)

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

    def close_view(self, text: str = ""):
        m = {
            "n": "closeView",
            "i": str(time.time()),
            "p": {"text": text},
        }
        self.value = text
        self._set_attr_json("method", m)
        self.update()

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
    def bar_bgcolor(self) -> ControlStateValue[str]:
        return self.__bar_bgcolor

    @bar_bgcolor.setter
    def bar_bgcolor(self, value: ControlStateValue[str]):
        self.__bar_bgcolor = value

    # bar_overlay_color
    @property
    def bar_overlay_color(self) -> ControlStateValue[str]:
        return self.__bar_overlay_color

    @bar_overlay_color.setter
    def bar_overlay_color(self, value: ControlStateValue[str]):
        self.__bar_overlay_color = value

    # bar_shadow_color
    @property
    def bar_shadow_color(self) -> Union[None, str, Dict[ControlState, str]]:
        return self.__bar_shadow_color

    @bar_shadow_color.setter
    def bar_shadow_color(self, value: Union[None, str, Dict[ControlState, str]]):
        self.__bar_shadow_color = value

    # bar_surface_tint_color
    @property
    def bar_surface_tint_color(self) -> Union[None, str, Dict[ControlState, str]]:
        return self.__bar_surface_tint_color

    @bar_surface_tint_color.setter
    def bar_surface_tint_color(self, value: Union[None, str, Dict[ControlState, str]]):
        self.__bar_surface_tint_color = value

    # bar_elevation
    @property
    def bar_elevation(self) -> Union[OptionalNumber, Dict[ControlState, Number]]:
        return self.__bar_elevation

    @bar_elevation.setter
    def bar_elevation(self, value: Union[OptionalNumber, Dict[ControlState, Number]]):
        self.__bar_elevation = value

    # bar_border_side
    @property
    def bar_border_side(
        self,
    ) -> Union[None, BorderSide, Dict[ControlState, BorderSide]]:
        return self.__bar_border_side

    @bar_border_side.setter
    def bar_border_side(
        self, value: Union[None, BorderSide, Dict[ControlState, BorderSide]]
    ):
        self.__bar_border_side = value

    # bar_shape
    @property
    def bar_shape(
        self,
    ) -> Union[None, OutlinedBorder, Dict[ControlState, OutlinedBorder]]:
        return self.__bar_shape

    @bar_shape.setter
    def bar_shape(
        self, value: Union[None, OutlinedBorder, Dict[ControlState, OutlinedBorder]]
    ):
        self.__bar_shape = value

    # bar_text_style
    @property
    def bar_text_style(self) -> Union[None, TextStyle, Dict[ControlState, TextStyle]]:
        return self.__bar_text_style

    @bar_text_style.setter
    def bar_text_style(
        self, value: Union[None, TextStyle, Dict[ControlState, TextStyle]]
    ):
        self.__bar_text_style = value

    # bar_hint_text_style
    @property
    def bar_hint_text_style(
        self,
    ) -> Union[None, TextStyle, Dict[ControlState, TextStyle]]:
        return self.__bar_hint_text_style

    @bar_hint_text_style.setter
    def bar_hint_text_style(
        self, value: Union[None, TextStyle, Dict[ControlState, TextStyle]]
    ):
        self.__bar_hint_text_style = value

    # bar_padding
    @property
    def bar_padding(self) -> Union[PaddingValue, Dict[ControlState, PaddingValue]]:
        return self.__bar_padding

    @bar_padding.setter
    def bar_padding(self, value: Union[PaddingValue, Dict[ControlState, PaddingValue]]):
        self.__bar_padding = value

    # view_leading
    @property
    def view_leading(self) -> Optional[Control]:
        return self.__view_leading

    @view_leading.setter
    def view_leading(self, value: Optional[Control]):
        self.__view_leading = value

    # view_surface_tint_color
    @property
    def view_surface_tint_color(self) -> Optional[ColorValue]:
        return self.__view_surface_tint_color

    @view_surface_tint_color.setter
    def view_surface_tint_color(self, value: Optional[ColorValue]):
        self.__view_surface_tint_color = value
        self._set_enum_attr("viewSurfaceTintColor", value, ColorEnums)

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

    # view_header_height
    @property
    def view_header_height(self) -> OptionalNumber:
        return self._get_attr("viewHeaderHeight")

    @view_header_height.setter
    def view_header_height(self, value: OptionalNumber):
        self._set_attr("viewHeaderHeight", value)

    # view_bgcolor
    @property
    def view_bgcolor(self) -> Optional[str]:
        return self.__view_bgcolor

    @view_bgcolor.setter
    def view_bgcolor(self, value: Optional[str]):
        self.__view_bgcolor = value
        self._set_enum_attr("viewBgcolor", value, ColorEnums)

    # divider_color
    @property
    def divider_color(self) -> Optional[ColorValue]:
        return self.__divider_color

    @divider_color.setter
    def divider_color(self, value: Optional[ColorValue]):
        self.__divider_color = value
        self._set_enum_attr("dividerColor", value, ColorEnums)

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

    # view_size_constraints
    @property
    def view_size_constraints(self) -> Optional[BoxConstraints]:
        return self.__view_size_constraints

    @view_size_constraints.setter
    def view_size_constraints(self, value: Optional[BoxConstraints]):
        self.__view_size_constraints = value

    # bar_scroll_padding
    @property
    def bar_scroll_padding(self) -> Optional[PaddingValue]:
        return self.__bar_scroll_padding

    @bar_scroll_padding.setter
    def bar_scroll_padding(self, value: Optional[PaddingValue]):
        self.__bar_scroll_padding = value

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

    # on_tap_outside_bar
    @property
    def on_tap_outside_bar(self) -> OptionalControlEventCallable:
        return self._get_event_handler("tapOutsideBar")

    @on_tap_outside_bar.setter
    def on_tap_outside_bar(self, handler: OptionalControlEventCallable):
        self._add_event_handler("tapOutsideBar", handler)
        self._set_attr("onTapOutsideBar", True if handler is not None else None)

    # on_submit
    @property
    def on_submit(self) -> OptionalControlEventCallable:
        return self._get_event_handler("submit")

    @on_submit.setter
    def on_submit(self, handler: OptionalControlEventCallable):
        self._add_event_handler("submit", handler)
        self._set_attr("onsubmit", True if handler is not None else None)
