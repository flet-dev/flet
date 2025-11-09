from typing import Optional

from typing_extensions import Self

import flet as ft
from flet_webview.types import (
    JavaScriptMode,
    RequestMethod,
    WebViewConsoleMessageEvent,
    WebViewJavaScriptEvent,
    WebViewScrollEvent,
)

__all__ = ["WebView"]


@ft.control("WebView")
class WebView(ft.LayoutControl):
    """
    Easily load webpages while allowing user interaction.

    Note:
        Supported only on the following platforms: iOS, Android, macOS, and Web.
        Concerning Windows and Linux support, subscribe to this
        [issue](https://github.com/flet-dev/flet-webview/issues/17).
    """

    url: Optional[str] = None
    """The URL of the web page to load."""

    prevent_links: Optional[list[str]] = None
    """List of url-prefixes that should not be followed/loaded/downloaded."""

    bgcolor: Optional[ft.ColorValue] = None
    """Defines the background color of the WebView."""

    on_page_started: Optional[ft.ControlEventHandler["WebView"]] = None
    """
    Fires soon as the first loading process of the webview page is started.

    The [`data`][flet.Event.] property of the event handler argument is of type
    `str` and contains the URL.

    Note:
        Works only on the following platforms: iOS, Android and macOS.
    """

    on_page_ended: Optional[ft.ControlEventHandler["WebView"]] = None
    """
    Fires when all the webview page loading processes are ended.

    The [`data`][flet.Event.] property of the event handler argument is of type
    `str` and contains the URL.

    Note:
        Works only on the following platforms: iOS, Android and macOS.
    """

    on_web_resource_error: Optional[ft.ControlEventHandler["WebView"]] = None
    """
    Fires when there is error with loading a webview page resource.

    The [`data`][flet.Event.] property of the event handler argument is of type
    `str` and contains the error message.

    Note:
        Works only on the following platforms: iOS, Android and macOS.
    """

    on_progress: Optional[ft.ControlEventHandler["WebView"]] = None
    """
    Fires when the progress of the webview page loading is changed.

    The [`data`][flet.Event.] property of the event handler argument is of type
    `int` and contains the progress value.

    Note:
        Works only on the following platforms: iOS, Android and macOS.
    """

    on_url_change: Optional[ft.ControlEventHandler["WebView"]] = None
    """
    Fires when the URL of the webview page is changed.

    The [`data`][flet.Event.] property of the event handler argument is of type
    `str` and contains the new URL.

    Note:
        Works only on the following platforms: iOS, Android and macOS.
    """

    on_scroll: Optional[ft.EventHandler[WebViewScrollEvent]] = None
    """
    Fires when the web page's scroll position changes.

    Note:
        Works only on the following platforms: iOS, Android and macOS.
    """

    on_console_message: Optional[ft.EventHandler[WebViewConsoleMessageEvent]] = None
    """
    Fires when a log message is written to the JavaScript console.

    Note:
        Works only on the following platforms: iOS, Android and macOS.
    """

    on_javascript_alert_dialog: Optional[ft.EventHandler[WebViewJavaScriptEvent]] = None
    """
    Fires when the web page attempts to display a JavaScript alert() dialog.

    Note:
        Works only on the following platforms: iOS, Android and macOS.
    """

    def _check_mobile_or_mac_platform(self):
        """
        Checks/Validates support for the current platform (iOS, Android, or macOS).
        """
        if self.page is None:
            raise RuntimeError("WebView must be added to page first.")
        if self.page.web or self.page.platform not in [
            ft.PagePlatform.ANDROID,
            ft.PagePlatform.IOS,
            ft.PagePlatform.MACOS,
        ]:
            raise ft.FletUnsupportedPlatformException(
                "This method is supported on Android, iOS and macOS platforms only."
            )

    async def reload(self):
        """
        Reloads the current URL.

        Note:
            Works only on the following platforms: iOS, Android, and macOS.
        """
        self._check_mobile_or_mac_platform()
        await self._invoke_method("reload")

    async def can_go_back(self) -> bool:
        """
        Whether there's a back history item.

        Note:
            Works only on the following platforms: iOS, Android, and macOS.

        Returns:
            `True` if there is a back history item, `False` otherwise.
        """
        self._check_mobile_or_mac_platform()
        return await self._invoke_method("can_go_back")

    async def can_go_forward(self) -> bool:
        """
        Whether there's a forward history item.

        Note:
            Works only on the following platforms: iOS, Android, and macOS.

        Returns:
            `True` if there is a forward history item, `False` otherwise.
        """
        self._check_mobile_or_mac_platform()
        return await self._invoke_method("can_go_forward")

    async def go_back(self):
        """
        Goes back in the history of the webview, if `can_go_back()` is `True`.

        Note:
            Works only on the following platforms: iOS, Android, and macOS.
        """
        self._check_mobile_or_mac_platform()
        await self._invoke_method("go_back")

    async def go_forward(self):
        """
        Goes forward in the history of the webview,
        if [`can_go_forward()`][(c).can_go_forward] is `True`.

        Note:
            Works only on the following platforms: iOS, Android, and macOS.
        """
        self._check_mobile_or_mac_platform()
        await self._invoke_method("go_forward")

    async def enable_zoom(self):
        """
        Enables zooming using the on-screen zoom controls and gestures.

        Note:
            Works only on the following platforms: iOS, Android, and macOS.
        """
        self._check_mobile_or_mac_platform()
        await self._invoke_method("enable_zoom")

    async def disable_zoom(self):
        """
        Disables zooming using the on-screen zoom controls and gestures.

        Note:
            Works only on the following platforms: iOS, Android, and macOS.
        """
        self._check_mobile_or_mac_platform()
        await self._invoke_method("disable_zoom")

    async def clear_cache(self):
        """
        Clears all caches used by the WebView.

        The following caches are cleared:
            - Browser HTTP Cache
            - Cache API caches. Service workers tend to use this cache.
            - Application cache

        Note:
            Works only on the following platforms: iOS, Android, and macOS.
        """
        self._check_mobile_or_mac_platform()
        await self._invoke_method("clear_cache")

    async def clear_local_storage(self):
        """
        Clears the local storage used by the WebView.

        Note:
            Works only on the following platforms: iOS, Android, and macOS.
        """
        self._check_mobile_or_mac_platform()
        await self._invoke_method("clear_local_storage")

    async def get_current_url(self) -> Optional[str]:
        """
        Gets the current URL that the WebView is displaying or `None`
        if no URL was ever loaded.

        Note:
            Works only on the following platforms: iOS, Android, and macOS.

        Returns:
            The current URL that the WebView is displaying or `None`
                if no URL was ever loaded.
        """
        self._check_mobile_or_mac_platform()
        return await self._invoke_method("get_current_url")

    async def get_title(self) -> Optional[str]:
        """
        Get the title of the currently loaded page.

        Note:
            Works only on the following platforms: iOS, Android, and macOS.

        Returns:
            The title of the currently loaded page.
        """
        self._check_mobile_or_mac_platform()
        return await self._invoke_method("get_title")

    async def get_user_agent(self) -> Optional[str]:
        """
        Get the value used for the HTTP `User-Agent:` request header.

        Note:
            Works only on the following platforms: iOS, Android, and macOS.

        Returns:
            The value used for the HTTP `User-Agent:` request header.
        """
        self._check_mobile_or_mac_platform()
        return await self._invoke_method("get_user_agent")

    async def load_file(self, path: str):
        """
        Loads the provided local file.

        Note:
            Works only on the following platforms: iOS, Android, and macOS.

        Args:
            path: The absolute path to the file.
        """
        self._check_mobile_or_mac_platform()
        await self._invoke_method(
            method_name="load_file",
            arguments={"path": path},
        )

    async def load_request(self, url: str, method: RequestMethod = RequestMethod.GET):
        """
        Makes an HTTP request and loads the response in the webview.

        Args:
            url: The URL to load.
            method: The HTTP method to use.

        Note:
            Works only on the following platforms: iOS, Android, and macOS.
        """
        self._check_mobile_or_mac_platform()
        await self._invoke_method(
            "load_request", arguments={"url": url, "method": method}
        )

    async def run_javascript(self, value: str):
        """
        Runs the given JavaScript in the context of the current page.

        Args:
            value: The JavaScript code to run.

        Note:
            Works only on the following platforms: iOS, Android, and macOS.
        """
        self._check_mobile_or_mac_platform()
        await self._invoke_method(
            method_name="run_javascript",
            arguments={"value": value},
        )

    async def load_html(self, value: str, base_url: Optional[str] = None) -> Self:
        """
        Loads the provided HTML string.

        Note:
            Works only on the following platforms: iOS, Android, and macOS.

        Args:
            value: The HTML string to load.
            base_url: The base URL to use when resolving relative URLs within the value.
        """
        self._check_mobile_or_mac_platform()
        await self._invoke_method(
            "load_html", arguments={"value": value, "base_url": base_url}
        )

        return self

    async def scroll_to(self, x: int, y: int):
        """
        Scrolls to the provided position of webview pixels.

        Note:
            Works only on the following platforms: iOS, Android, and macOS.

        Args:
            x: The x-coordinate of the scroll position.
            y: The y-coordinate of the scroll position.
        """
        self._check_mobile_or_mac_platform()
        await self._invoke_method(
            method_name="scroll_to",
            arguments={"x": x, "y": y},
        )

    async def scroll_by(self, x: int, y: int):
        """
        Scrolls by the provided number of webview pixels.

        Note:
            Works only on the following platforms: iOS, Android, and macOS.

        Args:
            x: The number of pixels to scroll by on the x-axis.
            y: The number of pixels to scroll by on the y-axis.
        """
        self._check_mobile_or_mac_platform()
        await self._invoke_method(
            method_name="scroll_by",
            arguments={"x": x, "y": y},
        )

    async def set_javascript_mode(self, mode: JavaScriptMode):
        """
        Sets the JavaScript mode of the WebView.

        Note:
            - Works only on the following platforms: iOS, Android, and macOS.
            - Disabling the JavaScript execution on the page may result to
                unexpected web page behaviour.

        Args:
            mode: The JavaScript mode to set.
        """
        self._check_mobile_or_mac_platform()
        await self._invoke_method(
            method_name="set_javascript_mode",
            arguments={"mode": mode},
        )
