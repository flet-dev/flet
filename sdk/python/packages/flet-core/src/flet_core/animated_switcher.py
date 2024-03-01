from enum import Enum
from typing import Any, Optional, Union

from flet_core.animation import AnimationCurve
from flet_core.constrained_control import ConstrainedControl
from flet_core.control import Control, OptionalNumber
from flet_core.ref import Ref
from flet_core.types import (
    AnimationValue,
    OffsetValue,
    ResponsiveNumber,
    RotateValue,
    ScaleValue,
)

try:
    from typing import Literal
except ImportError:
    from typing_extensions import Literal

TransitionValueString = Literal["fade", "rotation", "scale"]


class AnimatedSwitcherTransition(Enum):
    FADE = "fade"
    ROTATION = "rotation"
    SCALE = "scale"


class AnimatedSwitcher(ConstrainedControl):
    """
    A control that by default does a cross-fade between a new control and the control previously set on the AnimatedSwitcher as a `content`.

    Example:
    ```
    import flet as ft

    def main(page: ft.Page):

        c1 = ft.Container(
            ft.Text("Hello!", style=ft.TextThemeStyle.HEADLINE_MEDIUM),
            alignment=ft.alignment.center,
            width=200,
            height=200,
            bgcolor=ft.colors.GREEN,
        )
        c2 = ft.Container(
            ft.Text("Bye!", size=50),
            alignment=ft.alignment.center,
            width=200,
            height=200,
            bgcolor=ft.colors.YELLOW,
        )
        c = ft.AnimatedSwitcher(
            content=c1,
            transition=ft.AnimatedSwitcherTransition.SCALE,
            duration=500,
            reverse_duration=100,
            switch_in_curve=ft.AnimationCurve.BOUNCE_OUT,
            switch_out_curve=ft.AnimationCurve.BOUNCE_IN,
        )

        def animate(e):
            c.content = c2 if c.content == c1 else c1
            c.update()

        page.add(
            c,
            ft.ElevatedButton("Animate!", on_click=animate),
        )

    ft.app(target=main)
    ```

    -----

    Online docs: https://flet.dev/docs/controls/animatedswitcher
    """

    def __init__(
        self,
        content: Optional[Control] = None,
        duration: Optional[int] = None,
        reverse_duration: Optional[int] = None,
        switch_in_curve: Optional[AnimationCurve] = None,
        switch_out_curve: Optional[AnimationCurve] = None,
        transition: Optional[AnimatedSwitcherTransition] = None,
        #
        # ConstrainedControl
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
            visible=visible,
            disabled=disabled,
            data=data,
        )

        self.content = content
        self.duration = duration
        self.reverse_duration = reverse_duration
        self.switch_in_curve = switch_in_curve
        self.switch_out_curve = switch_out_curve
        self.transition = transition

    def _get_control_name(self):
        return "animatedswitcher"

    def before_update(self):
        super().before_update()

    def _get_children(self):
        children = []
        if self.__content is not None:
            self.__content._set_attr_internal("n", "content")
            children.append(self.__content)
        return children

    # content
    @property
    def content(self) -> Optional[Control]:
        return self.__content

    @content.setter
    def content(self, value: Optional[Control]):
        self.__content = value

    # duration
    @property
    def duration(self) -> Optional[int]:
        return self._get_attr("duration")

    @duration.setter
    def duration(self, value: Optional[int]):
        self._set_attr("duration", value)

    # reverse_duration
    @property
    def reverse_duration(self) -> Optional[int]:
        return self._get_attr("reverseDuration")

    @reverse_duration.setter
    def reverse_duration(self, value: Optional[int]):
        self._set_attr("reverseDuration", value)

    # switch_in_curve
    @property
    def switch_in_curve(self) -> Optional[AnimationCurve]:
        return self.__switch_in_curve

    @switch_in_curve.setter
    def switch_in_curve(self, value: Optional[AnimationCurve]):
        self.__switch_in_curve = value
        self._set_attr(
            "switchInCurve", value.value if isinstance(value, AnimationCurve) else value
        )

    # switch_out_curve
    @property
    def switch_out_curve(self) -> Optional[AnimationCurve]:
        return self.__switch_out_curve

    @switch_out_curve.setter
    def switch_out_curve(self, value: Optional[AnimationCurve]):
        self.__switch_out_curve = value
        self._set_attr(
            "switchOutCurve",
            value.value if isinstance(value, AnimationCurve) else value,
        )

    # transition
    @property
    def transition(self) -> Optional[AnimatedSwitcherTransition]:
        return self.__transition

    @transition.setter
    def transition(self, value: Optional[AnimatedSwitcherTransition]):
        self.__transition = value
        self._set_attr(
            "transition",
            value.value if isinstance(value, AnimatedSwitcherTransition) else value,
        )
