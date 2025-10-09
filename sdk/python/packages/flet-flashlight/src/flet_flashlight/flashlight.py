from typing import Optional

import flet as ft

from .exceptions import (
    FlashlightDisableException,
    FlashlightDisableExistentUserException,
    FlashlightDisableNotAvailableException,
    FlashlightEnableException,
    FlashlightEnableExistentUserException,
    FlashlightEnableNotAvailableException,
    FlashlightException,
)

__all__ = ["Flashlight"]


@ft.control("Flashlight")
class Flashlight(ft.Service):
    """
    A control to use FlashLight. Works on iOS and Android.
    """

    on = False
    """
    Whether the flashlight is currently turned on.
    """

    on_error: Optional[ft.ControlEventHandler["Flashlight"]] = None
    """
    Fires when an error occurs.

    The [`data`][flet.Event.data] property of the event handler argument
    contains information on the error.
    """

    async def turn_on(self):
        """
        Turns the flashlight on.
        """
        r = await self._invoke_method("on")
        if r is True:
            self.on = True
        else:  # error occured
            error_type = r.get("error_type")
            error_msg = r.get("error_msg")
            if error_type == "EnableTorchExistentUserException":
                raise FlashlightEnableExistentUserException(error_msg)
            elif error_type == "EnableTorchNotAvailableException":
                raise FlashlightEnableNotAvailableException(error_msg)
            else:
                raise FlashlightEnableException(error_msg)

    async def turn_off(self):
        """
        Turns the flashlight off.
        """
        r = await self._invoke_method("off")
        if r is True:
            self.on = False
        else:  # error occured
            error_type = r.get("error_type")
            error_msg = r.get("error_msg")
            if error_type == "DisableTorchExistentUserException":
                raise FlashlightDisableExistentUserException(error_msg)
            elif error_type == "DisableTorchNotAvailableException":
                raise FlashlightDisableNotAvailableException(error_msg)
            else:
                raise FlashlightDisableException(error_msg)

    async def toggle(self):
        """
        Toggles the flashlight on and off.
        """
        if self.on:
            await self.turn_off()
        else:
            await self.turn_on()

    async def is_available(self):
        """
        Checks if the flashlight is available on the device.
        """
        r = await self._invoke_method("is_available")
        if isinstance(r, bool):
            return r
        else:  # error occured
            error_msg = r.get("error_msg")
            raise FlashlightException(error_msg)
