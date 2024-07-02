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
    ImageFit,
    OptionalEventCallable,
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
        isolated: bool = False,
        original_size: bool = False,
        #
        # ConstrainedControl
        #
        ref: Optional[Ref] = None,
        key: Optional[str] = None,
        expand: Union[None, bool, int] = None,
        expand_loose: Optional[bool] = None,
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
        on_animation_end: OptionalEventCallable = None,
        tooltip: Optional[str] = None,
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
            visible=visible,
            disabled=disabled,
            data=data,
        )

        self.figure = figure
        self.isolated = isolated
        self.original_size = original_size

    def is_isolated(self):
        return self.__isolated

    def build(self):
        self.alignment = alignment.center
        self.__img = Image(fit=ImageFit.FILL)
        self.content = self.__img

    def before_update(self):
        super().before_update()
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
    def original_size(self) -> bool:
        return self.__original_size

    @original_size.setter
    def original_size(self, value: bool):
        self.__original_size = value

    # isolated
    @property
    def isolated(self) -> bool:
        return self.__isolated

    @isolated.setter
    def isolated(self, value: bool):
        self.__isolated = value

    # figure
    @property
    def figure(self) -> Optional[Figure]:
        return self.__figure

    @figure.setter
    def figure(self, value: Optional[Figure]):
        self.__figure = value
