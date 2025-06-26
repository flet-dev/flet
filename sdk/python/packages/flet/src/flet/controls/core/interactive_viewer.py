import asyncio
from typing import Optional

from flet.controls.adaptive_control import AdaptiveControl
from flet.controls.alignment import Alignment
from flet.controls.base_control import control
from flet.controls.constrained_control import ConstrainedControl
from flet.controls.control import Control
from flet.controls.control_event import OptionalEventHandler
from flet.controls.duration import OptionalDurationValue
from flet.controls.events import (
    ScaleEndEvent,
    ScaleStartEvent,
    ScaleUpdateEvent,
)
from flet.controls.margin import MarginValue
from flet.controls.types import ClipBehavior, Number

__all__ = ["InteractiveViewer"]


@control("InteractiveViewer")
class InteractiveViewer(ConstrainedControl, AdaptiveControl):
    """
    InteractiveViewer allows users to pan, zoom, and rotate content.

    Online docs: https://flet.dev/docs/controls/interactiveviewer
    """

    content: Control
    """
    The `Control` to be transformed by the `InteractiveViewer`.
    """

    pan_enabled: bool = True
    """
    Whether panning is enabled.

    Value is of type `bool` and defaults to `True`.
    """

    scale_enabled: bool = True
    """
    Whether scaling is enabled.

    Value is of type `bool` and defaults to `True`.
    """

    trackpad_scroll_causes_scale: bool = False
    """
    Whether scrolling up/down on a trackpad should cause scaling instead of panning.

    Value is of type `bool` and defaults to `False`.
    """

    constrained: bool = True
    """
    Whether the normal size constraints at this point in the widget tree are applied
    to the child.
    """

    max_scale: Number = 2.5
    """
    The maximum allowed scale. Must be greater than or equal to `min_scale`.

    Value is of type `float` and defaults to `2.5`.
    """

    min_scale: Number = 0.8
    """
    The minimum allowed scale. Must be greater than `0` and less than or equal to
    `max_scale`.

    Value is of type `float` and defaults to `0.8`.
    """

    interaction_end_friction_coefficient: Number = 0.0000135
    """
    Changes the deceleration behavior after a gesture. Must be greater than `0`.

    Value is of type `float` and defaults to `0.0000135`.
    """

    scale_factor: Number = 200
    """
    The amount of scale to be performed per pointer scroll.

    Value is of type `float` and defaults to `200.0`.
    """

    clip_behavior: ClipBehavior = ClipBehavior.HARD_EDGE
    """
    How to clip the `content`.

    Value is of type
    [`ClipBehavior`](https://flet.dev/docs/reference/types/clipbehavior) and defaults
    to `ClipBehavior.HARD_EDGE`.
    """

    alignment: Optional[Alignment] = None
    """
    Alignment of the `content` within.

    Value is of type
    [`Alignment`](https://flet.dev/docs/reference/types/alignment).
    """

    boundary_margin: MarginValue = 0
    """
    A margin for the visible boundaries of the `content`.

    Value is of type
    [`Margin`](https://flet.dev/docs/reference/types/margin).
    """

    interaction_update_interval: int = 200
    """
    The interval (in milliseconds) at which the `on_interaction_update` event is fired.

    Value is of type `int` and defaults to `200`.
    """

    on_interaction_start: OptionalEventHandler[ScaleStartEvent["InteractiveViewer"]] = (
        None
    )
    """
    Fires when the user begins a pan or scale gesture.

    Event handler argument is of type
    [`ScaleStartEvent`](https://flet.dev/docs/reference/types/scalestartevent).
    """

    on_interaction_update: OptionalEventHandler[
        ScaleUpdateEvent["InteractiveViewer"]
    ] = None
    """
    Fires when the user updates a pan or scale gesture.

    Event handler argument is of type
    [`ScaleUpdateEvent`](https://flet.dev/docs/reference/types/scaleupdateevent).
    """

    on_interaction_end: OptionalEventHandler[ScaleEndEvent["InteractiveViewer"]] = None
    """
    Fires when the user ends a pan or scale gesture.

    Event handler argument is of type
    [`ScaleEndEvent`](https://flet.dev/docs/reference/types/scaleendevent).
    """

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
