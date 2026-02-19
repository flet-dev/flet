from dataclasses import field
from typing import Optional

from flet.controls.animation import AnimationCurve
from flet.controls.base_control import control
from flet.controls.control import Control
from flet.controls.control_event import ControlEventHandler
from flet.controls.duration import Duration, DurationValue
from flet.controls.layout_control import LayoutControl
from flet.controls.types import ClipBehavior, Number

__all__ = ["PageView"]


DEFAULT_ANIMATION_DURATION = Duration(seconds=1)
DEFAULT_ANIMATION_CURVE = AnimationCurve.LINEAR


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

    selected_index: int = 0
    """
    The zero-based index of the currently visible page.

    Changing it later on (followed by [`update()`][flet.BaseControl.update])
    jumps to the specified page without animation.

    Raises:
        ValueError: If it is negative.
    """

    keep_page: bool = True
    """
    Whether this page view should restore the most recently viewed page when rebuilt.
    """

    horizontal: bool = True
    """
    Whether the pages should be arranged and scrolled horizontally.

    `False` implies vertical arrangement and scrolling.
    """

    reverse: bool = False
    """
    Whether to reverse the order in which pages are read and swiped.

    For example, if the reading direction is left-to-right and
    [`horizontal`][(c).] is `True`, then this page view scrolls from
    left to right when `reverse` is `False` and from right to left when
    `reverse` is `True`.

    Similarly, if [`horizontal`][(c).] is `False`, then this page view
    scrolls from top to bottom when `reverse` is `False` and from bottom to top
    when `reverse` is `True`.
    """

    viewport_fraction: Number = 1.0
    """
    The fraction of the viewport that each page should occupy in the
    scrolling direction (see [`horizontal`][(c).]).

    For example, `1.0` (default), means each page fills the viewport.

    Raises:
        ValueError: If it is less than or equal to `0.0`.
    """

    snap: bool = True
    """
    Whether the view should snap to exact page boundaries after a drag.

    If the [`pad_ends`][(c).] is `False` and [`viewport_fraction`][(c).] < `1.0`,
    the page will snap to the beginning of the viewport; otherwise, the page
    will snap to the center of the viewport.
    """

    implicit_scrolling: bool = False
    """
    Whether to allow adjacent pages to render partially before the user scrolls to them,
    enabling smoother transitions and improved accessibility by allowing focus to move
    seamlessly between pages during navigation.

    With this flag set to `False`, when accessibility focus reaches the end of
    the current page and the user attempts to move it to the next element, the
    focus will traverse to the next widget outside of the page view.

    With this flag set to `True`, when accessibility focus reaches the end of
    the current page and user attempts to move it to the next element, focus
    will traverse to the next page in the page view.
    """

    pad_ends: bool = True
    """
    Whether to add padding to both ends of the list.

    If this is set to `True` and [`viewport_fraction`][(c).] < `1.0`,
    padding will be added before the first page and after the last page so they snap
    to the center of the viewport when scrolled all the way to the start or end.

    Note:
        If [`viewport_fraction`][(c).] >= 1.0, this property has no effect.
    """

    clip_behavior: ClipBehavior = ClipBehavior.HARD_EDGE
    """
    Defines how pages are clipped if they overflow their bounds.
    """

    on_change: Optional[ControlEventHandler["PageView"]] = None
    """
    Fired when the visible page changes.

    The [`data`][flet.Event.] property of the event argument contains
    the index of the new page.
    """

    def before_update(self):
        super().before_update()
        if self.selected_index < 0:
            raise ValueError(
                f"selected_index must be greater than or equal to 0, "
                f"got {self.selected_index}"
            )
        if self.viewport_fraction <= 0:
            raise ValueError(
                f"viewport_fraction must be greater than 0, "
                f"got {self.viewport_fraction}"
            )

    async def go_to_page(
        self,
        index: int,
        animation_duration: DurationValue = DEFAULT_ANIMATION_DURATION,
        animation_curve: AnimationCurve = DEFAULT_ANIMATION_CURVE,
    ):
        """
        Animates to the page at `index`.

        Args:
            index: The index of the page to show.
            animation_duration: Length of the animation.
            animation_curve: The easing curve of the animation.

        Raises:
            ValueError: If `index` is negative.
        """
        if index < 0:
            raise ValueError(f"index must be greater than or equal to 0, got {index}")

        await self._invoke_method(
            "go_to_page",
            {"index": index, "duration": animation_duration, "curve": animation_curve},
        )

    async def jump_to_page(self, index: int):
        """
        Jumps immediately to the page at `index` without animation, moving the page
        position from its current value to the given value without animation nor
        range checking.

        Args:
            index: The index of the page to show.

        Raises:
            ValueError: If `index` is negative.
        """
        if index < 0:
            raise ValueError(f"index must be greater than or equal to 0, got {index}")

        await self._invoke_method("jump_to_page", {"index": index})

    async def jump_to(self, value: Number):
        """
        Immediately sets the scroll position to the given value, without animation
        and without validating whether the value is within bounds.

        Any active scrolling or animation is canceled.

        If the scroll position changes, a start/update/end sequence of scroll
        notifications is dispatched. This method does not generate overscroll
        notifications.

        After the jump, a ballistic activity is initiated if the value is outside
        the valid scroll range.

        Args:
            value: The new scroll position.
        """
        await self._invoke_method("jump_to", {"value": value})

    async def next_page(
        self,
        animation_duration: DurationValue = DEFAULT_ANIMATION_DURATION,
        animation_curve: AnimationCurve = DEFAULT_ANIMATION_CURVE,
    ):
        """
        Animates to the next page. Same as calling
        [`go_to_page()`][flet.PageView.go_to_page] with `selected_index + 1`.

        Args:
            animation_duration: Length of the animation.
            animation_curve: The easing curve of the animation.
        """
        await self._invoke_method(
            "next_page",
            {"duration": animation_duration, "curve": animation_curve},
        )

    async def previous_page(
        self,
        animation_duration: DurationValue = DEFAULT_ANIMATION_DURATION,
        animation_curve: AnimationCurve = DEFAULT_ANIMATION_CURVE,
    ):
        """
        Animates to the previous page. Same as calling
        [`go_to_page()`][flet.PageView.go_to_page] with `selected_index - 1`.

        Args:
            animation_duration: Length of the animation.
            animation_curve: The easing curve of the animation.
        """
        await self._invoke_method(
            "previous_page",
            {"duration": animation_duration, "curve": animation_curve},
        )
