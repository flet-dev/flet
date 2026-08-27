from dataclasses import dataclass, field
from typing import Any, Optional

from flet.controls.base_control import control
from flet.controls.control_event import ControlEventHandler, Event, EventHandler
from flet.controls.layout_control import LayoutControl
from flet.controls.padding import PaddingValue
from flet.utils.deprecated import deprecated

__all__ = ["FletApp", "FletAppOutputEvent", "FletAppWindowEvent"]


@dataclass
class FletAppOutputEvent(Event["FletApp"]):
    """One stdout/stderr line from the embedded Pyodide app."""

    text: str
    """The line of text. Pyodide line-buffers stdout/stderr by default,
    so each event is typically one `print(...)` worth of output (with
    its trailing newline)."""

    is_stderr: bool = False
    """True for stderr writes; False for stdout."""


@dataclass
class FletAppWindowEvent(Event["FletApp"]):
    """The embedded app asked its window to do something."""

    action: str
    """Either a `Window` method name (`close`, `maximize`, `minimize`,
    `center`, `destroy`, ...) or `"set"` when the app wrote window properties
    directly."""

    # Not `data`: that name is already the base Event's payload, and shadowing
    # it with a default reorders the base's own non-default fields.
    args: dict[str, Any] = field(default_factory=dict, metadata={"data_field": "data"})
    """Method arguments, or the properties written when `action` is `"set"`."""


