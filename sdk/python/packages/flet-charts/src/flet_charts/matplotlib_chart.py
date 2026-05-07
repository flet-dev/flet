import asyncio
import logging
import sys
import threading
from dataclasses import dataclass, field
from io import BytesIO
from typing import Any, Optional

import flet as ft
from flet_charts.matplotlib_chart_canvas import (
    MatplotlibChartCanvas,
    MatplotlibChartCanvasResizeEvent,
)

# Pyodide / WASM has no real threads — `asyncio.to_thread` runs synchronously
# on the same thread there, providing no benefit. Fall back to a same-loop
# render path on those platforms.
_HAS_THREADS = sys.platform != "emscripten"

_MATPLOTLIB_IMPORT_ERROR: Optional[ImportError] = None

try:
    import matplotlib  # type: ignore[import]
    from matplotlib.figure import Figure  # type: ignore[import]
except ImportError as e:  # pragma: no cover - depends on optional dependency
    matplotlib = None  # type: ignore[assignment]
    Figure = Any  # type: ignore[assignment]
    _MATPLOTLIB_IMPORT_ERROR = e
else:
    matplotlib.use("module://flet_charts.matplotlib_backends.backend_flet_agg")

__all__ = [
    "MatplotlibChart",
    "MatplotlibChartMessageEvent",
    "MatplotlibChartToolbarButtonsUpdateEvent",
]

logger = logging.getLogger("flet-charts.matplotlib")

figure_cursors = {
    "default": None,
    "pointer": ft.MouseCursor.CLICK,
    "crosshair": ft.MouseCursor.PRECISE,
    "move": ft.MouseCursor.MOVE,
    "wait": ft.MouseCursor.WAIT,
    "ew-resize": ft.MouseCursor.RESIZE_LEFT_RIGHT,
    "ns-resize": ft.MouseCursor.RESIZE_UP_DOWN,
}


def _require_matplotlib() -> None:
    """
    Ensure optional matplotlib dependency is available.

    Raises:
        ModuleNotFoundError: If `matplotlib` is not installed.
    """

    if matplotlib is None:
        raise ModuleNotFoundError(
            'Install "matplotlib" Python package to use MatplotlibChart control.'
        ) from _MATPLOTLIB_IMPORT_ERROR


@dataclass
class MatplotlibChartMessageEvent(ft.Event["MatplotlibChart"]):
    """
    Event carrying status text produced by the Matplotlib backend.
    """

    message: str
    """
    Message text.
    """


@dataclass
class MatplotlibChartToolbarButtonsUpdateEvent(ft.Event["MatplotlibChart"]):
    """
    Event describing enabled/disabled state changes for toolbar navigation buttons.
    """

    back_enabled: bool
    """
    Whether Back button is enabled or not.
    """
    forward_enabled: bool
    """
    Whether Forward button is enabled or not.
    """


