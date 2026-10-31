import asyncio
from contextlib import nullcontext
from unittest.mock import AsyncMock, patch

import msgpack
import pytest

import flet as ft
from flet.messaging.connection import Connection
from flet.messaging.protocol import configure_encode_object_for_msgpack
from flet.messaging.session import Session
from flet.pubsub.pubsub_hub import PubSubHub


class _SerializingConnection(Connection):
    def send_message(self, message):
        # Serialization records the snapshots used to unmount removed controls.
        msgpack.packb(
            message, default=configure_encode_object_for_msgpack(ft.BaseControl)
        )


@pytest.fixture
def session():
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
    async def refresh(e):
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
    started = asyncio.Event()
    released = asyncio.Event()

    async def refresh(e):
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
