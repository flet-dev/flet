from typing import Any, Optional

from flet.controls.control import Control
from flet.controls.control_event import ControlEvent, ControlEventHandler, EventHandler
from flet.controls.layout_control import LayoutControl
from flet.controls.types import ColorValue, Number, RefreshIndicatorTriggerMode

import flet as ft

__all__ = ["RefreshIndicator"]


@ft.control("RefreshIndicator")
class RefreshIndicator(LayoutControl):
    """
    A Material-style pull-to-refresh widget.

    Wraps a single scrollable child (e.g. :class:`~flet.ListView`,
    :class:`~flet.GridView`, or a :class:`~flet.Column` with
    :attr:`~flet.Column.scroll` enabled) and invokes
    :attr:`on_refresh` when the user pulls the indicator far enough.

    Example:
        ```python
        import asyncio
        import flet as ft

        async def handle_refresh(e: ft.ControlEvent):
            await asyncio.sleep(2)  # simulate work

        page.add(
            ft.RefreshIndicator(
                content=ft.ListView(controls=[...]),
                on_refresh=handle_refresh,
            )
        )
    """

    content: Control
    """
    The scrollable child wrapped by this indicator.

    The child **must** be scrollable (e.g. :class:`~flet.ListView`), or it
    must be wrapped in a control with ``AlwaysScrollableScrollPhysics``,
    otherwise the pull gesture will never reach the indicator.

    Note:
        Only a single control is supported. If you need multiple children,
        wrap them in a :class:`~flet.Column` (with
        :attr:`~flet.Column.scroll` enabled) or a :class:`~flet.ListView`.
    """

    color: Optional[ColorValue] = None
    """The progress-indicator foreground colour."""

    background_color: Optional[ColorValue] = None
    """The background colour of the indicator circle."""

    displacement: Number = 40.0
    """Distance from the top of the child at which the indicator settles."""

    edge_offset: Number = 0.0
    """Distance from the *bottom* edge when the child is scrolled to the end."""

    stroke_width: Number = 2.0
    """Width of the progress-indicator stroke."""

    trigger_mode: RefreshIndicatorTriggerMode = RefreshIndicatorTriggerMode.ON_EDGE
    """
    Whether a refresh can be triggered when the child is at the edge
    (`ON_EDGE`) or anywhere (`ANYWHERE`).
    """

    elevation: Number = 2.0
    """Shadow elevation of the indicator circle."""

    semantics_label: Optional[str] = None
    """Accessibility label for the refresh indicator."""

    semantics_value: Optional[str] = None
    """
    The :attr:`~flet.Semantics.value` for this progress indicator.

    Used by screen readers to announce the current progress value.
    """

    handle_nested_scrolls: bool = False
    """
    Flet-friendly replacement for a custom ``notification_predicate``.

    When ``True``, the indicator responds to scroll notifications from **all**
    nested scrollables (equivalent to a predicate that always returns
    ``True``).

    When ``False`` (default), the indicator only responds to the **first**
    scrollable descendant — matching Flutter's
    ``defaultScrollNotificationPredicate``.
    """

    on_refresh: Optional[ControlEventHandler["RefreshIndicator"]] = None
    """
    Fired when the user pulls the indicator far enough to trigger a refresh.
    when the async work is finished so the spinner disappears.
    """

    on_status_change: Optional[EventHandler[ControlEvent]] = None
    """
    Fired whenever the indicator's status changes.

    The ``e.data`` value is one of:

    * ``"drag"`` — the user is dragging the indicator down.
    * ``"armed"`` — the drag passed the trigger threshold.
    * ``"snap"`` — the indicator is animating into place.
    * ``"refresh"`` — the refresh handler is running.
    * ``"done"`` — the refresh handler finished successfully.
    * ``"canceled"`` — the drag was released before the threshold.

    See also:

    * Flutter's `RefreshIndicatorStatus
      <https://api.flutter.dev/flutter/material/RefreshIndicatorStatus.html>`_.
    """

    async def _trigger_event(
        self,
        event_name: str,
        event_data: Any,
        e: Optional[ControlEvent] = None,
    ) -> None:
        """
        Override dispatch so that after the ``on_refresh`` handler runs
        (or is skipped, or raises), the Dart side is always told to release
        its pending ``Completer`` and hide the spinner.
        """
        try:
            await super()._trigger_event(event_name, event_data, e)
        finally:
            if event_name == "refresh":
                try:
                    await self._invoke_method("finish_refresh")
                except Exception:
                    # Widget disposed mid-refresh or session gone —
                    # nothing to recover, just don't leak the exception.
                    pass

    async def trigger_refresh(self) -> None:
        """
        Programmatically fire a refresh (e.g. from a button).

        Runs the same dispatch path as a user pull, so the Dart spinner
        will appear and hide automatically.
        """
        await self._trigger_event("refresh", None)
