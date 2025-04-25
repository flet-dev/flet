import io
import re
import xml.etree.ElementTree as ET
from dataclasses import field

from flet.controls.alignment import Alignment
from flet.controls.base_control import control
from flet.controls.box import BoxFit
from flet.controls.core.image import Image
from flet.controls.material.container import Container

try:
    from matplotlib.figure import Figure
except ImportError:
    raise Exception(
        'Install "matplotlib" Python package to use MatplotlibChart control.'
    )
__all__ = ["MatplotlibChart"]


@control
class MatplotlibChart(Container):
    """
    Displays Matplotlib(https://matplotlib.org/) chart.

    Example:
    ```
    import matplotlib
    import matplotlib.pyplot as plt

    import flet as ft
    from flet.core.matplotlib_chart import MatplotlibChart

    matplotlib.use("svg")


    def main(page: ft.Page):

        fig, ax = plt.subplots()

        fruits = ["apple", "blueberry", "cherry", "orange"]
        counts = [40, 100, 30, 55]
        bar_labels = ["red", "blue", "_red", "orange"]
        bar_colors = ["tab:red", "tab:blue", "tab:red", "tab:orange"]

        ax.bar(fruits, counts, label=bar_labels, color=bar_colors)

        ax.set_ylabel("fruit supply")
        ax.set_title("Fruit supply by kind and color")
        ax.legend(title="Fruit color")

        page.add(MatplotlibChart(fig, expand=True))


    ft.app(target=main)
    ```

    -----

    Online docs: https://flet.dev/docs/controls/matplotlibchart
    """

    figure: Figure = field(metadata={"skip": True})
    original_size: bool = False
    transparent: bool = False

    def init(self):
        self.alignment = Alignment.center()
        self.__img = Image(fit=BoxFit.FILL)
        self.content = self.__img

    def before_update(self):
        super().before_update()
        if self.figure is not None:
            s = io.StringIO()
            self.figure.savefig(s, format="svg", transparent=self.transparent)
            svg = s.getvalue()

            if not self.original_size:
                root = ET.fromstring(svg)
                w = float(re.findall(r"\d+", root.attrib["width"])[0])
                h = float(re.findall(r"\d+", root.attrib["height"])[0])
                self.__img.aspect_ratio = w / h
            self.__img.src = svg
