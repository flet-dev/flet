import inspect
import logging
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Optional

from flet.controls.base_control import control
from flet.controls.context import _context_page, context
from flet.controls.control_event import (
    ControlEvent,
    ControlEventHandler,
    Event,
    EventHandler,
)
from flet.controls.exceptions import HostRequestRefused
from flet.controls.layout_control import LayoutControl
from flet.controls.padding import PaddingValue
from flet.controls.types import Brightness
from flet.utils.object_model import get_param_count

__all__ = [
    "FletApp",
    "FletAppGuestRequestEvent",
    "FletAppOutputEvent",
    "FletAppWindowEvent",
    "HostRequest",
]

logger = logging.getLogger("flet")


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


@dataclass
class FletAppGuestRequestEvent(Event["FletApp"]):
    """
    The embedded app asked its host to do something, with
    :meth:`Page.request_host() <flet.Page.request_host>`.

    `control` is the [`FletApp`][flet.FletApp] that runs the app that asked.
    """

    request: str
    """The request's name, for example `"fletbase.oauth"`. Names are chosen by
    the embedded app; by convention `package.action`."""

    args: Optional[dict[str, Any]] = None
    """The request's arguments. They come from the embedded app: treat them as
    untrusted input."""

    request_id: int = field(default=0, repr=False)
    """Identifies the request between the host and the embedded app."""


