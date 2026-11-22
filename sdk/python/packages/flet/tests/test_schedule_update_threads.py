"""Worker-thread scheduling and session lifecycle for component updates and effects."""

import asyncio
import threading
import time

import pytest
import pytest_asyncio

import flet as ft
from flet.components.component import Component
from flet.components.hooks.use_effect import EffectHook
from flet.controls.context import _context_page
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


def _create_connection() -> Connection:
    conn = _RecordingConnection()
    conn.pubsubhub = PubSubHub()
    conn.loop = asyncio.get_running_loop()
    return conn


def _create_session() -> Session:
    return Session(_create_connection())


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


async def _close(session: Session):
    """Closes `session` and waits for the tasks closing it started, such as the
    `close` event dispatch, so none is pending when the test's loop ends."""
    session.close()
    current = asyncio.current_task()
    await asyncio.gather(
        *(t for t in asyncio.all_tasks() if t is not current), return_exceptions=True
    )


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
    await _close(session)
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
        await _close(session)


@pytest.mark.asyncio
async def test_no_update_is_lost_when_many_threads_schedule_at_once(session):
    controls = [_FakeControl() for _ in range(8 * 100)]

    def worker(i):
        for control in controls[i * 100 : (i + 1) * 100]:
            session.schedule_update(control)

    errors = await asyncio.to_thread(_run_in_threads, worker, 8)

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
    """A worker that outlives the session's event loop must not crash, and its
    update isn't queued, as nothing would ever drain it."""

    async def start():
        session = _create_session()
        session.start_updates_scheduler()
        await asyncio.sleep(0)
        return session

    # The session is left open: closing it needs the loop. Closing the loop
    # cancels the scheduler, and nothing else is pending.
    session = asyncio.run(start())

    errors = _run_in_threads(lambda i: session.schedule_update(_FakeControl()), 1)

    assert errors == []
    assert not session._Session__pending_updates


@pytest.mark.asyncio
async def test_update_from_a_thread_after_close_is_not_queued():
    """After `close()` nobody drains the queues, so nothing must pile up in them."""
    session = _create_session()
    session.start_updates_scheduler()
    await asyncio.sleep(0)
    await _close(session)

    errors = _run_in_threads(lambda i: session.schedule_update(_FakeControl()), 1)
    await asyncio.sleep(0.05)

    assert errors == []
    assert not session._Session__pending_updates


@pytest.mark.asyncio
async def test_effect_from_a_thread_after_close_is_not_queued():
    session = _create_session()
    session.start_updates_scheduler()
    await asyncio.sleep(0)
    await _close(session)

    class _Hook:
        setup = None

    errors = _run_in_threads(lambda i: session.schedule_effect(_Hook(), False), 1)
    await asyncio.sleep(0.05)

    assert errors == []
    assert not session._Session__pending_effects


@pytest.mark.asyncio
async def test_pending_worker_update_is_discarded_on_disconnect(session):
    control = _FakeControl()

    # Join before yielding so the scheduler cannot process the update yet.
    errors = _run_in_threads(lambda i: session.schedule_update(control), 1)
    await session.disconnect(60)
    await asyncio.sleep(0)

    assert errors == []
    assert control.updates == 0
    assert not session._Session__pending_updates


@pytest.mark.asyncio
async def test_worker_effect_precedes_later_loop_effect(session):
    events = []
    component = Component(fn=lambda: None)
    component._state.mounted = True

    def first_setup():
        events.append("first setup")
        return lambda: events.append("first cleanup")

    hook = EffectHook(component, setup=first_setup)
    component._state.hooks.append(hook)
    assert _run_in_threads(lambda i: session.schedule_effect(hook, False), 1) == []
    hook.setup = lambda: events.append("second setup")
    session.schedule_effect(hook, False)

    assert await _wait_for(lambda: "first setup" in events and "second setup" in events)
    assert events == ["first setup", "first cleanup", "second setup"]


@pytest.mark.asyncio
async def test_reconnect_discards_pending_worker_updates_and_effects(session):
    old_control, new_control = _FakeControl(), _FakeControl()
    events = []
    component = Component(fn=lambda: None)
    component._state.mounted = True
    hook = EffectHook(component, setup=lambda: events.append("old"))
    component._state.hooks.append(hook)

    def submit_old_work(i):
        session.schedule_update(old_control)
        session.schedule_effect(hook, False)

    assert _run_in_threads(submit_old_work, 1) == []
    await session.disconnect(60)
    session.attach_connection(_create_connection())
    hook.setup = lambda: events.append("new")
    session.schedule_effect(hook, False)
    session.schedule_update(new_control)

    assert await _wait_for(lambda: new_control.updates == 1)
    assert old_control.updates == 0
    assert events == ["new"]


