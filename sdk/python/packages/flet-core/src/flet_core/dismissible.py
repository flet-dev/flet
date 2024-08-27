import json
from typing import Any, Dict, Optional, Union

from flet_core.adaptive_control import AdaptiveControl
from flet_core.constrained_control import ConstrainedControl
from flet_core.control import Control, OptionalNumber
from flet_core.control_event import ControlEvent
from flet_core.event_handler import EventHandler
from flet_core.ref import Ref
from flet_core.snack_bar import DismissDirection
from flet_core.tooltip import TooltipValue
from flet_core.types import (
    AnimationValue,
    OffsetValue,
    ResponsiveNumber,
    RotateValue,
    ScaleValue,
    OptionalEventCallable,
    OptionalControlEventCallable,
)
from flet_core.utils import deprecated


class Dismissible(ConstrainedControl, AdaptiveControl):
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
        background: Optional[Control] = None,
        secondary_background: Optional[Control] = None,
        dismiss_direction: Optional[DismissDirection] = None,
        dismiss_thresholds: Optional[Dict[DismissDirection, OptionalNumber]] = None,
        movement_duration: Optional[int] = None,
        resize_duration: Optional[int] = None,
        cross_axis_end_offset: OptionalNumber = None,
        on_update: OptionalEventCallable["DismissibleUpdateEvent"] = None,
        on_dismiss: OptionalEventCallable["DismissibleDismissEvent"] = None,
        on_confirm_dismiss: OptionalEventCallable["DismissibleDismissEvent"] = None,
        on_resize: OptionalControlEventCallable = None,
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
        on_animation_end: OptionalControlEventCallable = None,
        tooltip: TooltipValue = None,
        visible: Optional[bool] = None,
        disabled: Optional[bool] = None,
        data: Any = None,
        key: Optional[str] = None,
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
            tooltip=tooltip,
            visible=visible,
            disabled=disabled,
            data=data,
        )

        AdaptiveControl.__init__(self, adaptive=adaptive)

        self.__on_dismiss = EventHandler(lambda e: DismissibleDismissEvent(e))
        self.__on_update = EventHandler(lambda e: DismissibleUpdateEvent(e))
        self.__on_confirm_dismiss = EventHandler(lambda e: DismissibleDismissEvent(e))

        self._add_event_handler("dismiss", self.__on_dismiss.get_handler())
        self._add_event_handler("update", self.__on_update.get_handler())
        self._add_event_handler(
            "confirm_dismiss", self.__on_confirm_dismiss.get_handler()
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
        self.on_confirm_dismiss = on_confirm_dismiss
        self.on_resize = on_resize

    def _get_control_name(self):
        return "dismissible"

    def _get_children(self):
        self.__content._set_attr_internal("n", "content")
        children = [self.__content]
        if self.__background:
            self.__background._set_attr_internal("n", "background")
            children.append(self.__background)
        if self.__secondary_background:
            self.__secondary_background._set_attr_internal("n", "secondaryBackground")
            children.append(self.__secondary_background)
        return children

    def before_update(self):
        super().before_update()
        self._set_attr_json("dismissThresholds", self.__dismiss_thresholds)

    def confirm_dismiss(self, dismiss: bool):
        self.invoke_method("confirm_dismiss", {"dismiss": str(dismiss).lower()})

    @deprecated(
        reason="Use confirm_dismiss() method instead.",
        version="0.21.0",
        delete_version="0.26.0",
    )
    async def confirm_dismiss_async(self, dismiss: bool):
        self.confirm_dismiss(dismiss)

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
        return self._get_attr("movementDuration", data_type="int")

    @movement_duration.setter
    def movement_duration(self, value: Optional[int]):
        self._set_attr("movementDuration", value)

    # resizeDuration
    @property
    def resize_duration(self) -> Optional[int]:
        return self._get_attr("resizeDuration", data_type="int")

    @resize_duration.setter
    def resize_duration(self, value: Optional[int]):
        self._set_attr("resizeDuration", value)

    # crossAxisEndOffset
    @property
    def cross_axis_end_offset(self) -> OptionalNumber:
        return self._get_attr("crossAxisEndOffset", data_type="float")

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
        self._set_enum_attr("dismissDirection", value, DismissDirection)

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
    def on_dismiss(self) -> OptionalEventCallable["DismissibleDismissEvent"]:
        return self.__on_dismiss.handler

    @on_dismiss.setter
    def on_dismiss(self, handler: OptionalEventCallable["DismissibleDismissEvent"]):
        self.__on_dismiss.handler = handler
        self._set_attr("onDismiss", True if handler is not None else None)

    # on_confirm_dismiss
    @property
    def on_confirm_dismiss(self) -> OptionalEventCallable["DismissibleDismissEvent"]:
        return self.__on_confirm_dismiss.handler

    @on_confirm_dismiss.setter
    def on_confirm_dismiss(
        self, handler: OptionalEventCallable["DismissibleDismissEvent"]
    ):
        self.__on_confirm_dismiss.handler = handler
        self._set_attr("onConfirmDismiss", True if handler is not None else None)

    # on_update
    @property
    def on_update(self) -> OptionalEventCallable["DismissibleUpdateEvent"]:
        return self.__on_update.handler

    @on_update.setter
    def on_update(self, handler: OptionalEventCallable["DismissibleUpdateEvent"]):
        self.__on_update.handler = handler
        self._set_attr("onUpdate", True if handler is not None else None)

    # on_resize
    @property
    def on_resize(self):
        return self._get_event_handler("resize")

    @on_resize.setter
    def on_resize(self, handler: OptionalControlEventCallable):
        self._add_event_handler("resize", handler)
        self._set_attr("onResize", True if handler is not None else None)


class DismissibleDismissEvent(ControlEvent):
    def __init__(self, e: ControlEvent):
        super().__init__(e.target, e.name, e.data, e.control, e.page)
        self.direction = DismissDirection(e.data)


class DismissibleUpdateEvent(ControlEvent):
    def __init__(self, e: ControlEvent):
        super().__init__(e.target, e.name, e.data, e.control, e.page)
        d = json.loads(e.data)
        self.direction: DismissDirection = DismissDirection(d.get("direction"))
        self.progress: float = d.get("progress")
        self.reached: bool = d.get("reached")
        self.previous_reached: bool = d.get("previous_reached")
