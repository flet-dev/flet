import json
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Optional

from flet_core.control import Control
from flet_core.ref import Ref


class GeolocatorPositionAccuracy(Enum):
    LOWEST = "lowest"
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    BEST = "best"
    BEST_FOR_NAVIGATION = "bestForNavigation"
    REDUCED = "reduced"


class GeolocatorPermissionStatus(Enum):
    DENIED = "denied"
    DENIED_FOREVER = "deniedForever"
    WHILE_IN_USE = "whileInUse"
    ALWAYS = "always"
    UNABLE_TO_DETERMINE = "unableToDetermine"


@dataclass
class GeolocatorPosition:
    latitude: Optional[float] = field(default=None)
    longitude: Optional[float] = field(default=None)
    speed: Optional[float] = field(default=None)
    altitude: Optional[float] = field(default=None)
    timestamp: Optional[float] = field(default=None)
    accuracy: Optional[float] = field(default=None)
    altitude_accuracy: Optional[float] = field(default=None)
    heading: Optional[float] = field(default=None)
    heading_accuracy: Optional[float] = field(default=None)
    speed_accuracy: Optional[float] = field(default=None)
    floor: Optional[int] = field(default=None)
    is_mocked: Optional[bool] = field(default=None)


class Geolocator(Control):
    """
    A control that allows you to fetch GPS data from your device.
    This control is non-visual and should be added to `page.overlay` list


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

    def get_current_position(
        self,
        accuracy: Optional[
            GeolocatorPositionAccuracy
        ] = GeolocatorPositionAccuracy.BEST,
        wait_timeout: Optional[float] = 25,
    ) -> GeolocatorPosition:
        output = self.invoke_method(
            "get_current_position",
            {
                "accuracy": (
                    accuracy.value
                    if isinstance(accuracy, GeolocatorPositionAccuracy)
                    else accuracy
                )
            },
            wait_for_result=True,
            wait_timeout=wait_timeout,
        )
        return (
            GeolocatorPosition(**json.loads(output))
            if output is not None
            else GeolocatorPosition()
        )

    async def get_current_position_async(
        self,
        accuracy: Optional[
            GeolocatorPositionAccuracy
        ] = GeolocatorPositionAccuracy.BEST,
        wait_timeout: Optional[float] = 25,
    ) -> GeolocatorPosition:
        output = await self.invoke_method_async(
            "get_current_position",
            {
                "accuracy": (
                    accuracy.value
                    if isinstance(accuracy, GeolocatorPositionAccuracy)
                    else accuracy
                )
            },
            wait_for_result=True,
            wait_timeout=wait_timeout,
        )
        return (
            GeolocatorPosition(**json.loads(output))
            if output is not None
            else GeolocatorPosition()
        )

    def get_last_known_position(
        self,
        wait_timeout: Optional[float] = 25,
    ) -> GeolocatorPosition:
        assert not self.page.web, "get_last_known_position is not supported on web"
        output = self.invoke_method(
            "get_last_known_position",
            wait_for_result=True,
            wait_timeout=wait_timeout,
        )
        return (
            GeolocatorPosition(**json.loads(output))
            if output is not None
            else GeolocatorPosition()
        )

    async def get_last_known_position_async(
        self,
        wait_timeout: Optional[float] = 25,
    ) -> GeolocatorPosition:
        assert not self.page.web, "get_last_known_position is not supported on web"
        output = await self.invoke_method_async(
            "get_last_known_position",
            wait_for_result=True,
            wait_timeout=wait_timeout,
        )
        return (
            GeolocatorPosition(**json.loads(output))
            if output is not None
            else GeolocatorPosition()
        )

    def get_permission_status(
        self, wait_timeout: Optional[float] = 25
    ) -> GeolocatorPermissionStatus:
        p = self.invoke_method(
            "get_permission_status",
            wait_for_result=True,
            wait_timeout=wait_timeout,
        )
        return GeolocatorPermissionStatus(p)

    async def get_permission_status_async(
        self, wait_timeout: Optional[float] = 25
    ) -> GeolocatorPermissionStatus:
        p = await self.invoke_method_async(
            "get_permission_status",
            wait_for_result=True,
            wait_timeout=wait_timeout,
        )
        return GeolocatorPermissionStatus(p)

    def request_permission(
        self, wait_timeout: Optional[float] = 25
    ) -> GeolocatorPermissionStatus:
        p = self.invoke_method(
            "request_permission",
            wait_for_result=True,
            wait_timeout=wait_timeout,
        )
        return GeolocatorPermissionStatus(p)

    async def request_permission_async(
        self, wait_timeout: Optional[float] = 25
    ) -> GeolocatorPermissionStatus:
        p = await self.invoke_method_async(
            "request_permission",
            wait_for_result=True,
            wait_timeout=wait_timeout,
        )
        return GeolocatorPermissionStatus(p)

    def is_location_service_enabled(self, wait_timeout: Optional[float] = 10) -> bool:
        enabled = self.invoke_method(
            "request_permission",
            wait_for_result=True,
            wait_timeout=wait_timeout,
        )
        return enabled == "true"

    async def is_location_service_enabled_async(
        self, wait_timeout: Optional[float] = 10
    ) -> bool:
        enabled = await self.invoke_method_async(
            "is_location_service_enabled",
            wait_for_result=True,
            wait_timeout=wait_timeout,
        )
        return enabled == "true"

    def open_app_settings(self, wait_timeout: Optional[float] = 10) -> bool:
        assert not self.page.web, "open_app_settings is not supported on web"
        opened = self.invoke_method(
            "open_app_settings",
            wait_for_result=True,
            wait_timeout=wait_timeout,
        )
        return opened == "true"

    async def open_app_settings_async(self, wait_timeout: Optional[float] = 10) -> bool:
        assert not self.page.web, "open_app_settings is not supported on web"
        opened = await self.invoke_method_async(
            "open_app_settings",
            wait_for_result=True,
            wait_timeout=wait_timeout,
        )
        return opened == "true"

    def open_location_settings(self, wait_timeout: Optional[float] = 10) -> bool:
        assert not self.page.web, "open_location_settings is not supported on web"
        opened = self.invoke_method(
            "open_location_settings",
            wait_for_result=True,
            wait_timeout=wait_timeout,
        )
        return opened == "true"

    async def open_location_settings_async(
        self, wait_timeout: Optional[float] = 10
    ) -> bool:
        assert not self.page.web, "open_location_settings is not supported on web"
        opened = await self.invoke_method_async(
            "open_location_settings",
            wait_for_result=True,
            wait_timeout=wait_timeout,
        )
        return opened == "true"
