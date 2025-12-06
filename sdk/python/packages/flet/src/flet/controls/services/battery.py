from dataclasses import dataclass
from enum import Enum
from typing import Optional

from flet.controls.base_control import control
from flet.controls.control_event import Event, EventHandler
from flet.controls.services.service import Service

__all__ = ["Battery", "BatteryState", "BatteryStateChangeEvent"]


class BatteryState(Enum):
    """
    Battery state.
    """

    CHARGING = "charging"
    """
    The battery is currently charging.
    """
    CONNECTED_NOT_CHARGING = "connectedNotCharging"
    """
    The battery is connected to a power source but not charging.
    """
    DISCHARGING = "discharging"
    """
    The battery is discharging.
    """
    FULL = "full"
    """
    The battery is fully charged.
    """
    UNKNOWN = "unknown"
    """
    The battery state is unknown.
    """


@dataclass
class BatteryStateChangeEvent(Event["Battery"]):
    """
    Event fired when battery state changes.
    """

    state: BatteryState
    """
    Current battery state.
    """


@control("Battery")
class Battery(Service):
    """
    Provides access to device battery information and state changes.
    """

    on_state_change: Optional[EventHandler[BatteryStateChangeEvent]] = None
    """
    Called when battery state changes (charging, discharging, full, unknown).
    """

    async def get_battery_level(self) -> int:
        """
        Returns current battery level as a percentage `0..100`.
        """

        return await self._invoke_method("get_battery_level")

    async def get_battery_state(self) -> BatteryState:
        """
        Returns current battery state.
        """

        return BatteryState(await self._invoke_method("get_battery_state"))

    async def is_in_battery_save_mode(self) -> bool:
        """
        Returns `True` if the device is currently in battery save mode.
        """

        return await self._invoke_method("is_in_battery_save_mode")
