from typing import Any, List, Optional, Union

from flet_core.constrained_control import ConstrainedControl
from flet_core.control import Control, OptionalNumber
from flet_core.ref import Ref
from flet_core.types import (
    AnimationValue,
    CrossAxisAlignment,
    MainAxisAlignment,
    OffsetValue,
    ResponsiveNumber,
    RotateValue,
    ScaleValue,
)
from flet_core.utils import get_valid_enum, get_non_default_value


_CrossAxisAlignmentDefault = CrossAxisAlignment.START
_MainAxisAlignmentDefault = MainAxisAlignment.START


class ResponsiveRow(ConstrainedControl):
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
        controls: Optional[List[Control]] = None,
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
        visible: Optional[bool] = None,
        disabled: Optional[bool] = None,
        data: Any = None,
        #
        # Row specific
        #
        columns: Optional[ResponsiveNumber] = None,
        alignment: MainAxisAlignment = _MainAxisAlignmentDefault,
        vertical_alignment: CrossAxisAlignment = _CrossAxisAlignmentDefault,
        spacing: Optional[ResponsiveNumber] = None,
        run_spacing: Optional[ResponsiveNumber] = None,
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
            visible=visible,
            disabled=disabled,
            data=data,
        )

        self.controls = controls
        self.alignment = alignment
        self.vertical_alignment = vertical_alignment
        self.spacing = spacing
        self.run_spacing = run_spacing
        self.columns = columns

    def _get_control_name(self):
        return "responsiverow"

    def _before_build_command(self):
        super()._before_build_command()
        self._set_attr_json("columns", self.__columns)
        self._set_attr_json("spacing", self.__spacing)
        self._set_attr_json("runSpacing", self.__run_spacing)

    def _get_children(self):
        return self.__controls

    def clean(self):
        super().clean()
        self.__controls.clear()

    async def clean_async(self):
        await super().clean_async()
        self.__controls.clear()

    # horizontal_alignment
    @property
    def alignment(self) -> MainAxisAlignment:
        return self.__alignment

    @alignment.setter
    def alignment(self, value: MainAxisAlignment):
        self.__alignment = get_valid_enum(MainAxisAlignment, value, _MainAxisAlignmentDefault)
        self._set_attr("alignment", get_non_default_value(self.__alignment, _MainAxisAlignmentDefault))

    # vertical_alignment
    @property
    def vertical_alignment(self) -> CrossAxisAlignment:
        return self.__vertical_alignment

    @vertical_alignment.setter
    def vertical_alignment(self, value: CrossAxisAlignment):
        self.__vertical_alignment = get_valid_enum(CrossAxisAlignment, value, _CrossAxisAlignmentDefault)
        self._set_attr("verticalAlignment", get_non_default_value(
            self.__vertical_alignment, _CrossAxisAlignmentDefault,
        ))

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
    def controls(self, value):
        self.__controls = value if value is not None else []
