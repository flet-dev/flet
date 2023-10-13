from typing import Any, Optional, Union

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
        #content: Optional[Control] = None,
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
        bgcolor: Optional[str] = None,
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

        #self.content = content
        self.label = label
        self.bgcolor = bgcolor

    def _get_control_name(self):
        return "chip"

    # def _before_build_command(self):
    #     super()._before_build_command()
    #     self._set_attr_json("margin", self.__margin)

    # def _get_children(self):
    #     children = []
    #     if self.__content is not None:
    #         self.__content._set_attr_internal("n", "content")
    #         children.append(self.__content)
    #     return children

    # # margin
    # @property
    # def margin(self) -> MarginValue:
    #     return self.__margin

    # @margin.setter
    # def margin(self, value: MarginValue):
    #     self.__margin = value


    # label
    # @property
    # def label(self):
    #     return self._get_attr("label")

    # @label.setter
    # def label(self, value):
    #     self._set_attr("label", value)

    # # label
    # @property
    # def label(self) -> Optional[Control]:
    #     return self.__label

    # @label.setter
    # def label(self, value: Optional[Control]):
    #     self.__label = value

    # label
    @property
    def label(self) -> Control:
        return self.__label

    @label.setter
    def label(self, value: Control):
        self.__label = value
    
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
        # if self.__subtitle:
        #     self.__subtitle._set_attr_internal("n", "subtitle")
        #     children.append(self.__subtitle)
        # if self.__trailing:
        #     self.__trailing._set_attr_internal("n", "trailing")
        #     children.append(self.__trailing)
        return children