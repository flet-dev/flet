from enum import Enum
from typing import Annotated, Any, Optional

from flet.controls.base_control import control
from flet.controls.control import Control
from flet.controls.control_event import ControlEvent, ControlEventHandler
from flet.controls.layout_control import LayoutControl
from flet.controls.types import ColorValue, Number
from flet.utils.validation import V

__all__ = [
    "RefreshIndicator",
    "RefreshIndicatorTriggerMode",
]


class RefreshIndicatorTriggerMode(Enum):
    """Where a pull gesture can start a :class:`~flet.RefreshIndicator`."""

    ON_EDGE = "onEdge"
    """
    Only when the scrollable content is already at its top edge, as the drag starts.
    """

    ANYWHERE = "anywhere"
    """
    From anywhere in the scrollable content: a drag that starts scrolled down
    scrolls up to the top edge first, then pulls the indicator.
    """


@control("RefreshIndicator")
class RefreshIndicator(LayoutControl):
    """
    Shows a Material pull-to-refresh indicator above scrollable content.

    Pulling the :attr:`content` down from its top edge, far enough, calls
    :attr:`on_refresh` and shows a spinning progress indicator until that
    handler returns. Call :meth:`show` to refresh without a gesture.

    Note:
        The pull is a touch gesture: on desktop and web, mouse drags and the
        mouse wheel don't start it. Offer another way to refresh there, such as
        a button that calls :meth:`show`.
    """

    content: Annotated[
        Control,
        V.visible_control(),
    ]
    """
    The scrollable content, such as a :class:`~flet.ListView`, a
    :class:`~flet.GridView`, or a :class:`~flet.Column` with
    :attr:`~flet.Column.scroll` set.

    The pull gesture is made on this content, so it must be scrollable, but it
    can be pulled even when it is too short to scroll, such as an empty list.

    Raises:
        ValueError: If it is not visible.
    """

    color: Optional[ColorValue] = None
    """
    The color of the progress indicator.

    Defaults to :attr:`flet.ColorScheme.primary`.
    """

    bgcolor: Optional[ColorValue] = None
    """
    The color of the circle behind the progress indicator.

    Defaults to :attr:`flet.ProgressIndicatorTheme.refresh_bgcolor`, or else to
    :attr:`flet.Theme.canvas_color`.
    """

    displacement: Number = 40.0
    """
    How far below the top of the :attr:`content` the indicator rests while
    refreshing.
    """

    edge_offset: Number = 0.0
    """
    How far below the top of the :attr:`content` the indicator starts appearing,
    for example to start below a header that overlaps the content.
    """

    stroke_width: Number = 2.0
    """
    The width of the progress indicator's line.
    """

    elevation: Annotated[
        Number,
        V.ge(0),
    ] = 2.0
    """
    The elevation of the circle behind the progress indicator, which casts its
    shadow.

    Raises:
        ValueError: If it is not greater than or equal to `0`.
    """

    trigger_mode: RefreshIndicatorTriggerMode = RefreshIndicatorTriggerMode.ON_EDGE
    """
    Where a pull gesture can start a refresh.
    """

    handle_nested_scrolls: bool = False
    """
    Whether to react to the scrolling of scrollable controls nested in other
    scrollable controls in the :attr:`content`, rather than only to the
    outermost scrollable one.

    Turn it on when the scrolling that should pull the indicator happens in a
    nested scrollable, such as a :class:`~flet.ListView` inside a
    :class:`~flet.Column` with :attr:`~flet.Column.scroll` set.
    """

    semantics_label: Optional[str] = None
    """
    The label screen readers announce for the progress indicator.

    Defaults to the localized "Refresh" label of the app's locale.
    """

    semantics_value: Optional[str] = None
    """
    The progress value screen readers announce for the progress indicator.
    """

    on_refresh: Optional[ControlEventHandler["RefreshIndicator"]] = None
    """
    Called when the user pulls the indicator far enough, or :meth:`show` is
    called.

    The progress indicator spins until this handler returns, so make it an
    `async` handler that awaits the refresh work.
    """

    async def show(self, at_top: bool = True):
        """
        Shows the indicator and calls :attr:`on_refresh`, as a pull would.

        Args:
            at_top: Whether to show the indicator at the top of the
                :attr:`content`, rather than at its bottom.
        """
        await self._invoke_method("show", {"at_top": at_top})

    async def _trigger_event(
        self, event_name: str, event_data: Any, e: Optional[ControlEvent] = None
    ):
        """
        Dispatches events, and hides the progress indicator once
        :attr:`on_refresh` returns or raises.

        :attr:`on_refresh` may re-render the component, which replaces this control with
        a new instance that takes over its id. So the progress indicator is hidden
        through whichever instance has the id when the handler finishes. If none
        has it, the control was removed during the refresh, and removing it
        already hid the progress indicator.
        """
        session = self.page.session if event_name == "refresh" else None
        try:
            await super()._trigger_event(event_name, event_data, e)
        finally:
            if session is not None:
                current = session.index.get(self._i)
                if isinstance(current, RefreshIndicator):
                    await current._invoke_method("finish_refresh")
