"""`Session.schedule_update()` and `schedule_effect()` called from worker threads.

The pending queues and the `asyncio.Event` that wakes the updates scheduler are only
safe on the event loop thread, so calls from other threads (e.g. state changed in a
`page.run_thread()` worker) must be handed to the loop.
"""

import asyncio
import threading
import time

import pytest
import pytest_asyncio

from flet.messaging.connection import Connection
from flet.messaging.session import Session
from flet.pubsub.pubsub_hub import PubSubHub


class _RecordingConnection(Connection):
    def __init__(self):
        super().__init__()
        self.messages = []

    def send_message(self, message):
        self.messages.append(message)


class _FakeControl:
    """Counts the updates the scheduler makes."""

    def __init__(self):
        self.updates = 0

    def update(self):
        self.updates += 1


def _create_session() -> Session:
    conn = _RecordingConnection()
    conn.pubsubhub = PubSubHub()
    conn.loop = asyncio.get_running_loop()
    return Session(conn)


def _run_in_threads(target, count):
    errors = []

    def run(i):
        try:
            target(i)
        except Exception as e:  # noqa: BLE001 - the test asserts there are none
            errors.append(e)

    threads = [threading.Thread(target=run, args=(i,)) for i in range(count)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    return errors


async def _wait_for(condition, timeout=2.0):
    loop = asyncio.get_running_loop()
    deadline = loop.time() + timeout
    while not condition() and loop.time() < deadline:
        await asyncio.sleep(0.01)
    return condition()


@pytest_asyncio.fixture
async def session():
    loop = asyncio.get_running_loop()
    # Debug mode makes asyncio raise on non-thread-safe calls from other threads.
    debug = loop.get_debug()
    loop.set_debug(True)
    session = _create_session()
    session.start_updates_scheduler()
    await asyncio.sleep(0)  # the scheduler is now waiting for work
    yield session
    session.close()
    await asyncio.sleep(0)
    loop.set_debug(debug)


@pytest.mark.asyncio
async def test_update_scheduled_from_a_worker_thread_is_applied(session):
    control = _FakeControl()

    errors = _run_in_threads(lambda i: session.schedule_update(control), 1)

    assert errors == []
    assert await _wait_for(lambda: control.updates == 1)


@pytest.mark.asyncio
async def test_update_from_a_worker_thread_wakes_an_idle_loop():
    """Without debug mode and with nothing else waking the loop (no polling, as in
    an idle app), the update must still be applied right away."""
    session = _create_session()
    session.start_updates_scheduler()
    await asyncio.sleep(0)
    applied = asyncio.Event()

    class _Control:
        def update(self):
            applied.set()

    def worker():
        time.sleep(0.1)  # the loop is idle, waiting for `applied`
        session.schedule_update(_Control())

    thread = threading.Thread(target=worker)
    thread.start()
    try:
        await asyncio.wait_for(applied.wait(), 2)
    finally:
        thread.join()
        session.close()
        await asyncio.sleep(0)


@pytest.mark.asyncio
async def test_no_update_is_lost_when_many_threads_schedule_at_once(session):
    controls = [_FakeControl() for _ in range(8 * 100)]

    def worker(i):
        for control in controls[i * 100 : (i + 1) * 100]:
            session.schedule_update(control)

    errors = _run_in_threads(worker, 8)

    assert errors == []
    assert await _wait_for(lambda: all(c.updates >= 1 for c in controls))


@pytest.mark.asyncio
async def test_effect_scheduled_from_a_worker_thread_runs(session, monkeypatch):
    ran = []
    monkeypatch.setattr(
        session,
        "_Session__run_effect",
        lambda hook, setup: ran.append((hook, setup)),
    )
    setup = object()

    class _Hook:
        pass

    hook = _Hook()
    hook.setup = setup

    errors = _run_in_threads(lambda i: session.schedule_effect(hook, False), 1)

    assert errors == []
    assert await _wait_for(lambda: ran == [(hook, setup)])


@pytest.mark.asyncio
async def test_update_on_the_loop_thread_is_queued_right_away(session):
    """On the loop thread nothing is deferred: the control is queued at once."""
    control = _FakeControl()

    session.schedule_update(control)

    assert control in session._Session__pending_updates


def test_update_from_a_thread_after_the_loop_closed_is_ignored():
    """A worker that outlives the session's event loop must not crash."""

    async def start():
        session = _create_session()
        session.start_updates_scheduler()
        await asyncio.sleep(0)
        return session

    session = asyncio.run(start())  # the loop is closed when this returns

    errors = _run_in_threads(lambda i: session.schedule_update(_FakeControl()), 1)

    assert errors == []


@pytest.mark.asyncio
async def test_update_from_a_thread_after_close_is_not_queued():
    """After `close()` nobody drains the queues, so nothing must pile up in them."""
    session = _create_session()
    session.start_updates_scheduler()
    await asyncio.sleep(0)
    session.close()
    await asyncio.sleep(0)

    errors = _run_in_threads(lambda i: session.schedule_update(_FakeControl()), 1)
    await asyncio.sleep(0.05)

    assert errors == []
    assert not session._Session__pending_updates


@pytest.mark.asyncio
async def test_effect_from_a_thread_after_close_is_not_queued():
    session = _create_session()
    session.start_updates_scheduler()
    await asyncio.sleep(0)
    session.close()
    await asyncio.sleep(0)

    class _Hook:
        setup = None

    errors = _run_in_threads(lambda i: session.schedule_effect(_Hook(), False), 1)
    await asyncio.sleep(0.05)

    assert errors == []
    assert not session._Session__pending_effects


@pytest.mark.asyncio
async def test_update_handed_to_the_loop_before_disconnect_is_dropped(session):
    """A worker passes the check in `schedule_update()` and hands the update to the
    loop, but `disconnect()` runs first and clears the queues: the update must not
    put the control back and get applied on a disconnected session."""
    control = _FakeControl()

    # The thread is joined without yielding, so the update waits on the loop.
    errors = _run_in_threads(lambda i: session.schedule_update(control), 1)
    await session.disconnect(60)
    await asyncio.sleep(0.05)

    assert errors == []
    assert control.updates == 0
    assert not session._Session__pending_updates
