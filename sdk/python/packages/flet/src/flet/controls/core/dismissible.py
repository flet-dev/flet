import asyncio
from dataclasses import dataclass, field

from flet.controls.adaptive_control import AdaptiveControl
from flet.controls.base_control import control
from flet.controls.colors import Colors
from flet.controls.constrained_control import ConstrainedControl
from flet.controls.control import Control
from flet.controls.control_event import (
    Event,
    OptionalControlEventHandler,
    OptionalEventHandler,
)
from flet.controls.duration import Duration, DurationValue
from flet.controls.material.container import Container
from flet.controls.material.snack_bar import DismissDirection
from flet.controls.types import (
    Number,
    OptionalNumber,
)

__all__ = ["Dismissible", "DismissibleDismissEvent", "DismissibleUpdateEvent"]


@dataclass
class DismissibleDismissEvent(Event["Dismissible"]):
    direction: DismissDirection


@dataclass
class DismissibleUpdateEvent(Event["Dismissible"]):
    direction: DismissDirection
    progress: float
    reached: bool
    previous_reached: bool


@control("Dismissible")
class Dismissible(ConstrainedControl, AdaptiveControl):
    """
    A control that can be dismissed by dragging in the indicated `dismiss_direction`.
    When dragged or flung in the specified `dismiss_direction`, its content smoothly
    slides out of view.

    After completing the sliding animation, if a `resize_duration` is provided, this
    control further animates its height (or width, depending on what is perpendicular
    to the `dismiss_direction`), gradually reducing it to zero over the specified
    `resize_duration`.

    Online Docs: https://flet.dev/docs/controls/dismissible
    """

    content: Control
    """
    A child Control contained by the Dismissible.
    """

    background: Control = Container(bgcolor=Colors.TRANSPARENT)
    """
    A Control that is stacked behind the `content`.

    If `secondary_background` is also specified, then this control only appears when
    the content has been dragged down or to the right.
    """

    secondary_background: Control = Container(bgcolor=Colors.TRANSPARENT)
    """
    A control that is stacked behind the `content` and is exposed when the `content`
    has been dragged up or to the left.

    Has no effect if `background` is not specified.
    """

    dismiss_direction: DismissDirection = DismissDirection.HORIZONTAL
    """
    The direction in which the control can be dismissed.

    Value is of type
    [`DismissDirection`](https://flet.dev/docs/reference/types/dismissdirection).
    """

    dismiss_thresholds: dict[DismissDirection, OptionalNumber] = field(
        default_factory=dict
    )

    """
    The offset threshold the item has to be dragged in order to be considered dismissed.

    Ex: a threshold of `0.4` (the default) means that the item has to be dragged
    _at least_ 40% in order for it to be dismissed.

    It is specified as a dictionary where the key is of type
    [`DismissDirection`](https://flet.dev/docs/reference/types/dismissdirection) and
    the value is the threshold (fractional/decimal value between `0.0` and `1.0`):
    
    ```python
    ft.Dismissible(
        # ...
        dismiss_thresholds={
            ft.DismissDirection.VERTICAL: 0.1,
            ft.DismissDirection.START_TO_END: 0.7
        }
    )
    ```
    """

    movement_duration: DurationValue = field(
        default_factory=lambda: Duration(milliseconds=200)
    )
    """
    The duration for card to dismiss or to come back to original position if not 
    dismissed.
    """

    resize_duration: DurationValue = field(
        default_factory=lambda: Duration(milliseconds=300)
    )
    """
    The amount of time the control will spend contracting before `on_dismiss` is called.
    """

    cross_axis_end_offset: Number = 0.0
    """
    Specifies the end offset along the main axis once the card has been dismissed.

    If non-zero value is given then widget moves in cross direction depending on whether
    it is positive or negative.
    """

    on_update: OptionalEventHandler[DismissibleUpdateEvent] = None
    """
    Fires when this control has been dragged.
    """

    on_dismiss: OptionalEventHandler[DismissibleDismissEvent] = None
    """
    Fires when this control has been dismissed, after finishing resizing.
    """

    on_confirm_dismiss: OptionalEventHandler[DismissibleDismissEvent] = None
    """
    Gives the app an opportunity to confirm or veto a pending dismissal. The widget
    cannot be dragged again until the returned this pending dismissal is resolved.

    To resolve the pending dismissal, call the `confirm_dismiss(dismiss)` method
    passing it a boolean representing the decision. If `True`, then the control will be
    dismissed, otherwise it will be moved back to its original location.

    See the example at the top of this page for a possible implementation.
    """

    on_resize: OptionalControlEventHandler["Dismissible"] = None
    """
    Fires when this control changes size, for example, when contracting before
    being dismissed.
    """

    def before_update(self):
        super().before_update()
        assert self.content.visible, "content must be visible"

    async def confirm_dismiss_async(self, dismiss: bool):
        await self._invoke_method_async("confirm_dismiss", {"dismiss": dismiss})

    def confirm_dismiss(self, dismiss: bool):
        asyncio.create_task(self.confirm_dismiss_async(dismiss))
