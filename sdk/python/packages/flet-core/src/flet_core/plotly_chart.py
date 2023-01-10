import io
import re
import xml.etree.ElementTree as ET
from typing import Any, Optional, Union

from flet_core import alignment
from flet_core.container import Container
from flet_core.control import OptionalNumber
from flet_core.image import Image
from flet_core.ref import Ref
from flet_core.types import (
    AnimationValue,
    OffsetValue,
    ResponsiveNumber,
    RotateValue,
    ScaleValue,
)

try:
    from plotly.graph_objects import Figure
except ImportError:
    raise Exception('Install "plotly" Python package to use PlotlyChart control.')


class PlotlyChart(Container):
    """
    Displays Plotly(https://plotly.com/python/) chart.

    Example:
    ```
    import plotly.express as px

    import flet as ft
    from flet_core.plotly_chart import PlotlyChart

    def main(page: ft.Page):

        df = px.data.gapminder().query("continent=='Oceania'")
        fig = px.line(df, x="year", y="lifeExp", color="country")

        page.add(PlotlyChart(fig, expand=True))

    ft.app(target=main)
    ```

    -----

    Online docs: https://flet.dev/docs/controls/plotlychart
    """

    def __init__(
        self,
        figure: Optional[Figure] = None,
        ref: Optional[Ref] = None,
        expand: Union[None, bool, int] = None,
        col: Optional[ResponsiveNumber] = None,
        opacity: OptionalNumber = None,
        rotate: RotateValue = None,
        scale: ScaleValue = None,
        offset: OffsetValue = None,
        aspect_ratio: OptionalNumber = None,
        animate_opacity: AnimationValue = None,
        animate_size: AnimationValue = None,
        animate_position: AnimationValue = None,
        animate_rotation: AnimationValue = None,
        animate_scale: AnimationValue = None,
        animate_offset: AnimationValue = None,
        on_animation_end=None,
        tooltip: Optional[str] = None,
        visible: Optional[bool] = None,
        disabled: Optional[bool] = None,
        data: Any = None,
        #
        # Specific
        #
        isolated: bool = False,
        original_size: bool = False,
    ):

        Container.__init__(
            self,
            ref=ref,
            expand=expand,
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
            visible=visible,
            disabled=disabled,
            data=data,
        )

        self.figure = figure
        self.isolated = isolated
        self.original_size = original_size

    def _is_isolated(self):
        return self.__isolated

    def _build(self):
        self.alignment = alignment.center
        self.__img = Image(fit="fill")
        self.content = self.__img

    def _before_build_command(self):
        super()._before_build_command()
        if self.__figure is not None:
            svg = self.__figure.to_image(format="svg").decode("utf-8")

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

    # maintain_aspect_ratio
    @property
    def maintain_aspect_ratio(self) -> bool:
        return self.__maintain_aspect_ratio

    @maintain_aspect_ratio.setter
    def maintain_aspect_ratio(self, value: bool):
        self.__maintain_aspect_ratio = value
