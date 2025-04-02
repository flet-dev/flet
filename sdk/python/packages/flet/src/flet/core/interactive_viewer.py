from dataclasses import field
from typing import Callable, Optional

from flet.core.adaptive_control import AdaptiveControl
from flet.core.alignment import Alignment
from flet.core.constrained_control import ConstrainedControl
from flet.core.control import Control, control
from flet.core.control_event import ControlEvent
from flet.core.types import (
    ClipBehavior,
    DurationValue,
    MarginValue,
    Number,
    Offset,
    OptionalNumber,
)

__all__ = [
    "InteractiveViewer",
    "InteractiveViewerInteractionStartEvent",
    "InteractiveViewerInteractionUpdateEvent",
    "InteractiveViewerInteractionEndEvent",
]


class InteractiveViewerInteractionStartEvent(ControlEvent):
    pointer_count: int
    global_focal_point: Offset
    local_focal_point: Offset


class InteractiveViewerInteractionUpdateEvent(ControlEvent):
    pointer_count: int
    global_focal_point: Offset
    local_focal_point: Offset
    scale: float
    horizontal_scale: float
    vertical_scale: float
    rotation: float


class InteractiveViewerInteractionEndEvent(ControlEvent):
    pointer_count: int
    scale_velocity: float


@control("InteractiveViewer")
class InteractiveViewer(ConstrainedControl, AdaptiveControl):
    """
    InteractiveViewer allows users to pan, zoom, and rotate content.

    -----

    Online docs: https://flet.dev/docs/controls/interactiveviewer
    """

    content: Control
    pan_enabled: Optional[bool] = None
    scale_enabled: Optional[bool] = None
    trackpad_scroll_causes_scale: Optional[bool] = None
    constrained: Optional[bool] = None
    max_scale: Number = field(default=2.5)
    min_scale: Number = field(default=0.8)
    interaction_end_friction_coefficient: OptionalNumber = None
    scale_factor: OptionalNumber = None
    clip_behavior: Optional[ClipBehavior] = None
    alignment: Optional[Alignment] = None
    boundary_margin: Optional[MarginValue] = None
    interaction_update_interval: int = field(default=200)
    on_interaction_start: Optional[
        Callable[[InteractiveViewerInteractionStartEvent], None]
    ] = None
    on_interaction_update: Optional[
        Callable[[InteractiveViewerInteractionUpdateEvent], None]
    ] = (None,)
    on_interaction_end: Optional[
        Callable[[InteractiveViewerInteractionEndEvent], None]
    ] = None

    def before_update(self):
        super().before_update()
        assert self.content.visible, "content must be visible"
        assert self.min_scale > 0, "min_scale must be greater than 0"
        assert self.max_scale > 0, "max_scale must be greater than 0"
        assert (
            self.max_scale >= self.min_scale
        ), "max_scale must be greather than or equal to min_scale"
        assert (
            self.interaction_end_friction_coefficient is None
            or self.interaction_end_friction_coefficient > 0
        ), "interaction_end_friction_coefficient must be greater than 0"

    def reset(self, animation_duration: Optional[DurationValue] = None):
        self.invoke_method(
            "reset", arguments={"duration": self._convert_attr_json(animation_duration)}
        )

    def save_state(self):
        self.invoke_method("save_state")

    def restore_state(self):
        self.invoke_method("restore_state")

    def zoom(self, factor: Number):
        self.invoke_method("zoom", arguments={"factor": str(factor)})

    def pan(self, dx: Number, dy: Number):
        self.invoke_method("pan", arguments={"dx": str(dx), "dy": str(dy)})
