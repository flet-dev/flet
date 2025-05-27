import asyncio
from dataclasses import dataclass
from typing import Optional

from flet.controls.adaptive_control import AdaptiveControl
from flet.controls.alignment import Alignment
from flet.controls.base_control import control
from flet.controls.constrained_control import ConstrainedControl
from flet.controls.control import Control
from flet.controls.duration import OptionalDurationValue
from flet.controls.events import (
    ScaleEndEvent,
    ScaleStartEvent,
    ScaleUpdateEvent,
)
from flet.controls.margin import MarginValue
from flet.controls.types import ClipBehavior, Number, OptionalEventCallable

__all__ = [
    "InteractiveViewer",
    "InteractiveViewerInteractionStartEvent",
    "InteractiveViewerInteractionUpdateEvent",
    "InteractiveViewerInteractionEndEvent",
]


@dataclass
class InteractiveViewerInteractionStartEvent(ScaleStartEvent):
    pass


@dataclass
class InteractiveViewerInteractionUpdateEvent(ScaleUpdateEvent):
    pass


@dataclass
class InteractiveViewerInteractionEndEvent(ScaleEndEvent):
    pass


@control("InteractiveViewer")
class InteractiveViewer(ConstrainedControl, AdaptiveControl):
    """
    InteractiveViewer allows users to pan, zoom, and rotate content.

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
        asyncio.create_task(self.reset_async(animation_duration))

    async def reset_async(self, animation_duration: OptionalDurationValue = None):
        await self._invoke_method_async(
            "reset", arguments={"animation_duration": animation_duration}
        )

    def save_state(self):
        asyncio.create_task(self.save_state_async())

    async def save_state_async(self):
        await self._invoke_method_async("save_state")

    def restore_state(self):
        asyncio.create_task(self.restore_state_async())

    async def restore_state_async(self):
        await self._invoke_method_async("restore_state")

    def zoom(self, factor: Number):
        asyncio.create_task(self.zoom_async(factor))

    async def zoom_async(self, factor: Number):
        await self._invoke_method_async("zoom", arguments={"factor": factor})

    def pan(self, dx: Number, dy: Number = 0, dz: Number = 0):
        asyncio.create_task(self.pan_async(dx, dy, dz))

    async def pan_async(self, dx: Number, dy: Number = 0, dz: Number = 0):
        await self._invoke_method_async("pan", arguments={"dx": dx, "dy": dy, "dz": dz})
