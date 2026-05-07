import asyncio

from matplotlib import _api
from matplotlib.backends import backend_webagg_core


class TimerFletAsyncio(backend_webagg_core.TimerAsyncio):
    """Asyncio timer that's safe to start from a worker thread.

    Matplotlib's stock `TimerAsyncio._timer_start` calls
    `asyncio.ensure_future`, which requires the calling thread to have a
    current event loop. Flet's matplotlib chart runs `canvas.draw()` in a
    worker thread to keep the asyncio loop free for input events; that
    thread has no event loop. We capture the loop at construction time and
    schedule via `run_coroutine_threadsafe` when invoked from off-loop.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        try:
            self._loop = asyncio.get_running_loop()
        except RuntimeError:
            self._loop = asyncio.get_event_loop_policy().get_event_loop()

    def _timer_start(self):
        self._timer_stop()
        coro = self._timer_task(max(self.interval / 1_000.0, 1e-6))
        try:
            current = asyncio.get_running_loop()
        except RuntimeError:
            current = None
        if current is self._loop:
            self._task = self._loop.create_task(coro)
        else:
            self._task = asyncio.run_coroutine_threadsafe(coro, self._loop)


class FigureCanvasFletAgg(backend_webagg_core.FigureCanvasWebAggCore):
    """Canvas implementation used to render Matplotlib figures in Flet."""

    manager_class = _api.classproperty(lambda cls: FigureManagerFletAgg)
    supports_blit = False
    _timer_cls = TimerFletAsyncio


class FigureManagerFletAgg(backend_webagg_core.FigureManagerWebAgg):
    """Figure manager binding Matplotlib WebAgg tooling to Flet transport."""

    _toolbar2_class = backend_webagg_core.NavigationToolbar2WebAgg


FigureCanvas = FigureCanvasFletAgg
FigureManager = FigureManagerFletAgg
interactive = True
