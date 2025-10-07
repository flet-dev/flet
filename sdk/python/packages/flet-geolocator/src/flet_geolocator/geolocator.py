from dataclasses import field
from typing import Optional

import flet as ft
from flet_geolocator.types import (
    GeolocatorConfiguration,
    GeolocatorPermissionStatus,
    GeolocatorPosition,
    GeolocatorPositionChangeEvent,
)

__all__ = ["Geolocator"]


@ft.control("Geolocator")
class Geolocator(ft.Service):
    """
    A control that allows you to fetch GPS data from your device.
    """

    configuration: Optional[GeolocatorConfiguration] = None
    """
    Some additional configuration.
    """

    on_position_change: Optional[ft.EventHandler[GeolocatorPositionChangeEvent]] = None
    """
    Fires when the position of the device changes.
    """

    on_error: Optional[ft.ControlEventHandler["Geolocator"]] = None
    """
    Fires when an error occurs.

    The [`data`][flet.Event.data] property of the event
    handler argument contains information on the error.
    """

    position: Optional[GeolocatorPosition] = field(
        default=None, init=False
    )  # TODO: make this property readonly
    """
    The current position of the device. (read-only)

    Starts as `None` and will be updated when the position changes.
    """

    async def get_current_position(
        self,
        configuration: Optional[GeolocatorConfiguration] = None,
        timeout: float = 30,
    ) -> GeolocatorPosition:
        """
        Gets the current position of the device with the desired accuracy and settings.

        Note:
            Depending on the availability of different location services,
            this can take several seconds. It is recommended to call the
            [`get_last_known_position`][..] method first to receive a
            known/cached position and update it with the result of the
            [`get_current_position`][..] method.

        Args:
            configuration: Additional configuration for the location request.
                If not specified, then the [`Geolocator.configuration`][(p).]
                property is used.
            timeout: The maximum amount of time (in seconds) to wait for a response.

        Returns:
            The current position of the device as a [`GeolocatorPosition`][(p).].

        Raises:
            TimeoutError: If the request times out.
        """
        r = await self._invoke_method(
            method_name="get_current_position",
            arguments={"configuration": configuration or self.configuration},
            timeout=timeout,
        )
        return GeolocatorPosition(**r)

    async def get_last_known_position(self, timeout: float = 10) -> GeolocatorPosition:
        """
        Gets the last known position stored on the user's device.
        The accuracy can be defined using the
        [`Geolocator.configuration`][(p).] property.

        Note:
            This method is not supported on web platform.

        Args:
            timeout: The maximum amount of time (in seconds) to wait for a response.

        Returns:
            The last known position of the device as a [`GeolocatorPosition`][(p).].

        Raises:
            AssertionError: If invoked on a web platform.
            TimeoutError: If the request times out.
        """
        assert not self.page.web, "get_last_known_position is not supported on web"
        r = await self._invoke_method(
            "get_last_known_position",
            timeout=timeout,
        )
        return GeolocatorPosition(**r)

    async def get_permission_status(
        self, timeout: float = 10
    ) -> GeolocatorPermissionStatus:
        """
        Gets which permission the app has been granted to access the device's location.

        Args:
            timeout: The maximum amount of time (in seconds) to wait for a response.

        Returns:
            The status of the permission.

        Raises:
            TimeoutError: If the request times out.
        """
        r = await self._invoke_method(
            "get_permission_status",
            timeout=timeout,
        )
        return GeolocatorPermissionStatus(r)

    async def request_permission(self, timeout: int = 60) -> GeolocatorPermissionStatus:
        """
        Requests the device for access to the device's location.

        Args:
            timeout: The maximum amount of time (in seconds) to wait for a response.

        Returns:
            The status of the permission request.

        Raises:
            TimeoutError: If the request times out.
        """
        r = await self._invoke_method(
            "request_permission",
            timeout=timeout,
        )
        return GeolocatorPermissionStatus(r)

    async def is_location_service_enabled(self, timeout: float = 10) -> bool:
        """
        Checks if location service is enabled.

        Args:
            timeout: The maximum amount of time (in seconds) to wait for a response.

        Returns:
            `True` if location service is enabled, `False` otherwise.

        Raises:
            TimeoutError: If the request times out.
        """
        return await self._invoke_method("is_location_service_enabled", timeout=timeout)

    async def open_app_settings(self, timeout: float = 10) -> bool:
        """
        Attempts to open the app's settings.

        Note:
            This method is not supported on web platform.

        Args:
            timeout: The maximum amount of time (in seconds) to wait for a response.

        Returns:
            `True` if the app's settings were opened successfully, `False` otherwise.

        Raises:
            AssertionError: If invoked on a web platform.
            TimeoutError: If the request times out.
        """
        assert not self.page.web, "open_app_settings is not supported on web"
        return await self._invoke_method(
            "open_app_settings",
            timeout=timeout,
        )

    async def open_location_settings(self, timeout: float = 10) -> bool:
        """
        Attempts to open the device's location settings.

        Note:
            This method is not supported on web platform.

        Args:
            timeout: The maximum amount of time (in seconds) to wait for a response.

        Returns:
            `True` if the device's settings were opened successfully, `False` otherwise.

        Raises:
            AssertionError: If invoked on a web platform.
            TimeoutError: If the request times out.
        """
        assert not self.page.web, "open_location_settings is not supported on web"
        return await self._invoke_method(
            "open_location_settings",
            timeout=timeout,
        )

    async def distance_between(
        self,
        start_latitude: ft.Number,
        start_longitude: ft.Number,
        end_latitude: ft.Number,
        end_longitude: ft.Number,
        timeout: float = 10,
    ):
        """
        Calculates the distance between the supplied coordinates in meters.

        The distance between the coordinates is calculated using the
        Haversine formula (see https://en.wikipedia.org/wiki/Haversine_formula).

        Args:
            start_latitude: The latitude of the starting point, in degrees.
            start_longitude: The longitude of the starting point, in degrees.
            end_latitude: The latitude of the ending point, in degrees.
            end_longitude: The longitude of the ending point, in degrees.
            timeout: The maximum amount of time (in seconds) to wait for a response.

        Returns:
            The distance between the coordinates in meters.

        Raises:
            TimeoutError: If the request times out.
        """
        await self._invoke_method(
            method_name="distance_between",
            arguments={
                "start_latitude": start_latitude,
                "start_longitude": start_longitude,
                "end_latitude": end_latitude,
                "end_longitude": end_longitude,
            },
            timeout=timeout,
        )
