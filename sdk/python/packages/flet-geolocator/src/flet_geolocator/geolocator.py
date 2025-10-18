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
    ) -> GeolocatorPosition:
        """
        Gets the current position of the device with the desired accuracy and settings.

        Note:
            Depending on the availability of different location services,
            this can take several seconds. It is recommended to call the
            [`get_last_known_position`][(c).] method first to receive a
            known/cached position and update it with the result of the
            [`get_current_position`][(c).] method.

        Args:
            configuration: Additional configuration for the location request.
                If not specified, then the [`Geolocator.configuration`][(p).]
                property is used.

        Returns:
            The current position of the device as a [`GeolocatorPosition`][(p).].
        """
        r = await self._invoke_method(
            method_name="get_current_position",
            arguments={"configuration": configuration or self.configuration},
        )
        return GeolocatorPosition(**r)

    async def get_last_known_position(self) -> GeolocatorPosition:
        """
        Gets the last known position stored on the user's device.
        The accuracy can be defined using the
        [`Geolocator.configuration`][(p).] property.

        Note:
            This method is not supported on web platform.

        Returns:
            The last known position of the device as a [`GeolocatorPosition`][(p).].

        Raises:
            FletUnsupportedPlatformException: If invoked on a web platform.
        """
        if self.page.web:
            raise ft.FletUnsupportedPlatformException(
                "get_last_known_position is not supported on web"
            )
        r = await self._invoke_method(
            "get_last_known_position",
        )
        return GeolocatorPosition(**r)

    async def get_permission_status(self) -> GeolocatorPermissionStatus:
        """
        Gets which permission the app has been granted to access the device's location.

        Returns:
            The status of the permission.
        """
        r = await self._invoke_method(
            "get_permission_status",
        )
        return GeolocatorPermissionStatus(r)

    async def request_permission(self) -> GeolocatorPermissionStatus:
        """
        Requests the device for access to the device's location.

        Returns:
            The status of the permission request.
        """
        r = await self._invoke_method(
            "request_permission",
        )
        return GeolocatorPermissionStatus(r)

    async def is_location_service_enabled(self) -> bool:
        """
        Checks if location service is enabled.

        Returns:
            `True` if location service is enabled, `False` otherwise.
        """
        return await self._invoke_method("is_location_service_enabled")

    async def open_app_settings(self) -> bool:
        """
        Attempts to open the app's settings.

        Note:
            This method is not supported on web platform.

        Returns:
            `True` if the app's settings were opened successfully, `False` otherwise.

        Raises:
            FletUnsupportedPlatformException: If invoked on a web platform.
        """
        if self.page.web:
            raise ft.FletUnsupportedPlatformException(
                "open_app_settings is not supported on web"
            )
        return await self._invoke_method(
            "open_app_settings",
        )

    async def open_location_settings(self) -> bool:
        """
        Attempts to open the device's location settings.

        Note:
            This method is not supported on web platform.

        Returns:
            `True` if the device's settings were opened successfully, `False` otherwise.

        Raises:
            FletUnsupportedPlatformException: If invoked on a web platform.
        """
        if self.page.web:
            raise ft.FletUnsupportedPlatformException(
                "open_location_settings is not supported on web"
            )
        return await self._invoke_method(
            "open_location_settings",
        )

    async def distance_between(
        self,
        start_latitude: ft.Number,
        start_longitude: ft.Number,
        end_latitude: ft.Number,
        end_longitude: ft.Number,
    ) -> ft.Number:
        """
        Calculates the distance between the supplied coordinates in meters.

        The distance between the coordinates is calculated using the
        Haversine formula (see https://en.wikipedia.org/wiki/Haversine_formula).

        Args:
            start_latitude: The latitude of the starting point, in degrees.
            start_longitude: The longitude of the starting point, in degrees.
            end_latitude: The latitude of the ending point, in degrees.
            end_longitude: The longitude of the ending point, in degrees.

        Returns:
            The distance between the coordinates in meters.
        """
        return await self._invoke_method(
            method_name="distance_between",
            arguments={
                "start_latitude": start_latitude,
                "start_longitude": start_longitude,
                "end_latitude": end_latitude,
                "end_longitude": end_longitude,
            },
        )
