"""Tests for logging unhandled exceptions from background tasks, threads and
PubSub subscribers."""

import asyncio
import logging
import threading
from concurrent.futures import ThreadPoolExecutor

import pytest
import pytest_asyncio

from flet.messaging.connection import Connection
from flet.messaging.session import Session
from flet.pubsub.pubsub_hub import PubSubHub

# Long enough for a thread or task to run and log; short enough to stay cheap.
SETTLE = 0.2


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


async def failing_task():
    raise ValueError("task failed")


class TestRunTaskErrors:
    """`page.run_task()` logs the exception of a task nothing awaits."""

    @pytest.mark.asyncio
    async def test_exception_of_an_unawaited_task_is_logged(self, page, caplog):
        """A failing task nothing awaits is logged on `flet`, with its name."""
        page.run_task(failing_task)
        await asyncio.sleep(SETTLE)

        [record] = _errors(caplog)
        assert "failing_task" in record.getMessage()
        assert isinstance(record.exc_info[1], ValueError)

    @pytest.mark.asyncio
    async def test_exception_of_an_awaited_task_is_not_logged(self, page, caplog):
        """A failing task that is awaited raises there instead of being logged."""
        with pytest.raises(ValueError, match="task failed"):
            await page.run_task(failing_task)
        await asyncio.sleep(SETTLE)

        assert [r for r in caplog.records if r.levelno >= logging.ERROR] == []

    @pytest.mark.asyncio
    async def test_cancelled_task_is_not_logged(self, page, caplog):
        """Cancelling a task isn't an error."""
        future = page.run_task(asyncio.sleep, 10)
        await asyncio.sleep(0)
        future.cancel()
        await asyncio.sleep(SETTLE)

        assert _errors(caplog) == []


class TestRunThreadErrors:
    """`page.run_thread()` logs the exception of its function."""

    @pytest.mark.asyncio
    async def test_exception_is_logged(self, page, caplog):
        """A failing function is logged on `flet`, with its name."""

        def failing_function():
            raise ValueError("thread failed")

        page.run_thread(failing_function)
        await asyncio.sleep(SETTLE)

        [record] = _errors(caplog)
        assert "failing_function" in record.getMessage()
        assert isinstance(record.exc_info[1], ValueError)


class TestPubSubSubscriberErrors:
    """PubSub logs the exception of a subscriber and still delivers to others."""

    @pytest.mark.asyncio
    async def test_async_subscriber_exception_is_logged(self, caplog):
        """A failing async subscriber is logged on `flet`, with its name."""
        hub = PubSubHub(loop=asyncio.get_running_loop())

        async def failing_subscriber(message):
            raise ValueError(f"failed on {message}")

        hub.subscribe("session", failing_subscriber)
        hub.send_all("hello")
        await asyncio.sleep(SETTLE)

        [record] = _errors(caplog)
        assert "failing_subscriber" in record.getMessage()
        assert str(record.exc_info[1]) == "failed on hello"

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
        await asyncio.sleep(SETTLE)

        [record] = _errors(caplog)
        assert "failing_subscriber" in record.getMessage()
        assert str(record.exc_info[1]) == "failed on hello"
        assert received.is_set()
