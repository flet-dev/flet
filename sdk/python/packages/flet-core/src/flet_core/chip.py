from typing import Any, Optional, Union
import json

from flet_core.constrained_control import ConstrainedControl
from flet_core.control import Control, OptionalNumber
from flet_core.ref import Ref
from flet_core.types import (
    AnimationValue,
    MarginValue,
    OffsetValue,
    ResponsiveNumber,
    RotateValue,
    ScaleValue,
)
from flet_core.event_handler import EventHandler
from flet_core.control_event import ControlEvent


class Chip(ConstrainedControl):
    """
    Chips are compact elements that represent an attribute, text, entity, or action.

    Example:
    ```
    import flet as ft

    # Example is under construction
    ```

    -----

    Online docs: https://flet.dev/docs/controls/chip
    """

    def __init__(
        self,
        # content: Optional[Control] = None,
        ref: Optional[Ref] = None,
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
        key: Optional[str] = None,
        #
        # Specific
        #
        # margin: MarginValue = None,
        # elevation: OptionalNumber = None,
        # color: Optional[str] = None,
        # shadow_color: Optional[str] = None,
        # surface_tint_color: Optional[str] = None,
        label: Control = None,
        leading: Optional[Control] = None,
        bgcolor: Optional[str] = None,
        selected: Optional[bool] = False,
        on_click=None,
        on_delete=None,
        on_select=None,
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

        def convert_container_tap_event_data(e):
            d = json.loads(e.data)
            # return ContainerTapEvent(**d)
            return ControlEvent(**d)

        # self.__on_click = EventHandler(convert_container_tap_event_data)
        self.on_click = on_click
        self.on_delete = on_delete
        self.on_select = on_select
        # self._add_event_handler("click", self.__on_click.get_handler())
        # self.content = content
        self.label = label
        self.leading = leading
        self.bgcolor = bgcolor
        self.selected = selected

    def _get_control_name(self):
        return "chip"

    # selected
    @property
    def selected(self) -> Optional[bool]:
        return self._get_attr("selected")

    @selected.setter
    def selected(self, value: Optional[bool]):
        self._set_attr("selected", value)

    # on_click
    @property
    def on_click(self):
        return self._get_event_handler("click")

    @on_click.setter
    def on_click(self, handler):
        self._add_event_handler("click", handler)
        self._set_attr("onclick", True if handler is not None else None)

    # on_delete
    @property
    def on_delete(self):
        return self._get_event_handler("delete")

    @on_delete.setter
    def on_delete(self, handler):
        self._add_event_handler("delete", handler)
        self._set_attr("onDelete", True if handler is not None else None)

    # on_select
    @property
    def on_select(self):
        return self._get_event_handler("select")

    @on_select.setter
    def on_select(self, handler):
        self._add_event_handler("select", handler)
        self._set_attr("onSelect", True if handler is not None else None)

    # label
    @property
    def label(self) -> Control:
        return self.__label

    @label.setter
    def label(self, value: Control):
        self.__label = value

    # leading
    @property
    def leading(self) -> Optional[Control]:
        return self.__leading

    @leading.setter
    def leading(self, value: Optional[Control]):
        self.__leading = value

    # bgcolor
    @property
    def bgcolor(self):
        return self._get_attr("bgcolor")

    @bgcolor.setter
    def bgcolor(self, value):
        self._set_attr("bgcolor", value)

    def _get_children(self):
        children = []
        if self.__label:
            self.__label._set_attr_internal("n", "label")
            children.append(self.__label)
        if self.__leading:
            self.__leading._set_attr_internal("n", "leading")
            children.append(self.__leading)
        # if self.__trailing:
        #     self.__trailing._set_attr_internal("n", "trailing")
        #     children.append(self.__trailing)
        return children
