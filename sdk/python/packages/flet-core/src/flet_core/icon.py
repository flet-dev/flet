from typing import Any, Optional, Union

from flet_core.constrained_control import ConstrainedControl
from flet_core.control import OptionalNumber
from flet_core.ref import Ref
from flet_core.types import (
    AnimationValue,
    OffsetValue,
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
        name: Optional[str] = None,
        color: Optional[str] = None,
        size: OptionalNumber = None,
        semantics_label: Optional[str] = None,
        #
        # ConstrainedControl
        #
        ref: Optional[Ref] = None,
        key: Optional[str] = None,
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
        tooltip: Optional[str] = None,
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
            visible=visible,
            disabled=disabled,
            data=data,
        )

        self.name = name
        self.color = color
        self.size = size
        self.semantics_label = semantics_label

    def _get_control_name(self):
        return "icon"

    # name
    @property
    def name(self):
        return self._get_attr("name")

    @name.setter
    def name(self, value):
        self._set_attr("name", value)

    # color
    @property
    def color(self):
        return self._get_attr("color")

    @color.setter
    def color(self, value):
        self._set_attr("color", value)

    # size
    @property
    def size(self) -> OptionalNumber:
        return self._get_attr("size")

    @size.setter
    def size(self, value: OptionalNumber):
        self._set_attr("size", value)

    # semantics_label
    @property
    def semantics_label(self):
        return self._get_attr("semanticsLabel")

    @semantics_label.setter
    def semantics_label(self, value):
        self._set_attr("semanticsLabel", value)
