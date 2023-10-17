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
        autofocus: Optional[bool] = None,
        label: Control = None,
        leading: Optional[Control] = None,
        bgcolor: Optional[str] = None,
        selected: Optional[bool] = False,
        check_color: Optional[str] = None,
        delete_button_tooltip_message: Optional[str] = None,
        delete_icon: Optional[Control] = None,
        on_click=None,
        on_delete=None,
        on_select=None,
        on_focus=None,
        on_blur=None,
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

        self.on_click = on_click
        self.on_delete = on_delete
        self.on_select = on_select
        self.on_focus = on_focus
        self.on_blur = on_blur
        self.autofocus = autofocus
        self.label = label
        self.leading = leading
        self.bgcolor = bgcolor
        self.check_color = check_color
        self.selected = selected
        self.delete_button_tooltip_message = delete_button_tooltip_message
        self.delete_icon = delete_icon

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

    # delete_button_tooltip_message
    @property
    def delete_button_tooltip_message(self):
        return self._get_attr("deleteButtonTooltipMessage")

    @delete_button_tooltip_message.setter
    def delete_button_tooltip_message(self, value):
        self._set_attr("deleteButtonTooltipMessage", value)

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

    # delete_icon
    @property
    def delete_icon(self) -> Optional[Control]:
        return self.__delete_icon

    @delete_icon.setter
    def delete_icon(self, value: Optional[Control]):
        self.__delete_icon = value

    # autofocus
    @property
    def autofocus(self) -> Optional[bool]:
        return self._get_attr("autofocus", data_type="bool", def_value=False)

    @autofocus.setter
    def autofocus(self, value: Optional[bool]):
        self._set_attr("autofocus", value)

    # bgcolor
    @property
    def bgcolor(self):
        return self._get_attr("bgcolor")

    @bgcolor.setter
    def bgcolor(self, value):
        self._set_attr("bgcolor", value)

    # check_color
    @property
    def check_color(self):
        return self._get_attr("checkColor")

    @check_color.setter
    def check_color(self, value):
        self._set_attr("checkColor", value)

    def _get_children(self):
        children = []
        if self.__label:
            self.__label._set_attr_internal("n", "label")
            children.append(self.__label)
        if self.__leading:
            self.__leading._set_attr_internal("n", "leading")
            children.append(self.__leading)
        if self.__delete_icon:
            self.__delete_icon._set_attr_internal("n", "deleteIcon")
            children.append(self.__delete_icon)
        return children

    # on_focus
    @property
    def on_focus(self):
        return self._get_event_handler("focus")

    @on_focus.setter
    def on_focus(self, handler):
        self._add_event_handler("focus", handler)

    # on_blur
    @property
    def on_blur(self):
        return self._get_event_handler("blur")

    @on_blur.setter
    def on_blur(self, handler):
        self._add_event_handler("blur", handler)
