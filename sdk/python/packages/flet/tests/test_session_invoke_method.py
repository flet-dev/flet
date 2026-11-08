import asyncio
import gc
import weakref

import pytest

from flet.messaging.connection import Connection
from flet.messaging.session import Session
from flet.pubsub.pubsub_hub import PubSubHub


class _RecordingConnection(Connection):
    def __init__(self):
        super().__init__()
        self.messages = []

    def send_message(self, message):
        self.messages.append(message)


class _Result(dict):
    """A response whose lifetime can be observed without inspecting the session."""


@pytest.mark.asyncio
@pytest.mark.parametrize("response_before_cancel", [False, True])
async def test_cancelled_call_does_not_retain_response(response_before_cancel):
    conn = _RecordingConnection()
    conn.pubsubhub = PubSubHub()
    conn.loop = asyncio.get_running_loop()
    session = Session(conn)
    try:
        call = asyncio.create_task(session.page.get_package_info())
        await asyncio.sleep(0)
        request = conn.messages[-1].body

        result = _Result(app_name="My App", version="1.0.0")
        result_ref = weakref.ref(result)
        if response_before_cancel:
            session.handle_invoke_method_results(
                request.control_id, request.call_id, result, None
            )

        call.cancel()
        with pytest.raises(asyncio.CancelledError):
            await call

        if not response_before_cancel:
            session.handle_invoke_method_results(
                request.control_id, request.call_id, result, None
            )
        del result
        gc.collect()

        assert result_ref() is None
    finally:
        session.close()


@pytest.mark.asyncio
@pytest.mark.parametrize("close_session", [False, True])
async def test_failed_call_does_not_retain_late_response(close_session):
    conn = _RecordingConnection()
    conn.pubsubhub = PubSubHub()
    conn.loop = asyncio.get_running_loop()
    session = Session(conn)
    try:
        call = asyncio.create_task(
            session.invoke_method(
                session.page._i,
                "get_package_info",
                {},
                timeout=None if close_session else 0,
            )
        )
        await asyncio.sleep(0)
        request = conn.messages[-1].body

        if close_session:
            session.close()
            with pytest.raises(RuntimeError, match="Session closed"):
                await call
        else:
            with pytest.raises((TimeoutError, asyncio.TimeoutError)):
                await call

        result = _Result(app_name="My App", version="1.0.0")
        result_ref = weakref.ref(result)
        session.handle_invoke_method_results(
            request.control_id, request.call_id, result, None
        )
        del result
        gc.collect()

        assert result_ref() is None
    finally:
        session.close()