@pytest.mark.asyncio
async def test_worker_submission_before_startup_leaves_wakeup_to_loop(monkeypatch):
    session = _create_session()
    control = _FakeControl()
    owner = threading.current_thread()
    ready = session._Session__updates_ready
    set_ready = ready.set

    def set_on_loop():
        assert threading.current_thread() is owner
        set_ready()

    monkeypatch.setattr(ready, "set", set_on_loop)
    try:
        assert _run_in_threads(lambda i: session.schedule_update(control), 1) == []
        session.start_updates_scheduler()
        assert await _wait_for(lambda: control.updates == 1)
    finally:
        await _close(session)


@pytest.mark.asyncio
async def test_many_worker_updates_post_one_wakeup(session, monkeypatch):
    """Updates queued while a wakeup is still on its way to the loop don't post
    another one."""
    loop = asyncio.get_running_loop()
    call_soon_threadsafe = loop.call_soon_threadsafe
    wakeups = []

    def counting(callback, *args, **kwargs):
        if callback == session._Session__on_posted_wakeup:
            wakeups.append(callback)
        return call_soon_threadsafe(callback, *args, **kwargs)

    monkeypatch.setattr(loop, "call_soon_threadsafe", counting)
    controls = [_FakeControl() for _ in range(1000)]

    # The loop doesn't run while the workers do, so the first wakeup stays pending.
    def worker(i):
        for control in controls[i * 250 : (i + 1) * 250]:
            session.schedule_update(control)

    assert _run_in_threads(worker, 4) == []

    assert len(wakeups) == 1
    assert await _wait_for(lambda: all(c.updates == 1 for c in controls))

    # Once that wakeup ran, the next worker update posts a new one.
    assert _run_in_threads(lambda i: session.schedule_update(controls[0]), 1) == []
    assert len(wakeups) == 2
    assert await _wait_for(lambda: controls[0].updates == 2)


@pytest.mark.asyncio
async def test_update_starts_the_scheduler_when_nothing_started_it():
    """An app that doesn't render components never starts the scheduler, so
    queuing work starts it, from the loop or from a worker thread."""
    session = _create_session()
    on_loop, from_worker = _FakeControl(), _FakeControl()
    try:
        session.schedule_update(on_loop)
        assert await _wait_for(lambda: on_loop.updates == 1)

        session._Session__updates_task.cancel()
        await asyncio.sleep(0)
        assert _run_in_threads(lambda i: session.schedule_update(from_worker), 1) == []
        assert await _wait_for(lambda: from_worker.updates == 1)
    finally:
        await _close(session)


@pytest.mark.asyncio
@pytest.mark.parametrize("close", [True, False])
async def test_finalizer_queuing_work_while_the_queues_are_dropped(session, close):
    """Dropping the queues on close or disconnect can release the last reference
    to a control whose finalizer queues work. That must not deadlock on the queue
    lock, and the work is dropped."""
    finalized = []

    class _Finalizing(_FakeControl):
        def __del__(self):
            session.schedule_update(_FakeControl())
            finalized.append(True)

    session._Session__pending_updates.add(_Finalizing())
    if close:
        session.close()
    else:
        await session.disconnect(60)

    assert finalized == [True]
    assert not session._Session__pending_updates


@pytest.mark.asyncio
async def test_set_state_from_worker_threads_is_applied_on_the_loop():
    """`set_state` called from worker threads applies every change on the event
    loop, so it can't race a render of the component."""
    session = _create_session()
    token = _context_page.set(session.page)
    loop_thread = threading.current_thread()
    updater_threads = set()
    setters = []

    @ft.component
    def App():
        count, set_count = ft.use_state(0)
        setters.append(set_count)
        return ft.Text(f"count {count}")

    def increment(count):
        updater_threads.add(threading.current_thread())
        return count + 1

    def worker(i):
        for _ in range(100):
            setters[-1](increment)

    try:
        session.page.render(App)
        session.get_page_patch()

        errors = await asyncio.to_thread(_run_in_threads, worker, 4)

        assert errors == []
        assert await _wait_for(
            lambda: any(
                isinstance(c, ft.Text) and c.value == "count 400"
                for c in session.index.values()
            )
        )
        assert updater_threads == {loop_thread}
    finally:
        _context_page.reset(token)
        await _close(session)
