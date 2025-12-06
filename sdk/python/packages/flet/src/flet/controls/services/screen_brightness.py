from dataclasses import dataclass
from typing import Optional

from flet.controls.base_control import control
from flet.controls.control_event import Event, EventHandler
from flet.controls.exceptions import FletUnsupportedPlatformException
from flet.controls.services.service import Service
from flet.controls.types import Number

__all__ = ["ScreenBrightness", "ScreenBrightnessChangeEvent"]


@dataclass
class ScreenBrightnessChangeEvent(Event["ScreenBrightness"]):
    """
    Event fired when screen brightness changes.
    """

    brightness: float
    """
    The new screen brightness, in range `0.0..1.0`.
    """


@control("ScreenBrightness")
class ScreenBrightness(Service):
    """
    Provides access to control and observe system and application screen brightness.

    Note:
        * Supported platforms: Android, iOS.

    /// admonition | Running on Android
        type: warning
    To adjust the system brightness on Android, add the following permission
    in your `pyproject.toml` file:
    ```toml
    [tool.flet.android.permission]
    "android.permission.WRITE_SETTINGS" = true
    ```
    ///
    """

    on_system_screen_brightness_change: Optional[
        EventHandler[ScreenBrightnessChangeEvent]
    ] = None
    """
    Called when the **system** screen brightness changes.
    """

    on_application_screen_brightness_change: Optional[
        EventHandler[ScreenBrightnessChangeEvent]
    ] = None
    """
    Called when the **application** screen brightness changes.
    """

    async def get_system_screen_brightness(self) -> float:
        """
        Returns the current system screen brightness, in range `0.0..1.0`.
        """

        return await self._invoke_method("get_system_screen_brightness")

    async def can_change_system_screen_brightness(self) -> bool:
        """
        Returns whether the app is allowed to change the system screen brightness.
        """

        return await self._invoke_method("can_change_system_screen_brightness")

    async def set_system_screen_brightness(self, brightness: Number):
        """
        Sets the system screen brightness.
        """

        await self._invoke_method("set_system_screen_brightness", {"value": brightness})

    async def get_application_screen_brightness(self) -> float:
        """
        Returns the current application screen brightness, in range `0.0..1.0`.
        """

        return await self._invoke_method("get_application_screen_brightness")

    async def set_application_screen_brightness(self, brightness: Number):
        """
        Sets the application screen brightness.
        """

        await self._invoke_method(
            "set_application_screen_brightness", {"value": brightness}
        )

    async def reset_application_screen_brightness(self):
        """
        Resets the application screen brightness back to the system value.
        """

        await self._invoke_method("reset_application_screen_brightness")

    async def is_animate(self) -> bool:
        """
        Returns `True` if brightness changes are animated (platform dependent).
        """

        return await self._invoke_method("is_animate")

    async def set_animate(self, animate: bool):
        """
        Enables or disables animation for brightness changes.
        """

        await self._invoke_method("set_animate", {"value": animate})

    async def is_auto_reset(self) -> bool:
        """
        Returns `True` if brightness resets automatically on lifecycle changes.
        """

        return await self._invoke_method("is_auto_reset")

    async def set_auto_reset(self, auto_reset: bool):
        """
        Enables or disables automatic reset to system brightness on lifecycle changes.
        """

        await self._invoke_method("set_auto_reset", {"value": auto_reset})

    def before_update(self):
        if self.page.web or not self.page.platform.is_mobile():
            raise FletUnsupportedPlatformException(
                f"{self.__class__.__name__} is only supported on Android and iOS."
            )
