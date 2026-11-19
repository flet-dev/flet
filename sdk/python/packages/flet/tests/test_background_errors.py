"""Tests for logging unhandled exceptions from background tasks, threads and
PubSub subscribers."""

import asyncio
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
        """An awaited task's exception that isn't retrieved is logged once the
        future is discarded."""
        future = page.run_task(failing_task)
        # Stands in for an awaiter cancelled, or whose loop closed, just as the
        # task failed: it started waiting but never got the outcome.
        future._awaited = True
        assert await _until(future.done)
        assert _errors(caplog) == []

        del future
        gc.collect()

        [record] = _errors(caplog)
        assert "failing_task" in record.getMessage()

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
    async def test_subscriber_can_unsubscribe_while_receiving(self):
        """A subscriber called inline can unsubscribe without blocking the
        publish."""
        hub = PubSubHub(loop=asyncio.get_running_loop())
        received = []

        def subscriber(message):
            received.append(message)
            hub.unsubscribe("session")

        hub.subscribe("session", subscriber)
        publish = threading.Thread(target=hub.send_all, args=["hello"], daemon=True)
        publish.start()
        publish.join(TIMEOUT)

        assert not publish.is_alive()
        assert received == ["hello"]
