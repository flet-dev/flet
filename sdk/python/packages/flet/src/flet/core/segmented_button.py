import json
from typing import Any, List, Optional, Set, Union

from flet.core.alignment import Axis
from flet.core.animation import AnimationValue
from flet.core.badge import BadgeValue
from flet.core.buttons import ButtonStyle
from flet.core.constrained_control import ConstrainedControl
from flet.core.control import Control, OptionalNumber
from flet.core.ref import Ref
from flet.core.tooltip import TooltipValue
from flet.core.types import (
    OffsetValue,
    OptionalControlEventCallable,
    PaddingValue,
    ResponsiveNumber,
    RotateValue,
    ScaleValue,
)


class Segment(Control):
    def __init__(
        self,
        value: str,
        icon: Optional[Control] = None,
        label: Optional[Control] = None,
        #
        # Control
        #
        ref: Optional[Ref] = None,
        expand: Union[None, bool, int] = None,
        expand_loose: Optional[bool] = None,
        col: Optional[ResponsiveNumber] = None,
        opacity: OptionalNumber = None,
        tooltip: Optional[str] = None,
        badge: Optional[BadgeValue] = None,
        visible: Optional[bool] = None,
        disabled: Optional[bool] = None,
        data: Any = None,
    ):
        Control.__init__(
            self,
            ref=ref,
            expand=expand,
            expand_loose=expand_loose,
            col=col,
            opacity=opacity,
            tooltip=tooltip,
            badge=badge,
            visible=visible,
            disabled=disabled,
            data=data,
        )

        self.value = value
        self.label = label
        self.icon = icon

    def _get_control_name(self):
        return "segment"

    def _get_children(self):
        children = []
        if self.__label:
            self.__label._set_attr_internal("n", "label")
            children.append(self.__label)
        if self.__icon:
            self.__icon._set_attr_internal("n", "icon")
            children.append(self.__icon)
        return children

    # label
    @property
    def label(self) -> Optional[Control]:
        return self.__label

    @label.setter
    def label(self, value: Optional[Control]):
        self.__label = value

    # icon
    @property
    def icon(self) -> Optional[Control]:
        return self.__icon

    @icon.setter
    def icon(self, value: Optional[Control]):
        self.__icon = value

    # value
    @property
    def value(self) -> str:
        return self._get_attr("value")

    @value.setter
    def value(self, value: str):
        self._set_attr("value", value)

    # tooltip
    @property
    def tooltip(self) -> Optional[str]:
        return self._get_attr("tooltip")

    @tooltip.setter
    def tooltip(self, value: Optional[str]):
        self._set_attr("tooltip", value)


class SegmentedButton(ConstrainedControl):
    """
    A segmented button control.

    -----

    Online docs: https://flet.dev/docs/controls/segmentedbutton
    """

    def __init__(
        self,
        segments: List[Segment],
        style: Optional[ButtonStyle] = None,
        allow_empty_selection: Optional[bool] = None,
        allow_multiple_selection: Optional[bool] = None,
        selected: Optional[Set] = None,
        selected_icon: Optional[Control] = None,
        show_selected_icon: Optional[bool] = None,
        direction: Optional[Axis] = None,
        padding: Optional[PaddingValue] = None,
        on_change: OptionalControlEventCallable = None,
        #
        # ConstrainedControl
        #
        ref: Optional[Ref] = None,
        key: Optional[str] = None,
        width: OptionalNumber = None,
        height: OptionalNumber = None,
        left: OptionalNumber = None,
        top: OptionalNumber = None,
        right: OptionalNumber = None,
        bottom: OptionalNumber = None,
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
            left=left,
            top=top,
            right=right,
            bottom=bottom,
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

        self.segments = segments
        self.show_selected_icon = show_selected_icon
        self.allow_multiple_selection = allow_multiple_selection
        self.allow_empty_selection = allow_empty_selection
        self.selected_icon = selected_icon
        self.selected = selected
        self.style = style
        self.direction = direction
        self.padding = padding
        self.on_change = on_change

    def _get_control_name(self):
        return "segmentedbutton"

    def before_update(self):
        super().before_update()
        assert any(
            segment.visible for segment in self.__segments
        ), "segments must have at minimum one visible Segment"
        assert (
            len(self.selected) > 0 or self.allow_empty_selection
        ), "allow_empty_selection must be True for selected to be empty"
        assert (
            len(self.selected) < 2 or self.allow_multiple_selection
        ), "allow_multiple_selection must be True for selected to have more than one item"
        style = self.__style or ButtonStyle()
        style.side = self._wrap_attr_dict(style.side)
        style.shape = self._wrap_attr_dict(style.shape)
        style.padding = self._wrap_attr_dict(style.padding)
        self._set_attr_json("style", style)
        self._set_attr_json("padding", self.__padding)

    def _get_children(self):
        for segment in self.segments:
            segment._set_attr_internal("n", "segment")
        children: List[Control] = self.__segments
        if self.__selected_icon:
            self.__selected_icon._set_attr_internal("n", "selectedIcon")
            children.append(self.__selected_icon)
        return children

    def __contains__(self, item):
        return item in self.__segments

    # style
    @property
    def style(self) -> Optional[ButtonStyle]:
        return self.__style

    @style.setter
    def style(self, value: Optional[ButtonStyle]):
        self.__style = value

    # on_change
    @property
    def on_change(self) -> OptionalControlEventCallable:
        return self._get_event_handler("change")

    @on_change.setter
    def on_change(self, handler: OptionalControlEventCallable):
        self._add_event_handler("change", handler)

    # segments
    @property
    def segments(self) -> List[Segment]:
        return self.__segments

    @segments.setter
    def segments(self, value: List[Segment]):
        self.__segments = value

    # padding
    @property
    def padding(self) -> Optional[PaddingValue]:
        return self.__padding

    @padding.setter
    def padding(self, value: Optional[PaddingValue]):
        self.__padding = value

    # allow_empty_selection
    @property
    def allow_empty_selection(self) -> bool:
        return self._get_attr("allowEmptySelection", data_type="bool", def_value=False)

    @allow_empty_selection.setter
    def allow_empty_selection(self, value: Optional[bool]):
        self._set_attr("allowEmptySelection", value)

    # allow_multiple_selection
    @property
    def allow_multiple_selection(self) -> bool:
        return self._get_attr(
            "allowMultipleSelection", data_type="bool", def_value=False
        )

    @allow_multiple_selection.setter
    def allow_multiple_selection(self, value: Optional[bool]):
        self._set_attr("allowMultipleSelection", value)

    # selected
    @property
    def selected(self) -> Optional[Set]:
        s = self._get_attr("selected")
        return set(json.loads(s)) if s else s

    @selected.setter
    def selected(self, value: Optional[Set]):
        self._set_attr(
            "selected",
            (
                json.dumps(list(value), separators=(",", ":"))
                if value is not None
                else None
            ),
        )

    # show_selected_icon
    @property
    def show_selected_icon(self) -> bool:
        return self._get_attr("showSelectedIcon", data_type="bool", def_value=True)

    @show_selected_icon.setter
    def show_selected_icon(self, value: Optional[bool]):
        self._set_attr("showSelectedIcon", value)

    # direction
    @property
    def direction(self) -> Optional[Axis]:
        return self.__direction

    @direction.setter
    def direction(self, value: Optional[Axis]):
        self.__direction = value
        self._set_enum_attr("direction", value, Axis)

    # selected_icon
    @property
    def selected_icon(self) -> Optional[Control]:
        return self.__selected_icon

    @selected_icon.setter
    def selected_icon(self, value: Optional[Control]):
        self.__selected_icon = value
