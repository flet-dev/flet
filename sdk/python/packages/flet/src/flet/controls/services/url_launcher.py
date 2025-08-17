from typing import Optional, Union

from flet.controls.base_control import control
from flet.controls.services.service import Service
from flet.controls.types import Url, UrlTarget

__all__ = ["UrlLauncher"]


@control("UrlLauncher")
class UrlLauncher(Service):
    async def launch_url(
        self,
        url: Union[str, Url],
        *,
        web_popup_window_name: Optional[Union[str, UrlTarget]] = None,
        web_popup_window: bool = False,
        web_popup_window_width: Optional[int] = None,
        web_popup_window_height: Optional[int] = None,
    ) -> None:
        """
        Opens a web browser or popup window to a given `url`.

        Args:
            url: The URL to open.
            web_popup_window_name: Window tab/name to open URL in.
            web_popup_window: Whether to open the URL in a browser popup window.
            web_popup_window_width: Popup window width.
            web_popup_window_height: Popup window height.
        """
        await self._invoke_method(
            "launch_url",
            {
                "url": url,
                "web_popup_window_name": web_popup_window_name,
                "web_popup_window": web_popup_window,
                "web_popup_window_width": web_popup_window_width,
                "web_popup_window_height": web_popup_window_height,
            },
        )

    async def can_launch_url(self, url: Union[str, Url]) -> bool:
        """
        Checks whether the specified URL can be handled by some app
        installed on the device.

        Args:
            url: The URL to check.

        Returns:
            `True` if it is possible to verify that there is a handler available.
            `False` if there is no handler available,
            or the application does not have permission to check. For example:

            - On recent versions of Android and iOS, this will always return `False`
                unless the application has been configuration to allow querying the
                system for launch support.
            - On web, this will always return `False` except for a few specific schemes
                that are always assumed to be supported (such as http(s)), as web pages
                are never allowed to query installed applications.
        """
        return await self._invoke_method(
            "can_launch_url",
            {"url": url},
        )

    async def close_in_app_web_view(self) -> None:
        """
        Closes the in-app web view if it is currently open.

        This method invokes the platform-specific functionality to close
        any web view that was previously opened within the application.
        """
        await self._invoke_method("close_in_app_web_view")
