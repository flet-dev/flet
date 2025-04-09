from dataclasses import dataclass, field
from typing import Optional

from flet.controls.adaptive_control import AdaptiveControl
from flet.controls.alignment import Alignment
from flet.controls.constrained_control import ConstrainedControl
from flet.controls.control import Control, control
from flet.controls.control_event import ControlEvent
from flet.controls.duration import OptionalDurationValue
from flet.controls.margin import MarginValue
from flet.controls.transform import Offset
from flet.controls.types import ClipBehavior, Number, OptionalEventCallable

__all__ = [
    "InteractiveViewer",
    "InteractiveViewerInteractionStartEvent",
    "InteractiveViewerInteractionUpdateEvent",
    "InteractiveViewerInteractionEndEvent",
]


@dataclass
class InteractiveViewerInteractionStartEvent(ControlEvent):
    pointer_count: int = field(metadata={"data_field": "pc"})
    global_focal_point: Offset
    local_focal_point: Offset


@dataclass
class InteractiveViewerInteractionUpdateEvent(ControlEvent):
    pointer_count: int = field(metadata={"data_field": "pc"})
    global_focal_point: Offset
    local_focal_point: Offset
    scale: float = field(metadata={"data_field": "s"})
    horizontal_scale: float = field(metadata={"data_field": "hs"})
    vertical_scale: float = field(metadata={"data_field": "vs"})
    rotation: float = field(metadata={"data_field": "rot"})


@dataclass
class InteractiveViewerInteractionEndEvent(ControlEvent):
    pointer_count: int = field(metadata={"data_field": "pc"})
    scale_velocity: float = field(metadata={"data_field": "sv"})


@control("InteractiveViewer")
class InteractiveViewer(ConstrainedControl, AdaptiveControl):
    """
    InteractiveViewer allows users to pan, zoom, and rotate content.

    -----

    Online docs: https://flet.dev/docs/controls/interactiveviewer
    """

    content: Control
    pan_enabled: bool = True
    scale_enabled: bool = True
    trackpad_scroll_causes_scale: bool = False
    constrained: bool = True
    max_scale: Number = 2.5
    min_scale: Number = 0.8
    interaction_end_friction_coefficient: Number = 0.0000135
    scale_factor: Number = 200
    clip_behavior: ClipBehavior = ClipBehavior.HARD_EDGE
    alignment: Optional[Alignment] = None
    boundary_margin: MarginValue = 0
    interaction_update_interval: int = 200
    on_interaction_start: OptionalEventCallable[
        InteractiveViewerInteractionStartEvent
    ] = None
    on_interaction_update: OptionalEventCallable[
        InteractiveViewerInteractionUpdateEvent
    ] = None
    on_interaction_end: OptionalEventCallable[
        InteractiveViewerInteractionEndEvent
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

    def reset(self, animation_duration: OptionalDurationValue = None):
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
