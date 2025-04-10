import asyncio
from dataclasses import dataclass, field
from typing import Dict

from flet.controls.adaptive_control import AdaptiveControl
from flet.controls.colors import Colors
from flet.controls.constrained_control import ConstrainedControl
from flet.controls.control import Control, control
from flet.controls.control_event import ControlEvent
from flet.controls.duration import Duration, DurationValue
from flet.controls.material.container import Container
from flet.controls.material.snack_bar import DismissDirection
from flet.controls.types import (
    Number,
    OptionalControlEventCallable,
    OptionalEventCallable,
    OptionalNumber,
)

__all__ = ["Dismissible", "DismissibleDismissEvent", "DismissibleUpdateEvent"]


@control("Dismissible")
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

    content: Control
    background: Control = Container(bgcolor=Colors.TRANSPARENT)
    secondary_background: Control = Container(bgcolor=Colors.TRANSPARENT)
    dismiss_direction: DismissDirection = DismissDirection.HORIZONTAL
    dismiss_thresholds: Dict[DismissDirection, OptionalNumber] = field(
        default_factory=dict
    )
    movement_duration: DurationValue = field(
        default_factory=lambda: Duration(milliseconds=200)
    )
    resize_duration: DurationValue = field(
        default_factory=lambda: Duration(milliseconds=300)
    )
    cross_axis_end_offset: Number = 0.0
    on_update: OptionalEventCallable["DismissibleUpdateEvent"] = None
    on_dismiss: OptionalEventCallable["DismissibleDismissEvent"] = None
    on_confirm_dismiss: OptionalEventCallable["DismissibleDismissEvent"] = None
    on_resize: OptionalControlEventCallable = None

    def before_update(self):
        super().before_update()
        assert self.content.visible, "content must be visible"

    async def confirm_dismiss_async(self, dismiss: bool):
        await self._invoke_method_async("confirm_dismiss", {"dismiss": dismiss})

    def confirm_dismiss(self, dismiss: bool):
        asyncio.create_task(self.confirm_dismiss_async(dismiss))


@dataclass
class DismissibleDismissEvent(ControlEvent):
    direction: DismissDirection


@dataclass
class DismissibleUpdateEvent(ControlEvent):
    direction: DismissDirection
    progress: float
    reached: bool
    previous_reached: bool
