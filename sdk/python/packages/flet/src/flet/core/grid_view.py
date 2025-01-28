from typing import Any, Callable, List, Optional, Sequence, Union

from flet.core.adaptive_control import AdaptiveControl
from flet.core.animation import AnimationValue
from flet.core.constrained_control import ConstrainedControl
from flet.core.control import Control, OptionalNumber
from flet.core.ref import Ref
from flet.core.scrollable_control import OnScrollEvent, ScrollableControl
from flet.core.types import (
    ClipBehavior,
    OffsetValue,
    OptionalControlEventCallable,
    PaddingValue,
    ResponsiveNumber,
    RotateValue,
    ScaleValue,
)


class GridView(ConstrainedControl, ScrollableControl, AdaptiveControl):
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
        controls: Optional[Sequence[Control]] = None,
        horizontal: Optional[bool] = None,
        runs_count: Optional[int] = None,
        max_extent: Optional[int] = None,
        spacing: OptionalNumber = None,
        run_spacing: OptionalNumber = None,
        child_aspect_ratio: OptionalNumber = None,
        padding: Optional[PaddingValue] = None,
        clip_behavior: Optional[ClipBehavior] = None,
        semantic_child_count: Optional[int] = None,
        cache_extent: OptionalNumber = None,
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
        # ScrollableControl
        #
        auto_scroll: Optional[bool] = None,
        reverse: Optional[bool] = None,
        on_scroll_interval: OptionalNumber = None,
        on_scroll: Optional[Callable[[OnScrollEvent], None]] = None,
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
        )

        ScrollableControl.__init__(
            self,
            auto_scroll=auto_scroll,
            reverse=reverse,
            on_scroll_interval=on_scroll_interval,
            on_scroll=on_scroll,
        )

        AdaptiveControl.__init__(self, adaptive=adaptive)

        self.__controls: List[Control] = []
        self.controls = controls
        self.horizontal = horizontal
        self.runs_count = runs_count
        self.max_extent = max_extent
        self.spacing = spacing
        self.run_spacing = run_spacing
        self.child_aspect_ratio = child_aspect_ratio
        self.padding = padding
        self.clip_behavior = clip_behavior
        self.semantic_child_count = semantic_child_count
        self.cache_extent = cache_extent

    def _get_control_name(self):
        return "gridview"

    def __contains__(self, item):
        return item in self.__controls

    def before_update(self):
        super().before_update()
        self._set_attr_json("padding", self.__padding)

    def _get_children(self):
        return self.__controls

    def clean(self):
        super().clean()
        self.__controls.clear()

    # horizontal
    @property
    def horizontal(self) -> bool:
        return self._get_attr("horizontal", data_type="bool", def_value=False)

    @horizontal.setter
    def horizontal(self, value: Optional[bool]):
        self._set_attr("horizontal", value)

    # cache_extent
    @property
    def cache_extent(self) -> OptionalNumber:
        return self._get_attr("cacheExtent")

    @cache_extent.setter
    def cache_extent(self, value: OptionalNumber):
        self._set_attr("cacheExtent", value)

    # runs_count
    @property
    def runs_count(self) -> Optional[int]:
        return self._get_attr("runsCount")

    @runs_count.setter
    def runs_count(self, value: Optional[int]):
        self._set_attr("runsCount", value)

    # max_extent
    @property
    def max_extent(self) -> OptionalNumber:
        return self._get_attr("maxExtent")

    @max_extent.setter
    def max_extent(self, value: OptionalNumber):
        self._set_attr("maxExtent", value)

    # spacing
    @property
    def spacing(self) -> OptionalNumber:
        return self._get_attr("spacing")

    @spacing.setter
    def spacing(self, value: OptionalNumber):
        self._set_attr("spacing", value)

    # run_spacing
    @property
    def run_spacing(self) -> OptionalNumber:
        return self._get_attr("runSpacing")

    @run_spacing.setter
    def run_spacing(self, value: OptionalNumber):
        self._set_attr("runSpacing", value)

    # child_aspect_ratio
    @property
    def child_aspect_ratio(self) -> OptionalNumber:
        return self._get_attr("childAspectRatio")

    @child_aspect_ratio.setter
    def child_aspect_ratio(self, value: OptionalNumber):
        self._set_attr("childAspectRatio", value)

    # padding
    @property
    def padding(self) -> Optional[PaddingValue]:
        return self.__padding

    @padding.setter
    def padding(self, value: Optional[PaddingValue]):
        self.__padding = value

    # controls
    @property
    def controls(self):
        return self.__controls

    @controls.setter
    def controls(self, value: Optional[Sequence[Control]]):
        self.__controls = list(value) if value is not None else []

    # clip_behavior
    @property
    def clip_behavior(self) -> Optional[ClipBehavior]:
        return self.__clip_behavior

    @clip_behavior.setter
    def clip_behavior(self, value: Optional[ClipBehavior]):
        self.__clip_behavior = value
        self._set_enum_attr("clipBehavior", value, ClipBehavior)

    # semantic_child_count
    @property
    def semantic_child_count(self) -> Optional[int]:
        return self._get_attr("semanticChildCount", data_type="int")

    @semantic_child_count.setter
    def semantic_child_count(self, value: Optional[int]):
        self._set_attr("semanticChildCount", value)
