import asyncio
import gc
import time
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


class _FailingConnection(Connection):
    def send_message(self, message):
        raise ConnectionError("connection lost")


def _create_session(conn: Connection) -> Session:
    conn.pubsubhub = PubSubHub()
    conn.loop = asyncio.get_running_loop()
    return Session(conn)


class _Result(dict):
    """A response whose lifetime can be observed without inspecting the session."""


@pytest.mark.asyncio
@pytest.mark.parametrize("timeout", [None, 5])
@pytest.mark.parametrize(
    "order",
    [
        "response_then_cancel",
        "cancel_then_response",  # same event-loop turn, before the call resumes
        "response_after_cancelled",
    ],
)
async def test_cancelled_call_does_not_retain_response(order, timeout):
    """Cancelled calls raise CancelledError and drop their response, whenever
    it arrives."""
    conn = _RecordingConnection()
    session = _create_session(conn)
    try:
        call = asyncio.create_task(
            session.invoke_method(
                session.page._i, "get_package_info", {}, timeout=timeout
            )
        )
        await asyncio.sleep(0)
        request = conn.messages[-1].body

        result = _Result(app_name="My App", version="1.0.0")
        result_ref = weakref.ref(result)

        def respond(response):
            session.handle_invoke_method_results(
                request.control_id, request.call_id, response, None
            )

        if order == "response_then_cancel":
            respond(result)
            call.cancel()
        elif order == "cancel_then_response":
            call.cancel()
            respond(result)
        else:
            call.cancel()

        with pytest.raises(asyncio.CancelledError):
            await call

        if order == "response_after_cancelled":
            respond(result)
        # The finished task and its CancelledError still reference the call's
        # frames until released, like any local; the session must not.
        del call, result, respond
        await asyncio.sleep(0)
        gc.collect()

        assert result_ref() is None
    finally:
        session.close()
        await asyncio.sleep(0)


@pytest.mark.asyncio
@pytest.mark.parametrize("close_session", [False, True])
async def test_failed_call_does_not_retain_late_response(close_session):
    """Timed-out and session-closed calls drop a response that arrives later."""
    conn = _RecordingConnection()
    session = _create_session(conn)
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
            with pytest.raises(TimeoutError, match="Timeout waiting for invokeMethod"):
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
        if not close_session:
            session.close()
        await asyncio.sleep(0)


@pytest.mark.asyncio
async def test_failed_send_does_not_register_call():
    """A call whose request can't be sent leaves nothing pending."""
    session = _create_session(_FailingConnection())
    try:
        with pytest.raises(ConnectionError):
            await session.invoke_method(session.page._i, "get_package_info", {})

        assert session._Session__method_calls == {}
    finally:
        session.close()
        await asyncio.sleep(0)


@pytest.mark.asyncio
async def test_call_after_close_fails_immediately():
    """A call made on a closed session fails instead of waiting forever."""
    conn = _RecordingConnection()
    session = _create_session(conn)
    session.close()
    await asyncio.sleep(0)

    with pytest.raises(RuntimeError, match="Session closed"):
        await asyncio.wait_for(
            session.invoke_method(session.page._i, "get_package_info", {}),
            timeout=1,
        )

    assert conn.messages == []
    assert session._Session__method_calls == {}


@pytest.mark.asyncio
async def test_response_after_close_does_not_override_closure_error():
    """A response that races session close can't turn the failure into success."""
    conn = _RecordingConnection()
    session = _create_session(conn)
    call = asyncio.create_task(
        session.invoke_method(session.page._i, "get_package_info", {})
    )
    await asyncio.sleep(0)
    request = conn.messages[-1].body

    session.close()
    session.handle_invoke_method_results(
        request.control_id, request.call_id, {"app_name": "My App"}, None
    )

    with pytest.raises(RuntimeError, match="Session closed"):
        await call
    await asyncio.sleep(0)


@pytest.mark.asyncio
async def test_reply_after_timeout_fires_does_not_override_timeout():
    """A reply arriving after the timeout fired, but before the call resumes,
    doesn't turn the timeout into success."""
    conn = _RecordingConnection()
    session = _create_session(conn)
    loop = asyncio.get_running_loop()
    try:
        call = asyncio.create_task(
            session.invoke_method(session.page._i, "get_package_info", {}, timeout=0.01)
        )
        await asyncio.sleep(0)
        request = conn.messages[-1].body

        # Due right after the call's timeout, so both run in the same
        # event-loop turn once the loop is unblocked - timeout first.
        loop.call_later(
            0.01,
            session.handle_invoke_method_results,
            request.control_id,
            request.call_id,
            {"app_name": "My App"},
            None,
        )
        time.sleep(0.05)

        with pytest.raises(TimeoutError, match="Timeout waiting for invokeMethod"):
            await call
    finally:
        session.close()
        await asyncio.sleep(0)
