from typing import Any, Optional, Union, List, Tuple

from flet_core.constrained_control import ConstrainedControl
from flet_core.control import OptionalNumber
from flet_core.map.map_configuration import MapConfiguration, MapLatitudeLongitude
from flet_core.map.map_layer import MapLayer
from flet_core.ref import Ref
from flet_core.tooltip import TooltipValue
from flet_core.transform import Offset
from flet_core.types import (
    AnimationValue,
    OffsetValue,
    ResponsiveNumber,
    RotateValue,
    ScaleValue,
    OptionalControlEventCallable,
    Number,
)


class Map(ConstrainedControl):
    """
    Map Control.

    -----

    Online docs: https://flet.dev/docs/controls/map
    """

    def __init__(
        self,
        layers: List[MapLayer],
        configuration: MapConfiguration = MapConfiguration(),
        #
        # ConstrainedControl
        #
        ref: Optional[Ref] = None,
        key: Optional[str] = None,
        width: OptionalNumber = None,
        height: OptionalNumber = None,
        left: OptionalNumber = None,
        top: OptionalNumber = None,
        right: OptionalNumber = None,
        bottom: OptionalNumber = None,
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
        on_animation_end: OptionalControlEventCallable = None,
        tooltip: TooltipValue = None,
        visible: Optional[bool] = None,
        disabled: Optional[bool] = None,
        data: Any = None,
    ):
        ConstrainedControl.__init__(
            self,
            ref=ref,
            key=key,
            width=width,
            height=height,
            left=left,
            top=top,
            right=right,
            bottom=bottom,
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

        self.configuration = configuration
        self.layers = layers

    def move(
        self,
        coordinates: MapLatitudeLongitude,
        zoom: Number,
        offset: Union[Offset, Tuple[Union[Number], Union[Number]]] = Offset(0.0, 0.0),
        wait_timeout: Optional[float] = 5,
    ) -> bool:
        if isinstance(offset, tuple):
            offset = Offset(offset[0], offset[1])
        result = self.invoke_method(
            "move",
            arguments={
                "lat": str(coordinates.latitude),
                "long": str(coordinates.longitude),
                "zoom": str(zoom),
                "ox": str(offset.x),
                "oy": str(offset.y),
            },
            wait_for_result=True,
            wait_timeout=wait_timeout,
        )
        return result == "true"

    def move_and_rotate(
        self,
        coordinates: MapLatitudeLongitude,
        zoom: Number,
        degree: Number,
        wait_timeout: Optional[float] = 5,
    ) -> bool:
        result = self.invoke_method(
            "move_and_rotate",
            arguments={
                "lat": str(coordinates.latitude),
                "long": str(coordinates.longitude),
                "zoom": str(zoom),
                "degree": str(degree),
            },
            wait_for_result=True,
            wait_timeout=wait_timeout,
        )
        return result == "true"

    def rotate_around_point(
        self,
        degree: Number,
        point: Optional[Tuple[Union[Number], Union[Number]]] = None,
        offset: Optional[Union[Offset, Tuple[Union[Number], Union[Number]]]] = None,
        wait_timeout: Optional[float] = 5,
    ) -> bool:
        if isinstance(offset, tuple):
            offset = Offset(offset[0], offset[1])
        result = self.invoke_method(
            "rotate_around_point",
            arguments={
                "degree": str(degree),
                "ox": str(offset.x) if offset else "None",
                "oy": str(offset.y) if offset else "None",
                "px": str(point[0]) if point else "None",
                "py": str(point[1]) if point else "None",
            },
            wait_for_result=True,
            wait_timeout=wait_timeout,
        )
        return result == "true"

    def _get_control_name(self):
        return "map"

    def _get_children(self):
        return self.__layers + [self.__configuration]

    # configuration
    @property
    def configuration(self) -> MapConfiguration:
        return self.__configuration

    @configuration.setter
    def configuration(self, value: MapConfiguration):
        self.__configuration = value

    # layers
    @property
    def layers(self) -> List[MapLayer]:
        return self.__layers

    @layers.setter
    def layers(self, value: List[MapLayer]):
        self.__layers = value
