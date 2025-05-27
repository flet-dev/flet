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
except ImportError as e:
    raise Exception(
        'Install "matplotlib" Python package to use MatplotlibChart control.'
    ) from e
__all__ = ["MatplotlibChart"]


@control(kw_only=True)
class MatplotlibChart(Container):
    """
    Displays Matplotlib(https://matplotlib.org/) chart.

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
