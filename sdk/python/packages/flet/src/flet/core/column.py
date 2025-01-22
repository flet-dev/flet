from typing import Any, Callable, Optional, Sequence, Union

from flet.core.adaptive_control import AdaptiveControl
from flet.core.animation import AnimationValue
from flet.core.constrained_control import ConstrainedControl
from flet.core.control import Control
from flet.core.ref import Ref
from flet.core.scrollable_control import OnScrollEvent, ScrollableControl
from flet.core.types import (
    CrossAxisAlignment,
    MainAxisAlignment,
    OffsetValue,
    OptionalControlEventCallable,
    OptionalNumber,
    ResponsiveNumber,
    RotateValue,
    ScaleValue,
    ScrollMode,
)


class Column(ConstrainedControl, ScrollableControl, AdaptiveControl):
    """
    Container allows to decorate a control with background color and border and position it with padding, margin and alignment.

    Example:

    ```
    import flet as ft

    def main(page: ft.Page):
        page.title = "Column example"

        page.add(
            ft.Column(
                expand=True,
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

    Online docs: https://flet.dev/docs/controls/column
    """

    def __init__(
        self,
        controls: Optional[Sequence[Control]] = None,
        alignment: Optional[MainAxisAlignment] = None,
        horizontal_alignment: Optional[CrossAxisAlignment] = None,
        spacing: OptionalNumber = None,
        tight: Optional[bool] = None,
        wrap: Optional[bool] = None,
        run_spacing: OptionalNumber = None,
        run_alignment: Optional[MainAxisAlignment] = None,
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
        rtl: Optional[bool] = None,
        #
        # ScrollableControl and AdaptiveControl
        #
        scroll: Optional[ScrollMode] = None,
        auto_scroll: Optional[bool] = None,
        on_scroll_interval: OptionalNumber = None,
        on_scroll: Optional[Callable[[OnScrollEvent], None]] = None,
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
        self.horizontal_alignment = horizontal_alignment
        self.alignment = alignment
        self.spacing = spacing
        self.tight = tight
        self.wrap = wrap
        self.run_spacing = run_spacing
        self.run_alignment = run_alignment

    def _get_control_name(self):
        return "column"

    def _get_children(self):
        return self.__controls

    def __contains__(self, item):
        return item in self.__controls

    # Public methods
    def clean(self):
        super().clean()
        self.__controls.clear()

    # tight
    @property
    def tight(self) -> bool:
        return self._get_attr("tight", data_type="bool", def_value=False)

    @tight.setter
    def tight(self, value: Optional[bool]):
        self._set_attr("tight", value)

    # alignment
    @property
    def alignment(self) -> Optional[MainAxisAlignment]:
        return self.__alignment

    @alignment.setter
    def alignment(self, value: Optional[MainAxisAlignment]):
        self.__alignment = value
        self._set_enum_attr("alignment", value, MainAxisAlignment)

    # run_alignment
    @property
    def run_alignment(self) -> Optional[MainAxisAlignment]:
        return self.__run_alignment

    @run_alignment.setter
    def run_alignment(self, value: Optional[MainAxisAlignment]):
        self.__run_alignment = value
        self._set_enum_attr("runAlignment", value, MainAxisAlignment)

    # horizontal_alignment
    @property
    def horizontal_alignment(self) -> Optional[CrossAxisAlignment]:
        return self.__horizontal_alignment

    @horizontal_alignment.setter
    def horizontal_alignment(self, value: Optional[CrossAxisAlignment]):
        self.__horizontal_alignment = value
        self._set_enum_attr("horizontalAlignment", value, CrossAxisAlignment)

    # spacing
    @property
    def spacing(self) -> OptionalNumber:
        return self._get_attr("spacing", data_type="float", def_value=10)

    @spacing.setter
    def spacing(self, value: OptionalNumber):
        self._set_attr("spacing", value)

    # wrap
    @property
    def wrap(self) -> bool:
        return self._get_attr("wrap", data_type="bool", def_value=False)

    @wrap.setter
    def wrap(self, value: Optional[bool]):
        self._set_attr("wrap", value)

    # run_spacing
    @property
    def run_spacing(self) -> OptionalNumber:
        return self._get_attr("runSpacing", data_type="float")

    @run_spacing.setter
    def run_spacing(self, value: OptionalNumber):
        self._set_attr("runSpacing", value)

    # controls
    @property
    def controls(self):
        return self.__controls

    @controls.setter
    def controls(self, value: Optional[Sequence[Control]]):
        self.__controls = list(value) if value is not None else []
