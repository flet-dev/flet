import json
from dataclasses import dataclass
from enum import Enum
from typing import Any, Optional

from flet.core.control import Control
from flet.core.control_event import ControlEvent
from flet.core.event_handler import EventHandler
from flet.core.ref import Ref
from flet.core.types import (
    ColorValue,
    DurationValue,
    OptionalControlEventCallable,
    OptionalEventCallable,
    OptionalNumber,
)
from flet.utils import deprecated


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


class GeolocatorActivityType(Enum):
    AUTOMOTIVE_NAVIGATION = "automotiveNavigation"
    FITNESS = "fitness"
    OTHER_NAVIGATION = "otherNavigation"
    AIRBORNE = "airborne"
    OTHER = "other"


@dataclass
class GeolocatorPosition:
    latitude: OptionalNumber = None
    longitude: OptionalNumber = None
    speed: OptionalNumber = None
    altitude: OptionalNumber = None
    timestamp: OptionalNumber = None
    accuracy: OptionalNumber = None
    altitude_accuracy: OptionalNumber = None
    heading: OptionalNumber = None
    heading_accuracy: OptionalNumber = None
    speed_accuracy: OptionalNumber = None
    floor: Optional[int] = None
    is_mocked: Optional[bool] = None


@dataclass
class GeolocatorSettings:
    accuracy: Optional[GeolocatorPositionAccuracy] = None
    distance_filter: Optional[int] = None
    time_limit: Optional[DurationValue] = None


@dataclass
class GeolocatorWebSettings(GeolocatorSettings):
    maximum_age: Optional[DurationValue] = None


@dataclass
class GeolocatorAppleSettings(GeolocatorSettings):
    activity_type: Optional[GeolocatorActivityType] = None
    pause_location_updates_automatically: Optional[bool] = False
    show_background_location_indicator: Optional[bool] = False
    allow_background_location_updates: Optional[bool] = True


@dataclass
class GeolocatorAndroidSettings(GeolocatorSettings):
    force_location_manager: Optional[bool] = False
    interval_duration: Optional[DurationValue] = False
    foreground_notification_text: Optional[str] = None
    foreground_notification_title: Optional[str] = None
    foreground_notification_channel_name: Optional[str] = "Background Location"
    foreground_notification_enable_wake_lock: Optional[bool] = False
    foreground_notification_enable_wifi_lock: Optional[bool] = False
    foreground_notification_set_ongoing: Optional[bool] = False
    foreground_notification_color: Optional[ColorValue] = None


class GeolocatorPositionChangeEvent(ControlEvent):
    def __init__(self, e: ControlEvent):
        super().__init__(e.target, e.name, e.data, e.control, e.page)
        d = json.loads(e.data)
        self.latitude: float = d.get("lat")
        self.longitude: float = d.get("long")


@deprecated(
    reason="Geolocator control has been moved to a separate Python package: https://pypi.org/project/flet-geolocator. "
    + "Read more about this change in Flet blog: https://flet.dev/blog/flet-v-0-26-release-announcement",
    version="0.26.0",
    delete_version="0.29.0",
)
class Geolocator(Control):
    """
    A control that allows you to fetch GPS data from your device.
    This control is non-visual and should be added to `page.overlay` list.

    -----

    Online docs: https://flet.dev/docs/controls/geolocator
    """

    def __init__(
        self,
        # Control
        #
        ref: Optional[Ref] = None,
        data: Any = None,
        location_settings: Optional[GeolocatorSettings] = None,
        on_position_change: OptionalEventCallable[GeolocatorPositionChangeEvent] = None,
        on_error: OptionalControlEventCallable = None,
    ):
        Control.__init__(
            self,
            ref=ref,
            data=data,
        )
        self.__on_position_change = EventHandler(
            lambda e: GeolocatorPositionChangeEvent(e)
        )
        self._add_event_handler(
            "positionChange", self.__on_position_change.get_handler()
        )
        self.on_position_change = on_position_change
        self.on_error = on_error
        self.location_settings = location_settings

    def _get_control_name(self):
        return "geolocator"

    def before_update(self):
        self._set_attr_json("locationSettings", self.location_settings)

    def get_current_position(
        self,
        accuracy: Optional[
            GeolocatorPositionAccuracy
        ] = GeolocatorPositionAccuracy.BEST,
        location_settings: Optional[GeolocatorSettings] = None,
        wait_timeout: Optional[float] = 25,
    ) -> GeolocatorPosition:
        ls = (
            location_settings
            or self.location_settings
            or GeolocatorSettings(accuracy=accuracy)
        )
        output = self.invoke_method(
            "get_current_position",
            {"location_settings": self._convert_attr_json(ls)},
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
        location_settings: Optional[GeolocatorSettings] = None,
        wait_timeout: Optional[float] = 25,
    ) -> GeolocatorPosition:
        ls = (
            location_settings
            or self.location_settings
            or GeolocatorSettings(accuracy=accuracy)
        )
        output = await self.invoke_method_async(
            "get_current_position",
            {"location_settings": self._convert_attr_json(ls)},
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
            "is_location_service_enabled",
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

    @property
    def on_position_change(
        self,
    ) -> OptionalEventCallable[GeolocatorPositionChangeEvent]:
        return self.__on_position_change.handler

    @on_position_change.setter
    def on_position_change(
        self, handler: OptionalEventCallable[GeolocatorPositionChangeEvent]
    ):
        self.__on_position_change.handler = handler
        self._set_attr("onPositionChange", True if handler is not None else None)

    @property
    def on_error(self) -> OptionalControlEventCallable:
        return self._get_attr("error")

    @on_error.setter
    def on_error(self, handler: OptionalControlEventCallable):
        self._add_event_handler("error", handler)
