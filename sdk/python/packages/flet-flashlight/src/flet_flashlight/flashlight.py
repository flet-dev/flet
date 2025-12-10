import flet as ft

__all__ = ["Flashlight"]


@ft.control("Flashlight")
class Flashlight(ft.Service):
    """
    A control to use FlashLight. Works on iOS and Android.
    """

    async def turn_on(self):
        """
        Turns the flashlight on.
        """
        await self._invoke_method("on")

    async def turn_off(self):
        """
        Turns the flashlight off.
        """
        await self._invoke_method("off")

    async def is_available(self):
        """
        Checks if the flashlight is available on the device.
        """
        return await self._invoke_method("is_available")
