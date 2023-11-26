from typing import List, Optional, Union, Any

from flet_core.constrained_control import ConstrainedControl
from flet_core.control import Control, OptionalNumber
from flet_core.ref import Ref
from flet_core.types import (
    ClipBehavior,
    ClipBehaviorString,
    ResponsiveNumber,
    RotateValue,
    ScaleValue,
    OffsetValue,
    PaddingValue,
    AnimationValue,
    NotchShape,
)


class BottomAppBar(ConstrainedControl):
    """
    A material design bottom app bar.

    -----

    Online docs: https://flet.dev/docs/controls/bottomappbar
    """

    def __init__(
        self,
        content: Optional[Control] = None,
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
        visible: Optional[bool] = None,
        disabled: Optional[bool] = None,
        data: Any = None,
        #
        # Specific
        #
        surface_tint_color: Optional[str] = None,
        bgcolor: Optional[str] = None,
        shadow_color: Optional[str] = None,
        padding: PaddingValue = None,
        clip_behavior: Optional[ClipBehavior] = None,
        shape: Optional[NotchShape] = None,
        notch_margin: OptionalNumber = None,
        elevation: OptionalNumber = None,
    ):
        ConstrainedControl.__init__(
            self,
            ref=ref,
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
            visible=visible,
            disabled=disabled,
            data=data,
        )

        self.__leading: Optional[Control] = None
        self.__title: Optional[Control] = None
        self.__actions: List[Control] = []

        self.content = content
        self.surface_tint_color = surface_tint_color
        self.bgcolor = bgcolor
        self.shadow_color = shadow_color
        self.padding = padding
        self.shape = shape
        self.clip_behavior = clip_behavior
        self.notch_margin = notch_margin
        self.elevation = elevation

    def _get_control_name(self):
        return "bottomappbar"

    def _before_build_command(self):
        super()._before_build_command()
        self._set_attr_json("padding", self.__padding)

    def _get_children(self):
        children = []
        if self.__content is not None:
            self.__content._set_attr_internal("n", "content")
            children.append(self.__content)
        return children

    # content
    @property
    def content(self) -> Optional[Control]:
        return self.__content

    @content.setter
    def content(self, value: Optional[Control]):
        self.__content = value

    # surface_tint_color
    @property
    def surface_tint_color(self):
        return self._get_attr("surfaceTintColor")

    @surface_tint_color.setter
    def surface_tint_color(self, value):
        self._set_attr("surfaceTintColor", value)

    # bgcolor
    @property
    def bgcolor(self):
        return self._get_attr("bgcolor")

    @bgcolor.setter
    def bgcolor(self, value):
        self._set_attr("bgcolor", value)

    # shadow_color
    @property
    def shadow_color(self):
        return self._get_attr("shadowColor")

    @shadow_color.setter
    def shadow_color(self, value):
        self._set_attr("shadowColor", value)

    # padding
    @property
    def padding(self) -> PaddingValue:
        return self.__padding

    @padding.setter
    def padding(self, value: PaddingValue):
        self.__padding = value

    # shape
    @property
    def shape(self):
        return self.__shape

    @shape.setter
    def shape(self, value: Optional[NotchShape]):
        self.__shape = value
        self._set_attr("shape", value.value if isinstance(value, NotchShape) else value)

    # clip_behavior
    @property
    def clip_behavior(self) -> Optional[ClipBehavior]:
        return self.__clip_behavior

    @clip_behavior.setter
    def clip_behavior(self, value: Optional[ClipBehavior]):
        self.__clip_behavior = value
        if isinstance(value, ClipBehavior):
            self._set_attr("clipBehavior", value.value)
        else:
            self.__set_clip_behavior(value)

    def __set_clip_behavior(self, value: Optional[ClipBehaviorString]):
        self._set_attr("clipBehavior", value)

    # notch_margin
    @property
    def notch_margin(self) -> OptionalNumber:
        return self._get_attr("notchMargin")

    @notch_margin.setter
    def notch_margin(self, value: OptionalNumber):
        self._set_attr("notchMargin", value)

    # elevation
    @property
    def elevation(self) -> OptionalNumber:
        return self._get_attr("elevation")

    @elevation.setter
    def elevation(self, value: OptionalNumber):
        self._set_attr("elevation", value)
