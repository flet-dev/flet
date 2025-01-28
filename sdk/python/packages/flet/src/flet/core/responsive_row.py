from typing import Any, Optional, Sequence, Union

from flet.core.adaptive_control import AdaptiveControl
from flet.core.animation import AnimationValue
from flet.core.constrained_control import ConstrainedControl
from flet.core.control import Control, OptionalNumber
from flet.core.ref import Ref
from flet.core.types import (
    CrossAxisAlignment,
    MainAxisAlignment,
    OffsetValue,
    OptionalControlEventCallable,
    ResponsiveNumber,
    RotateValue,
    ScaleValue,
)


class ResponsiveRow(ConstrainedControl, AdaptiveControl):
    """
    ResponsiveRow allows aligning child controls to virtual columns. By default, a virtual grid has 12 columns, but that can be customized with `ResponsiveRow.columns` property.

    Similar to `expand` property, every control now has `col` property which allows specifying how many columns a control should span.

    Example:

    ```
    import flet as ft

    def main(page: ft.Page):

        page.add(
            ft.ResponsiveRow(
                [
                    ft.TextField(label="TextField 1", col={"md": 4}),
                    ft.TextField(label="TextField 2", col={"md": 4}),
                    ft.TextField(label="TextField 3", col={"md": 4}),
                ],
                run_spacing={"xs": 10},
            ),
        )

    ft.app(target=main)
    ```

    -----

    Online docs: https://flet.dev/docs/controls/responsiverow
    """

    def __init__(
        self,
        controls: Optional[Sequence[Control]] = None,
        columns: Optional[ResponsiveNumber] = None,
        alignment: Optional[MainAxisAlignment] = None,
        vertical_alignment: Optional[CrossAxisAlignment] = None,
        spacing: Optional[ResponsiveNumber] = None,
        run_spacing: Optional[ResponsiveNumber] = None,
        rtl: Optional[bool] = None,
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
        visible: Optional[bool] = None,
        disabled: Optional[bool] = None,
        data: Any = None,
        #
        # AdaptiveControl
        #
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
            visible=visible,
            disabled=disabled,
            data=data,
            rtl=rtl,
        )

        AdaptiveControl.__init__(self, adaptive=adaptive)

        self.controls = controls
        self.alignment = alignment
        self.vertical_alignment = vertical_alignment
        self.spacing = spacing
        self.run_spacing = run_spacing
        self.columns = columns

    def _get_control_name(self):
        return "responsiverow"

    def before_update(self):
        super().before_update()
        self._set_attr_json("columns", self.__columns)
        self._set_attr_json("spacing", self.__spacing)
        self._set_attr_json("runSpacing", self.__run_spacing)

    def _get_children(self):
        return self.__controls

    def clean(self):
        super().clean()
        self.__controls.clear()

    # horizontal_alignment
    @property
    def alignment(self) -> Optional[MainAxisAlignment]:
        return self.__alignment

    @alignment.setter
    def alignment(self, value: Optional[MainAxisAlignment]):
        self.__alignment = value
        self._set_enum_attr("alignment", value, MainAxisAlignment)

    # vertical_alignment
    @property
    def vertical_alignment(self) -> Optional[CrossAxisAlignment]:
        return self.__vertical_alignment

    @vertical_alignment.setter
    def vertical_alignment(self, value: Optional[CrossAxisAlignment]):
        self.__vertical_alignment = value
        self._set_enum_attr("verticalAlignment", value, CrossAxisAlignment)

    # columns
    @property
    def columns(self) -> Optional[ResponsiveNumber]:
        return self.__columns

    @columns.setter
    def columns(self, value: Optional[ResponsiveNumber]):
        self.__columns = value

    # spacing
    @property
    def spacing(self) -> Optional[ResponsiveNumber]:
        return self.__spacing

    @spacing.setter
    def spacing(self, value: Optional[ResponsiveNumber]):
        self.__spacing = value

    # run_spacing
    @property
    def run_spacing(self) -> Optional[ResponsiveNumber]:
        return self.__run_spacing

    @run_spacing.setter
    def run_spacing(self, value: Optional[ResponsiveNumber]):
        self.__run_spacing = value

    # controls
    @property
    def controls(self):
        return self.__controls

    @controls.setter
    def controls(self, value: Optional[Sequence[Control]]):
        self.__controls = list(value) if value is not None else []
