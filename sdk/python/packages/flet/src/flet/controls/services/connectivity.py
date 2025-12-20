from dataclasses import dataclass
from enum import Enum
from typing import Optional

from flet.controls.base_control import control
from flet.controls.control_event import Event, EventHandler
from flet.controls.services.service import Service

__all__ = ["Connectivity", "ConnectivityChangeEvent", "ConnectivityType"]


class ConnectivityType(Enum):
    """
    Connectivity states.
    """

    BLUETOOTH = "bluetooth"
    """
    Bluetooth connectivity.
    """
    ETHERNET = "ethernet"
    """
    Ethernet connectivity.
    """
    MOBILE = "mobile"
    """
    Mobile data connectivity.
    """
    NONE = "none"
    """
    No connectivity.
    """
    OTHER = "other"
    """
    Other connectivity.
    """
    VPN = "vpn"
    """
    VPN connectivity.
    """
    WIFI = "wifi"
    """
    Wi-Fi connectivity.
    """


@dataclass
class ConnectivityChangeEvent(Event["Connectivity"]):
    """Event fired when connectivity changes."""

    connectivity: list[ConnectivityType]
    """
    Current connectivity type(s).
    """


@control("Connectivity")
class Connectivity(Service):
    """
    Provides device connectivity status and change notifications.
    """

    on_change: Optional[EventHandler[ConnectivityChangeEvent]] = None
    """
    Called when connectivity changes.
    """

    async def get_connectivity(self) -> list[ConnectivityType]:
        """
        Returns the current connectivity type(s).
        """

        result = await self._invoke_method("get_connectivity")
        return [ConnectivityType(r) for r in result]
