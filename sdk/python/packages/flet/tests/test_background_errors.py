"""Tests for logging unhandled exceptions from background tasks, threads and
PubSub subscribers."""

import asyncio
import functools
import gc
import logging
import threading
from concurrent.futures import ThreadPoolExecutor

import pytest
import pytest_asyncio

from flet.messaging.connection import Connection
from flet.messaging.session import Session
from flet.pubsub.pubsub_hub import PubSubHub

# Upper bound for a task, thread or subscriber to fail and be logged.
TIMEOUT = 5.0


class LoopConnection(Connection):
    """Connection on the running event loop that discards outbound messages."""

    def __init__(self):
        super().__init__()
        self.loop = asyncio.get_running_loop()
        self.executor = ThreadPoolExecutor()
        self.pubsubhub = PubSubHub(loop=self.loop, executor=self.executor)

    def send_message(self, message):
        pass


@pytest_asyncio.fixture
async def page():
    """A page of a session on the running event loop."""
    session = Session(LoopConnection())
    yield session.page


def _errors(caplog) -> list[logging.LogRecord]:
    """The ERROR records logged on the `flet` logger."""
    return [
        r for r in caplog.records if r.name == "flet" and r.levelno == logging.ERROR
    ]


def _all_errors(caplog) -> list[logging.LogRecord]:
    """The ERROR records logged on any logger."""
    return [r for r in caplog.records if r.levelno >= logging.ERROR]


async def _until(condition) -> bool:
    """Wait for `condition()` to hold, up to `TIMEOUT`."""
    loop = asyncio.get_running_loop()
    deadline = loop.time() + TIMEOUT
    while not condition() and loop.time() < deadline:
        await asyncio.sleep(0.01)
    return condition()


async def failing_task():
    raise ValueError("task failed")


async def failing_task_with(token):
    raise ValueError("task failed")


async def _cancel_awaiter_as_task_fails(page, caplog) -> bool:
    """
    Cancel a task's awaiter right after the task's exception is handed to it,
    before it resumes.

    Runs in its own coroutine so its references to the future are gone once it
    returns. Returns whether the awaiter was cancelled with nothing logged.
    """
    fail = asyncio.Event()

    async def task():
        await fail.wait()
        raise ValueError("task failed")

    async def wait_for(future):
        return await future

    future = page.run_task(task)
    awaiter = asyncio.create_task(wait_for(future))
    await asyncio.sleep(0)
    future.add_done_callback(lambda _: awaiter.cancel())
    fail.set()
    cancelled = False
    try:
        await awaiter
    except asyncio.CancelledError:
        cancelled = True
    return cancelled and _errors(caplog) == []


class TestRunTaskErrors:
    """`page.run_task()` logs the exception of a task nothing awaits."""

    @pytest.mark.asyncio
    async def test_exception_of_an_unawaited_task_is_logged(self, page, caplog):
        """A failing task nothing awaits is logged on `flet`, with its name."""
        page.run_task(failing_task)

        assert await _until(lambda: _errors(caplog))
        [record] = _errors(caplog)
        assert "failing_task" in record.getMessage()
        assert isinstance(record.exc_info[1], ValueError)

    @pytest.mark.asyncio
    async def test_partial_task_is_named_without_its_arguments(self, page, caplog):
        """A task given as a `functools.partial` is named after its function,
        without its arguments."""
        page.run_task(functools.partial(failing_task_with, "secret-token"))

        assert await _until(lambda: _errors(caplog))
        [record] = _errors(caplog)
        assert "failing_task_with" in record.getMessage()
        assert "secret-token" not in record.getMessage()

    @pytest.mark.asyncio
    async def test_exception_of_an_awaited_task_is_not_logged(self, page, caplog):
        """A failing task that is awaited raises there instead of being logged."""
        future = page.run_task(failing_task)

        with pytest.raises(ValueError, match="task failed"):
            await future
        del future
        gc.collect()

        assert _all_errors(caplog) == []

    @pytest.mark.asyncio
    async def test_exception_an_awaiter_never_gets_is_logged_on_discard(
        self, page, caplog
    ):
        """An exception that reaches an awaiter just as it's cancelled is logged
        once the future is discarded."""
        assert await _cancel_awaiter_as_task_fails(page, caplog)
        # The loop's current callback holds the cancelled awaiter until it
        # returns.
        await asyncio.sleep(0)
        gc.collect()

        [record] = _errors(caplog)
        assert "task" in record.getMessage()
        assert str(record.exc_info[1]) == "task failed"

    @pytest.mark.asyncio
    async def test_cancelled_task_is_not_logged(self, page, caplog):
        """Cancelling a task isn't an error."""
        future = page.run_task(asyncio.sleep, 10)
        await asyncio.sleep(0)
        future.cancel()

        assert await _until(future.done)
        await asyncio.sleep(0)
        assert _all_errors(caplog) == []


