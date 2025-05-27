import re
import xml.etree.ElementTree as ET
from dataclasses import field

from flet.controls.alignment import Alignment
from flet.controls.base_control import control
from flet.controls.box import BoxFit
from flet.controls.core.image import Image
from flet.controls.material.container import Container

try:
    from plotly.graph_objects import Figure
except ImportError as e:
    raise Exception(
        'Install "plotly" Python package to use PlotlyChart control.'
        ) from e

__all__ = ["PlotlyChart"]


@control
class PlotlyChart(Container):
    """
    Displays Plotly(https://plotly.com/python/) chart.

    Online docs: https://flet.dev/docs/controls/plotlychart
    """

    figure: Figure = field(metadata={"skip": True})
    """
    Plotly figure to draw - an instance of `plotly.graph_objects.Figure` class.
    """

    original_size: bool = False
    """
    `True` to display chart in original size.

    `False` (default) to display a chart that fits configured bounds.
    """


    def init(self):
        self.alignment = Alignment.center()
        self.__img = Image(fit=BoxFit.FILL)
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
            print("svg length:", len(svg))
            self.__img.src = svg
