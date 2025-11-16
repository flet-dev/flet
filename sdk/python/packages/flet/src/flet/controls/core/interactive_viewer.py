from dataclasses import field
from typing import Optional

from flet.controls.alignment import Alignment
from flet.controls.base_control import control
from flet.controls.control import Control
from flet.controls.control_event import EventHandler
from flet.controls.duration import DurationValue
from flet.controls.events import (
    ScaleEndEvent,
    ScaleStartEvent,
    ScaleUpdateEvent,
)
from flet.controls.layout_control import LayoutControl
from flet.controls.margin import Margin, MarginValue
from flet.controls.types import ClipBehavior, Number

__all__ = ["InteractiveViewer"]


@control("InteractiveViewer")
class InteractiveViewer(LayoutControl):
    """
    Allows you to pan, zoom, and rotate its [`content`][(c).].
    """

    content: Control
    """
    The `Control` to be transformed.

    Must be visible.

    Raises:
        ValueError: If [`content`][(c).] is not visible.
    """

    pan_enabled: bool = True
    """
    Whether panning is enabled.
    """

    scale_enabled: bool = True
    """
    Whether scaling is enabled.
    """

    trackpad_scroll_causes_scale: bool = False
    """
    Whether scrolling up/down on a trackpad should cause scaling instead of panning.
    """

    constrained: bool = True
    """
    Whether the normal size constraints at this point in the control tree are applied
    to the [`content`][(c).].

    If set to `False`, then the content will be given infinite constraints. This
    is often useful when a content should be bigger than this `InteractiveViewer`.

    For example, for a content which is bigger than the viewport but can be
    panned to reveal parts that were initially offscreen, `constrained` must
    be set to `False` to allow it to size itself properly. If `constrained` is
    `True` and the content can only size itself to the viewport, then areas
    initially outside of the viewport will not be able to receive user
    interaction events. If experiencing regions of the content that are not
    receptive to user gestures, make sure `constrained` is `False` and the content
    is sized properly.
    """

    max_scale: Number = 2.5
    """
    The maximum allowed scale.

    Raises:
        ValueError: If it is not greater than `0` or is less than
            [`min_scale`][(c).].
    """

    min_scale: Number = 0.8
    """
    The minimum allowed scale.

    The effective scale is limited by the value of [`boundary_margin`][(c).].
    If scaling would cause the content to be displayed outside the defined boundary,
    it is prevented. By default, `boundary_margin` is set to `Margin.all(0)`,
    so scaling below `1.0` is typically not possible unless you increase the
    `boundary_margin` value.

    Raises:
        ValueError: If it is not greater than `0` or less than [`max_scale`][(c).].
    """

    interaction_end_friction_coefficient: Number = 0.0000135
    """
    Changes the deceleration behavior after a gesture.

    Raises:
        ValueError: If it is less than or equal to `0`.
    """

    scale_factor: Number = 200
    """
    The amount of scale to be performed per pointer scroll.

    Increasing this value above the default causes scaling to feel slower,
    while decreasing it causes scaling to feel faster.

    Note:
        Has effect only on pointer device scrolling, not pinch to zoom.
    """

    clip_behavior: ClipBehavior = ClipBehavior.HARD_EDGE
    """
    Defines how to clip the [`content`][(c).].

    If set to [`ClipBehavior.NONE`][flet.], the [`content`][(c).] can visually overflow
    the bounds of this `InteractiveViewer`, but gesture events (such as pan or zoom)
    will only be recognized within the viewer's area. Ensure this `InteractiveViewer`
    is sized appropriately when using [`ClipBehavior.NONE`][flet.].
    """

    alignment: Optional[Alignment] = None
    """
    The alignment of the [`content`][(c).] within this viewer.
    """

    boundary_margin: MarginValue = field(default_factory=lambda: Margin.all(0))
    """
    A margin for the visible boundaries of the [`content`][(c).].

    Any transformation that results in the viewport being able to view outside
    of the boundaries will be stopped at the boundary. The boundaries do not
    rotate with the rest of the scene, so they are always aligned with the
    viewport.

    To produce no boundaries at all, pass an infinite value.

    Defaults to `Margin.all(0)`, which results in boundaries that are the
    exact same size and position as the [`content`][(c).].
    """

    interaction_update_interval: int = 200
    """
    The interval (in milliseconds) at which the
    [`on_interaction_update`][(c).] event is fired.
    """

    on_interaction_start: Optional[
        EventHandler[ScaleStartEvent["InteractiveViewer"]]
    ] = None
    """
    Called when the user begins a pan or scale gesture.
    """

    on_interaction_update: Optional[
        EventHandler[ScaleUpdateEvent["InteractiveViewer"]]
    ] = None
    """
    Called when the user updates a pan or scale gesture.
    """

    on_interaction_end: Optional[EventHandler[ScaleEndEvent["InteractiveViewer"]]] = (
        None
    )
    """
    Called when the user ends a pan or scale gesture.
    """

    def before_update(self):
        super().before_update()
        if not self.content.visible:
            raise ValueError("content must be visible")
        if self.min_scale <= 0:
            raise ValueError(f"min_scale must be greater than 0, got {self.min_scale}")
        if self.max_scale <= 0:
            raise ValueError(f"max_scale must be greater than 0, got {self.max_scale}")
        if self.max_scale < self.min_scale:
            raise ValueError(
                "max_scale must be greater than or equal to min_scale, "
                f"got max_scale={self.max_scale}, min_scale={self.min_scale}"
            )
        if self.interaction_end_friction_coefficient <= 0:
            raise ValueError(
                "interaction_end_friction_coefficient must be greater than 0, "
                f"got {self.interaction_end_friction_coefficient}"
            )

    async def reset(self, animation_duration: Optional[DurationValue] = None):
        await self._invoke_method(
            "reset", arguments={"animation_duration": animation_duration}
        )

    async def save_state(self):
        await self._invoke_method("save_state")

    async def restore_state(self):
        await self._invoke_method("restore_state")

    async def zoom(self, factor: Number):
        await self._invoke_method("zoom", arguments={"factor": factor})

    async def pan(self, dx: Number, dy: Number = 0, dz: Number = 0):
        await self._invoke_method("pan", arguments={"dx": dx, "dy": dy, "dz": dz})