class TestRunThreadErrors:
    """`page.run_thread()` logs the exception of its function."""

    @pytest.mark.asyncio
    async def test_exception_is_logged(self, page, caplog):
        """A failing function is logged on `flet`, with its name."""

        def failing_function():
            raise ValueError("thread failed")

        page.run_thread(failing_function)

        assert await _until(lambda: _errors(caplog))
        [record] = _errors(caplog)
        assert "failing_function" in record.getMessage()
        assert isinstance(record.exc_info[1], ValueError)


class TestPubSubSubscriberErrors:
    """PubSub logs the exception of a subscriber and still delivers to others."""

    @pytest.mark.asyncio
    async def test_async_subscriber_exception_is_logged(self, caplog):
        """A failing async subscriber is logged, and the others still get the
        message."""
        hub = PubSubHub(loop=asyncio.get_running_loop())
        received = []

        async def failing_subscriber(message):
            raise ValueError(f"failed on {message}")

        async def subscriber(message):
            received.append(message)

        hub.subscribe("session 1", failing_subscriber)
        hub.subscribe("session 2", subscriber)
        hub.send_all("hello")

        assert await _until(lambda: _errors(caplog) and received)
        [record] = _errors(caplog)
        assert "failing_subscriber" in record.getMessage()
        assert str(record.exc_info[1]) == "failed on hello"
        assert received == ["hello"]

    @pytest.mark.asyncio
    async def test_async_subscriber_with_wrong_arguments_is_logged(self, caplog):
        """An async subscriber that can't take the message is logged, and the
        others still get it."""
        hub = PubSubHub(loop=asyncio.get_running_loop())
        received = []

        async def no_arguments():
            pass

        async def subscriber(message):
            received.append(message)

        hub.subscribe("session 1", no_arguments)
        hub.subscribe("session 2", subscriber)
        hub.send_all("hello")

        assert await _until(lambda: _errors(caplog) and received)
        [record] = _errors(caplog)
        assert "no_arguments" in record.getMessage()
        assert isinstance(record.exc_info[1], TypeError)

    @pytest.mark.asyncio
    @pytest.mark.parametrize("executor", [True, False], ids=["pool", "inline"])
    async def test_sync_subscriber_exception_is_logged(self, caplog, executor):
        """A failing sync subscriber is logged, and the others still get the
        message."""
        hub = PubSubHub(
            loop=asyncio.get_running_loop(),
            executor=ThreadPoolExecutor() if executor else None,
        )
        received = threading.Event()

        def failing_subscriber(message):
            raise ValueError(f"failed on {message}")

        hub.subscribe("session 1", failing_subscriber)
        hub.subscribe("session 2", lambda message: received.set())
        hub.send_all("hello")

        assert await _until(lambda: _errors(caplog) and received.is_set())
        [record] = _errors(caplog)
        assert "failing_subscriber" in record.getMessage()
        assert str(record.exc_info[1]) == "failed on hello"

    @pytest.mark.asyncio
    async def test_subscriber_with_failing_repr_is_logged(self, caplog):
        """A failing subscriber whose `repr()` raises is still logged by name, and
        the others still get the message."""
        hub = PubSubHub(loop=asyncio.get_running_loop())
        received = []

        class Subscriber:
            def __call__(self, message):
                raise ValueError(f"failed on {message}")

            def __repr__(self):
                raise RuntimeError("no repr")

        hub.subscribe("session 1", Subscriber())
        hub.subscribe("session 2", received.append)
        hub.send_all("hello")

        assert await _until(lambda: _errors(caplog) and received)
        [record] = _errors(caplog)
        assert "Subscriber" in record.getMessage()
        assert str(record.exc_info[1]) == "failed on hello"