@ft.control(kw_only=True, isolated=True)
class MatplotlibChart(ft.GestureDetector):
    """
    Displays a [Matplotlib](https://matplotlib.org/) chart.

    To display a Matplotlib figure with a built-in toolbar UI, use
    :class:`~flet_charts.MatplotlibChartWithToolbar`.

    Warning:
        This control requires the [`matplotlib`](https://matplotlib.org/)
        Python package to be installed.

        See this [installation guide](index.md#installation) for more information.
    """

    figure: Figure = field(metadata={"skip": True})
    """
    Matplotlib figure to draw - an instance of
    [`matplotlib.figure.Figure`](https://matplotlib.org/stable/api/_as_gen/matplotlib.figure.Figure.html#matplotlib.figure.Figure).
    """

    on_message: Optional[ft.EventHandler[MatplotlibChartMessageEvent]] = None
    """
    The event is triggered on figure message update.
    """

    on_toolbar_buttons_update: Optional[
        ft.EventHandler[MatplotlibChartToolbarButtonsUpdateEvent]
    ] = None
    """
    Triggers when toolbar buttons status is updated.
    """

    def init(self):
        _require_matplotlib()
        super().init()

    def build(self):
        self.mouse_cursor = ft.MouseCursor.WAIT
        self.__started = False
        self.__dpr = self.page.media.device_pixel_ratio
        logger.debug(f"DPR: {self.__dpr}")
        self.__image_mode = "full"

        self.mpl_canvas = MatplotlibChartCanvas(
            on_resize=self._on_canvas_resize,
            expand=True,
        )
        # Rubberband (zoom selection) overlay drawn on top of the chart image.
        self._rubberband = ft.Container(
            visible=False,
            border=ft.Border.all(1, ft.Colors.with_opacity(0.6, ft.Colors.GREY)),
        )
        self._stack = ft.Stack(
            controls=[self.mpl_canvas, self._rubberband],
            expand=True,
        )
        self.keyboard_listener = ft.KeyboardListener(
            self._stack,
            autofocus=True,
            on_key_down=self._on_key_down,
            on_key_up=self._on_key_up,
        )
        self.content = self.keyboard_listener
        self.on_enter = self._on_enter
        self.on_hover = self._on_hover
        self.on_exit = self._on_exit
        self.on_pan_start = self._pan_start
        self.on_pan_update = self._pan_update
        self.on_pan_end = self._pan_end
        self.on_right_pan_start = self._right_pan_start
        self.on_right_pan_update = self._right_pan_update
        self.on_right_pan_end = self._right_pan_end
        self.img_count = 1
        self._receive_queue = asyncio.Queue()
        self._main_loop = asyncio.get_event_loop()
        self._width = 0
        self._height = 0
        self._waiting = False
        # Serializes worker-thread renders against main-thread matplotlib
        # operations like `figure.savefig()` (download). matplotlib's
        # print_figure temporarily nulls `canvas.manager` while saving, which
        # would crash an in-flight `canvas.draw()` running in our render
        # thread.
        self._mpl_lock = threading.Lock()

    def _on_key_down(self, e: ft.KeyboardEvent) -> None:
        """
        Handle key-down notifications from keyboard listener.

        Args:
            e: Keyboard event payload.
        """

        logger.debug(f"ON KEY DOWN: {e}")

    def _on_key_up(self, e: ft.KeyboardEvent) -> None:
        """
        Handle key-up notifications from keyboard listener.

        Args:
            e: Keyboard event payload.
        """

        logger.debug(f"ON KEY UP: {e}")

    def _on_enter(self, e: ft.HoverEvent):
        """
        Notify backend that pointer entered the chart area.

        Args:
            e: Hover event containing local pointer coordinates.
        """

        logger.debug(f"_on_enter: {e.local_position.x}, {e.local_position.y}")
        self.send_message(
            {
                "type": "figure_enter",
                "x": e.local_position.x * self.__dpr,
                "y": e.local_position.y * self.__dpr,
                "button": 0,
                "buttons": 0,
                "modifiers": [],
            }
        )

    def _on_hover(self, e: ft.HoverEvent):
        """
        Notify backend about pointer movement over chart area.

        Args:
            e: Hover event containing local pointer coordinates.
        """

        logger.debug(f"_on_hover: {e.local_position.x}, {e.local_position.y}")
        self.send_message(
            {
                "type": "motion_notify",
                "x": e.local_position.x * self.__dpr,
                "y": e.local_position.y * self.__dpr,
                "button": 0,
                "buttons": 0,
                "modifiers": [],
            }
        )

    def _on_exit(self, e: ft.HoverEvent):
        """
        Notify backend that pointer left the chart area.

        Args:
            e: Hover event containing local pointer coordinates.
        """

        logger.debug(f"_on_exit: {e.local_position.x}, {e.local_position.y}")
        self.send_message(
            {
                "type": "figure_leave",
                "x": e.local_position.x * self.__dpr,
                "y": e.local_position.y * self.__dpr,
                "button": 0,
                "buttons": 0,
                "modifiers": [],
            }
        )

    def _pan_start(self, e: ft.DragStartEvent):
        """
        Start primary-button drag interaction.

        Args:
            e: Drag start event containing local pointer coordinates.
        """

        logger.debug(f"_pan_start: {e.local_position.x}, {e.local_position.y}")
        asyncio.create_task(self.keyboard_listener.focus())
        self.send_message(
            {
                "type": "button_press",
                "x": e.local_position.x * self.__dpr,
                "y": e.local_position.y * self.__dpr,
                "button": 0,
                "buttons": 1,
                "modifiers": [],
            }
        )

    def _pan_update(self, e: ft.DragUpdateEvent):
        """
        Continue primary-button drag interaction.

        Args:
            e: Drag update event containing local pointer coordinates.
        """

        logger.debug(f"_pan_update: {e.local_position.x}, {e.local_position.y}")
        self.send_message(
            {
                "type": "motion_notify",
                "x": e.local_position.x * self.__dpr,
                "y": e.local_position.y * self.__dpr,
                "button": 0,
                "buttons": 1,
                "modifiers": [],
            }
        )

    def _pan_end(self, e: ft.DragEndEvent):
        """
        End primary-button drag interaction.

        Args:
            e: Drag end event containing local pointer coordinates.
        """

        logger.debug(f"_pan_end: {e.local_position.x}, {e.local_position.y}")
        self.send_message(
            {
                "type": "button_release",
                "x": e.local_position.x * self.__dpr,
                "y": e.local_position.y * self.__dpr,
                "button": 0,
                "buttons": 0,
                "modifiers": [],
            }
        )

    def _right_pan_start(self, e: ft.PointerEvent):
        """
        Start secondary-button drag interaction.

        Args:
            e: Pointer event containing local pointer coordinates.
        """

        logger.debug(f"_pan_start: {e.local_position.x}, {e.local_position.y}")
        self.send_message(
            {
                "type": "button_press",
                "x": e.local_position.x * self.__dpr,
                "y": e.local_position.y * self.__dpr,
                "button": 2,
                "buttons": 2,
                "modifiers": [],
            }
        )

    def _right_pan_update(self, e: ft.PointerEvent):
        """
        Continue secondary-button drag interaction.

        Args:
            e: Pointer event containing local pointer coordinates.
        """

        logger.debug(f"_pan_update: {e.local_position.x}, {e.local_position.y}")
        self.send_message(
            {
                "type": "motion_notify",
                "x": e.local_position.x * self.__dpr,
                "y": e.local_position.y * self.__dpr,
                "button": 0,
                "buttons": 2,
                "modifiers": [],
            }
        )

    def _right_pan_end(self, e: ft.PointerEvent):
        """
        End secondary-button drag interaction.

        Args:
            e: Pointer event containing local pointer coordinates.
        """

        logger.debug(f"_pan_end: {e.local_position.x}, {e.local_position.y}")
        self.send_message(
            {
                "type": "button_release",
                "x": e.local_position.x * self.__dpr,
                "y": e.local_position.y * self.__dpr,
                "button": 2,
                "buttons": 0,
                "modifiers": [],
            }
        )

    def will_unmount(self):
        """
        Called when the control is about to be removed from the page.
        """
        self.figure.canvas.manager.remove_web_socket(self)

    def home(self):
        """
        Resets the view to the original state.
        """
        logger.debug("home)")
        self.send_message({"type": "toolbar_button", "name": "home"})

    def back(self):
        """
        Goes back to the previous view.
        """
        logger.debug("back()")
        self.send_message({"type": "toolbar_button", "name": "back"})

    def forward(self):
        """
        Goes forward to the next view.
        """
        logger.debug("forward)")
        self.send_message({"type": "toolbar_button", "name": "forward"})

    def pan(self):
        """
        Activates the pan tool.
        """
        logger.debug("pan()")
        self.send_message({"type": "toolbar_button", "name": "pan"})

    def zoom(self):
        """
        Activates the zoom tool.
        """
        logger.debug("zoom()")
        self.send_message({"type": "toolbar_button", "name": "zoom"})

    def download(self, format) -> bytes:
        """
        Downloads the current figure in the specified format.
        Args:
            format (str): The format to download the figure in (e.g., 'png',
                'jpg', 'svg', etc.).
        Returns:
            bytes: The figure image in the specified format as a byte array.
        """
        logger.debug(f"Download in format: {format}")
        buff = BytesIO()
        with self._mpl_lock:
            self.figure.savefig(buff, format=format, dpi=self.figure.dpi * self.__dpr)
        return buff.getvalue()

    async def _receive_loop(self):
        """
        Consume backend messages and apply canvas/state updates.

        The loop handles both binary image frames and JSON control messages
        (cursor updates, draw requests, rubber-band overlays, status text, and
        toolbar history state).
        """

        while True:
            is_binary, content = await self._receive_queue.get()

            # Coalesce stale items so interaction stays snappy:
            # - Drop a binary frame if a newer one is queued behind it.
            # - Drop a "draw" request if another is queued — the latest one
            #   will trigger the render with the most up-to-date state.
            # Without this, every pointer event during pan/zoom triggers its
            # own render and the chart visibly "plays back" buffered motion
            # after the user releases the mouse.
            if is_binary:
                if any(it[0] for it in self._receive_queue._queue):
                    continue
            elif (
                isinstance(content, dict)
                and content.get("type") == "draw"
                and any(
                    not it[0]
                    and isinstance(it[1], dict)
                    and it[1].get("type") == "draw"
                    for it in self._receive_queue._queue
                )
            ):
                continue

            if is_binary:
                assert isinstance(content, (bytes, bytearray))
                logger.debug(f"receive_binary({len(content)})")
                is_full = self.__image_mode == "full"
                # Hand the frame to the client widget — full PNG replaces the
                # backbuffer, diff PNG composites onto it. Awaiting naturally
                # rate-limits this loop to the client's processing speed and
                # yields the asyncio loop for incoming events.
                if is_full:
                    await self.mpl_canvas.apply_full(bytes(content))
                else:
                    await self.mpl_canvas.apply_diff(bytes(content))
                self.img_count += 1
                self._waiting = False
            else:
                logger.debug(f"receive_json({content})")
                if content["type"] == "image_mode":
                    self.__image_mode = content["mode"]
                elif content["type"] == "cursor":
                    self.mouse_cursor = figure_cursors[content["cursor"]]
                    self.update()
                elif content["type"] == "draw" and not self._waiting:
                    self._waiting = True
                    if _HAS_THREADS:
                        # Native runtime: render in a worker thread so the
                        # asyncio loop stays free for input events. handle_draw
                        # ends up in Agg/PIL C code that releases the GIL, so
                        # threading is effective. _waiting + the queue-dedupe
                        # above ensure only one render is ever in flight.
                        # The lock prevents overlap with main-thread savefig.
                        asyncio.create_task(asyncio.to_thread(self._draw_locked))
                    else:
                        # Pyodide / WASM: no real threads available. Render
                        # synchronously on the loop. Yield first so any
                        # backed-up pointer events can update matplotlib state
                        # before the (blocking) render runs.
                        for _ in range(10):
                            await asyncio.sleep(0)
                        self.send_message({"type": "draw"})
                elif content["type"] == "rubberband":
                    if (
                        content["x0"] != -1
                        and content["y0"] != -1
                        and content["x1"] != -1
                        and content["y1"] != -1
                    ):
                        x0 = content["x0"] / self.__dpr
                        y0 = self._height - content["y0"] / self.__dpr
                        x1 = content["x1"] / self.__dpr
                        y1 = self._height - content["y1"] / self.__dpr
                        self._rubberband.left = min(x0, x1)
                        self._rubberband.top = min(y0, y1)
                        self._rubberband.width = abs(x1 - x0)
                        self._rubberband.height = abs(y1 - y0)
                        self._rubberband.visible = True
                    else:
                        self._rubberband.visible = False
                    self._rubberband.update()
                elif content["type"] == "resize":
                    self.send_message({"type": "refresh"})
                elif content["type"] == "message":
                    await self._trigger_event(
                        "message", {"message": content["message"]}
                    )
                elif content["type"] == "history_buttons":
                    await self._trigger_event(
                        "toolbar_buttons_update",
                        {
                            "back_enabled": content["Back"],
                            "forward_enabled": content["Forward"],
                        },
                    )

    def send_message(self, message):
        """Sends a message to the figure's canvas manager."""
        logger.debug(f"send_message({message})")
        manager = self.figure.canvas.manager
        if manager is not None:
            manager.handle_json(message)

    def _draw_locked(self):
        """Worker-thread entry point for triggering a render.

        Holds `_mpl_lock` for the duration of the synchronous draw so it
        can't overlap with main-thread `figure.savefig()`, which temporarily
        nulls `canvas.manager` and would crash an in-flight render.
        """
        with self._mpl_lock:
            self.send_message({"type": "draw"})

    def send_json(self, content):
        """Sends a JSON message to the front end."""
        logger.debug(f"send_json: {content}")
        self._main_loop.call_soon_threadsafe(
            lambda: self._receive_queue.put_nowait((False, content))
        )

    def send_binary(self, blob):
        """Sends a binary message to the front end."""
        self._main_loop.call_soon_threadsafe(
            lambda: self._receive_queue.put_nowait((True, blob))
        )

    async def _on_canvas_resize(self, e: MatplotlibChartCanvasResizeEvent):
        """
        Handle canvas resize and initialize backend session on first resize.

        On first call, starts receive loop, registers this control with figure
        manager, and requests initial image state. On every call, stores current
        dimensions and sends a resize message to backend.

        Args:
            e: Canvas resize event.
        """

        logger.debug(f"on_canvas_resize: {e.width}, {e.height}")

        if not self.__started:
            self.__started = True
            asyncio.create_task(self._receive_loop())
            self.figure.canvas.manager.add_web_socket(self)
            self.send_message({"type": "send_image_mode"})
            self.send_message(
                {"type": "set_device_pixel_ratio", "device_pixel_ratio": self.__dpr}
            )
            self.send_message({"type": "refresh"})
        self._width = e.width
        self._height = e.height
        self.send_message(
            {"type": "resize", "width": self._width, "height": self._height}
        )
