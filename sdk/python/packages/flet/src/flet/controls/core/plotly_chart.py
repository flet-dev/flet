import re
import xml.etree.ElementTree as ET
from dataclasses import field
from typing import Any, Optional, Union

from flet.controls.alignment import Alignment
from flet.controls.animation import AnimationValue
from flet.controls.base_control import control
from flet.controls.box import BoxFit
from flet.controls.core.image import Image
from flet.controls.material.badge import BadgeValue
from flet.controls.material.container import Container
from flet.controls.material.tooltip import TooltipValue
from flet.controls.ref import Ref
from flet.controls.transform import OffsetValue, RotateValue, ScaleValue
from flet.controls.types import (
    ImageFit,
    OptionalControlEventCallable,
    OptionalNumber,
    ResponsiveNumber,
)

try:
    from plotly.graph_objects import Figure
except ImportError:
    raise Exception('Install "plotly" Python package to use PlotlyChart control.')

__all__ = ["PlotlyChart"]


@control
class PlotlyChart(Container):
    """
    Displays Plotly(https://plotly.com/python/) chart.

    Example:
    ```
    import plotly.express as px

    import flet as ft
    from flet.core.plotly_chart import PlotlyChart

    def main(page: ft.Page):

        df = px.data.gapminder().query("continent=='Oceania'")
        fig = px.line(df, x="year", y="lifeExp", color="country")

        page.add(PlotlyChart(fig, expand=True))

    ft.app(target=main)
    ```

    -----

    Online docs: https://flet.dev/docs/controls/plotlychart
    """

    figure: Figure = field(metadata={"skip": True})
    original_size: bool = False

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
