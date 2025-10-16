import asyncio
import logging
from dataclasses import dataclass, field
from io import BytesIO
from typing import Any, Optional

import flet as ft
import flet.canvas as fc

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
    if matplotlib is None:
        raise ModuleNotFoundError(
            'Install "matplotlib" Python package to use MatplotlibChart control.'
        ) from _MATPLOTLIB_IMPORT_ERROR


@dataclass
class MatplotlibChartMessageEvent(ft.Event["MatplotlibChart"]):
    message: str
    """
    Message text.
    """


@dataclass
class MatplotlibChartToolbarButtonsUpdateEvent(ft.Event["MatplotlibChart"]):
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

        self.canvas = fc.Canvas(
            # resize_interval=10,
            on_resize=self._on_canvas_resize,
            expand=True,
        )
        self.keyboard_listener = ft.KeyboardListener(
            self.canvas,
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

    def _on_key_down(self, e):
        logger.debug(f"ON KEY DOWN: {e}")

    def _on_key_up(self, e):
        logger.debug(f"ON KEY UP: {e}")

    def _on_enter(self, e: ft.HoverEvent):
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
        self.figure.savefig(buff, format=format, dpi=self.figure.dpi * self.__dpr)
        return buff.getvalue()

    async def _receive_loop(self):
        while True:
            is_binary, content = await self._receive_queue.get()
            if is_binary:
                logger.debug(f"receive_binary({len(content)})")
                if self.__image_mode == "full":
                    await self.canvas.clear_capture()

                self.canvas.shapes = [
                    fc.Image(
                        src_bytes=content,
                        x=0,
                        y=0,
                        width=self.figure.bbox.size[0] / self.__dpr,
                        height=self.figure.bbox.size[1] / self.__dpr,
                    )
                ]
                ft.context.disable_auto_update()
                self.canvas.update()
                await self.canvas.capture()
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
                    self.send_message({"type": "draw"})
                elif content["type"] == "rubberband":
                    if len(self.canvas.shapes) == 2:
                        self.canvas.shapes.pop()
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
                        self.canvas.shapes.append(
                            fc.Rect(
                                x=x0,
                                y=y0,
                                width=x1 - x0,
                                height=y1 - y0,
                                paint=ft.Paint(
                                    stroke_width=1, style=ft.PaintingStyle.STROKE
                                ),
                            )
                        )
                    self.canvas.update()
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

    async def _on_canvas_resize(self, e: fc.CanvasResizeEvent):
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
