import asyncio
import inspect
import logging
import sys
import threading
import weakref
from collections.abc import Awaitable, Coroutine
from concurrent.futures import CancelledError, Future, ThreadPoolExecutor
from dataclasses import InitVar, dataclass, field
from functools import partial
from typing import (
    TYPE_CHECKING,
    Any,
    Callable,
    Optional,
    TypeVar,
    Union,
)
from urllib.parse import urlparse

from flet.auth.authorization import Authorization
from flet.auth.oauth_provider import OAuthProvider
from flet.components.component import Renderer
from flet.components.public_utils import unwrap_component
from flet.controls.base_control import BaseControl, control
from flet.controls.base_page import BasePage
from flet.controls.context import _context_page, context
from flet.controls.control import Control
from flet.controls.control_event import (
    ControlEvent,
    ControlEventHandler,
    Event,
    EventHandler,
)
from flet.controls.core.view import View
from flet.controls.core.window import Window
from flet.controls.device_info import (
    AndroidDeviceInfo,
    DeviceInfo,
    IosDeviceInfo,
    LinuxDeviceInfo,
    MacOsDeviceInfo,
    WebDeviceInfo,
    WindowsDeviceInfo,
)
from flet.controls.exceptions import FletUnsupportedPlatformException
from flet.controls.multi_view import MultiView
from flet.controls.query_string import QueryString
from flet.controls.ref import Ref
from flet.controls.services.browser_context_menu import BrowserContextMenu
from flet.controls.services.clipboard import Clipboard
from flet.controls.services.service import Service
from flet.controls.services.shared_preferences import SharedPreferences
from flet.controls.services.storage_paths import StoragePaths
from flet.controls.services.url_launcher import UrlLauncher
from flet.controls.types import (
    AppLifecycleState,
    Brightness,
    DeviceOrientation,
    PagePlatform,
    Url,
    UrlTarget,
    Wrapper,
)
from flet.utils import is_pyodide
from flet.utils.deprecated import deprecated
from flet.utils.from_dict import from_dict
from flet.utils.strings import random_string

if not is_pyodide():
    from flet.auth.authorization_service import AuthorizationService

    AuthorizationImpl = AuthorizationService
else:
    AuthorizationImpl = Authorization

if TYPE_CHECKING:
    from flet.messaging.session import Session
    from flet.pubsub.pubsub_client import PubSubClient

try:
    from typing import ParamSpec
except ImportError:
    from typing_extensions import ParamSpec


logger = logging.getLogger("flet")


AT = TypeVar("AT", bound=Authorization)
InputT = ParamSpec("InputT")
RetT = TypeVar("RetT")


@control("ServiceRegistry")
class ServiceRegistry(Service):
    _services: list[Service] = field(default_factory=list)

    def __post_init__(self, ref: Optional[Ref[Any]]):
        super().__post_init__(ref)
        self._internals["uid"] = random_string(10)
        self._lock: threading.Lock = threading.Lock()

    def register_service(self, service: Service):
        with self._lock:
            logger.debug(
                f"Registering service {service._c}({service._i}) to registry {self._i}"
            )
            self._services.append(service)
            self.update()

    def unregister_services(self):
        with self._lock:
            original_len = len(self._services)
            min_refs = 3 if sys.version_info >= (3, 14) else 4
            self._services = [
                service
                for service in self._services
                if sys.getrefcount(service) > min_refs
            ]
            removed_count = original_len - len(self._services)
            if removed_count > 0:
                logger.debug(f"Removed {removed_count} services from the registry")
                self.update()


@dataclass
class RouteChangeEvent(Event["Page"]):
    route: str


@dataclass
class PlatformBrightnessChangeEvent(Event["Page"]):
    brightness: Brightness


@dataclass
class ViewPopEvent(Event["Page"]):
    route: str
    view: Optional[View] = None


@dataclass
class KeyboardEvent(Event["Page"]):
    key: str
    shift: bool
    ctrl: bool
    alt: bool
    meta: bool


@dataclass
class LoginEvent(Event["Page"]):
    error: Optional[str]
    error_description: Optional[str]


@dataclass
class InvokeMethodResults:
    method_id: str
    result: Optional[str]
    error: Optional[str]


@dataclass
class AppLifecycleStateChangeEvent(Event["Page"]):
    state: AppLifecycleState


