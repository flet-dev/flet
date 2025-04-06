from dataclasses import dataclass, field
from typing import Dict, Optional

from flet.controls.adaptive_control import AdaptiveControl
from flet.controls.constrained_control import ConstrainedControl
from flet.controls.control import Control, control
from flet.controls.control_event import ControlEvent
from flet.controls.duration import OptionalDurationValue
from flet.controls.material.snack_bar import DismissDirection
from flet.controls.types import (
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
    background: Optional[Control] = None
    secondary_background: Optional[Control] = None
    dismiss_direction: Optional[DismissDirection] = None
    dismiss_thresholds: Optional[Dict[DismissDirection, OptionalNumber]] = None
    movement_duration: OptionalDurationValue = None
    resize_duration: OptionalDurationValue = None
    cross_axis_end_offset: OptionalNumber = None
    on_update: OptionalEventCallable["DismissibleUpdateEvent"] = None
    on_dismiss: OptionalEventCallable["DismissibleDismissEvent"] = None
    on_confirm_dismiss: OptionalEventCallable["DismissibleDismissEvent"] = None
    on_resize: OptionalControlEventCallable = None

    def before_update(self):
        super().before_update()

    def confirm_dismiss(self, dismiss: bool):
        self.invoke_method("confirm_dismiss", {"dismiss": str(dismiss).lower()})


@dataclass
class DismissibleDismissEvent(ControlEvent):
    direction: Optional[DismissDirection] = None


@dataclass
class DismissibleUpdateEvent(ControlEvent):
    direction: DismissDirection = field(metadata={"data_field": "direction"})
    progress: float = field(metadata={"data_field": "progress"})
    reached: bool = field(metadata={"data_field": "reached"})
    previous_reached: bool = field(metadata={"data_field": "previous_reached"})
