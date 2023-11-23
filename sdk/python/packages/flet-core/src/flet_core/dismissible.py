from typing import Any, Optional, Dict, Union

from flet_core.constrained_control import ConstrainedControl
from flet_core.snack_bar import DismissDirection
from flet_core.control import Control, OptionalNumber
from flet_core.ref import Ref
from flet_core.types import (
    ResponsiveNumber,
    ScaleValue,
    AnimationValue,
    RotateValue,
    OffsetValue,
)


class Dismissible(ConstrainedControl):
    """
    A control that can be dismissed by dragging in the indicated `dismiss_direction`. When dragged or flung in the
    specified `dismiss_direction`, it's content smoothly slides out of view.

    After completing the sliding animation, if a `resize_duration` is provided, this control further animates its
    height (or width, depending on what is perpendicular to the `dismiss_direction`), gradually reducing it to zero
    over the specified `resize_duration`.

    -------

    Online Docs: https://flet.dev/docs/controls/dismissible
    """

    def __init__(
        self,
        content: Control,
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
        tooltip: Optional[str] = None,
        visible: Optional[bool] = None,
        disabled: Optional[bool] = None,
        data: Any = None,
        key: Optional[str] = None,
        #
        # Specific
        #
        background: Optional[Control] = None,
        secondary_background: Optional[Control] = None,
        dismiss_direction: Optional[DismissDirection] = None,
        dismiss_thresholds: Optional[Dict[DismissDirection, OptionalNumber]] = None,
        movement_duration: Optional[int] = None,
        resize_duration: Optional[int] = None,
        cross_axis_end_offset: OptionalNumber = None,
        on_update=None,
        on_dismiss=None,
        on_resize=None,
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
            tooltip=tooltip,
            visible=visible,
            disabled=disabled,
            data=data,
        )

        self.content = content
        self.background = background
        self.secondary_background = secondary_background
        self.dismiss_direction = dismiss_direction
        self.dismiss_thresholds = dismiss_thresholds
        self.movement_duration = movement_duration
        self.resize_duration = resize_duration
        self.cross_axis_end_offset = cross_axis_end_offset
        self.on_update = on_update
        self.on_dismiss = on_dismiss
        self.on_resize = on_resize

    def _get_control_name(self):
        return "dismissible"

    def _get_children(self):
        children = []
        if self.__content:
            self.__content._set_attr_internal("n", "content")
            children.append(self.__content)
        if self.__background:
            self.__background._set_attr_internal("n", "background")
            children.append(self.__background)
        if self.__secondary_background:
            self.__secondary_background._set_attr_internal("n", "secondaryBackground")
            children.append(self.__secondary_background)
        return children

    def _before_build_command(self):
        super()._before_build_command()
        self._set_attr_json("dismissThresholds", self.__dismiss_thresholds)

    # content
    @property
    def content(self) -> Control:
        return self.__content

    @content.setter
    def content(self, value: Control):
        self.__content = value

    # background
    @property
    def background(self) -> Optional[Control]:
        return self.__background

    @background.setter
    def background(self, value: Optional[Control]):
        self.__background = value

    # secondary_background
    @property
    def secondary_background(self) -> Optional[Control]:
        return self.__secondary_background

    @secondary_background.setter
    def secondary_background(self, value: Optional[Control]):
        self.__secondary_background = value

    # movementDuration
    @property
    def movement_duration(self) -> Optional[int]:
        return self._get_attr("movementDuration")

    @movement_duration.setter
    def movement_duration(self, value: Optional[int]):
        self._set_attr("movementDuration", value)

    # resizeDuration
    @property
    def resize_duration(self) -> Optional[int]:
        return self._get_attr("resizeDuration")

    @resize_duration.setter
    def resize_duration(self, value: Optional[int]):
        self._set_attr("resizeDuration", value)

    # crossAxisEndOffset
    @property
    def cross_axis_end_offset(self) -> OptionalNumber:
        return self._get_attr("crossAxisEndOffset")

    @cross_axis_end_offset.setter
    def cross_axis_end_offset(self, value: OptionalNumber):
        self._set_attr("crossAxisEndOffset", value)

    # dismissDirection
    @property
    def dismiss_direction(self) -> Optional[DismissDirection]:
        return self.__dismiss_direction

    @dismiss_direction.setter
    def dismiss_direction(self, value: Optional[DismissDirection]):
        self.__dismiss_direction = value
        self._set_attr(
            "dismissDirection",
            value.value if isinstance(value, DismissDirection) else value,
        )

    # dismissThresholds
    @property
    def dismiss_thresholds(self) -> Optional[Dict[DismissDirection, OptionalNumber]]:
        return self.__dismiss_thresholds

    @dismiss_thresholds.setter
    def dismiss_thresholds(
        self, value: Optional[Dict[DismissDirection, OptionalNumber]]
    ):
        self.__dismiss_thresholds = value

    # on_dismiss
    @property
    def on_dismiss(self):
        return self._get_event_handler("action")

    @on_dismiss.setter
    def on_dismiss(self, handler):
        self._add_event_handler("dismiss", handler)

    # on_update
    @property
    def on_update(self):
        return self._get_event_handler("update")

    @on_update.setter
    def on_update(self, handler):
        self._add_event_handler("update", handler)

    # on_resize
    @property
    def on_resize(self):
        return self._get_event_handler("resize")

    @on_resize.setter
    def on_resize(self, handler):
        self._add_event_handler("resize", handler)
