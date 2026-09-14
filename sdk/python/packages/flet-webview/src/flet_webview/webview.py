import sys
from typing import Optional

if sys.version_info >= (3, 11):
    from typing import Self
else:
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
        On Linux the WebView is a native GTK widget rather than a Flutter texture,
        which constrains how it can be placed: other controls cannot be drawn over
        it, and a scale, rotation or skew transform — or a non-rectangular clip,
        such as a `Container.border_radius` or an enclosing `Card` — hides it
        entirely rather than merely leaving the corners square. Linux also has no
        WebAuthn/passkey support.

        Running a Linux app that uses this control requires `libwebkit2gtk-4.1-0`,
        which is unavailable before Debian 12 and Ubuntu 22.04. On Windows it
        requires the Edge WebView2 runtime, which ships with Windows 11 and is
        present on most, but not all, Windows 10 installations.
    """

    url: Optional[str] = None
    """
    The URL of the web page to load.

    Note:
        A `file://` URL pointing to a local file is not supported on the web
        platform, where only URLs the browser can load in an iframe work. On
        every other platform it loads that file's sibling assets (scripts,
        stylesheets, images) as well, and is equivalent to calling
        :meth:`load_file` with the same file once this control is mounted.

        On Windows the file is served from an internal virtual host, so
        :meth:`get_current_url` and :attr:`on_url_change` report an
        `https://...webview.invalid/` URL rather than the original `file://` one.
    """

    prevent_links: Optional[list[str]] = None
    """List of url-prefixes that should not be followed/loaded/downloaded."""

    bgcolor: Optional[ft.ColorValue] = None
    """Defines the background color of the WebView."""

    on_page_started: Optional[ft.ControlEventHandler["WebView"]] = None
    """
    Fires soon as the first loading process of the webview page is started.

    The :attr:`~flet.Event.data` property of the event handler argument is of type
    `str` and contains the URL.

    Note:
        Not supported on the web platform.
    """

    on_page_ended: Optional[ft.ControlEventHandler["WebView"]] = None
    """
    Fires when all the webview page loading processes are ended.

    The :attr:`~flet.Event.data` property of the event handler argument is of type
    `str` and contains the URL.

    Note:
        Not supported on the web platform.
    """

    on_web_resource_error: Optional[ft.ControlEventHandler["WebView"]] = None
    """
    Fires when there is error with loading a webview page resource.

    The :attr:`~flet.Event.data` property of the event handler argument is of type
    `str` and contains the error message.

    Note:
        Not supported on the web platform.
    """

    on_progress: Optional[ft.ControlEventHandler["WebView"]] = None
    """
    Fires when the progress of the webview page loading is changed.

    The :attr:`~flet.Event.data` property of the event handler argument is of type
    `int` and contains the progress value.

    Note:
        Not supported on the web platform.
    """

    on_url_change: Optional[ft.ControlEventHandler["WebView"]] = None
    """
    Fires when the URL of the webview page is changed.

    The :attr:`~flet.Event.data` property of the event handler argument is of type
    `str` and contains the new URL.

    Note:
        Not supported on the web platform.
    """

    on_scroll: Optional[ft.EventHandler[WebViewScrollEvent]] = None
    """
    Fires when the web page's scroll position changes.

    Note:
        Not supported on the following platforms: macOS and web.

        On Windows and Linux this is delivered by an injected script that reports
        the scroll position of the document only, so scrolling inside a nested
        overflow container does not fire it. Setting
        :attr:`~flet_webview.JavaScriptMode.DISABLED` disables it there.
    """

    on_console_message: Optional[ft.EventHandler[WebViewConsoleMessageEvent]] = None
    """
    Fires when a log message is written to the JavaScript console.

    Note:
        Not supported on the web platform.

        On Windows and Linux this is delivered by an injected script, so setting
        :attr:`~flet_webview.JavaScriptMode.DISABLED` disables it. On Linux
        :attr:`~flet_webview.WebViewConsoleMessageEvent.severity_level` is always
        :attr:`~flet_webview.LogLevelSeverity.LOG`, whichever `console` method
        the page called.
    """

    on_javascript_alert_dialog: Optional[ft.EventHandler[WebViewJavaScriptEvent]] = None
    """
    Fires when the web page attempts to display a JavaScript alert() dialog.

    Note:
        Not supported on the following platforms: Windows and web. On Windows,
        Edge WebView2 always shows its own alert dialog and does not surface the
        request.

        Setting this handler suppresses the platform's built-in alert dialog on
        Linux, so the app becomes responsible for showing one. Leave it unset to
        keep the native dialog.
    """

    def _check_platform_support(self):
        """
        Checks/Validates that the current platform supports the `WebView` methods.

        Every native platform is supported, so only the web platform is rejected:
        `webview_web.dart` registers no invoke-method listener, so none of these
        methods have anything to call there.

        Raises:
            RuntimeError: If this control has not been added to a page yet.
            FletUnsupportedPlatformException: If the app is running on the web.
        """
        if self.page is None:
            raise RuntimeError("WebView must be added to page first.")
        if self.page.web:
            raise ft.FletUnsupportedPlatformException(
                "This method is not supported on the web platform."
            )

    async def reload(self):
        """
        Reloads the current URL.

        Note:
            Not supported on the web platform.
        """
        self._check_platform_support()
        await self._invoke_method("reload")

    async def can_go_back(self) -> bool:
        """
        Whether there's a back history item.

        Note:
            Not supported on the web platform.

        Returns:
            `True` if there is a back history item, `False` otherwise.
        """
        self._check_platform_support()
        return await self._invoke_method("can_go_back")

    async def can_go_forward(self) -> bool:
        """
        Whether there's a forward history item.

        Note:
            Not supported on the web platform.

        Returns:
            `True` if there is a forward history item, `False` otherwise.
        """
        self._check_platform_support()
        return await self._invoke_method("can_go_forward")

    async def go_back(self):
        """
        Goes back in the history of the webview, if `can_go_back()` is `True`.

        Note:
            Not supported on the web platform.
        """
        self._check_platform_support()
        await self._invoke_method("go_back")

    async def go_forward(self):
        """
        Goes forward in the history of the webview,
        if :meth:`can_go_forward` is `True`.

        Note:
            Not supported on the web platform.
        """
        self._check_platform_support()
        await self._invoke_method("go_forward")

    async def enable_zoom(self):
        """
        Enables zooming using the on-screen zoom controls and gestures.

        Note:
            Not supported on the web platform.
        """
        self._check_platform_support()
        await self._invoke_method("enable_zoom")

    async def disable_zoom(self):
        """
        Disables zooming using the on-screen zoom controls and gestures.

        Note:
            Not supported on the web platform.
        """
        self._check_platform_support()
        await self._invoke_method("disable_zoom")

    async def clear_cache(self):
        """
        Clears all caches used by the WebView.

        The following caches are cleared:
            - Browser HTTP Cache
            - Cache API caches. Service workers tend to use this cache.
            - Application cache

        Note:
            Not supported on the web platform.
        """
        self._check_platform_support()
        await self._invoke_method("clear_cache")

    async def clear_local_storage(self):
        """
        Clears the local storage used by the WebView.

        Note:
            Not supported on the web platform.
        """
        self._check_platform_support()
        await self._invoke_method("clear_local_storage")

    async def get_current_url(self) -> Optional[str]:
        """
        Gets the current URL that the WebView is displaying or `None`
        if no URL was ever loaded.

        Note:
            Not supported on the web platform.

        Returns:
            The current URL that the WebView is displaying or `None`
                if no URL was ever loaded.
        """
        self._check_platform_support()
        return await self._invoke_method("get_current_url")

    async def get_title(self) -> Optional[str]:
        """
        Get the title of the currently loaded page.

        Note:
            Not supported on the web platform.

        Returns:
            The title of the currently loaded page.
        """
        self._check_platform_support()
        return await self._invoke_method("get_title")

    async def get_user_agent(self) -> Optional[str]:
        """
        Get the value used for the HTTP `User-Agent:` request header.

        Note:
            Not supported on the web platform.

        Returns:
            The value used for the HTTP `User-Agent:` request header.
        """
        self._check_platform_support()
        return await self._invoke_method("get_user_agent")

    async def load_file(self, path: str):
        """
        Loads the provided local file.

        Note:
            Not supported on the web platform.

        Args:
            path: The absolute path to the file.
        """
        self._check_platform_support()
        await self._invoke_method(
            method_name="load_file",
            arguments={"path": path},
        )

    async def load_request(self, url: str, method: RequestMethod = RequestMethod.GET):
        """
        Makes an HTTP request and loads the response in the webview.

        Args:
            url: The URL to load. A `file://` URL is loaded as a local file,
                the same way :meth:`load_file` does.
            method: The HTTP method to use. Ignored for `file://` URLs.

        Note:
            Not supported on the web platform.
        """
        self._check_platform_support()
        await self._invoke_method(
            "load_request", arguments={"url": url, "method": method}
        )

    async def run_javascript(self, value: str):
        """
        Runs the given JavaScript in the context of the current page.

        Args:
            value: The JavaScript code to run.

        Note:
            Not supported on the web platform.
        """
        self._check_platform_support()
        await self._invoke_method(
            method_name="run_javascript",
            arguments={"value": value},
        )

    async def load_html(self, value: str, base_url: Optional[str] = None) -> Self:
        """
        Loads the provided HTML string.

        Note:
            Not supported on the web platform.

        Args:
            value: The HTML string to load.
            base_url: The base URL to use when resolving relative URLs within the value.
                May be a `file://` URL, in which case the referenced local files are
                made readable to the webview — except on Windows, where relative
                local resources are blocked regardless, and where a `<base href>`
                tag is spliced into `value` to emulate this argument (overriding
                any `<base>` the HTML already declares).
        """
        self._check_platform_support()
        await self._invoke_method(
            "load_html", arguments={"value": value, "base_url": base_url}
        )

        return self

    async def scroll_to(self, x: int, y: int):
        """
        Scrolls to the provided position of webview pixels.

        Note:
            Not supported on the web platform.

        Args:
            x: The x-coordinate of the scroll position.
            y: The y-coordinate of the scroll position.
        """
        self._check_platform_support()
        await self._invoke_method(
            method_name="scroll_to",
            arguments={"x": x, "y": y},
        )

    async def scroll_by(self, x: int, y: int):
        """
        Scrolls by the provided number of webview pixels.

        Note:
            Not supported on the web platform.

        Args:
            x: The number of pixels to scroll by on the x-axis.
            y: The number of pixels to scroll by on the y-axis.
        """
        self._check_platform_support()
        await self._invoke_method(
            method_name="scroll_by",
            arguments={"x": x, "y": y},
        )

    async def set_javascript_mode(self, mode: JavaScriptMode):
        """
        Sets the JavaScript mode of the WebView.

        Note:
            - Not supported on the web platform.
            - Disabling the JavaScript execution on the page may result to
                unexpected web page behaviour.
            - Defaults to :attr:`flet_webview.JavaScriptMode.UNRESTRICTED`,
                which is applied before the first page load.

        Args:
            mode: The JavaScript mode to set.
        """
        self._check_platform_support()
        await self._invoke_method(
            method_name="set_javascript_mode",
            arguments={"mode": mode},
        )
