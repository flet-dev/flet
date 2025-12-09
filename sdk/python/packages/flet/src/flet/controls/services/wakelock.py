from flet.controls.base_control import control
from flet.controls.services.service import Service

__all__ = ["Wakelock"]


@control("Wakelock")
class Wakelock(Service):
    """
    Prevents the device from sleeping while enabled.
    """

    async def enable(self):
        """
        Keeps the device awake.
        """

        await self._invoke_method("enable")

    async def disable(self):
        """
        Allows the device to sleep again.
        """

        await self._invoke_method("disable")

    async def is_enabled(self) -> bool:
        """
        Returns `True` if the wakelock is currently enabled.
        """

        return await self._invoke_method("is_enabled")
