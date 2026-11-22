"""Event handlers run what they return: a coroutine, an async generator or a generator.

A plain function that calls an `async` handler, such as `lambda: save(item)`, returns
a coroutine. Flet awaits it as it would an `async def` handler, instead of dropping
it without running. A task or a future the handler started is left to run on its own.
"""

import asyncio
import inspect
import types

import msgpack
import pytest

from flet.controls.base_control import BaseControl
from flet.controls.core.text import Text
from flet.messaging.connection import Connection
from flet.messaging.protocol import configure_encode_object_for_msgpack
from flet.messaging.session import Session
from flet.pubsub.pubsub_hub import PubSubHub


class RecordingConnection(Connection):
    """Connection that packs each outbound message, as the real transports do."""

    def __init__(self):
        super().__init__()
        self.pubsubhub = PubSubHub()
        self.sent = 0

    def send_message(self, message):
        msgpack.packb(
            [message.action, message.body],
            default=configure_encode_object_for_msgpack(BaseControl),
        )
        self.sent += 1


def _mounted_session(text: Text) -> Session:
    """A session showing `text`, bootstrapped as `REGISTER_CLIENT` would."""
    session = Session(RecordingConnection())
    session.page.controls.append(text)
    msgpack.packb(
        session.get_page_patch(),
        default=configure_encode_object_for_msgpack(BaseControl),
    )
    return session


async def _tap(text: Text) -> Session:
    session = _mounted_session(text)
    session.errors = []  # type: ignore[attr-defined]
    session.error = session.errors.append  # type: ignore[method-assign, attr-defined]
    await session.dispatch_event(text._i, "tap", None)
    return session


@pytest.mark.asyncio
async def test_lambda_returning_a_coroutine_is_awaited():
    """`lambda: save("a")` with an `async` `save` runs `save` before the event ends."""
    log: list[str] = []
    text = Text("start")

    async def save(item: str):
        await asyncio.sleep(0)
        text.value = f"saved {item}"
        log.append(item)

    text.on_tap = lambda: save("a")
    await _tap(text)

    assert log == ["a"]
    assert text.value == "saved a"


@pytest.mark.asyncio
@pytest.mark.parametrize("marked", [False, True], ids=["plain", "marked"])
async def test_handler_advances_async_generator(marked):
    text = Text("start")

    async def values():
        text.value = "advanced"
        yield

    stream = values()

    def advance():
        return stream.__anext__()

    if marked:
        if not hasattr(inspect, "markcoroutinefunction"):
            pytest.skip("markcoroutinefunction requires Python 3.12")
        advance = inspect.markcoroutinefunction(advance)

    try:
        text.on_tap = advance
        await _tap(text)
        assert text.value == "advanced"
    finally:
        await stream.aclose()


@pytest.mark.asyncio
@pytest.mark.skipif(
    not hasattr(inspect, "markcoroutinefunction"),
    reason="markcoroutinefunction requires Python 3.12",
)
async def test_marked_handler_awaits_returned_future():
    future = asyncio.get_running_loop().create_future()
    future.set_exception(ValueError("handler future failed"))

    @inspect.markcoroutinefunction
    def handler():
        return future

    session = await _tap(Text("start", on_tap=handler))
    assert len(session.errors) == 1
    assert "handler future failed" in session.errors[0]


@pytest.mark.asyncio
async def test_handler_awaits_generator_based_coroutine():
    text = Text("start")

    @types.coroutine
    def update():
        # The task suspends once before it has a result to send back.
        ready = asyncio.create_task(asyncio.sleep(0, result="done"))
        text.value = yield from ready

    text.on_tap = lambda: update()
    await _tap(text)
    assert text.value == "done"


@pytest.mark.asyncio
async def test_lambda_with_event_returning_a_coroutine_is_awaited():
    """A one-argument lambda gets the event and its coroutine is awaited."""
    seen: list[str] = []
    text = Text("start")

    async def handle(e):
        await asyncio.sleep(0)
        seen.append(e.name)

    text.on_tap = lambda e: handle(e)
    await _tap(text)

    assert seen == ["tap"]


@pytest.mark.asyncio
async def test_coroutine_error_is_reported_like_an_async_handler_error():
    """An exception in the returned coroutine is reported, as for `async def`."""
    text = Text("start")

    async def fail():
        raise ValueError("boom")

    text.on_tap = lambda: fail()
    session = await _tap(text)

    assert len(session.errors) == 1  # type: ignore[attr-defined]
    assert "boom" in session.errors[0]  # type: ignore[attr-defined]


@pytest.mark.asyncio
async def test_lambda_returning_a_generator_is_iterated():
    """A lambda that calls a generator handler runs it to the end."""
    log: list[str] = []
    text = Text("start")

    def steps(n: int):
        for i in range(n):
            log.append(f"step {i}")
            yield

    text.on_tap = lambda: steps(2)
    await _tap(text)

    assert log == ["step 0", "step 1"]


@pytest.mark.asyncio
async def test_lambda_returning_an_async_generator_is_iterated():
    """A lambda that calls an async generator handler runs it to the end."""
    log: list[str] = []
    text = Text("start")

    async def steps(n: int):
        for i in range(n):
            await asyncio.sleep(0)
            log.append(f"step {i}")
            yield

    text.on_tap = lambda: steps(2)
    await _tap(text)

    assert log == ["step 0", "step 1"]


@pytest.mark.asyncio
async def test_task_returned_by_a_lambda_is_not_awaited():
    """`lambda: asyncio.create_task(...)` stays fire-and-forget."""
    started = asyncio.Event()
    release = asyncio.Event()
    text = Text("start")

    async def work():
        started.set()
        await release.wait()

    text.on_tap = lambda: asyncio.create_task(work())
    await asyncio.wait_for(_tap(text), timeout=1)

    await started.wait()
    release.set()


@pytest.mark.asyncio
async def test_async_def_and_plain_handlers_still_run():
    """`async def` and plain handlers behave as before."""
    log: list[str] = []

    async def async_handler(e):
        await asyncio.sleep(0)
        log.append("async")

    def plain_handler():
        log.append("plain")
        return 42  # a value that isn't a coroutine or a generator is ignored

    await _tap(Text("a", on_tap=async_handler))
    await _tap(Text("b", on_tap=plain_handler))

    assert log == ["async", "plain"]