class HostRequest(Enum):
    """
    Special answers of a [`FletApp.on_guest_request`][flet.FletApp.on_guest_request]
    handler.
    """

    UNHANDLED = "unhandled"
    """The host doesn't handle this request: the embedded app's
    :meth:`Page.request_host() <flet.Page.request_host>` raises
    :class:`~flet.HostRequestError` with `kind` `"unhandled"`."""


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

    platform_brightness: Optional[Brightness] = None
    """
    Overrides the system light/dark appearance the embedded app sees.

    By default the embedded app follows the host's platform brightness. Set
    this to preview it as though its device were in light or dark mode: an app
    whose [`theme_mode`][flet.Page.theme_mode] is `SYSTEM` switches to its dark
    or light theme, [`page.platform_brightness`][flet.Page.platform_brightness]
    reports the value, and
    [`on_platform_brightness_change`][flet.Page.on_platform_brightness_change]
    fires when it changes. An app that forces `LIGHT` or `DARK` keeps it, as
    on a real device.

    `None` follows the host.
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

    storage_prefix: Optional[str] = None
    """
    Prefix put in front of every key the embedded app stores with
    [`SharedPreferences`][flet.SharedPreferences].

    The embedded app runs in the host's process (on web, the host's browser
    origin), so without a prefix the two would share one store, and see and
    overwrite each other's keys. The prefix is applied on the client; the app
    itself uses plain key names and never sees it.

    - `None` (default): the embedded app is isolated under a prefix derived
      from its [`url`][(c).] (or [`assets_dir`][(c).] when `url` is empty),
      `fletapp.<hash>.`. Its data is kept for as long as that location stays
      the same.
    - A string such as `"app.42."`: use that prefix. Set this when the
      embedded app's URL changes between runs (a cache-busting query, say)
      but its saved data should stay, or to give each embedded app a
      readable namespace. End it with a separator so `"app.1."` and
      `"app.12."` don't overlap.
    - `""`: share the host's keys. Only for an embedded app you trust as
      much as the host.

    The prefix nests under the host's own: if the host app itself runs under
    `"app.1."`, an embedded app with `"preview."` stores keys under
    `"app.1.preview."`, so it can never reach outside its host's space.
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

    on_guest_request: Optional[EventHandler[FletAppGuestRequestEvent]] = None
    """
    Called when the embedded app asks its host to do something, with
    :meth:`Page.request_host() <flet.Page.request_host>`.

    The handler's return value is the reply, which the embedded app gets back
    from `request_host()`. It can be anything Flet can send: `None`, numbers,
    strings, bytes, lists and dicts of them. The handler may be async and may
    take as long as it needs, for example while the user signs in.

    - Return [`HostRequest.UNHANDLED`][flet.HostRequest.UNHANDLED] for a
      request this host doesn't handle.
    - Raise :class:`~flet.HostRequestRefused` to decline it, for example when
      the user said no.
    - Any other exception fails the request; the embedded app gets its message,
      never the traceback.

    While this is not set, every request of the embedded app fails with
    `"unhandled"`, without reaching the host. Nothing is allowed by default:
    decide on each request by its name, and treat its `args` as untrusted
    input. Never let them choose what the host acts on.

    Example:
        ```python
        async def on_request(e: ft.FletAppGuestRequestEvent):
            if e.request != "share":
                return ft.HostRequest.UNHANDLED
            if not await confirm(f"Share {e.args.get('title')!r}?"):
                raise ft.HostRequestRefused("The user said no.")
            return {"shared": True}

        ft.FletApp(url=..., on_guest_request=on_request)
        ```
    """

    async def _trigger_event(
        self, event_name: str, event_data: Any, e: Optional[ControlEvent] = None
    ):
        if event_name != "guest_request" or not isinstance(event_data, dict):
            return await super()._trigger_event(event_name, event_data, e)
        event = FletAppGuestRequestEvent(
            control=self,
            name=event_name,
            request=str(event_data.get("request") or ""),
            args=event_data.get("args"),
            request_id=int(event_data.get("request_id") or 0),
        )
        # Answered in a task of its own, so a handler that takes minutes
        # doesn't hold up the host's other events.
        self.page.run_task(self._answer_guest_request, event)

    async def _answer_guest_request(self, e: FletAppGuestRequestEvent):
        """Runs `on_guest_request` for request `e` and sends its reply."""
        handler = self.on_guest_request
        session = self.page.session
        reply: dict[str, Any]
        try:
            if not callable(handler):
                result = HostRequest.UNHANDLED
            else:
                _context_page.set(self.page)
                context.reset_auto_update()
                result = handler() if get_param_count(handler) == 0 else handler(e)
                if inspect.isawaitable(result):
                    result = await result
            if result is HostRequest.UNHANDLED:
                reply = _guest_request_error(
                    "unhandled", f"The host app doesn't handle {e.request!r}."
                )
            else:
                reply = {"result": result}
        except HostRequestRefused as ex:
            reply = _guest_request_error("refused", str(ex))
        except Exception as ex:
            logger.error("Unhandled error in 'on_guest_request' handler", exc_info=True)
            reply = _guest_request_error(
                "failed", str(ex) or "The host app failed to answer."
            )
        await session.after_event(self)

        try:
            await self._send_guest_reply(e.request_id, reply)
        except (TypeError, ValueError):
            # The result can't be sent; the embedded app should still hear back.
            await self._send_guest_reply(
                e.request_id,
                _guest_request_error(
                    "failed", "The host app's answer can't be sent to the app."
                ),
            )

    async def _send_guest_reply(self, request_id: int, reply: dict[str, Any]):
        try:
            await self._invoke_method(
                "reply_guest_request", arguments={"request_id": request_id, **reply}
            )
        except RuntimeError:
            # Removed, or the session closed, while answering: the embedded
            # app has gone with it.
            logger.debug("FletApp: no one to answer guest request %s", request_id)

    async def wait_idle(
        self, idle_ms: int = 300, timeout_ms: int = 30000
    ) -> dict[str, Any]:
        """
        Waits until the embedded app has rendered its UI and gone quiet.

        Useful for a host that needs to know when the embedded app is ready,
        e.g. before taking a screenshot of it or reading its output after a
        restart.

        Args:
            idle_ms: How long, in milliseconds, the embedded app must send no
                UI updates after its first one to count as idle.
            timeout_ms: Give up after this many milliseconds.

        Returns:
            A dict with `status` and `error`. `status` is `"idle"` once the
            app sent at least one UI update, then none for `idle_ms`, and
            that update is on screen; `"error"` if the app failed to start
            or crashed (`error` holds the message; `on_error` fires as
            well); `"timeout"` if it didn't settle within `timeout_ms`, for
            example an app that updates continuously. A new call supersedes
            a pending one, which returns `"timeout"`.
        """
        return await self._invoke_method(
            "wait_idle",
            arguments={"idle_ms": idle_ms, "timeout_ms": timeout_ms},
            timeout=timeout_ms / 1000 + 5,
        )


def _guest_request_error(kind: str, message: str) -> dict[str, Any]:
    return {"error": {"kind": kind, "message": message}}
