import json
import time
from typing import Any, List, Optional, Set, Union

from flet_core.buttons import ButtonStyle
from flet_core.constrained_control import ConstrainedControl
from flet_core.control import Control, OptionalNumber
from flet_core.ref import Ref
from flet_core.types import (
    AnimationValue,
    OffsetValue,
    ResponsiveNumber,
    RotateValue,
    ScaleValue,
)


class Segment(Control):
    def __init__(
        self,
        value: str,
        ref: Optional[Ref] = None,
        expand: Union[None, bool, int] = None,
        col: Optional[ResponsiveNumber] = None,
        opacity: OptionalNumber = None,
        tooltip: Optional[str] = None,
        visible: Optional[bool] = None,
        disabled: Optional[bool] = None,
        data: Any = None,
        #
        # Specific
        #
        icon: Optional[Control] = None,
        label: Optional[Control] = None,
    ):
        Control.__init__(
            self,
            ref=ref,
            expand=expand,
            col=col,
            opacity=opacity,
            tooltip=tooltip,
            visible=visible,
            disabled=disabled,
            data=data,
        )

        self.value = value
        self.label = label
        self.icon = icon

    def _get_control_name(self):
        return "segment"

    def _before_build_command(self):
        super()._before_build_command()

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


class SegmentedButton(ConstrainedControl):
    """


    -----

    Online docs: https://flet.dev/docs/controls/segmentedbutton
    """

    def __init__(
        self,
        segments: List[Segment],
        ref: Optional[Ref] = None,
        key: Optional[str] = None,
        width: OptionalNumber = None,
        height: OptionalNumber = None,
        left: OptionalNumber = None,
        top: OptionalNumber = None,
        right: OptionalNumber = None,
        bottom: OptionalNumber = None,
        expand: Union[None, bool, int] = None,
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
        #
        # Specific
        #
        style: Optional[ButtonStyle] = None,
        allow_empty_selection: Optional[bool] = None,
        allow_multiple_selection: Optional[bool] = None,
        selected: Optional[Set] = None,
        selected_icon: Optional[Control] = None,
        show_selected_icon: Optional[bool] = None,
        on_change=None,
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
        self.on_change = on_change

    def _get_control_name(self):
        return "segmentedbutton"

    def _before_build_command(self):
        super()._before_build_command()
        if self.__style is None:
            self.__style = ButtonStyle()
            self.__style.side = self._wrap_attr_dict(self.__style.side)
            self.__style.shape = self._wrap_attr_dict(self.__style.shape)
        self._set_attr_json("style", self.__style)

    def _get_children(self):
        children = []
        for segment in self.segments:
            segment._set_attr_internal("n", "segment")
            children.append(segment)
        if self.__selected_icon:
            self.__selected_icon._set_attr_internal("n", "selectedIcon")
            children.append(self.__selected_icon)
        return children

    # style
    @property
    def style(self) -> Optional[ButtonStyle]:
        return self.__style

    @style.setter
    def style(self, value: Optional[ButtonStyle]):
        self.__style = value

    # on_change
    @property
    def on_change(self):
        return self._get_event_handler("change")

    @on_change.setter
    def on_change(self, handler):
        self._add_event_handler("change", handler)

    # segments
    @property
    def segments(self):
        return self.__segments

    @segments.setter
    def segments(self, value):
        self.__segments = value if value is not None else []

    # allow_empty_selection
    @property
    def allow_empty_selection(self) -> Optional[bool]:
        return self._get_attr("allowEmptySelection", data_type="bool", def_value=False)

    @allow_empty_selection.setter
    def allow_empty_selection(self, value: Optional[bool]):
        self._set_attr("allowEmptySelection", value)

    # allow_multiple_selection
    @property
    def allow_multiple_selection(self) -> Optional[bool]:
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
            json.dumps(list(value), separators=(",", ":"))
            if value is not None
            else None,
        )

    # show_selected_icon
    @property
    def show_selected_icon(self) -> Optional[bool]:
        return self._get_attr("showSelectedIcon", data_type="bool", def_value=True)

    @show_selected_icon.setter
    def show_selected_icon(self, value: Optional[bool]):
        self._set_attr("showSelectedIcon", value)

    # selected_icon
    @property
    def selected_icon(self) -> Optional[Control]:
        return self.__selected_icon

    @selected_icon.setter
    def selected_icon(self, value: Optional[Control]):
        self.__selected_icon = value
