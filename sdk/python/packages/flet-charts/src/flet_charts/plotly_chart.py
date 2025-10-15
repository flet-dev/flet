import re
import xml.etree.ElementTree as ET
from dataclasses import field
from typing import Any, Optional

import flet as ft

_PLOTLY_IMPORT_ERROR: Optional[ImportError] = None

try:
    from plotly.graph_objects import Figure
except ImportError as e:  # pragma: no cover - depends on optional dependency
    Figure = Any  # type: ignore[assignment]
    _PLOTLY_IMPORT_ERROR = e

__all__ = ["PlotlyChart"]


def _require_plotly() -> None:
    if _PLOTLY_IMPORT_ERROR is not None:
        raise ModuleNotFoundError(
            'Install "plotly" Python package to use PlotlyChart control.'
        ) from _PLOTLY_IMPORT_ERROR


@ft.control(kw_only=True)
class PlotlyChart(ft.Container):
    """
    Displays a [Plotly](https://plotly.com/python/) chart.

    Warning:
        This control requires the [`plotly`](https://plotly.com/python/) Python
        package to be installed.

        See this [installation guide](index.md#installation) for more information.
    """

    figure: Figure = field(metadata={"skip": True})
    """
    Plotly figure to draw.

    The value is an instance of [`plotly.graph_objects.Figure`](https://plotly.com/python-api-reference/generated/plotly.graph_objects.Figure.html).
    """

    original_size: bool = False
    """
    Whether to display this chart in original size.

    Set to `False` for it to fit it's configured bounds.
    """

    def init(self):
        _require_plotly()
        self.alignment = ft.Alignment.CENTER
        self.__img = ft.Image(fit=ft.BoxFit.FILL)
        self.content = self.__img

    def before_update(self):
        super().before_update()
        if self.figure is not None:
            svg = self.figure.to_image(format="svg").decode("utf-8")

            if not self.original_size:
                root = ET.fromstring(svg)
                w = float(re.findall(r"\d+", root.attrib["width"])[0])
                h = float(re.findall(r"\d+", root.attrib["height"])[0])
                self.__img.aspect_ratio = w / h
            self.__img.src = svg
