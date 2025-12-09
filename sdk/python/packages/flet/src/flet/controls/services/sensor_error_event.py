from dataclasses import dataclass

from flet.controls.control_event import Event, EventControlType

__all__ = ["SensorErrorEvent"]


@dataclass(kw_only=True)
class SensorErrorEvent(Event[EventControlType]):
    """
    Generic sensor error event. `message` contains the platform error text.
    """

    message: str
    """Human-readable description of the sensor error."""
