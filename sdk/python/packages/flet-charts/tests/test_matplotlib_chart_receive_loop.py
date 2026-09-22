"""Fault isolation in ``MatplotlibChart._receive_loop``.

The loop is the sole consumer of ``_receive_queue``, and it does more than
shuffle bytes: ``send_message`` hands a "draw" straight to Matplotlib's
canvas manager, so the figure renders *inside* this task. Any render error
— a bad artist, a font that fails to rasterize, a degenerate 3D view —
therefore surfaces here. Unguarded, it would end the loop: no frame would
ever be applied again, the chart would freeze with no visible error, and
the traceback would only appear much later as asyncio's "Task exception was
never retrieved" when the dead task is garbage-collected.

These tests drive the real ``_receive_loop`` with the failures injected at
the two points that can raise — the canvas apply, and the synchronous
Matplotlib render behind ``send_message``.
"""

import asyncio
import types

from flet_charts.matplotlib_chart import MatplotlibChart


def _make_chart_standin():
    """Minimal ``self`` for the real ``_receive_loop``: the queue/state
    attrs ``build()`` would create, plus a fake canvas and ``send_message``
    so a failure can be injected at either point."""
    chart = types.SimpleNamespace()
    chart._receive_queue = asyncio.Queue()
    chart._waiting = False
    chart.img_count = 0
    chart._MatplotlibChart__image_mode = "full"
    chart.applied = []
    chart.sent = []

    async def apply_raw_packet(packet):
        if packet == b"boom":
            raise RuntimeError("FT_Render_Glyph failed: raster overflow")
        chart.applied.append(packet)

    chart.mpl_canvas = types.SimpleNamespace(apply_raw_packet=apply_raw_packet)

    def send_message(message):
        chart.sent.append(message)
        if chart.render_fails:
            raise RuntimeError("FT_Render_Glyph failed: raster overflow")

    chart.send_message = send_message
    chart.render_fails = False
    chart._handle_message = types.MethodType(MatplotlibChart._handle_message, chart)
    return chart


def _feed_frame(chart, payload=b"frame"):
    chart._receive_queue.put_nowait((True, ("raw", payload)))


async def _drain(chart):
    """Run the real loop long enough to consume the queue, then stop it.

    Returns whether the loop was still alive at that point — a loop killed
    by an exception is `done()` before anything cancels it.
    """
    task = asyncio.create_task(MatplotlibChart._receive_loop(chart))
    await asyncio.sleep(0.05)
    alive = not task.done()
    task.cancel()
    return alive


def test_failing_render_does_not_kill_the_loop():
    """A "draw" whose render raises must not stop frames that follow."""

    async def scenario():
        chart = _make_chart_standin()
        chart.render_fails = True
        chart._receive_queue.put_nowait((False, {"type": "draw"}))
        chart.render_fails = False
        _feed_frame(chart)
        alive = await _drain(chart)
        return chart.applied, chart._waiting, alive

    applied, waiting, alive = asyncio.run(scenario())
    assert applied == [b"frame"], "loop must keep applying frames after a render error"
    assert not waiting, "a draw that raised must not leave the draw gate latched"
    assert alive, "the loop task must still be running"


def test_failing_frame_apply_does_not_kill_the_loop():
    """An error while applying one frame must not lose the next one."""

    async def scenario():
        chart = _make_chart_standin()
        _feed_frame(chart, b"boom")
        _feed_frame(chart, b"good")
        await _drain(chart)
        return chart.applied

    assert asyncio.run(scenario()) == [b"good"]


def test_draw_gate_reopens_after_a_render_error():
    """``_waiting`` gates draw requests; a failed draw never produces the
    frame that clears it, so the loop must clear it itself — otherwise no
    further draw is ever requested and the chart stays frozen."""

    async def scenario():
        chart = _make_chart_standin()
        chart.render_fails = True
        chart._receive_queue.put_nowait((False, {"type": "draw"}))
        await _drain(chart)
        first = list(chart.sent)

        chart.render_fails = False
        chart._receive_queue.put_nowait((False, {"type": "draw"}))
        await _drain(chart)
        return first, chart.sent

    first, sent = asyncio.run(scenario())
    assert first == [{"type": "draw"}]
    assert sent == [{"type": "draw"}, {"type": "draw"}], (
        "a later draw notification must still reach Matplotlib"
    )
