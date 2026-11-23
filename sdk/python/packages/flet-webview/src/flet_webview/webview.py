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
        - On Windows this control requires the Edge WebView2 runtime, which
          ships with Windows 11 and is present on most Windows 10 installations.
        - On Linux it requires `libwebkit2gtk-4.1-0`, which is available from
          Debian 12 and Ubuntu 22.04 (with current updates) onward.
        - On Linux the WebView is a native GTK widget rather than a Flutter
          texture: other controls cannot be drawn over it, and a scale, rotation
          or skew transform hides it entirely. Rectangular clips and the rounded
          corners of a `Card` apply to it, but other clips, such as a `Container`
          with `border_radius` or a circular `shape`, hide it entirely.
        - On web the page is shown in an `<iframe>`. Pages that forbid being
          embedded, and pages from another origin that do not allow embedding
          under the `Cross-Origin-Embedder-Policy: require-corp` header Flet's
          web server sends, stay blank.
        - On web the browser keeps the app from scripting or observing pages
          from another origin, so JavaScript, the page title, scrolling, console
          messages and alerts are available only for same-origin pages and for
          HTML loaded with :meth:`load_html`.
    """

    url: Optional[str] = None
    """
    The URL of the web page to load.

    Changing it loads the new URL. To load the same URL again, call
    :meth:`reload` or :meth:`load_request`.

    Note:
        A `file://` URL pointing to a local file loads that file's sibling
        assets (scripts, stylesheets, images) as well, and is equivalent to
        calling :meth:`load_file` with the same file once this control is
        mounted. It is not supported on web.
    """

    prevent_links: Optional[list[str]] = None
    """
    List of url-prefixes that should not be followed/loaded/downloaded.

    Note:
        - On Windows, while this list is not empty, every allowed navigation is
          restarted as a `GET` request, so a form submitted with `POST` loses
          its data.
        - On web only the pages the app loads itself are checked, not links
          followed inside the page.
    """

    bgcolor: Optional[ft.ColorValue] = None
    """
    Defines the background color of the WebView.

    Note:
        On macOS this colors only the area around the page, which shows when
        scrolling past its edges.
    """

    on_page_started: Optional[ft.ControlEventHandler["WebView"]] = None
    """
    Fires soon as the first loading process of the webview page is started.

    The :attr:`~flet.Event.data` property of the event handler argument is of type
    `str` and contains the URL.

    Note:
        On web this fires only for the pages the app loads itself, not for links
        followed inside the page.
    """

    on_page_ended: Optional[ft.ControlEventHandler["WebView"]] = None
    """
    Fires when all the webview page loading processes are ended.

    The :attr:`~flet.Event.data` property of the event handler argument is of type
    `str` and contains the URL.

    Note:
        - On web this also fires when the browser refused to show the page.
        - On web with the
          [`canvaskit` renderer](https://flet.dev/docs/publish/web/static-website/#web-renderer),
          while :attr:`on_scroll` is set, this does not fire for a page from
          another origin or for a `POST` response.
    """

    on_web_resource_error: Optional[ft.ControlEventHandler["WebView"]] = None
    """
    Fires when there is error with loading a webview page resource.

    The :attr:`~flet.Event.data` property of the event handler argument is of type
    `str` and contains the error message.

    Note:
        - It also fires when :attr:`url` cannot be loaded, for example a URL
          without a scheme.
        - It also fires for a certificate error, and the page is not loaded.
          On web the browser handles certificate errors itself.
        - On web it otherwise fires only for requests made with
          :attr:`~flet_webview.RequestMethod.POST`. The browser does not report
          why a page shown in an `<iframe>` failed to load.
    """

    on_progress: Optional[ft.ControlEventHandler["WebView"]] = None
    """
    Fires when the progress of the webview page loading is changed.

    The :attr:`~flet.Event.data` property of the event handler argument is of type
    `int` and contains the progress value.

    Note:
        - On Windows and web the progress is only ever `0` or `100`.
        - On web with the
          [`canvaskit` renderer](https://flet.dev/docs/publish/web/static-website/#web-renderer),
          while :attr:`on_scroll` is set, a page from another origin reports
          only `0`, and :attr:`on_page_ended` does not fire for it.
    """

    on_url_change: Optional[ft.ControlEventHandler["WebView"]] = None
    """
    Fires when the URL of the webview page is changed.

    The :attr:`~flet.Event.data` property of the event handler argument is of type
    `str` and contains the new URL.

    Note:
        On web, after a link is followed to another origin, this reports the last
        URL it could read, usually that of the page the app last loaded.
    """

    on_scroll: Optional[ft.EventHandler[WebViewScrollEvent]] = None
    """
    Fires when the web page's scroll position changes.

    Note:
        - Not supported on macOS.
        - On web it fires only for same-origin pages and HTML loaded with
          :meth:`load_html`.
        - On web with the
          [`canvaskit` renderer](https://flet.dev/docs/publish/web/static-website/#web-renderer),
          setting this handler keeps :attr:`on_page_ended` from firing for pages
          from another origin and for `POST` responses. `canvaskit` is the
          default for static web apps, and the renderer `auto` picks in browsers
          not based on Chromium.
        - On Android :attr:`~flet_webview.WebViewScrollEvent.x` and
          :attr:`~flet_webview.WebViewScrollEvent.y` are physical pixels: the
          page's `window.scrollX` and `window.scrollY` multiplied by
          `window.devicePixelRatio`.
    """

    on_console_message: Optional[ft.EventHandler[WebViewConsoleMessageEvent]] = None
    """
    Fires when a log message is written to the JavaScript console.

    Note:
        - On Windows, iOS and macOS a handler set after the control was added to
          the page receives messages from the next page loaded.
        - On Linux :attr:`~flet_webview.WebViewConsoleMessageEvent.severity_level`
          is always :attr:`~flet_webview.LogLevelSeverity.LOG`.
        - On Android `console.info()` messages have the
          :attr:`~flet_webview.LogLevelSeverity.LOG` severity level.
        - On web only messages logged after :attr:`on_page_ended` fired are
          delivered.
    """

    on_javascript_alert_dialog: Optional[ft.EventHandler[WebViewJavaScriptEvent]] = None
    """
    Fires when the web page attempts to display a JavaScript alert() dialog.

    Note:
        - Not supported on Windows, where Edge WebView2 always shows its own
          alert dialog.
        - On iOS and macOS `alert()` shows nothing unless this handler is set.
        - Setting this handler replaces the built-in alert dialog on Android,
          Linux and web, so the app becomes responsible for showing the
          message. The built-in dialog stays off after the handler is removed.
        - On web `alert()` does not block the page's script while this handler
          is set, and an alert raised before :attr:`on_page_ended` fired still
          opens the browser's dialog.
    """

    async def reload(self):
        """
        Reloads the current URL.

        Note:
            On web, after a link was followed to another origin, this reloads
            the last page whose URL it could read instead.
        """
        await self._invoke_method("reload")

    async def can_go_back(self) -> bool:
        """
        Whether there's a back history item.

        Note:
            On web the history contains only the pages the app loaded itself.

        Returns:
            `True` if there is a back history item, `False` otherwise.
        """
        return await self._invoke_method("can_go_back")

    async def can_go_forward(self) -> bool:
        """
        Whether there's a forward history item.

        Note:
            On web the history contains only the pages the app loaded itself.

        Returns:
            `True` if there is a forward history item, `False` otherwise.
        """
        return await self._invoke_method("can_go_forward")

    async def go_back(self):
        """
        Goes back in the history of the webview, if `can_go_back()` is `True`.

        Note:
            On web the history contains only the pages the app loaded itself.
        """
        await self._invoke_method("go_back")

    async def go_forward(self):
        """
        Goes forward in the history of the webview,
        if :meth:`can_go_forward` is `True`.

        Note:
            On web the history contains only the pages the app loaded itself.
        """
        await self._invoke_method("go_forward")

    async def enable_zoom(self):
        """
        Enables zooming using the on-screen zoom controls and gestures.
        """
        await self._invoke_method("enable_zoom")

    async def disable_zoom(self):
        """
        Disables zooming using the on-screen zoom controls and gestures.
        """
        await self._invoke_method("disable_zoom")

    async def clear_cache(self):
        """
        Clears all caches used by the WebView.

        The following caches are cleared:
            - Browser HTTP Cache
            - Cache API caches. Service workers tend to use this cache.
            - Application cache

        Note:
            - Not supported on web, where the WebView shares its caches with the
              app itself.
            - On Windows and Linux only the HTTP cache is cleared.

        Raises:
            FletUnsupportedPlatformException: If invoked on web.
        """
        if self.page.web:
            raise ft.FletUnsupportedPlatformException(
                "clear_cache is not supported on web"
            )
        await self._invoke_method("clear_cache")

    async def clear_local_storage(self):
        """
        Clears the local storage used by the WebView.

        Note:
            - Not supported on web, where the WebView shares its storage with the
              app itself.
            - On Windows this also clears IndexedDB and Cache API storage, for
              every WebView of the app.

        Raises:
            FletUnsupportedPlatformException: If invoked on web.
        """
        if self.page.web:
            raise ft.FletUnsupportedPlatformException(
                "clear_local_storage is not supported on web"
            )
        await self._invoke_method("clear_local_storage")

    async def get_current_url(self) -> Optional[str]:
        """
        Gets the current URL that the WebView is displaying or `None`
        if no URL was ever loaded.

        Note:
            On web, after a link is followed to another origin, this returns the
            last URL it could read, usually that of the page the app last
            loaded.

        Returns:
            The current URL that the WebView is displaying or `None`
                if no URL was ever loaded.
        """
        return await self._invoke_method("get_current_url")

    async def get_title(self) -> Optional[str]:
        """
        Get the title of the currently loaded page.

        Note:
            On web this is `None` for a page from another origin.

        Returns:
            The title of the currently loaded page.
        """
        return await self._invoke_method("get_title")

    async def get_user_agent(self) -> Optional[str]:
        """
        Get the value used for the HTTP `User-Agent:` request header.

        Note:
            On web this is the user agent of the browser running the app.

        Returns:
            The value used for the HTTP `User-Agent:` request header.
        """
        return await self._invoke_method("get_user_agent")

    async def load_file(self, path: str):
        """
        Loads the provided local file.

        Note:
            - Not supported on web.
            - On Windows the page is opened from its `file://` URL. It can load
              the stylesheets, scripts and images it links to, but it cannot
              read local files with `fetch()` or `XMLHttpRequest`, or load
              JavaScript modules (`<script type="module">`).

        Args:
            path: The absolute path to the file.

        Raises:
            FletUnsupportedPlatformException: If invoked on web.
        """
        if self.page.web:
            raise ft.FletUnsupportedPlatformException(
                "load_file is not supported on web"
            )
        await self._invoke_method(
            method_name="load_file",
            arguments={"path": path},
        )

    async def load_request(self, url: str, method: RequestMethod = RequestMethod.GET):
        """
        Makes an HTTP request and loads the response in the webview.

        Args:
            url: The URL to load. A `file://` URL is loaded as a local file,
                the same way :meth:`load_file` does, except on web.
            method: The HTTP method to use. Ignored for `file://` URLs.

        Note:
            - On Linux a :attr:`~flet_webview.RequestMethod.POST` request is sent
              outside the WebView and its response is then shown in it, so a
              failed request raises an error rather than firing
              :attr:`on_web_resource_error`.
            - On web a :attr:`~flet_webview.RequestMethod.POST` request is sent
              by the app itself, so the browser's cross-origin (CORS) rules apply
              to it.
            - On Windows a :attr:`~flet_webview.RequestMethod.POST` request fails
              and fires :attr:`on_web_resource_error`, because it is sent without
              a body.
        """
        await self._invoke_method(
            "load_request", arguments={"url": url, "method": method}
        )

    async def run_javascript(self, value: str):
        """
        Runs the given JavaScript in the context of the current page.

        Args:
            value: The JavaScript code to run.

        Note:
            On web this works only for a same-origin page or HTML loaded with
            :meth:`load_html`.
        """
        await self._invoke_method(
            method_name="run_javascript",
            arguments={"value": value},
        )

    async def load_html(self, value: str, base_url: Optional[str] = None) -> Self:
        """
        Loads the provided HTML string.

        Note:
            On web the HTML runs with the app's own origin, so its scripts can
            read and change the app's storage and cookies. Load only HTML you
            trust there.

        Args:
            value: The HTML string to load.
            base_url: The base URL to use when resolving relative URLs within the value.
                May be a `file://` URL, in which case the referenced local files are
                made readable to the webview, except on Windows and web.
        """
        await self._invoke_method(
            "load_html", arguments={"value": value, "base_url": base_url}
        )

        return self

    async def scroll_to(self, x: int, y: int):
        """
        Scrolls to the provided position of webview pixels.

        Note:
            - Not supported on macOS.
            - On Android the position is in physical pixels: the page's
              `window.scrollY` becomes `y` divided by `window.devicePixelRatio`.
            - On web this works only for a same-origin page or HTML loaded with
              :meth:`load_html`.

        Args:
            x: The x-coordinate of the scroll position.
            y: The y-coordinate of the scroll position.

        Raises:
            FletUnsupportedPlatformException: If invoked on macOS.
        """
        if not self.page.web and self.page.platform == ft.PagePlatform.MACOS:
            raise ft.FletUnsupportedPlatformException(
                "scroll_to is not supported on macOS"
            )
        await self._invoke_method(
            method_name="scroll_to",
            arguments={"x": x, "y": y},
        )

    async def scroll_by(self, x: int, y: int):
        """
        Scrolls by the provided number of webview pixels.

        Note:
            - Not supported on macOS.
            - On Android the amounts are physical pixels, so the page scrolls by
              `y` divided by `window.devicePixelRatio` CSS pixels.
            - On web this works only for a same-origin page or HTML loaded with
              :meth:`load_html`.

        Args:
            x: The number of pixels to scroll by on the x-axis.
            y: The number of pixels to scroll by on the y-axis.

        Raises:
            FletUnsupportedPlatformException: If invoked on macOS.
        """
        if not self.page.web and self.page.platform == ft.PagePlatform.MACOS:
            raise ft.FletUnsupportedPlatformException(
                "scroll_by is not supported on macOS"
            )
        await self._invoke_method(
            method_name="scroll_by",
            arguments={"x": x, "y": y},
        )

    async def set_javascript_mode(self, mode: JavaScriptMode):
        """
        Sets the JavaScript mode of the WebView.

        Note:
            - Disabling the JavaScript execution on the page may result to
                unexpected web page behaviour.
            - Defaults to :attr:`flet_webview.JavaScriptMode.UNRESTRICTED`,
                which is applied before the first page load.
            - On Windows, iOS, macOS and web the mode applies from the next page
              loaded.

        Args:
            mode: The JavaScript mode to set.
        """
        await self._invoke_method(
            method_name="set_javascript_mode",
            arguments={"mode": mode},
        )
