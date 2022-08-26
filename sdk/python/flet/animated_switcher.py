from typing import Any, Optional, Union

from beartype import beartype

from flet.animation import Curve, TransitionValue
from flet.constrained_control import ConstrainedControl
from flet.control import Control, OptionalNumber
from flet.ref import Ref
from flet.types import AnimationValue, OffsetValue, RotateValue, ScaleValue


class AnimatedSwitcher(ConstrainedControl):
    def __init__(
        self,
        content: Optional[Control] = None,
        ref: Optional[Ref] = None,
        width: OptionalNumber = None,
        height: OptionalNumber = None,
        left: OptionalNumber = None,
        top: OptionalNumber = None,
        right: OptionalNumber = None,
        bottom: OptionalNumber = None,
        expand: Union[None, bool, int] = None,
        opacity: OptionalNumber = None,
        rotate: RotateValue = None,
        scale: ScaleValue = None,
        offset: OffsetValue = None,
        animate_opacity: AnimationValue = None,
        animate_size: AnimationValue = None,
        animate_position: AnimationValue = None,
        animate_rotation: AnimationValue = None,
        animate_scale: AnimationValue = None,
        animate_offset: AnimationValue = None,
        tooltip: Optional[str] = None,
        visible: Optional[bool] = None,
        disabled: Optional[bool] = None,
        data: Any = None,
        #
        # Specific
        #
        duration: Optional[int] = None,
        reverse_duration: Optional[int] = None,
        switch_in_curve: Optional[Curve] = None,
        switch_out_curve: Optional[Curve] = None,
        transition: Optional[TransitionValue] = None,
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
            opacity=opacity,
            rotate=rotate,
            scale=scale,
            offset=offset,
            animate_opacity=animate_opacity,
            animate_size=animate_size,
            animate_position=animate_position,
            animate_rotation=animate_rotation,
            animate_scale=animate_scale,
            animate_offset=animate_offset,
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

    def _before_build_command(self):
        super()._before_build_command()

    def _get_children(self):
        children = []
        if self.__content != None:
            self.__content._set_attr_internal("n", "content")
            children.append(self.__content)
        return children

    # content
    @property
    def content(self) -> Optional[Control]:
        return self.__content

    @content.setter
    @beartype
    def content(self, value: Optional[Control]):
        self.__content = value

    # duration
    @property
    def duration(self) -> Optional[int]:
        return self._get_attr("duration")

    @duration.setter
    @beartype
    def duration(self, value: Optional[int]):
        self._set_attr("duration", value)

    # reverse_duration
    @property
    def reverse_duration(self) -> Optional[int]:
        return self._get_attr("reverseDuration")

    @reverse_duration.setter
    @beartype
    def reverse_duration(self, value: Optional[int]):
        self._set_attr("reverseDuration", value)

    # switch_in_curve
    @property
    def switch_in_curve(self) -> Optional[Curve]:
        return self._get_attr("switchInCurve")

    @switch_in_curve.setter
    @beartype
    def switch_in_curve(self, value: Optional[Curve]):
        self._set_attr("switchInCurve", value)

    # switch_out_curve
    @property
    def switch_out_curve(self) -> Optional[Curve]:
        return self._get_attr("switchOutCurve")

    @switch_out_curve.setter
    @beartype
    def switch_out_curve(self, value: Optional[Curve]):
        self._set_attr("switchOutCurve", value)

    # transition
    @property
    def transition(self) -> Optional[TransitionValue]:
        return self._get_attr("transition")

    @transition.setter
    @beartype
    def transition(self, value: Optional[TransitionValue]):
        self._set_attr("transition", value)
