from typing import Any, Optional, Union

from flet_core.constrained_control import ConstrainedControl
from flet_core.control import Control, OptionalNumber
from flet_core.ref import Ref
from flet_core.types import (
    AnimationValue,
    OffsetValue,
    ResponsiveNumber,
    RotateValue,
    ScaleValue,
    PaddingValue,
)

from flet_core.text_style import TextStyle
from flet_core.buttons import OutlinedBorder


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
        delete_icon_tooltip: Optional[str] = None,
        delete_icon: Optional[Control] = None,
        delete_icon_color: Optional[str] = None,
        disabled_color: Optional[str] = None,
        elevation: OptionalNumber = None,
        label_padding: PaddingValue = None,
        label_style: Optional[TextStyle] = None,
        padding: PaddingValue = None,
        selected_color: Optional[str] = None,
        selected_shadow_color: Optional[str] = None,
        shadow_color: Optional[str] = None,
        shape: Optional[OutlinedBorder] = None,
        show_checkmark: Optional[bool] = None,
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

        self.autofocus = autofocus
        self.label = label
        self.leading = leading
        self.bgcolor = bgcolor
        self.check_color = check_color
        self.selected = selected
        self.delete_icon_tooltip = delete_icon_tooltip
        self.delete_icon = delete_icon
        self.delete_icon_color = delete_icon_color
        self.disabled_color = disabled_color
        self.elevation = elevation
        self.label_padding = label_padding
        self.label_style = label_style
        self.padding = padding
        self.selected_color = selected_color
        self.selected_shadow_color = selected_shadow_color
        self.shadow_color = shadow_color
        self.shape = shape
        self.show_checkmark = show_checkmark
        self.on_click = on_click
        self.on_delete = on_delete
        self.on_select = on_select
        self.on_focus = on_focus
        self.on_blur = on_blur

    def _get_control_name(self):
        return "chip"

    def _before_build_command(self):
        super()._before_build_command()
        self._set_attr_json("labelPadding", self.__label_padding)
        self._set_attr_json("labelStyle", self.__label_style)
        self._set_attr_json("padding", self.__padding)
        self._set_attr_json("shape", self.__shape)

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

    # padding
    @property
    def padding(self) -> PaddingValue:
        return self.__padding

    @padding.setter
    def padding(self, value: PaddingValue):
        self.__padding = value

    # selected
    @property
    def selected(self) -> Optional[bool]:
        return self._get_attr("selected")

    @selected.setter
    def selected(self, value: Optional[bool]):
        self._set_attr("selected", value)

    # show_checkmark
    @property
    def show_checkmark(self) -> Optional[bool]:
        return self._get_attr("showCheckmark")

    @show_checkmark.setter
    def show_checkmark(self, value: Optional[bool]):
        self._set_attr("showCheckmark", value)

    # delete_icon_tooltip
    @property
    def delete_icon_tooltip(self):
        return self._get_attr("deleteButtonTooltipMessage")

    @delete_icon_tooltip.setter
    def delete_icon_tooltip(self, value):
        self._set_attr("deleteButtonTooltipMessage", value)

    # label
    @property
    def label(self) -> Control:
        return self.__label

    @label.setter
    def label(self, value: Control):
        self.__label = value

    # label_padding
    @property
    def label_padding(self) -> PaddingValue:
        return self.__label_padding

    @label_padding.setter
    def label_padding(self, value: PaddingValue):
        self.__label_padding = value

    # label_style
    @property
    def label_style(self):
        return self.__label_style

    @label_style.setter
    def label_style(self, value: Optional[TextStyle]):
        self.__label_style = value

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

    # delete_icon_color
    @property
    def delete_icon_color(self):
        return self._get_attr("deleteIconColor")

    @delete_icon_color.setter
    def delete_icon_color(self, value):
        self._set_attr("deleteIconColor", value)

    # disabled_color
    @property
    def disabled_color(self):
        return self._get_attr("disabledColor")

    @disabled_color.setter
    def disabled_color(self, value):
        self._set_attr("disabledColor", value)

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

    # selected_color
    @property
    def selected_color(self):
        return self._get_attr("selectedColor")

    @selected_color.setter
    def selected_color(self, value):
        self._set_attr("selectedColor", value)

    # selected_shadow_color
    @property
    def selected_shadow_color(self):
        return self._get_attr("selectedShadowColor")

    @selected_shadow_color.setter
    def selected_shadow_color(self, value):
        self._set_attr("selectedShadowColor", value)

    # shadow_color
    @property
    def shadow_color(self):
        return self._get_attr("shadowColor")

    @shadow_color.setter
    def shadow_color(self, value):
        self._set_attr("shadowColor", value)

    # elevation
    @property
    def elevation(self) -> OptionalNumber:
        return self._get_attr("elevation")

    @elevation.setter
    def elevation(self, value: OptionalNumber):
        self._set_attr("elevation", value)

    # shape
    @property
    def shape(self) -> Optional[OutlinedBorder]:
        return self.__shape

    @shape.setter
    def shape(self, value: Optional[OutlinedBorder]):
        self.__shape = value

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
