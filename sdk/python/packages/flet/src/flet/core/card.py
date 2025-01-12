from enum import Enum
from typing import Any, Optional, Union

from flet.core.adaptive_control import AdaptiveControl
from flet.core.animation import AnimationValue
from flet.core.badge import BadgeValue
from flet.core.buttons import OutlinedBorder
from flet.core.constrained_control import ConstrainedControl
from flet.core.control import Control, OptionalNumber
from flet.core.ref import Ref
from flet.core.tooltip import TooltipValue
from flet.core.types import (
    ClipBehavior,
    ColorEnums,
    ColorValue,
    MarginValue,
    OffsetValue,
    OptionalControlEventCallable,
    ResponsiveNumber,
    RotateValue,
    ScaleValue,
)


class CardVariant(Enum):
    ELEVATED = "elevated"
    FILLED = "filled"
    OUTLINED = "outlined"


class Card(ConstrainedControl, AdaptiveControl):
    """
    A material design card: a panel with slightly rounded corners and an elevation shadow.

    Example:
    ```
    import flet as ft

    def main(page):
        page.title = "Card Example"
        page.add(
            ft.Card(
                content=ft.Container(
                    content=ft.Column(
                        [
                            ft.ListTile(
                                leading=ft.Icon(ft.icons.ALBUM),
                                title=ft.Text("The Enchanted Nightingale"),
                                subtitle=ft.Text(
                                    "Music by Julie Gable. Lyrics by Sidney Stein."
                                ),
                            ),
                            ft.Row(
                                [ft.TextButton("Buy tickets"), ft.TextButton("Listen")],
                                alignment=ft.MainAxisAlignment.END,
                            ),
                        ]
                    ),
                    width=400,
                    padding=10,
                )
            )
        )

    ft.app(target=main)

    ```

    -----

    Online docs: https://flet.dev/docs/controls/card
    """

    def __init__(
        self,
        content: Optional[Control] = None,
        margin: Optional[MarginValue] = None,
        elevation: OptionalNumber = None,
        color: Optional[ColorValue] = None,
        shadow_color: Optional[ColorValue] = None,
        surface_tint_color: Optional[ColorValue] = None,
        shape: Optional[OutlinedBorder] = None,
        clip_behavior: Optional[ClipBehavior] = None,
        is_semantic_container: Optional[bool] = None,
        show_border_on_foreground: Optional[bool] = None,
        variant: Optional[CardVariant] = None,
        #
        # ConstrainedControl and AdaptiveControl
        #
        ref: Optional[Ref] = None,
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
        badge: Optional[BadgeValue] = None,
        visible: Optional[bool] = None,
        disabled: Optional[bool] = None,
        data: Any = None,
        key: Optional[str] = None,
        adaptive: Optional[bool] = None,
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
            badge=badge,
            visible=visible,
            disabled=disabled,
            data=data,
        )

        AdaptiveControl.__init__(self, adaptive=adaptive)

        self.content = content
        self.margin = margin
        self.elevation = elevation
        self.color = color
        self.shadow_color = shadow_color
        self.surface_tint_color = surface_tint_color
        self.shape = shape
        self.clip_behavior = clip_behavior
        self.is_semantic_container = is_semantic_container
        self.show_border_on_foreground = show_border_on_foreground
        self.variant = variant

    def _get_control_name(self):
        return "card"

    def before_update(self):
        super().before_update()
        self._set_attr_json("margin", self.__margin)
        self._set_attr_json("shape", self.__shape)

    def _get_children(self):
        children = []
        if self.__content is not None:
            self.__content._set_attr_internal("n", "content")
            children.append(self.__content)
        return children

    # margin
    @property
    def margin(self) -> Optional[MarginValue]:
        return self.__margin

    @margin.setter
    def margin(self, value: Optional[MarginValue]):
        self.__margin = value

    # elevation
    @property
    def elevation(self) -> OptionalNumber:
        return self._get_attr("elevation")

    @elevation.setter
    def elevation(self, value: OptionalNumber):
        self._set_attr("elevation", value)

    # color
    @property
    def color(self):
        return self.__color

    @color.setter
    def color(self, value):
        self.__color = value
        self._set_enum_attr("color", value, ColorEnums)

    # shadow_color
    @property
    def shadow_color(self):
        return self.__shadow_color

    @shadow_color.setter
    def shadow_color(self, value):
        self.__shadow_color = value
        self._set_enum_attr("shadowColor", value, ColorEnums)

    # surface_tint_color
    @property
    def surface_tint_color(self):
        return self.__surface_tint_color

    @surface_tint_color.setter
    def surface_tint_color(self, value):
        self.__surface_tint_color = value
        self._set_enum_attr("surfaceTintColor", value, ColorEnums)

    # shape
    @property
    def shape(self) -> Optional[OutlinedBorder]:
        return self.__shape

    @shape.setter
    def shape(self, value: Optional[OutlinedBorder]):
        self.__shape = value

    # content
    @property
    def content(self) -> Optional[Control]:
        return self.__content

    @content.setter
    def content(self, value: Optional[Control]):
        self.__content = value

    # clip_behavior
    @property
    def clip_behavior(self) -> Optional[ClipBehavior]:
        return self.__clip_behavior

    @clip_behavior.setter
    def clip_behavior(self, value: Optional[ClipBehavior]):
        self.__clip_behavior = value
        self._set_enum_attr("clipBehavior", value, ClipBehavior)

    # is_semantic_container
    @property
    def is_semantic_container(self) -> bool:
        return self._get_attr("isSemanticContainer", data_type="bool", def_value=True)

    @is_semantic_container.setter
    def is_semantic_container(self, value):
        self._set_attr("isSemanticContainer", value)

    # show_border_on_foreground
    @property
    def show_border_on_foreground(self) -> bool:
        return self._get_attr(
            "showBorderOnForeground", data_type="bool", def_value=True
        )

    @show_border_on_foreground.setter
    def show_border_on_foreground(self, value):
        self._set_attr("showBorderOnForeground", value)

    # variant
    @property
    def variant(self) -> Optional[CardVariant]:
        return self.__variant

    @variant.setter
    def variant(self, value: Optional[CardVariant]):
        self.__variant = value
        self._set_enum_attr("variant", value, CardVariant)
