from dataclasses import field
from typing import Optional

from flet.controls.animation import AnimationCurve
from flet.controls.base_control import control
from flet.controls.control import Control
from flet.controls.control_event import ControlEventHandler
from flet.controls.duration import DurationValue
from flet.controls.layout_control import LayoutControl
from flet.controls.types import ClipBehavior, Number

__all__ = ["PageView"]


@control("PageView")
class PageView(LayoutControl):
    """
    Displays its child [`controls`][(c).] one page at a time and lets users swipe
    between them, similar to a carousel.

    It is helpful for onboarding flows, photo carousels,
    or any scenario where content is divided into discrete full-width pages.
    """

    controls: list[Control] = field(default_factory=list)
    """
    A list of controls to display, one per page, in the order they should appear.
    """

    initial_page: int = 0
    """
    The zero-based page index that will be shown first.

    Raises:
        ValueError: If it is negative.
    """

    current_page: Optional[int] = None
    """
    The zero-based index of the currently visible page.

    This value is automatically kept in sync with user interaction.
    Setting it manually (followed by [`update()`][flet.Control.update])
    jumps to the specified page without animation.

    Raises:
        ValueError: If it is negative.
    """

    keep_page: bool = True
    """
    Whether the `PageView` should restore the most recently viewed page when rebuilt.
    """

    horizontal: bool = True
    """
    When `True` (default), pages scroll horizontally. If `False`, pages scroll vertically.
    """

    reverse: bool = False
    """
    Whether to reverse the order in which pages are read and swiped.
    """

    viewport_fraction: Number = 1.0
    """
    Fraction of the viewport that each page should occupy.

    For example, `1.0` (default) means every page is as wide/tall as the viewport.

    Raises:
        ValueError: If it is not greater than `0`.
    """

    page_snapping: bool = True
    """
    Whether the view should snap to exact page boundaries after a drag.
    """

    implicit_scrolling: bool = False
    """
    Whether to allow adjacent pages to render partially before the user scrolls to them.
    """

    pad_ends: bool = True
    """
    Adds padding before the first page and after the last page
    so they snap to the center of the viewport.
    """

    clip_behavior: ClipBehavior = ClipBehavior.HARD_EDGE
    """
    How pages are clipped if they overflow their bounds.
    """

    animation_duration: Optional[DurationValue] = None
    """
    The default duration to use for animations.
    """

    animation_curve: Optional[AnimationCurve] = None
    """
    The default easing curve to use for animations.
    """

    on_change: Optional[ControlEventHandler["PageView"]] = None
    """
    Fired when the visible page changes.

    The [`data`][flet.Event.] attribute contains the new page index.
    """

    def before_update(self):
        super().before_update()
        if self.initial_page < 0:
            raise ValueError(
                f"initial_page must be greater than or equal to 0, got {self.initial_page}"
            )
        if self.current_page is not None and self.current_page < 0:
            raise ValueError(
                f"current_page must be greater than or equal to 0, got {self.current_page}"
            )
        if self.viewport_fraction <= 0:
            raise ValueError(
                f"viewport_fraction must be greater than 0, got {self.viewport_fraction}"
            )

    async def go_to_page(
        self,
        index: int,
        animation_duration: Optional[DurationValue] = None,
        animation_curve: Optional[AnimationCurve] = None,
    ):
        """
        Animates to the page at `index`.

        Args:
            index: The zero-based page to show.
            animation_duration: Length of the animation.
                If `None`, defaults to [`animation_duration`][(c).].
            animation_curve: The easing curve of the animation.
                If `None`, defaults to [`animation_curve`][(c).].

        Raises:
            ValueError: If `index` is negative.
        """
        if index < 0:
            raise ValueError(f"index must be greater than or equal to 0, got {index}")

        await self._invoke_method(
            "go_to_page",
            {
                "index": index,
                "duration": animation_duration
                if animation_duration is None
                else self.animation_duration,
                "curve": animation_curve
                if animation_curve is not None
                else self.animation_curve,
            },
        )

    async def jump_to_page(self, index: int):
        """
        Jumps immediately to the page at `index` without animation.

        Raises:
            ValueError: If `index` is negative.
        """
        if index < 0:
            raise ValueError(f"index must be greater than or equal to 0, got {index}")

        await self._invoke_method("jump_to_page", {"index": index})

    async def jump_to(self, value: Number):
        """
        Jumps the scroll position from its current value to the given value,
        without animation, and without checking if the new value is in range.

        Any active animation is canceled. If the user is currently scrolling, that
        action is canceled.

        If this method changes the scroll position, a sequence of start/update/end
        scroll notifications will be dispatched. No overscroll notifications can
        be generated by this method.

        Immediately after the jump, a ballistic activity is started, in case the
        value was out of range.

        Args:
            value: The new scroll position.
        """
        await self._invoke_method("jump_to", {"value": value})

    async def next_page(
        self,
        animation_duration: Optional[DurationValue] = None,
        animation_curve: Optional[AnimationCurve] = None,
    ):
        """
        Animates forward by one page.

        Args:
            animation_duration: Length of the animation.
                If `None`, defaults to [`animation_duration`][(c).].
            animation_curve: The easing curve of the animation.
                If `None`, defaults to [`animation_curve`][(c).].
        """
        await self._invoke_method(
            "next_page",
            {
                "duration": animation_duration
                if animation_duration is None
                else self.animation_duration,
                "curve": animation_curve
                if animation_curve is not None
                else self.animation_curve,
            },
        )

    async def previous_page(
        self,
        animation_duration: Optional[DurationValue] = None,
        animation_curve: Optional[AnimationCurve] = None,
    ):
        """
        Animates backward by one page.

        Args:
            animation_duration: Length of the animation.
                If `None`, defaults to [`animation_duration`][(c).].
            animation_curve: The easing curve of the animation.
                If `None`, defaults to [`animation_curve`][(c).].
        """
        await self._invoke_method(
            "previous_page",
            {
                "duration": animation_duration
                if animation_duration is None
                else self.animation_duration,
                "curve": animation_curve
                if animation_curve is not None
                else self.animation_curve,
            },
        )
