from dataclasses import dataclass, field
from typing import Optional

from flet.controls.adaptive_control import AdaptiveControl
from flet.controls.base_control import control
from flet.controls.control import Control
from flet.controls.control_event import (
    ControlEventHandler,
    Event,
    EventHandler,
)
from flet.controls.duration import Duration, DurationValue
from flet.controls.layout_control import LayoutControl
from flet.controls.material.snack_bar import DismissDirection
from flet.controls.types import (
    Number,
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
class Dismissible(LayoutControl, AdaptiveControl):
    """
    A control that can be dismissed by dragging in the indicated
    [`dismiss_direction`][(c).].
    When dragged or flung in the specified [`dismiss_direction`][(c).],
    its [`content`][(c).] smoothly slides out of view.

    After completing the sliding animation, if a [`resize_duration`][(c).] is provided,
    this control further animates its height (or width, depending on what is
    perpendicular to the [`dismiss_direction`][(c).]), gradually reducing it to zero
    over the specified [`resize_duration`][(c).].
    """

    content: Control
    """
    The control that is being dismissed.

    Must be visible.

    Raises:
        ValueError: If the [`content`][(c).] is not visible.
    """

    background: Optional[Control] = None
    """
    A control that is stacked behind the [`content`][(c).].

    If [`secondary_background`][(c).] is also
    specified, then this control only appears when the content has been dragged
    down or to the right.
    """

    secondary_background: Optional[Control] = None
    """
    A control that is stacked behind the [`content`][(c).] and is
    exposed when it has been dragged up or to the left.

    Raises:
        ValueError: If it is provided and visible
            but the [`background`][(c).] is not provided and visible.
    """

    dismiss_direction: DismissDirection = DismissDirection.HORIZONTAL
    """
    The direction in which the control can be dismissed.
    """

    dismiss_thresholds: dict[DismissDirection, Optional[Number]] = field(
        default_factory=dict
    )
    """
    The offset threshold the item has to be dragged in order to be considered
    as dismissed. This is specified as a dictionary where the key is of
    type [`DismissDirection`][flet.] and the value is the threshold
    (a fractional/decimal value between `0.0` and `1.0`, inclusive).

    Example:
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
    The duration for [`content`][(c).] to dismiss or
    to come back to original position if not dismissed.
    """

    resize_duration: DurationValue = field(
        default_factory=lambda: Duration(milliseconds=300)
    )
    """
    The amount of time the control will spend contracting
    before [`on_dismiss`][(c).] is called.
    """

    cross_axis_end_offset: Number = 0.0
    """
    Specifies the end offset along the main axis once the
    [`content`][(c).] has been dismissed.

    If set to a non-zero value, then this dismissible moves in cross direction
    depending on whether it is positive or negative.
    """

    on_update: Optional[EventHandler[DismissibleUpdateEvent]] = None
    """
    Called when this control has been dragged.
    """

    on_dismiss: Optional[EventHandler[DismissibleDismissEvent]] = None
    """
    Called when this control has been dismissed, after finishing resizing.
    """

    on_confirm_dismiss: Optional[EventHandler[DismissibleDismissEvent]] = None
    """
    Gives the app an opportunity to confirm or veto a pending dismissal.
    This dismissible cannot be dragged again until this pending dismissal is resolved.

    To resolve the pending dismissal, call the
    [`confirm_dismiss()`][flet.Dismissible.confirm_dismiss] method
    passing it a boolean representing the decision. If `True`, then the control will be
    dismissed, otherwise it will be moved back to its original location.
    """

    on_resize: Optional[ControlEventHandler["Dismissible"]] = None
    """
    Called when this dismissible changes size, for example, when contracting before
    being dismissed.
    """

    def before_update(self):
        super().before_update()
        if not self.content.visible:
            raise ValueError("content must be visible")
        if (self.secondary_background and self.secondary_background.visible) and not (
            self.background and self.background.visible
        ):
            raise ValueError(
                "secondary_background can only be specified if background is also "
                "specified/visible"
            )

    async def confirm_dismiss(self, dismiss: bool):
        await self._invoke_method("confirm_dismiss", {"dismiss": dismiss})
