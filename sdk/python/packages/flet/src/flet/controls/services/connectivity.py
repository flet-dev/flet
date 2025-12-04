from dataclasses import dataclass
from enum import Enum
from typing import Optional

from flet.controls.base_control import control
from flet.controls.control_event import Event, EventHandler
from flet.controls.services.service import Service

__all__ = ["Connectivity", "ConnectivityChangeEvent", "ConnectivityResult"]


class ConnectivityResult(Enum):
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

    connectivity: list[ConnectivityResult]
    """
    Current connectivity state(s).
    """


@control("Connectivity")
class Connectivity(Service):
    """
    Provides device connectivity status and change notifications.
    """

    on_connectivity_change: Optional[EventHandler[ConnectivityChangeEvent]] = None
    """
    Called when connectivity changes.
    """

    async def check_connectivity(self) -> list[ConnectivityResult]:
        """
        Returns the current connectivity state(s).
        """

        result = await self._invoke_method("check_connectivity")
        return [ConnectivityResult(r) for r in result]
