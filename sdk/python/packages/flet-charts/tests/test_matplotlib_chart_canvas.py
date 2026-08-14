"""Frame-ack recovery in ``MatplotlibChartCanvas``.

``_send_and_wait`` awaits Dart's ``[0xFF]`` frame-applied ack. A frame in
flight when the platform view is disposed (e.g. the chart's tab is switched
away) loses its ack silently — ``DataChannel.send`` on a disposed channel is
a no-op — and an unbounded await would park ``MatplotlibChart._receive_loop``
(the sole frame consumer) for the rest of the session, with no exception to
observe. Recovery is two-layered:

* ``_capture_channel`` resolves all pending ack futures when Dart opens a
  fresh channel on remount — instant recovery on tab return.
* ``_send_and_wait`` bounds the ack await with ``FRAME_ACK_TIMEOUT`` and
  drops the frame on expiry — recovery even when no remount ever comes.

These tests drive the real library code with only the transport faked,
mirroring ``DataChannel``'s documented behavior (silent drop on a closed
channel).
"""

import asyncio
import types

from flet_charts import matplotlib_chart_canvas
from flet_charts.matplotlib_chart import MatplotlibChart
from flet_charts.matplotlib_chart_canvas import MatplotlibChartCanvas


class FakeChannel:
    """Live transport: acks each frame on the next loop tick (like Dart)."""

    def __init__(self, canvas):
        self.canvas = canvas
        self.closed = False
        self.sent = 0
        self._handler = None

    def on_bytes(self, handler):
        self._handler = handler

    def send(self, payload: bytes):
        if self.closed:
            return  # DataChannel behavior: silent drop, no raise
        self.sent += 1
        asyncio.get_running_loop().call_soon(self._ack)

    def _ack(self):
        if self.closed:
            return
        self.canvas._on_dart_message(b"\xff")


class DyingChannel(FakeChannel):
    """The tab-switch race: the packet leaves, the view is disposed before
    the ack returns — silently, exactly like the real disposed channel."""

    def send(self, payload: bytes):
        self.sent += 1
        self.closed = True


def _make_chart_standin():
    """Minimal ``self`` for the real ``_receive_loop``: a real canvas plus
    the queue/state attrs ``build()`` would normally create."""
    canvas = MatplotlibChartCanvas()
    canvas.init()

    chart = types.SimpleNamespace()
    chart.mpl_canvas = canvas
    chart._receive_queue = asyncio.Queue()
    chart._waiting = False
    chart.img_count = 0
    chart._MatplotlibChart__image_mode = "full"
    return chart, canvas


def _feed_frame(chart):
    chart._receive_queue.put_nowait((True, ("raw", b"frame")))


def _start_loop(chart):
    return asyncio.create_task(MatplotlibChart._receive_loop(chart))


def test_healthy_channel_drains_frames():
    async def scenario():
        chart, canvas = _make_chart_standin()
        canvas._channel = FakeChannel(canvas)
        task = _start_loop(chart)
        for _ in range(3):
            _feed_frame(chart)
        await asyncio.sleep(0.2)
        task.cancel()
        return chart.img_count, chart._receive_queue.qsize()

    applied, queued = asyncio.run(scenario())
    assert applied == 3
    assert queued == 0


def test_recapture_unparks_loop_instantly():
    """Channel dies with a frame in flight; frames queue unconsumed;
    capturing a fresh channel (tab return) must resolve the stale ack and
    drain the backlog — without waiting out the timeout."""

    async def scenario():
        chart, canvas = _make_chart_standin()
        canvas._channel = DyingChannel(canvas)
        task = _start_loop(chart)

        _feed_frame(chart)  # its ack will never arrive
        await asyncio.sleep(0.05)
        # img_count increments only after the ack await returns, so a parked
        # loop = frame taken off the queue but not yet counted as applied.
        parked = chart.img_count == 0 and chart._receive_queue.qsize() == 0
        for _ in range(4):
            _feed_frame(chart)

        # Tab return: Dart opens a fresh channel and the real
        # _capture_channel runs — only get_data_channel is stubbed (it needs
        # a mounted page to look up the channel by id).
        live = FakeChannel(canvas)
        canvas.get_data_channel = lambda cid: live
        canvas._capture_channel(types.SimpleNamespace(channel_id=2))
        await asyncio.sleep(0.2)
        task.cancel()
        return parked, chart.img_count, chart._receive_queue.qsize(), live.sent

    parked, applied, queued, sent_on_new = asyncio.run(scenario())
    assert parked, "precondition: loop parked awaiting the lost ack"
    assert applied == 5, "backlog must drain after recapture"
    assert queued == 0
    assert sent_on_new == 4


def test_capture_channel_flushes_stale_acks():
    """Unit-level: _capture_channel resolves pending futures and empties
    the FIFO."""

    async def scenario():
        canvas = MatplotlibChartCanvas()
        canvas.init()
        stale_fut = asyncio.get_running_loop().create_future()
        canvas._pending_acks.append(stale_fut)

        canvas.get_data_channel = lambda cid: FakeChannel(canvas)
        canvas._capture_channel(types.SimpleNamespace(channel_id=2))
        return stale_fut.done(), len(canvas._pending_acks)

    resolved, pending = asyncio.run(scenario())
    assert resolved, "stale ack must be resolved on recapture"
    assert pending == 0


def test_ack_timeout_drops_frame_and_keeps_fifo_aligned(monkeypatch):
    """No remount: the timeout alone must unpark the loop, and a LATE ack
    for the dropped frame must not resolve the next frame's future (the
    off-by-one that removing the timed-out future from the FIFO prevents)."""

    async def scenario():
        monkeypatch.setattr(matplotlib_chart_canvas, "FRAME_ACK_TIMEOUT", 0.1)
        chart, canvas = _make_chart_standin()

        class SlowThenLiveChannel(FakeChannel):
            def send(self, payload: bytes):
                self.sent += 1
                if self.sent == 1:
                    # ack arrives AFTER the 0.1s timeout — late, not lost
                    asyncio.get_running_loop().call_later(0.25, self._ack)
                else:
                    asyncio.get_running_loop().call_soon(self._ack)

        canvas._channel = SlowThenLiveChannel(canvas)
        task = _start_loop(chart)

        _feed_frame(chart)  # frame 1: ack too late -> dropped
        await asyncio.sleep(0.15)
        first_recovered = chart.img_count == 1

        _feed_frame(chart)  # frame 2: normal ack, must apply fast
        await asyncio.sleep(0.1)
        second_applied = chart.img_count == 2

        await asyncio.sleep(0.15)  # let the late ack land: must no-op
        task.cancel()
        return first_recovered, second_applied, len(canvas._pending_acks)

    first_recovered, second_applied, pending = asyncio.run(scenario())
    assert first_recovered, "timeout must unpark the loop (frame dropped)"
    assert second_applied, "later frames must ack against their own futures"
    assert pending == 0