@control("FletApp")
class FletApp(LayoutControl):
    """
    Renders another Flet app in the current app, similar to HTML IFrame, but for Flet.
    """

    url: Optional[str] = None
    """
    Flet app URL, e.g. `http://localhost:8550` or `flet.sock`.
    """

    args: Optional[dict[str, Any]] = None
    """
    Optional dictionary of arguments to pass to the Flet app.
    """

    route: Optional[str] = None
    """
    The embedded app's current route.

    Two-way: setting it navigates the embedded app, and when the embedded app
    navigates itself this property is updated to match and
    [`on_route_change`][(c).] fires. Leave it `None` to let the embedded app
    own its own routing.

    Note:
        The embedded app routes locally - it never touches the browser address
        bar or the platform's deep links, both of which belong to the host app.
    """

    title: Optional[str] = None
    """
    The embedded app's `page.title`.

    Written by the client whenever the embedded app sets its title, together
    with [`on_title_change`][(c).]. A guest's title belongs to whatever window
    its host draws around it - it does not touch the real OS window, because
    the window service is suppressed for embedded apps.
    """

    window_state: Optional[dict[str, Any]] = None
    """
    The simulated window the embedded app should believe it lives in.

    Keys are [`Window`][flet.Window] property names - `width`, `height`,
    `top`, `left`, `maximized`, `minimized`, `full_screen`, `focused`. What
    you set here is what the embedded app reads back from `page.window`, and
    changing it raises the matching `page.window.on_event` inside the app
    (`resize`, `maximize`, `focus`, ...) exactly as a real window would.

    An embedded app never drives the real OS window, so without this its
    `page.window` is inert.
    """

    media_padding: Optional[PaddingValue] = None
    """
    Overrides the safe-area insets the embedded app sees.

    The embedded app normally inherits the host window's `MediaQuery`, so on a
    desktop window its insets are zero regardless of what the app is being
    previewed as. Setting this makes the embedded app lay out as though it had
    those insets: `page.media.padding` reports them, and
    [`SafeArea`][flet.SafeArea] avoids them.

    Intended for previewing a phone layout inside a desktop window - a device
    frame in a designer, say - where the chrome drawn around the app is not
    something the platform knows about.
    """

    assets_dir: Optional[str] = None
    """
    Base location for assets referenced by the embedded app. On web this
    is a URL prefix joined with relative `src` values (e.g. on
    `Image`/`Lottie`/`Markdown`); on desktop it is a filesystem path.
    """

    force_pyodide: bool = False
    """
    Whether to force the use of Pyodide.
    """

    reconnect_interval_ms: Optional[int] = None
    """
    Delay, in milliseconds, between reconnection attempts.
    """

    reconnect_timeout_ms: Optional[int] = None
    """
    Total time to try reconnecting.
    """

    boot_screen_name: Optional[str] = None
    """
    Name of the boot screen to show while the embedded app starts up.

    When `None`, the built-in `"flet"` boot screen is used. Custom boot screens
    are provided by extensions; see the
    [boot screen docs](https://flet.dev/docs/publish/#boot-screen).
    """

    boot_screen_options: Optional[dict[str, Any]] = None
    """
    Options for the boot screen, passed through to the boot screen widget.

    For the built-in `"flet"` screen these include `spinner_size`,
    `startup_message`, `bgcolor_light`/`bgcolor_dark`, etc. See the
    [boot screen docs](https://flet.dev/docs/publish/#boot-screen).
    """

    app_error_message: Optional[str] = None
    """
    Template message to display when the app fails to load.
    Use `{message}` placeholder to include the error message
    and `{details}` to include error details.
    """

    on_error: Optional[ControlEventHandler["FletApp"]] = None
    """
    Called when a connection or any unhandled error occurs.
    """

    on_title_change: Optional[ControlEventHandler["FletApp"]] = None
    """
    Called when the embedded app sets `page.title`. The event `data` is the new
    title, which is also written back to [`title`][(c).].
    """

    on_window_event: Optional[EventHandler[FletAppWindowEvent]] = None
    """
    Called when the embedded app asks its window to do something - a method
    call like `page.window.close()`, or a property write like
    `page.window.maximized = True`.

    A request, not a command: nothing happens unless the host acts on it, which
    is how a host that does not simulate, say, minimizing simply ignores it.
    """

    on_route_change: Optional[ControlEventHandler["FletApp"]] = None
    """
    Called when the embedded app navigates itself. The event `data` is the new
    route, which is also written back to [`route`][(c).].

    Does not fire for navigation the host itself caused by setting
    [`route`][(c).].
    """

    on_connect: Optional[ControlEventHandler["FletApp"]] = None
    """
    Fires when the client allocates an in-process `dart_bridge` channel for this
    embedded app (`url="dartbridge://"`). The event `data` is the Dart native
    port the host must serve with a `FletDartBridgeServer` so the embedded app
    connects over it instead of a socket.

    Advanced / embedder use — hosts that run another Flet program in-process
    (e.g. a gallery or preview) start their server on this port in the handler.
    """

    on_python_output: Optional[EventHandler[FletAppOutputEvent]] = None
    """
    Fires once per stdout/stderr write inside the embedded Pyodide app.
    Pyodide line-buffers by default, so each event is typically one
    `print(...)` call. Only fires for embedded FletApps with
    `force_pyodide=True`; root-level Pyodide pages have nowhere to
    bubble the event.
    """

    @property
    @deprecated(
        reason="Use `boot_screen_options` instead, e.g. "
        "boot_screen_options={'spinner_size': 30}.",
        version="0.86.0",
        delete_version="0.89.0",
    )
    def show_app_startup_screen(self) -> bool:
        """
        Whether to show the app startup screen.
        """
        return bool((self.boot_screen_options or {}).get("spinner_size", 0))

    @show_app_startup_screen.setter
    @deprecated(
        reason="Use `boot_screen_options` instead, e.g. "
        "boot_screen_options={'spinner_size': 30}.",
        version="0.86.0",
        delete_version="0.89.0",
    )
    def show_app_startup_screen(self, value: bool) -> None:
        options = dict(self.boot_screen_options or {})
        if value:
            options.setdefault("spinner_size", 30)
        else:
            options.pop("spinner_size", None)
        self.boot_screen_options = options

    @property
    @deprecated(
        reason="Use `boot_screen_options` instead, e.g. "
        "boot_screen_options={'startup_message': '...'}.",
        version="0.86.0",
        delete_version="0.89.0",
    )
    def app_startup_screen_message(self) -> Optional[str]:
        """
        Message to display on the app startup screen.
        """
        return (self.boot_screen_options or {}).get("startup_message")

    @app_startup_screen_message.setter
    @deprecated(
        reason="Use `boot_screen_options` instead, e.g. "
        "boot_screen_options={'startup_message': '...'}.",
        version="0.86.0",
        delete_version="0.89.0",
    )
    def app_startup_screen_message(self, value: Optional[str]) -> None:
        options = dict(self.boot_screen_options or {})
        if value is not None:
            options["startup_message"] = value
        else:
            options.pop("startup_message", None)
        self.boot_screen_options = options
