import io
import re
import xml.etree.ElementTree as ET
from typing import Any, Optional, Union

from flet.core import alignment
from flet.core.animation import AnimationValue
from flet.core.badge import BadgeValue
from flet.core.container import Container
from flet.core.control import OptionalNumber
from flet.core.image import Image
from flet.core.ref import Ref
from flet.core.tooltip import TooltipValue
from flet.core.types import (
    ImageFit,
    OffsetValue,
    OptionalControlEventCallable,
    ResponsiveNumber,
    RotateValue,
    ScaleValue,
)

try:
    from matplotlib.figure import Figure
except ImportError:
    raise Exception(
        'Install "matplotlib" Python package to use MatplotlibChart control.'
    )


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

    def __init__(
        self,
        figure: Optional[Figure] = None,
        isolated: bool = False,
        original_size: bool = False,
        transparent: bool = False,
        #
        # ConstrainedControl
        #
        ref: Optional[Ref] = None,
        key: Optional[str] = None,
        expand: Union[None, bool, int] = None,
        expand_loose: Optional[bool] = None,
        col: Optional[ResponsiveNumber] = None,
        opacity: OptionalNumber = None,
        rotate: Optional[RotateValue] = None,
        scale: Optional[ScaleValue] = None,
        offset: Optional[OffsetValue] = None,
        aspect_ratio: OptionalNumber = None,
        animate_opacity: Optional[AnimationValue] = None,
        animate_size: Optional[AnimationValue] = None,
        animate_position: Optional[AnimationValue] = None,
        animate_rotation: Optional[AnimationValue] = None,
        animate_scale: Optional[AnimationValue] = None,
        animate_offset: Optional[AnimationValue] = None,
        on_animation_end: OptionalControlEventCallable = None,
        tooltip: Optional[TooltipValue] = None,
        badge: Optional[BadgeValue] = None,
        visible: Optional[bool] = None,
        disabled: Optional[bool] = None,
        data: Any = None,
    ):
        Container.__init__(
            self,
            ref=ref,
            key=key,
            expand=expand,
            expand_loose=expand_loose,
            col=col,
            opacity=opacity,
            rotate=rotate,
            scale=scale,
            offset=offset,
            aspect_ratio=aspect_ratio,
            animate_opacity=animate_opacity,
            animate_size=animate_size,
            animate_position=animate_position,
            animate_rotation=animate_rotation,
            animate_scale=animate_scale,
            animate_offset=animate_offset,
            on_animation_end=on_animation_end,
            tooltip=tooltip,
            badge=badge,
            visible=visible,
            disabled=disabled,
            data=data,
        )

        self.figure = figure
        self.isolated = isolated
        self.original_size = original_size
        self.transparent = transparent

    def is_isolated(self):
        return self.__isolated

    def build(self):
        self.alignment = alignment.center
        self.__img = Image(fit=ImageFit.FILL)
        self.content = self.__img

    def before_update(self):
        super().before_update()
        if self.__figure is not None:
            s = io.StringIO()
            self.__figure.savefig(s, format="svg", transparent=self.__transparent)
            svg = s.getvalue()

            if not self.__original_size:
                root = ET.fromstring(svg)
                w = float(re.findall(r"\d+", root.attrib["width"])[0])
                h = float(re.findall(r"\d+", root.attrib["height"])[0])
                self.__img.aspect_ratio = w / h
            self.__img.src = svg

    # original_size
    @property
    def original_size(self):
        return self.__original_size

    @original_size.setter
    def original_size(self, value):
        self.__original_size = value

    # isolated
    @property
    def isolated(self):
        return self.__isolated

    @isolated.setter
    def isolated(self, value):
        self.__isolated = value

    # figure
    @property
    def figure(self):
        return self.__figure

    @figure.setter
    def figure(self, value):
        self.__figure = value

    # transparent
    @property
    def transparent(self) -> bool:
        return self.__transparent

    @transparent.setter
    def transparent(self, value: bool):
        self.__transparent = value
