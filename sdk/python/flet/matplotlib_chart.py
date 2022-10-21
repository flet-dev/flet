import io
import re
import xml.etree.ElementTree as ET
from typing import Any, Optional, Union

from beartype import beartype

from flet import alignment
from flet.container import Container
from flet.control import OptionalNumber
from flet.image import Image
from flet.ref import Ref
from flet.types import AnimationValue, OffsetValue, RotateValue, ScaleValue

try:
    from matplotlib.figure import Figure
except ImportError:
    raise Exception(
        'Install "matplotlib" Python package to use MatplotlibChart control.'
    )


class MatplotlibChart(Container):
    def __init__(
        self,
        figure: Optional[Figure] = None,
        ref: Optional[Ref] = None,
        expand: Union[None, bool, int] = None,
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
    ):

        Container.__init__(
            self,
            ref=ref,
            expand=expand,
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

    def _is_isolated(self):
        return True

    def _build(self):
        self.alignment = alignment.center
        self.__img = Image(fit="fill")
        self.content = self.__img

    def _before_build_command(self):
        super()._before_build_command()
        if self.__figure is not None:
            s = io.StringIO()
            self.__figure.savefig(s, format="svg")
            svg = s.getvalue()

            root = ET.fromstring(svg)
            w = float(re.findall(r"\d+", root.attrib["width"])[0])
            h = float(re.findall(r"\d+", root.attrib["height"])[0])
            self.__img.aspect_ratio = w / h
            self.__img.src = svg

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
    @beartype
    def maintain_aspect_ratio(self, value: bool):
        self.__maintain_aspect_ratio = value
