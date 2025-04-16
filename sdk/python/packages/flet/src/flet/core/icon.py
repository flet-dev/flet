from typing import Any, List, Optional, Union

from flet.core.animation import AnimationValue
from flet.core.badge import BadgeValue
from flet.core.box import BoxShadow
from flet.core.constrained_control import ConstrainedControl
from flet.core.control import OptionalNumber
from flet.core.ref import Ref
from flet.core.tooltip import TooltipValue
from flet.core.types import (
    BlendMode,
    ColorEnums,
    ColorValue,
    IconEnums,
    IconValue,
    OffsetValue,
    OptionalControlEventCallable,
    ResponsiveNumber,
    RotateValue,
    ScaleValue,
)


class Icon(ConstrainedControl):
    """
    Displays a Material icon.

    Icon browser: https://flet-icons-browser.fly.dev/#/

    Example:
    ```
    import flet as ft

    def main(page: ft.Page):
        page.add(
            ft.Row(
                [
                    ft.Icon(name=ft.icons.FAVORITE, color=ft.colors.PINK),
                    ft.Icon(name=ft.icons.AUDIOTRACK, color=ft.colors.GREEN_400, size=30),
                    ft.Icon(name=ft.icons.BEACH_ACCESS, color=ft.colors.BLUE, size=50),
                    ft.Icon(name="settings", color="#c1c1c1"),
                ]
            )
        )

    ft.app(target=main)

    ```

    -----

    Online docs: https://flet.dev/docs/controls/icon
    """

    def __init__(
        self,
        name: Optional[IconValue] = None,
        color: Optional[ColorValue] = None,
        size: OptionalNumber = None,
        semantics_label: Optional[str] = None,
        shadows: Union[BoxShadow, List[BoxShadow], None] = None,
        fill: OptionalNumber = None,
        apply_text_scaling: Optional[bool] = None,
        grade: OptionalNumber = None,
        weight: OptionalNumber = None,
        optical_size: OptionalNumber = None,
        blend_mode: Optional[BlendMode] = None,
        #
        # ConstrainedControl
        #
        ref: Optional[Ref] = None,
        key: Optional[str] = None,
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

        self.name = name
        self.color = color
        self.size = size
        self.semantics_label = semantics_label
        self.shadows = shadows
        self.fill = fill
        self.apply_text_scaling = apply_text_scaling
        self.grade = grade
        self.weight = weight
        self.optical_size = optical_size
        self.blend_mode = blend_mode

    def _get_control_name(self):
        return "icon"

    def before_update(self):
        super().before_update()
        self._set_attr_json("shadows", self.__shadows)

    # name
    @property
    def name(self) -> Optional[IconValue]:
        return self.__name

    @name.setter
    def name(self, value: Optional[IconValue]):
        self.__name = value
        self._set_enum_attr("name", value, IconEnums)

    # blend_mode
    @property
    def blend_mode(self) -> Optional[BlendMode]:
        return self.__blend_mode

    @blend_mode.setter
    def blend_mode(self, value: Optional[BlendMode]):
        self.__blend_mode = value
        self._set_enum_attr("blendMode", value, BlendMode)

    # color
    @property
    def color(self) -> Optional[ColorValue]:
        return self.__color

    @color.setter
    def color(self, value: Optional[ColorValue]):
        self.__color = value
        self._set_enum_attr("color", value, ColorEnums)

    # size
    @property
    def size(self) -> OptionalNumber:
        return self._get_attr("size", data_type="float")

    @size.setter
    def size(self, value: OptionalNumber):
        self._set_attr("size", value)

    # semantics_label
    @property
    def semantics_label(self) -> Optional[str]:
        return self._get_attr("semanticsLabel")

    @semantics_label.setter
    def semantics_label(self, value: Optional[str]):
        self._set_attr("semanticsLabel", value)

    # shadows
    @property
    def shadows(self) -> Union[BoxShadow, List[BoxShadow], None]:
        return self.__shadows

    @shadows.setter
    def shadows(self, value: Union[BoxShadow, List[BoxShadow], None]):
        self.__shadows = value

    # fill
    @property
    def fill(self) -> OptionalNumber:
        return self._get_attr("fill", data_type="float")

    @fill.setter
    def fill(self, value: OptionalNumber):
        self._set_attr("fill", value)

    # apply_text_scaling
    @property
    def apply_text_scaling(self) -> Optional[bool]:
        return self._get_attr("applyTextScaling", data_type="bool")

    @apply_text_scaling.setter
    def apply_text_scaling(self, value: Optional[bool]):
        self._set_attr("applyTextScaling", value)

    # grade
    @property
    def grade(self) -> OptionalNumber:
        return self._get_attr("grade", data_type="float")

    @grade.setter
    def grade(self, value: OptionalNumber):
        self._set_attr("grade", value)

    # weight
    @property
    def weight(self) -> OptionalNumber:
        return self._get_attr("weight", data_type="float")

    @weight.setter
    def weight(self, value: OptionalNumber):
        self._set_attr("weight", value)

    # optical_size
    @property
    def optical_size(self) -> OptionalNumber:
        return self._get_attr("opticalSize", data_type="float")

    @optical_size.setter
    def optical_size(self, value: OptionalNumber):
        self._set_attr("opticalSize", value)
