from typing import Any, Optional, Union

from beartype import beartype
from beartype.typing import List

from flet.constrained_control import ConstrainedControl
from flet.control import Control, OptionalNumber
from flet.ref import Ref
from flet.types import (
    AnimationValue,
    OffsetValue,
    PaddingValue,
    ResponsiveNumber,
    RotateValue,
    ScaleValue,
)


class GridView(ConstrainedControl):
    """
    A scrollable, 2D array of controls.

    GridView is very effective for large lists (thousands of items). Prefer it over wrapping `Column` or `Row` for smooth scrolling.

    Example:
    ```
    import flet as ft

    def main(page: ft.Page):
        page.title = "GridView Example"
        page.theme_mode = ft.ThemeMode.DARK
        page.padding = 50
        page.update()

        images = ft.GridView(
            expand=1,
            runs_count=5,
            max_extent=150,
            child_aspect_ratio=1.0,
            spacing=5,
            run_spacing=5,
        )

        page.add(images)

        for i in range(0, 60):
            images.controls.append(
                ft.Image(
                    src=f"https://picsum.photos/150/150?{i}",
                    fit=ft.ImageFit.NONE,
                    repeat=ft.ImageRepeat.NO_REPEAT,
                    border_radius=ft.border_radius.all(10),
                )
            )
        page.update()

    ft.app(target=main)

    ```

    -----

    Online docs: https://flet.dev/docs/controls/gridview
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
        # Specific
        #
        horizontal: Optional[bool] = None,
        runs_count: Optional[int] = None,
        max_extent: Optional[int] = None,
        spacing: OptionalNumber = None,
        run_spacing: OptionalNumber = None,
        child_aspect_ratio: OptionalNumber = None,
        padding: PaddingValue = None,
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

        self.__controls: List[Control] = []
        self.controls = controls
        self.horizontal = horizontal
        self.runs_count = runs_count
        self.max_extent = max_extent
        self.spacing = spacing
        self.run_spacing = run_spacing
        self.child_aspect_ratio = child_aspect_ratio
        self.padding = padding

    def _get_control_name(self):
        return "gridview"

    def _before_build_command(self):
        super()._before_build_command()
        self._set_attr_json("padding", self.__padding)

    def _get_children(self):
        return self.__controls

    def clean(self):
        Control.clean(self)
        self.__controls.clear()

    # horizontal
    @property
    def horizontal(self) -> Optional[bool]:
        return self._get_attr("horizontal")

    @horizontal.setter
    @beartype
    def horizontal(self, value: Optional[bool]):
        self._set_attr("horizontal", value)

    # runs_count
    @property
    def runs_count(self) -> Optional[int]:
        return self._get_attr("runsCount")

    @runs_count.setter
    @beartype
    def runs_count(self, value: Optional[int]):
        self._set_attr("runsCount", value)

    # max_extent
    @property
    def max_extent(self) -> OptionalNumber:
        return self._get_attr("maxExtent")

    @max_extent.setter
    @beartype
    def max_extent(self, value: OptionalNumber):
        self._set_attr("maxExtent", value)

    # spacing
    @property
    def spacing(self) -> OptionalNumber:
        return self._get_attr("spacing")

    @spacing.setter
    @beartype
    def spacing(self, value: OptionalNumber):
        self._set_attr("spacing", value)

    # run_spacing
    @property
    def run_spacing(self) -> OptionalNumber:
        return self._get_attr("runSpacing")

    @run_spacing.setter
    @beartype
    def run_spacing(self, value: OptionalNumber):
        self._set_attr("runSpacing", value)

    # child_aspect_ratio
    @property
    def child_aspect_ratio(self) -> OptionalNumber:
        return self._get_attr("childAspectRatio")

    @child_aspect_ratio.setter
    @beartype
    def child_aspect_ratio(self, value: OptionalNumber):
        self._set_attr("childAspectRatio", value)

    # padding
    @property
    def padding(self) -> PaddingValue:
        return self.__padding

    @padding.setter
    @beartype
    def padding(self, value: PaddingValue):
        self.__padding = value

    # controls
    @property
    def controls(self):
        return self.__controls

    @controls.setter
    def controls(self, value):
        self.__controls = value if value is not None else []
