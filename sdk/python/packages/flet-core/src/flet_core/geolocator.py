from enum import Enum
from typing import Any, Optional
from dataclasses import dataclass
from flet_core.control import Control
from flet_core.ref import Ref


class LocationAccuracy(Enum):
    LOWEST = "lowest"
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    BEST = "best"
    BESTFORNAVIGATION = "bestForNavigation"
    REDUCED = "reduced"


@dataclass
class Position:
    latitude: float
    longitude: float
    speed: float
    altitude: float
    timestamp: str


class Geolocator(Control):
    """
    A control that allows you to record audio from your device.

    -----

    Online docs: https://flet.dev/docs/controls/geolocator
    """

    def __init__(
        self,
        # Control
        #
        ref: Optional[Ref] = None,
        data: Any = None,
    ):
        Control.__init__(
            self,
            ref=ref,
            data=data,
        )

    def _get_control_name(self):
        return "geolocator"

    def get_location(
        self,
        location_accuracy: Optional[LocationAccuracy] = LocationAccuracy.BEST,
        wait_timeout: Optional[float] = 25,
    ) -> Position:
        output = self.invoke_method(
            "getLocation",
            {
                "locationAccuracy": (
                    location_accuracy.value
                    if isinstance(location_accuracy, LocationAccuracy)
                    else location_accuracy
                )
            },
            wait_for_result=True,
            wait_timeout=wait_timeout,
        )
        return self.__string2dict(string=output)

    async def get_location_async(
        self,
        location_accuracy: Optional[LocationAccuracy] = LocationAccuracy.BEST,
        wait_timeout: Optional[float] = 25,
    ) -> Position:
        output = await self.invoke_method_async(
            "getLocation",
            {
                "locationAccuracy": (
                    location_accuracy.value
                    if isinstance(location_accuracy, LocationAccuracy)
                    else location_accuracy
                )
            },
            wait_for_result=True,
            wait_timeout=wait_timeout,
        )
        return self.__string2dict(string=output)

    def __string2dict(self, string: str) -> Position:
        if string != "null":
            try:
                for each in string.split(","):
                    temp = each.split(".")
                    if temp[1] != "null":
                        # out[temp[0]] = float(temp[1])
                        if temp[0] == "timestamp":
                            Position.timestamp = temp[1]
                        elif temp[0] == "latitude":
                            Position.latitude = temp[1]
                        elif temp[0] == "longitude":
                            Position.longitude = temp[1]
                        elif temp[0] == "altitude":
                            Position.altitude = temp[1]
                        elif temp[0] == "speed":
                            Position.speed = temp[1]
            except Exception as e:
                print(e, "in __string2dict")
        else:
            Position.timestamp = None
            Position.latitude = None
            Position.longitude = None
            Position.altitude = None
            Position.speed = None
        return Position
