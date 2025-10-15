from dataclasses import field
from typing import Any, Optional

import flet as ft
import flet_charts

_MATPLOTLIB_IMPORT_ERROR: Optional[ImportError] = None

try:
    from matplotlib.figure import Figure  # type: ignore
except ImportError as e:  # pragma: no cover - depends on optional dependency
    Figure = Any  # type: ignore[assignment]
    _MATPLOTLIB_IMPORT_ERROR = e

_download_formats = [
    "eps",
    "jpeg",
    "pgf",
    "pdf",
    "png",
    "ps",
    "raw",
    "svg",
    "tif",
    "webp",
]


def _require_matplotlib() -> None:
    if _MATPLOTLIB_IMPORT_ERROR is not None:
        raise ModuleNotFoundError(
            'Install "matplotlib" Python package to use MatplotlibChart control.'
        ) from _MATPLOTLIB_IMPORT_ERROR


@ft.control(kw_only=True, isolated=True)
class MatplotlibChartWithToolbar(ft.Column):
    figure: Figure = field(metadata={"skip": True})
    """
    Matplotlib figure to draw - an instance of
    [`matplotlib.figure.Figure`](https://matplotlib.org/stable/api/_as_gen/matplotlib.figure.Figure.html#matplotlib.figure.Figure).
    """

    def build(self):
        _require_matplotlib()
        self.mpl = flet_charts.MatplotlibChart(
            figure=self.figure,
            expand=True,
            on_message=self.on_message,
            on_toolbar_buttons_update=self.on_toolbar_update,
        )
        self.home_btn = ft.IconButton(ft.Icons.HOME, on_click=lambda: self.mpl.home())
        self.back_btn = ft.IconButton(
            ft.Icons.ARROW_BACK_ROUNDED, on_click=lambda: self.mpl.back()
        )
        self.fwd_btn = ft.IconButton(
            ft.Icons.ARROW_FORWARD_ROUNDED, on_click=lambda: self.mpl.forward()
        )
        self.pan_btn = ft.IconButton(
            ft.Icons.OPEN_WITH,
            selected_icon=ft.Icons.OPEN_WITH,
            selected_icon_color=ft.Colors.AMBER_800,
            on_click=self.pan_click,
        )
        self.zoom_btn = ft.IconButton(
            ft.Icons.ZOOM_IN,
            selected_icon=ft.Icons.ZOOM_IN,
            selected_icon_color=ft.Colors.AMBER_800,
            on_click=self.zoom_click,
        )
        self.download_btn = ft.IconButton(
            ft.Icons.DOWNLOAD, on_click=self.download_click
        )
        self.download_fmt = ft.Dropdown(
            value="png",
            options=[ft.DropdownOption(fmt) for fmt in _download_formats],
        )
        self.msg = ft.Text()
        self.controls = [
            ft.Row(
                controls=[
                    self.home_btn,
                    self.back_btn,
                    self.fwd_btn,
                    self.pan_btn,
                    self.zoom_btn,
                    self.download_btn,
                    self.download_fmt,
                    self.msg,
                ]
            ),
            self.mpl,
        ]
        if not self.expand:
            if not self.height:
                self.height = self.figure.bbox.height
            if not self.width:
                self.width = self.figure.bbox.width

    def on_message(self, e: flet_charts.MatplotlibChartMessageEvent):
        self.msg.value = e.message
        self.msg.update()

    def on_toolbar_update(
        self, e: flet_charts.MatplotlibChartToolbarButtonsUpdateEvent
    ):
        self.back_btn.disabled = not e.back_enabled
        self.fwd_btn.disabled = not e.forward_enabled
        self.update()

    def pan_click(self):
        self.mpl.pan()
        self.pan_btn.selected = not self.pan_btn.selected
        self.zoom_btn.selected = False

    def zoom_click(self):
        self.mpl.zoom()
        self.pan_btn.selected = False
        self.zoom_btn.selected = not self.zoom_btn.selected

    async def download_click(self):
        fmt = self.download_fmt.value
        buffer = self.mpl.download(fmt)
        title = self.figure.canvas.manager.get_window_title()
        await ft.FilePicker().save_file(file_name=f"{title}.{fmt}", src_bytes=buffer)
