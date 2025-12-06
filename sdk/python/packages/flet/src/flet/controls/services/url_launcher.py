from dataclasses import dataclass, field
from enum import Enum
from typing import Optional, Union

from flet.controls.base_control import control
from flet.controls.services.service import Service
from flet.controls.types import Url

__all__ = [
    "BrowserConfiguration",
    "LaunchMode",
    "UrlLauncher",
    "WebViewConfiguration",
]


class LaunchMode(Enum):
    """
    Preferred launch mode for opening a URL.
    """

    PLATFORM_DEFAULT = "platformDefault"
    """Platform decides how to open the URL."""

    IN_APP_WEB_VIEW = "inAppWebView"
    """Load the URL inside an in-app web view."""

    IN_APP_BROWSER_VIEW = "inAppBrowserView"
    """Load the URL inside an in-app browser view (e.g., custom tabs)."""

    EXTERNAL_APPLICATION = "externalApplication"
    """Pass the URL to another application to handle."""

    EXTERNAL_NON_BROWSER_APPLICATION = "externalNonBrowserApplication"
    """Pass the URL to a non-browser application to handle."""


@dataclass
class WebViewConfiguration:
    """
    Configuration options for in-app web views.
    """

    enable_javascript: bool = True
    """Whether JavaScript execution is allowed."""

    enable_dom_storage: bool = True
    """Whether DOM storage is enabled."""

    headers: dict[str, str] = field(default_factory=dict)
    """Additional HTTP headers to include with the request."""


@dataclass
class BrowserConfiguration:
    """
    Configuration options for in-app browser views.
    """

    show_title: bool = False
    """Whether the browser view should display the page title."""


@control("UrlLauncher")
class UrlLauncher(Service):
    """
    Provides access to URL launching capabilities.
    """

    async def launch_url(
        self,
        url: Union[str, Url],
        *,
        mode: LaunchMode = LaunchMode.PLATFORM_DEFAULT,
        web_view_configuration: Optional[WebViewConfiguration] = None,
        browser_configuration: Optional[BrowserConfiguration] = None,
        web_only_window_name: Optional[str] = None,
    ):
        """
        Opens a web browser or in-app view to a given `url`.

        Args:
            url: The URL to open.
            mode: Preferred launch mode for opening the URL.
            web_view_configuration: Optional configuration for in-app web views.
            browser_configuration: Optional configuration for in-app browser views.
            web_only_window_name: Window name for web-only launches.
        """
        await self._invoke_method(
            "launch_url",
            {
                "url": url,
                "mode": mode,
                "web_view_configuration": web_view_configuration,
                "browser_configuration": browser_configuration,
                "web_only_window_name": web_only_window_name,
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
                - On web, this will always return `False` except for a few specific
                    schemes that are always assumed to be supported (such as http(s)),
                    as web pages are never allowed to query installed applications.
        """
        return await self._invoke_method(
            "can_launch_url",
            {"url": url},
        )

    async def close_in_app_web_view(self):
        """
        Closes the in-app web view if it is currently open.
        """
        await self._invoke_method("close_in_app_web_view")

    async def open_window(
        self,
        url: Union[str, Url],
        *,
        title: Optional[str] = None,
        width: Optional[float] = None,
        height: Optional[float] = None,
    ):
        """
        Opens a popup browser window in web environments.

        Args:
            url: The URL to open in the popup window.
            title: The popup window title.
            width: Desired popup width in logical pixels.
            height: Desired popup height in logical pixels.
        """
        await self._invoke_method(
            "open_window",
            {
                "url": url,
                "title": title,
                "width": width,
                "height": height,
            },
        )

    async def supports_launch_mode(self, mode: LaunchMode) -> bool:
        """
        Checks whether the specified launch mode is supported.

        Args:
            mode: Launch mode to verify.

        Returns:
            `True` if the launch mode is supported by the platform; otherwise `False`.
        """
        return await self._invoke_method("supports_launch_mode", {"mode": mode})

    async def supports_close_for_launch_mode(self, mode: LaunchMode) -> bool:
        """
        Checks whether `close_in_app_web_view` is supported for a launch mode.

        Args:
            mode: Launch mode to verify close support for.

        Returns:
            `True` if closing an in-app web view is supported; otherwise `False`.
        """
        return await self._invoke_method(
            "supports_close_for_launch_mode", {"mode": mode}
        )
