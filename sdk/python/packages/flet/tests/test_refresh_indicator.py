import asyncio
from contextlib import nullcontext
from unittest.mock import AsyncMock, patch

import msgpack
import pytest

import flet as ft
from flet.controls.context import _context_page
from flet.messaging.connection import Connection
from flet.messaging.protocol import configure_encode_object_for_msgpack
from flet.messaging.session import Session
from flet.pubsub.pubsub_hub import PubSubHub


class _SerializingConnection(Connection):
    """A connection that serializes messages as a real one does, then drops them."""

    def send_message(self, message):
        """Serializes `message` without sending it. Serializing records the snapshots
        the session uses to unmount removed controls."""
        msgpack.packb(
            message, default=configure_encode_object_for_msgpack(ft.BaseControl)
        )


@pytest.fixture
def session():
    """A session with its initial page patch already serialized."""
    connection = _SerializingConnection()
    connection.pubsubhub = PubSubHub()
    session = Session(connection)
    msgpack.packb(
        session.get_page_patch(),
        default=configure_encode_object_for_msgpack(ft.BaseControl),
    )
    return session


@pytest.mark.asyncio
@pytest.mark.parametrize("raises", [False, True])
async def test_refresh_finishes_while_mounted(session, raises):
    """A mounted indicator is told to finish its refresh, even when `on_refresh`
    raises."""

    async def refresh(e):
        """Finishes at once, or raises when the test asks it to."""
        if raises:
            raise ValueError("Refresh failed")

    indicator = ft.RefreshIndicator(content=ft.ListView(), on_refresh=refresh)
    session.page.add(indicator)

    with patch.object(session, "invoke_method", new_callable=AsyncMock) as invoke:
        with (
            pytest.raises(ValueError, match="Refresh failed")
            if raises
            else nullcontext()
        ):
            await indicator._trigger_event("refresh", None)

        invoke.assert_awaited_once_with(indicator._i, "finish_refresh", None, None)


@pytest.mark.asyncio
@pytest.mark.parametrize("nested", [False, True])
@pytest.mark.parametrize("remove_in_handler", [False, True])
@pytest.mark.parametrize("raises", [False, True])
async def test_refresh_skips_cleanup_after_removal(
    session, nested, remove_in_handler, raises
):
    """An indicator removed during `on_refresh`, by the handler or by other code,
    isn't told to finish: removing it already hid the progress indicator."""
    started = asyncio.Event()
    released = asyncio.Event()

    async def refresh(e):
        """Waits to be released, then removes the indicator or raises if asked."""
        started.set()
        await released.wait()
        if remove_in_handler:
            session.page.clean()
        if raises:
            raise ValueError("Refresh failed")

    indicator = ft.RefreshIndicator(content=ft.ListView(), on_refresh=refresh)
    session.page.add(ft.Container(indicator) if nested else indicator)

    with patch.object(session, "invoke_method", new_callable=AsyncMock) as invoke:
        task = asyncio.create_task(indicator._trigger_event("refresh", None))
        await asyncio.wait_for(started.wait(), timeout=1)
        if not remove_in_handler:
            session.page.clean()
        released.set()

        with (
            pytest.raises(ValueError, match="Refresh failed")
            if raises
            else nullcontext()
        ):
            await task

        assert indicator._i not in session.index
        invoke.assert_not_awaited()


async def _flush(turns=10):
    """Gives the event loop `turns` turns, so scheduled renders and effects run."""
    for _ in range(turns):
        await asyncio.sleep(0)


@pytest.mark.asyncio
@pytest.mark.parametrize("keep_indicator", [True, False])
async def test_refresh_through_component_rerender(keep_indicator):
    """A refresh whose handler re-renders the component finishes through the
    re-rendered indicator, and sends nothing when the re-render removes it."""
    connection = _SerializingConnection()
    connection.pubsubhub = PubSubHub()
    session = Session(connection)
    token = _context_page.set(session.page)

    @ft.component
    def App():
        """Shows a refresh count, or a text instead of the indicator once
        refreshed when the indicator isn't kept."""
        count, set_count = ft.use_state(0)

        async def refresh():
            """Bumps the count, which re-renders `App`, then yields."""
            set_count(count + 1)
            await asyncio.sleep(0)

        if count and not keep_indicator:
            return ft.Text("Refreshed")
        return ft.RefreshIndicator(
            content=ft.ListView([ft.Text(f"Pulled {count} times")]),
            on_refresh=refresh,
        )

    try:
        session.page.render(App)
        session.get_page_patch()
        await _flush()
        indicator = next(
            c for c in session.index.values() if isinstance(c, ft.RefreshIndicator)
        )

        with patch.object(session, "invoke_method", new_callable=AsyncMock) as invoke:
            await indicator._trigger_event("refresh", None)
            await _flush()

            if keep_indicator:
                assert session.index[indicator._i] is not indicator
                invoke.assert_awaited_once_with(
                    indicator._i, "finish_refresh", None, None
                )
            else:
                assert indicator._i not in session.index
                invoke.assert_not_awaited()
    finally:
        session.close()
        await _flush()
        _context_page.reset(token)
