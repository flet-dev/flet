import io
import re
import xml.etree.ElementTree as ET
from typing import Any, Optional, Union
import math
import base64
from io import BytesIO
import requests
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

import numpy as np

try:
    from matplotlib.figure import Figure
except ImportError:
    raise Exception(
        'Install "matplotlib" Python package to use MatplotlibChart control.'
    )
try:
    from PIL import Image
except ImportError:
    raise Exception(
        'Install "pillow" Python package to use FletMap control.'
    )


class FletMap(Container):
    def __init__(
        self,
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
        latitude: float = 0.0,
        longtitude: float = 0.0,
        delta_lat: float = 0.0,
        delta_long: float = 0.0,
        zoom: float = 0.0,
        isolated: bool = False,
        original_size: bool = False,
        transparent: bool = False,
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

        self.latitude = latitude
        self.longtitude = longtitude
        self.delta_lat = delta_lat
        self.delta_long = delta_long
        self.zoom = zoom
        self.isolated = isolated
        self.original_size = original_size
        self.transparent = transparent
        self.__figure=Figure()
        

    def _is_isolated(self):
        return self.__isolated

    def _build(self):
        self.alignment = alignment.center
        self.__img = Image(fit="fill")
        self.content = self.__img

    def _get_image_cluster(self):
        headers = {"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36"}
        smurl = r"http://a.tile.openstreetmap.org/{0}/{1}/{2}.png"
        xmin, ymax =self.deg2num(self.latitude, self.longtitude, self.zoom)
        xmax, ymin =self.deg2num(self.latitude + self.delta_lat, self.longtitude + self.delta_long, self.zoom)
    
        cluster = Image.new('RGB',((xmax-xmin+1)*256-1,(ymax-ymin+1)*256-1) ) 
        for xtile in range(xmin, xmax+1):
            for ytile in range(ymin,  ymax+1):
                try:
                    imgurl = smurl.format(self.zoom, xtile, ytile)
                    print("Opening: " + imgurl)
                    imgstr = requests.get(imgurl, headers=headers)
                    tile = Image.open(BytesIO(imgstr.content))
                    cluster.paste(tile, box = ((xtile-xmin)*256 ,  (ytile-ymin)*255))
                except: 
                    print("Couldn't download image")
                    tile = None
    
        return cluster

    def _before_build_command(self):
        super()._before_build_command()
        cluster = self._get_image_cluster()
        # s = io.StringIO()
        # self.__figure.savefig(
        #     s, format="svg", transparent=self.__transparent)
        # svg = s.getvalue()

        # if not self.__original_size:
        #     root = ET.fromstring(svg)
        #     w = float(re.findall(r"\d+", root.attrib["width"])[0])
        #     h = float(re.findall(r"\d+", root.attrib["height"])[0])
        #     self.__img.aspect_ratio = w / h
        self.__img.src_base64 = base64.b64encode(np.asarray(cluster))

    @staticmethod
    def deg2num(self, lat_deg, lon_deg, zoom):
        lat_rad = math.radians(lat_deg)
        n = 2.0 ** zoom
        xtile = int((lon_deg + 180.0) / 360.0 * n)
        ytile = int((1.0 - math.log(math.tan(lat_rad) +
                    (1 / math.cos(lat_rad))) / math.pi) / 2.0 * n)
        return (xtile, ytile)

    @staticmethod
    def num2deg(self, xtile, ytile, zoom):
        n = 2.0 ** zoom
        lon_deg = xtile / n * 360.0 - 180.0
        lat_rad = math.atan(math.sinh(math.pi * (1 - 2 * ytile / n)))
        lat_deg = math.degrees(lat_rad)
        return (lat_deg, lon_deg)

    # zoom
    @property
    def zoom(self):
        return self.__zoom

    @zoom.setter
    def zoom(self, value):
        self.__zoom = value

    # delta_long
    @property
    def delta_long(self):
        return self.__delta_long

    @delta_long.setter
    def latitude(self, value):
        self.__delta_long = value

    # delta_lat
    @property
    def delta_lat(self):
        return self.__delta_lat

    @delta_lat.setter
    def delta_lat(self, value):
        self.__delta_lat = value

    # latitude
    @property
    def latitude(self):
        return self.__latitude

    @latitude.setter
    def latitude(self, value):
        self.__latitude = value

    # longtitude
    @property
    def longtitude(self):
        return self.__longtitude

    @longtitude.setter
    def latitude(self, value):
        self.__longtitude = value

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

    # maintain_aspect_ratio
    @property
    def maintain_aspect_ratio(self) -> bool:
        return self.__maintain_aspect_ratio

    @maintain_aspect_ratio.setter
    def maintain_aspect_ratio(self, value: bool):
        self.__maintain_aspect_ratio = value

    # transparent
    @property
    def transparent(self) -> bool:
        return self.__transparent

    @transparent.setter
    def transparent(self, value: bool):
        self.__transparent = value




