from typing import Any, List, Optional, Union

from flet_core.adaptive_control import AdaptiveControl
from flet_core.constrained_control import ConstrainedControl
from flet_core.control import Control, OptionalNumber
from flet_core.ref import Ref
from flet_core.scrollable_control import ScrollableControl
from flet_core.types import (
    AnimationValue,
    CrossAxisAlignment,
    MainAxisAlignment,
    OffsetValue,
    ResponsiveNumber,
    RotateValue,
    ScaleValue,
    ScrollMode,
)
from flet_core.utils import deprecated


class Row(ConstrainedControl, ScrollableControl, AdaptiveControl):
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
        alignment: MainAxisAlignment = MainAxisAlignment.NONE,
        vertical_alignment: CrossAxisAlignment = CrossAxisAlignment.NONE,
        spacing: OptionalNumber = None,
        tight: Optional[bool] = None,
        wrap: Optional[bool] = None,
        run_spacing: OptionalNumber = None,
        #
        # ScrollableControl specific
        #
        scroll: Optional[ScrollMode] = None,
        auto_scroll: Optional[bool] = None,
        on_scroll_interval: OptionalNumber = None,
        on_scroll: Any = None,
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
        rtl: Optional[bool] = None,
        #
        # Adaptive
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

        ScrollableControl.__init__(
            self,
            scroll=scroll,
            auto_scroll=auto_scroll,
            on_scroll_interval=on_scroll_interval,
            on_scroll=on_scroll,
        )

        AdaptiveControl.__init__(self, adaptive=adaptive)

        self.controls = controls
        self.alignment = alignment
        self.vertical_alignment = vertical_alignment
        self.spacing = spacing
        self.tight = tight
        self.wrap = wrap
        self.run_spacing = run_spacing

    def _get_control_name(self):
        return "row"

    def _get_children(self):
        return self.__controls

    def clean(self):
        super().clean()
        self.__controls.clear()

    @deprecated(
        reason="Use clean() method instead.",
        version="0.21.0",
        delete_version="1.0",
    )
    async def clean_async(self):
        self.clean()

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
        self._set_attr(
            "alignment", value.value if isinstance(value, MainAxisAlignment) else value
        )

    # vertical_alignment
    @property
    def vertical_alignment(self) -> CrossAxisAlignment:
        return self.__vertical_alignment

    @vertical_alignment.setter
    def vertical_alignment(self, value: CrossAxisAlignment):
        self.__vertical_alignment = value
        self._set_attr(
            "verticalAlignment",
            value.value if isinstance(value, CrossAxisAlignment) else value,
        )

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

    # controls
    @property
    def controls(self):
        return self.__controls

    @controls.setter
    def controls(self, value: Optional[List[Control]]):
        self.__controls = value if value is not None else []
