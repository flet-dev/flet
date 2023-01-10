from typing import Any, List, Optional, Union

from flet_core.constrained_control import ConstrainedControl
from flet_core.control import Control, OptionalNumber
from flet_core.ref import Ref
from flet_core.types import (
    AnimationValue,
    CrossAxisAlignment,
    CrossAxisAlignmentString,
    MainAxisAlignment,
    MainAxisAlignmentString,
    OffsetValue,
    ResponsiveNumber,
    RotateValue,
    ScaleValue,
    ScrollMode,
    ScrollModeString,
)


class Row(ConstrainedControl):
    """
    A control that displays its children in a horizontal array.

    To cause a child control to expand and fill the available horizontal space, set its `expand` property.

    Example:

    ```
    import flet as ft


    def main(page: ft.Page):
        page.title = "Row example"

        page.add(
            ft.Row(
                controls=[
                    ft.Container(
                        expand=1,
                        content=ft.Text("Container 1"),
                        bgcolor=ft.colors.GREEN_100,
                    ),
                    ft.Container(
                        expand=2, content=ft.Text("Container 2"), bgcolor=ft.colors.RED_100
                    ),
                ],
            ),
        ),


    ft.app(target=main)
    ```

    -----

    Online docs: https://flet.dev/docs/controls/row
    """

    def __init__(
        self,
        controls: Optional[List[Control]] = None,
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
        # Row specific
        #
        alignment: MainAxisAlignment = MainAxisAlignment.NONE,
        vertical_alignment: CrossAxisAlignment = CrossAxisAlignment.NONE,
        spacing: OptionalNumber = None,
        tight: Optional[bool] = None,
        wrap: Optional[bool] = None,
        run_spacing: OptionalNumber = None,
        scroll: Optional[ScrollMode] = None,
        auto_scroll: Optional[bool] = None,
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

        self.controls = controls
        self.alignment = alignment
        self.vertical_alignment = vertical_alignment
        self.spacing = spacing
        self.tight = tight
        self.wrap = wrap
        self.run_spacing = run_spacing
        self.scroll = scroll
        self.auto_scroll = auto_scroll

    def _get_control_name(self):
        return "row"

    def _get_children(self):
        return self.__controls

    def clean(self):
        super().clean()
        self.__controls.clear()

    async def clean_async(self):
        await super().clean_async()
        self.__controls.clear()

    # tight
    @property
    def tight(self) -> Optional[bool]:
        return self._get_attr("tight", data_type="bool", def_value=False)

    @tight.setter
    def tight(self, value: Optional[bool]):
        self._set_attr("tight", value)

    # horizontal_alignment
    @property
    def alignment(self) -> MainAxisAlignment:
        return self.__alignment

    @alignment.setter
    def alignment(self, value: MainAxisAlignment):
        self.__alignment = value
        if isinstance(value, MainAxisAlignment):
            self._set_attr("alignment", value.value)
        else:
            self.__set_alignment(value)

    def __set_alignment(self, value: MainAxisAlignmentString):
        self._set_attr("alignment", value)

    # vertical_alignment
    @property
    def vertical_alignment(self) -> CrossAxisAlignment:
        return self.__vertical_alignment

    @vertical_alignment.setter
    def vertical_alignment(self, value: CrossAxisAlignment):
        self.__vertical_alignment = value
        if isinstance(value, CrossAxisAlignment):
            self._set_attr("verticalAlignment", value.value)
        else:
            self.__set_vertical_alignment(value)

    def __set_vertical_alignment(self, value: CrossAxisAlignmentString):
        self._set_attr("verticalAlignment", value)

    # spacing
    @property
    def spacing(self) -> OptionalNumber:
        return self._get_attr("spacing")

    @spacing.setter
    def spacing(self, value: OptionalNumber):
        self._set_attr("spacing", value)

    # wrap
    @property
    def wrap(self) -> Optional[bool]:
        return self._get_attr("wrap", data_type="bool", def_value=False)

    @wrap.setter
    def wrap(self, value: Optional[bool]):
        self._set_attr("wrap", value)

    # run_spacing
    @property
    def run_spacing(self) -> OptionalNumber:
        return self._get_attr("runSpacing")

    @run_spacing.setter
    def run_spacing(self, value: OptionalNumber):
        self._set_attr("runSpacing", value)

    # scroll
    @property
    def scroll(self) -> Optional[ScrollMode]:
        return self.__scroll

    @scroll.setter
    def scroll(self, value: Optional[ScrollMode]):
        self.__scroll = value
        if isinstance(value, ScrollMode):
            self._set_attr("scroll", value.value)
        else:
            self.__set_scroll(value)

    def __set_scroll(self, value: Optional[ScrollModeString]):
        if value == True:
            value = "auto"
        elif value == False:
            value = None
        self._set_attr("scroll", value)

    # auto_scroll
    @property
    def auto_scroll(self) -> Optional[bool]:
        return self._get_attr("autoScroll")

    @auto_scroll.setter
    def auto_scroll(self, value: Optional[bool]):
        self._set_attr("autoScroll", value)

    # controls
    @property
    def controls(self):
        return self.__controls

    @controls.setter
    def controls(self, value: Optional[List[Control]]):
        self.__controls = value if value is not None else []