@dataclass
class MultiViewAddEvent(Event["Page"]):
    view_id: int
    initial_data: Any


@dataclass
class MultiViewRemoveEvent(Event["Page"]):
    view_id: int


@control("Page", isolated=True, post_init_args=2)
class Page(BasePage):
    """
    Page is a container for [`View`][flet.] controls.

    A page instance and the root view are automatically created when a new
    user session started.
    """

    sess: InitVar["Session"]
    """
    The session that this page belongs to.
    """

    multi_views: list[MultiView] = field(default_factory=list)
    """
    The list of multi-views associated with this page.
    """

    window: Window = field(default_factory=lambda: Window())
    """
    Provides properties/methods/events to monitor and control the
    app's native OS window.
    """

    route: str = "/"
    """
    Gets current app route.

    Note:
        This property is read-only.
    """

    web: bool = False
    """
    `True` if the application is running in the web browser.

    Note:
        This property is read-only.
    """

    pwa: bool = False
    """
    `True` if the application is running as Progressive Web App (PWA).

    Note:
        This property is read-only.
    """
    debug: bool = False
    """
    `True` if Flutter client of Flet app is running in debug mode.

    Note:
        This property is read-only.
    """

    wasm: bool = False
    """
    `True` if the application is running in WebAssembly (WASM) mode.

    Note:
        This property is read-only.
    """

    test: bool = False
    """
    `True` if the application is running with test mode.

    Note:
        This property is read-only.
    """

    multi_view: bool = False
    """
    `True` if the application is running with multi-view support.

    Note:
        This property is read-only.
    """

    pyodide: bool = False
    """
    `True` if the application is running in Pyodide (WebAssembly) mode.

    Note:
        This property is read-only.
    """

    platform_brightness: Optional[Brightness] = None
    """
    The current brightness mode of the host platform.

    Note:
        This property is read-only.
    """

    client_ip: Optional[str] = None
    """
    IP address of the connected user.

    Note:
        This property is web- and read-only only.
    """

    client_user_agent: Optional[str] = None
    """
    Browser details of the connected user.

    Note:
        This property is web- and read-only only.
    """

    platform: Optional[PagePlatform] = None
    """
    The operating system the application is running on.
    """

    fonts: Optional[dict[str, str]] = None
    """
    Defines the custom fonts to be used in the application.

    Value is a dictionary, in which the keys represent the font family name
    used for reference and the values:
    - Key: The font family name used for reference.
    - Value: The font source, either an absolute URL or a relative path to a
        local asset. The following font file formats are supported `.ttc`, `.ttf`
        and `.otf`.

    Usage example [here](https://flet.dev/docs/cookbook/fonts#importing-fonts).
    """

    on_platform_brightness_change: Optional[
        EventHandler[PlatformBrightnessChangeEvent]
    ] = None
    """
    Called when brightness of app host platform has changed.
    """

    on_app_lifecycle_state_change: Optional[
        EventHandler[AppLifecycleStateChangeEvent]
    ] = None
    """
    Triggers when app lifecycle state changes.
    """

    on_route_change: Optional[EventHandler[RouteChangeEvent]] = None
    """
    Called when page route changes either programmatically, by editing
    application URL or using browser Back/Forward buttons.
    """

    on_view_pop: Optional[EventHandler[ViewPopEvent]] = None
    """
    Called when the user clicks automatic "Back" button in
    [`AppBar`][flet.] control.
    """

    on_keyboard_event: Optional[EventHandler[KeyboardEvent]] = None
    """
    Called when a keyboard key is pressed.
    """

    on_connect: Optional[ControlEventHandler["Page"]] = None
    """
    Called when a web user (re-)connects to a page session.

    It is not triggered when an app page is first opened, but is triggered when
    the page is refreshed, or Flet web client has re-connected after computer
    was unlocked. This event could be used to detect when a web user becomes
    "online".
    """

    on_disconnect: Optional[ControlEventHandler["Page"]] = None
    """
    Called when a web user disconnects from a page session, i.e. closes browser
    tab/window.
    """

    on_close: Optional[ControlEventHandler["Page"]] = None
    """
    Called when a session has expired after configured amount of time
    (60 minutes by default).
    """

    on_login: Optional[EventHandler[LoginEvent]] = None
    """
    Called upon successful or failed OAuth authorization flow.

    See [Authentication](https://docs.flet.dev/cookbook/authentication#checking-authentication-results)
    guide for more information and examples.
    """

    on_logout: Optional[ControlEventHandler["Page"]] = None
    """
    Called after `page.logout()` call.
    """

    on_error: Optional[ControlEventHandler["Page"]] = None
    """
    Called when unhandled exception occurs.
    """

    on_multi_view_add: Optional[EventHandler[MultiViewAddEvent]] = None
    """
    TBD
    """

    on_multi_view_remove: Optional[EventHandler[MultiViewRemoveEvent]] = None
    """
    TBD
    """
    _services: ServiceRegistry = field(default_factory=ServiceRegistry)

    def __post_init__(
        self,
        ref,
        sess: "Session",
    ) -> None:
        BasePage.__post_init__(self, ref)
        self._i = 1
        self.__session = weakref.ref(sess)
        self.__last_route = None
        self.__query: QueryString = QueryString(self)
        self.__authorization: Optional[Authorization] = None

    def get_control(self, id: int) -> Optional[BaseControl]:
        """
        Get a control by its `id`.

        Example:
            ```python
            def main(page: ft.Page):
                x = ft.IconButton(ft.Icons.ADD)
                page.add(x)
                print(type(page.get_control(x._i)))
            ```
        """
        return self.session.index.get(id)

    def render(
        self,
        component: Callable[..., Union[list[View], View, list[Control], Control]],
        *args,
        **kwargs,
    ):
        logger.debug("Page.render()")
        self._notify = self.__notify
        self.views[0].controls = Renderer().render(component, *args, **kwargs)
        self.__render()

    def render_views(
        self,
        component: Callable[..., Union[list[View], View, list[Control], Control]],
        *args,
        **kwargs,
    ):
        logger.debug("Page.render_views()")
        self._notify = self.__notify
        self.views = Renderer().render(component, *args, **kwargs)
        self.__render()

    def __render(self):
        self.update()
        context.enable_components_mode()
        self.session.start_updates_scheduler()

    def schedule_update(self):
        self.session.schedule_update(self)

    def update(self, *controls) -> None:
        if len(controls) == 0:
            self.__update(self)
        else:
            self.__update(*controls)

    def __notify(self, name: str, value: Any):
        self.schedule_update()

    def __update(self, *controls: Control):
        for c in controls:
            self.session.patch_control(c)

    def error(self, message: str) -> None:
        self.session.error(message)

    def before_event(self, e: ControlEvent):
        if isinstance(e, RouteChangeEvent):
            if self.__last_route == e.route:
                return False
            self.__last_route = e.route
            self.query()

        elif isinstance(e, ViewPopEvent):
            for v in unwrap_component(self.views):
                v = unwrap_component(v)
                if v.route == e.route:
                    e.view = v
                    break

        return super().before_event(e)

    def run_task(
        self,
        handler: Callable[InputT, Awaitable[RetT]],
        *args: InputT.args,
        **kwargs: InputT.kwargs,
    ) -> Future[RetT]:
        """
        Run `handler` coroutine as a new Task in the event loop associated with the
        current page.
        """
        _context_page.set(self)
        if not inspect.iscoroutinefunction(handler):
            raise TypeError("handler must be a coroutine function")

        future = asyncio.run_coroutine_threadsafe(
            handler(*args, **kwargs), self.session.connection.loop
        )

        def _on_completion(f):
            try:
                exception = f.exception()
                if exception:
                    raise exception
            except CancelledError:
                pass

        future.add_done_callback(_on_completion)

        return future

    def __context_wrapper(self, handler: Callable[..., Any]) -> Wrapper:
        def wrapper(*args, **kwargs):
            _context_page.set(self)
            handler(*args, **kwargs)

        return wrapper

    def run_thread(
        self,
        handler: Callable[InputT, Any],
        *args: InputT.args,
        **kwargs: InputT.kwargs,
    ) -> None:
        """
        Run `handler` function as a new Thread in the executor associated with the
        current page.
        """
        handler_with_context = self.__context_wrapper(handler)
        if is_pyodide():
            handler_with_context(*args, **kwargs)
        else:
            loop = self.session.connection.loop
            loop.call_soon_threadsafe(
                loop.run_in_executor,
                self.executor,
                partial(handler_with_context, *args, **kwargs),
            )

    @deprecated(
        "Use push_route() instead.",
        version="0.80.0",
        delete_version="0.90.0",
        show_parentheses=True,
    )
    def go(
        self, route: str, skip_route_change_event: bool = False, **kwargs: Any
    ) -> None:
        """
        A helper method that updates [`page.route`](#route), calls
        [`page.on_route_change`](#on_route_change) event handler to update views and
        finally calls `page.update()`.
        """

        asyncio.create_task(self.push_route(route, **kwargs))

    async def push_route(self, route: str, **kwargs: Any) -> None:
        """
        Pushes a new navigation route to the browser history stack.
        Changing route will fire [`page.on_route_change`](#on_route_change) event
        handler.

        Example:
            ```python
            import asyncio

            import flet as ft


            def main(page: ft.Page):
                page.title = "Routes Example"

                def route_change():
                    page.views.clear()
                    page.views.append(
                        ft.View(
                            route="/",
                            controls=[
                                ft.AppBar(
                                    title=ft.Text("Flet app"),
                                ),
                                ft.Button(
                                    "Visit Store",
                                    on_click=lambda: asyncio.create_task(
                                        page.push_route("/store")
                                    ),
                                ),
                            ],
                        )
                    )
                    if page.route == "/store":
                        page.views.append(
                            ft.View(
                                route="/store",
                                controls=[
                                    ft.AppBar(
                                        title=ft.Text("Store"),
                                    ),
                                    ft.Button(
                                        "Go Home",
                                        on_click=lambda: asyncio.create_task(
                                            page.push_route("/")
                                        ),
                                    ),
                                ],
                            )
                        )
                    page.update()

                async def view_pop(e):
                    if e.view is not None:
                        print("View pop:", e.view)
                        page.views.remove(e.view)
                        top_view = page.views[-1]
                        await page.push_route(top_view.route)

                page.on_route_change = route_change
                page.on_view_pop = view_pop

                route_change()


            if __name__ == "__main__":
                ft.run(main)
            ```

        Args:
            route: New navigation route.
            **kwargs: Additional query string parameters to be added to the route.
        """

        new_route = route if not kwargs else route + self.query.post(kwargs)
        await self._invoke_method(
            "push_route",
            arguments={"route": new_route},
        )

    def get_upload_url(self, file_name: str, expires: int) -> str:
        """
        Generates presigned upload URL for built-in upload storage:

        * `file_name` - a relative to upload storage path.
        * `expires` - a URL time-to-live in seconds.

        Example:
            ```python
            upload_url = page.get_upload_url("dir/filename.ext", 60)
            ```

            To enable built-in upload storage, provide the `upload_dir `
            argument to `ft.run()` call:

            ```python
            ft.run(main, upload_dir="uploads")
            ```
        """
        return self.session.connection.get_upload_url(file_name, expires)

    async def login(
        self,
        provider: OAuthProvider,
        fetch_user: bool = True,
        fetch_groups: bool = False,
        scope: Optional[list[str]] = None,
        saved_token: Optional[str] = None,
        on_open_authorization_url: Optional[
            Callable[[str], Coroutine[Any, Any, None]]
        ] = None,
        complete_page_html: Optional[str] = None,
        redirect_to_page: Optional[bool] = False,
        authorization: type[AT] = AuthorizationImpl,
    ) -> AT:
        """
        Starts OAuth flow.

        See [Authentication](https://docs.flet.dev/cookbook/authentication)
        guide for more information and examples.
        """
        self.__authorization = authorization(
            provider,
            fetch_user=fetch_user,
            fetch_groups=fetch_groups,
            scope=scope,
        )
        if saved_token is None:
            authorization_url, state = self.__authorization.get_authorization_data()
            auth_attrs = {"state": state}
            if complete_page_html:
                auth_attrs["completePageHtml"] = complete_page_html
            if redirect_to_page:
                up = urlparse(provider.redirect_url)
                auth_attrs["completePageUrl"] = up._replace(
                    path=f"{self.session.connection.page_name}{self.route}"
                ).geturl()
            self.session.connection.oauth_authorize(auth_attrs)
            if on_open_authorization_url:
                await on_open_authorization_url(authorization_url)
            else:
                if self.web:
                    await UrlLauncher().open_window(
                        authorization_url, title="flet_oauth_signin"
                    )
                else:
                    await UrlLauncher().launch_url(authorization_url)
        else:
            await self.__authorization.dehydrate_token(saved_token)

            e = LoginEvent(name="login", control=self, error="", error_description="")
            if self.on_login:
                asyncio.create_task(self._trigger_event("login", event_data=None, e=e))

        return self.__authorization

    async def _authorize_callback(self, data: dict[str, Optional[str]]) -> None:
        assert self.__authorization
        state = data.get("state")
        assert state == self.__authorization.state

        if not self.web:
            if self.platform in ["ios", "android"]:
                # close web view on mobile
                await self.close_in_app_web_view()
            else:
                # activate desktop window
                await self.window.to_front()
        e = LoginEvent(
            error=data.get("error"),
            error_description=data.get("error_description"),
            control=self,
            name="login",
        )
        if not e.error:
            # perform token request

            code = data.get("code")
            assert code not in [None, ""]
            try:
                await self.__authorization.request_token(code)
            except Exception as ex:
                e.error = str(ex)
        if self.on_login:
            asyncio.create_task(self._trigger_event("login", event_data=None, e=e))

    def logout(self) -> None:
        """
        Clears current authentication context. See
        [Authentication](https://docs.flet.dev/cookbook/authentication#signing-out) guide for more
        information and examples.
        """  # noqa: E501
        self.__authorization = None
        e = ControlEvent(name="logout", control=self)
        if self.on_logout:
            asyncio.create_task(self._trigger_event("logout", event_data=None, e=e))

    @deprecated(
        "Use UrlLauncher().launch_url() instead.",
        version="0.90.0",
        show_parentheses=True,
    )
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
            web_popup_window_name: Window tab/name to open URL in. Use
                [`UrlTarget.SELF`][flet.]
                for the same browser tab, [`UrlTarget.BLANK`][flet.]
                for a new browser tab (or in external application on mobile device),
                or a custom name for a named tab.
            web_popup_window: Display the URL in a browser popup window.
            web_popup_window_width: Popup window width.
            web_popup_window_height: Popup window height.
        """
        if web_popup_window:
            await UrlLauncher().open_window(
                url,
                title=web_popup_window_name,
                width=web_popup_window_width,
                height=web_popup_window_height,
            )
        else:
            await UrlLauncher().launch_url(url)

    @deprecated(
        "Use UrlLauncher().can_launch_url() instead.",
        version="0.90.0",
        show_parentheses=True,
    )
    async def can_launch_url(self, url: str) -> bool:
        """
        Checks whether the specified URL can be handled by some app
        installed on the device.

        Args:
            url: The URL to check.

        Returns:
            `True` if it is possible to verify that there is a handler available.
                `False` if there is no handler available, or the application does not
                have permission to check. For example:

                - On recent versions of Android and iOS, this will always return `False`
                    unless the application has been configuration to allow querying the
                    system for launch support.
                - In web mode, this will always return `False` except for a few specific
                    schemes that are always assumed to be supported (such as http(s)),
                    as web pages are never allowed to query installed applications.
        """
        return await UrlLauncher().can_launch_url(url)

    @deprecated(
        "Use UrlLauncher().close_in_app_web_view() instead.",
        version="0.90.0",
        show_parentheses=True,
    )
    async def close_in_app_web_view(self) -> None:
        """
        Closes in-app web view opened with `launch_url()`.

        📱 Mobile only.
        """
        await UrlLauncher().close_in_app_web_view()

    @property
    def session(self) -> "Session":
        """
        The session that this page belongs to.
        """
        if sess := self.__session():
            return sess
        raise RuntimeError("An attempt to fetch destroyed session.")

    @property
    def query(self) -> QueryString:
        """
        The query parameters of the current page.
        """
        return self.__query

    @property
    def url(self) -> Optional[str]:
        """
        The URL of the current page.
        """
        return self.session.connection.page_url

    @property
    def name(self) -> str:
        """
        The name of the current page.
        """
        return self.session.connection.page_name

    @property
    def loop(self) -> asyncio.AbstractEventLoop:
        """
        The event loop for the current page.
        """
        return self.session.connection.loop

    @property
    def executor(self) -> Optional[ThreadPoolExecutor]:
        """
        The executor for the current page.
        """
        return self.session.connection.executor

    @property
    def auth(self) -> Optional[Authorization]:
        """
        The current authorization context, or `None` if the user is not authorized.
        """
        return self.__authorization

    @property
    def pubsub(self) -> "PubSubClient":
        """
        The PubSub client for the current page.
        """
        return self.session.pubsub_client

    @property
    @deprecated("Use UrlLauncher() instead.", version="0.80.0", delete_version="0.90.0")
    def url_launcher(self) -> UrlLauncher:
        """
        DEPRECATED: The UrlLauncher service for the current page.
        """
        return UrlLauncher()

    @property
    @deprecated(
        "Use BrowserContextMenu() instead.", version="0.80.0", delete_version="0.90.0"
    )
    def browser_context_menu(self):
        """
        DEPRECATED: The BrowserContextMenu service for the current page.
        """

        return BrowserContextMenu()

    @property
    @deprecated(
        "Use SharedPreferences() instead.", version="0.80.0", delete_version="0.90.0"
    )
    def shared_preferences(self):
        """
        DEPRECATED: The SharedPreferences service for the current page.
        """

        return SharedPreferences()

    @property
    @deprecated("Use Clipboard() instead.", version="0.80.0", delete_version="0.90.0")
    def clipboard(self):
        """
        DEPRECATED: The Clipboard service for the current page.
        """

        return Clipboard()

    @property
    @deprecated(
        "Use StoragePaths() instead.", version="0.80.0", delete_version="0.90.0"
    )
    def storage_paths(self):
        """
        DEPRECATED: The StoragePaths service for the current page.
        """

        return StoragePaths()

    async def get_device_info(self) -> Optional[DeviceInfo]:
        """
        Returns device information.

        Returns:
            The device information object for the current platform,
                or `None` if unavailable.
        """
        info = await self._invoke_method("get_device_info")

        if self.web:
            return from_dict(WebDeviceInfo, info)
        elif self.platform == PagePlatform.ANDROID:
            return from_dict(AndroidDeviceInfo, info)
        elif self.platform == PagePlatform.IOS:
            return from_dict(IosDeviceInfo, info)
        elif self.platform == PagePlatform.MACOS:
            return from_dict(MacOsDeviceInfo, info)
        elif self.platform == PagePlatform.LINUX:
            return from_dict(LinuxDeviceInfo, info)
        elif self.platform == PagePlatform.WINDOWS:
            return from_dict(WindowsDeviceInfo, info)
        else:
            return None

    async def set_allowed_device_orientations(
        self, orientations: list[DeviceOrientation]
    ) -> None:
        """
        Constrains the allowed orientations for the app when running on a mobile device.

        Args:
            orientations: A list of allowed device orientations.
                Set to an empty list to use the system default behavior.

        Raises:
            FletUnsupportedPlatformException: If the method is called
                on a non-mobile platform.

        Limitations:
            - **Android**: On Android 16 (API 36) or later, this method won't be able to
                change the orientation of **devices with a display width ≥ 600 dp**
                cannot change orientation. For more details see Android 16 docs
                [here](https://developer.android.com/about/versions/16/behavior-changes-16#ignore-orientation).
                Also, Android limits the [orientations](https://developer.android.com/reference/android/R.attr#screenOrientation) to the following combinations:
                    - `[]` → `unspecified`
                    - `[PORTRAIT_UP]` → `portrait`
                    - `[LANDSCAPE_LEFT]` → `landscape`
                    - `[PORTRAIT_DOWN]` → `reversePortrait`
                    - `[PORTRAIT_UP, PORTRAIT_DOWN]` → `userPortrait`
                    - `[LANDSCAPE_RIGHT]` → `reverseLandscape`
                    - `[LANDSCAPE_LEFT, LANDSCAPE_RIGHT]` → `userLandscape`
                    - `[PORTRAIT_UP, LANDSCAPE_LEFT, LANDSCAPE_RIGHT]` → `user`
                    - `[PORTRAIT_UP, PORTRAIT_DOWN, LANDSCAPE_LEFT, LANDSCAPE_RIGHT]` → `fullUser`

            - **iOS**: This setting will only be respected on iPad if multitasking is disabled.
                You can decide to opt out of multitasking on iPad, then this will work
                but your app will not support Slide Over and Split View multitasking
                anymore. Should you decide to opt out of multitasking you can do this by
                setting "Requires full screen" to true in the Xcode Deployment Info.
        """  # noqa: E501
        if not self.platform.is_mobile():
            raise FletUnsupportedPlatformException(
                "set_allowed_device_orientations is only supported on mobile platforms"
            )
        await self._invoke_method(
            "set_allowed_device_orientations",
            arguments={"orientations": orientations},
        )
