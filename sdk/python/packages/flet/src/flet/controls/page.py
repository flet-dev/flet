import asyncio
import logging
import weakref
from collections.abc import Awaitable, Coroutine
from concurrent.futures import CancelledError, Future, ThreadPoolExecutor
from contextvars import ContextVar
from dataclasses import InitVar, dataclass, field
from functools import partial
from typing import (
    TYPE_CHECKING,
    Any,
    Callable,
    Optional,
    TypeVar,
)
from urllib.parse import urlparse

from flet.auth.authorization import Authorization
from flet.auth.oauth_provider import OAuthProvider
from flet.controls.adaptive_control import AdaptiveControl
from flet.controls.base_control import BaseControl, control
from flet.controls.control import Control
from flet.controls.control_event import (
    ControlEvent,
    Event,
    OptionalControlEventHandler,
    OptionalEventHandler,
)
from flet.controls.core.view import View
from flet.controls.core.window import Window
from flet.controls.exceptions import FletException
from flet.controls.multi_view import MultiView
from flet.controls.page_view import PageView
from flet.controls.query_string import QueryString
from flet.controls.ref import Ref
from flet.controls.services.browser_context_menu import BrowserContextMenu
from flet.controls.services.clipboard import Clipboard
from flet.controls.services.service import Service
from flet.controls.services.shared_preferences import SharedPreferences
from flet.controls.services.storage_paths import StoragePaths
from flet.controls.services.url_launcher import UrlLauncher
from flet.controls.session_storage import SessionStorage
from flet.controls.types import (
    AppLifecycleState,
    Brightness,
    PagePlatform,
    Wrapper,
)
from flet.utils import classproperty, is_pyodide
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
try:
    from typing import ParamSpec
except ImportError:
    from typing_extensions import ParamSpec

_session_page = ContextVar("flet_session_page", default=None)


class context:
    @classproperty
    def page(cls) -> Optional["Page"]:
        return _session_page.get()


AT = TypeVar("AT", bound=Authorization)
InputT = ParamSpec("InputT")
RetT = TypeVar("RetT")


@control("ServiceRegistry")
class ServiceRegistry(Service):
    services: list[Service] = field(default_factory=list)

    def __post_init__(self, ref: Optional[Ref[Any]]):
        super().__post_init__(ref)
        self._internals["uid"] = random_string(10)


@dataclass
class RouteChangeEvent(Event["Page"]):
    route: str


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


class PageDisconnectedException(FletException):
    def __init__(self, message):
        super().__init__(message)


@control("Page", isolated=True, post_init_args=2)
class Page(PageView):
    """
    Page is a container for `View` (https://flet.dev/docs/controls/view) controls.

    A page instance and the root view are automatically created when a new
    user session started.

    Online docs: https://flet.dev/docs/controls/page
    """

    sess: InitVar["Session"]
    """
    TBD
    """

    multi_views: list[MultiView] = field(default_factory=list)
    """
    TBD
    """

    window: Window = field(default_factory=lambda: Window())
    """
    A class with properties/methods/events to control app's native OS window.

    Value is of type [Window](https://flet.dev/docs/reference/types/window).
    """

    browser_context_menu: BrowserContextMenu = field(
        default_factory=lambda: BrowserContextMenu(), metadata={"skip": True}
    )
    """
    Used to enable or disable the context menu that appears when the user
    right-clicks on the web page.

    Value is of type
    [BrowserContextMenu](https://flet.dev/docs/reference/types/browsercontextmenu).

    🌎 Web only.
    """

    shared_preferences: SharedPreferences = field(
        default_factory=lambda: SharedPreferences(), metadata={"skip": True}
    )
    """
    TBD
    """

    clipboard: Clipboard = field(
        default_factory=lambda: Clipboard(), metadata={"skip": True}
    )
    """
    TBD
    """

    storage_paths: StoragePaths = field(
        default_factory=lambda: StoragePaths(), metadata={"skip": True}
    )
    """
    TBD
    """

    url_launcher: UrlLauncher = field(
        default_factory=lambda: UrlLauncher(), metadata={"skip": True}
    )
    """
    TBD
    """

    _user_services: ServiceRegistry = field(default_factory=lambda: ServiceRegistry())
    """
    TBD
    """

    _page_services: ServiceRegistry = field(default_factory=lambda: ServiceRegistry())
    """
    TBD
    """

    route: Optional[str] = None
    """
    Get or sets page's navigation route. See
    [Navigation and routing](https://flet.dev/docs/getting-started/navigation-and-routing)
    section for more information and examples.
    """

    web: bool = False
    """
    `True` if the application is running in the web browser.
    """

    pwa: bool = False
    """
    `True` if the application is running as Progressive Web App (PWA).

    Value is read-only.
    """

    debug: bool = False
    """
    `True` if Flutter client of Flet app is running in debug mode.
    """

    wasm: bool = False
    """
    TBD
    """

    multi_view: bool = False
    """
    TBD
    """

    platform: Optional[PagePlatform] = None
    """
    Operating system the application is running on.

    Value is of type [PagePlatform](https://flet.dev/docs/reference/types/pageplatform).
    """

    platform_brightness: Optional[Brightness] = None
    """
    The current brightness mode of the host platform.

    Value is read-only and of type
    [Brightness](https://flet.dev/docs/reference/types/brightness).
    """

    client_ip: Optional[str] = None
    """
    IP address of the connected user.

    🌎 Web only.
    """

    client_user_agent: Optional[str] = None
    """
    Browser details of the connected user.

    🌎 Web only.
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

    on_platform_brightness_change: OptionalControlEventHandler["Page"] = None
    """
    Fires when brightness of app host platform has changed.
    """

    on_app_lifecycle_state_change: OptionalEventHandler[
        AppLifecycleStateChangeEvent
    ] = None
    """
    Triggers when app lifecycle state changes.

    Event handler argument is of type
    [AppLifecycleStateChangeEvent](https://flet.dev/docs/reference/types/applifecyclestatechangeevent).
    """

    on_route_change: OptionalEventHandler[RouteChangeEvent] = None
    """
    Fires when page route changes either programmatically, by editing
    application URL or using browser Back/Forward buttons.

    Event handler argument is of type
    [RouteChangeEvent](https://flet.dev/docs/reference/types/routechangeevent).
    """

    on_view_pop: OptionalEventHandler[ViewPopEvent] = None
    """
    Fires when the user clicks automatic "Back" button in
    [AppBar](https://flet.dev/docs/controls/appbar) control.

    Event handler argument is of type
    [ViewPopEvent](https://flet.dev/docs/reference/types/viewpopevent).
    """

    on_keyboard_event: OptionalEventHandler[KeyboardEvent] = None
    """
    Fires when a keyboard key is pressed.

    Event handler argument is of type
    [KeyboardEvent](https://flet.dev/docs/reference/types/keyboardevent).
    """

    on_connect: OptionalControlEventHandler["Page"] = None
    """
    Fires when a web user (re-)connects to a page session.

    It is not triggered when an app page is first opened, but is triggered when
    the page is refreshed, or Flet web client has re-connected after computer
    was unlocked. This event could be used to detect when a web user becomes
    "online".
    """

    on_disconnect: OptionalControlEventHandler["Page"] = None
    """
    Fires when a web user disconnects from a page session, i.e. closes browser
    tab/window.
    """

    on_close: OptionalControlEventHandler["Page"] = None
    """
    Fires when a session has expired after configured amount of time
    (60 minutes by default).
    """

    on_login: OptionalEventHandler[LoginEvent] = None
    """
    Fires upon successful or failed OAuth authorization flow.

    See [Authentication](https://flet.dev/docs/cookbook/authentication#checking-authentication-results)
    guide for more information and examples.
    """

    on_logout: OptionalControlEventHandler["Page"] = None
    """
    Fires after `page.logout()` call.
    """

    on_error: OptionalControlEventHandler["Page"] = None
    """
    Fires when unhandled exception occurs.
    """

    on_multi_view_add: OptionalEventHandler[MultiViewAddEvent] = None
    """
    TBD
    """

    on_multi_view_remove: OptionalEventHandler[MultiViewRemoveEvent] = None
    """
    TBD
    """

    def __post_init__(
        self,
        ref,
        sess: "Session",
    ) -> None:
        AdaptiveControl.__post_init__(self, ref)
        self._i = 1
        self.__session = weakref.ref(sess)

        # page services
        self._page_services.services = [
            self.browser_context_menu,
            self.shared_preferences,
            self.clipboard,
            self.url_launcher,
            self.storage_paths,
        ]
        self.__last_route = None
        self.__query: QueryString = QueryString(self)
        self.__session_storage: SessionStorage = SessionStorage()
        self.__authorization: Optional[Authorization] = None

    def get_control(self, id: int) -> Optional[BaseControl]:
        """
        Get a control by its `id`.

        Example:

        ```python
        import flet as ft

        def main(page: ft.Page):
            x = ft.IconButton(ft.Icons.ADD)
            page.add(x)
            print(type(page.get_control(x.uid)))

        ft.app(main)
        ```
        """
        return self.get_session().index.get(id)

    def update(self, *controls) -> None:
        if len(controls) == 0:
            self.__update(self)
        else:
            self.__update(*controls)

    def get_session(self):
        if sess := self.__session():
            return sess
        raise Exception("An attempt to fetch destroyed session.")

    def __update(self, *controls: Control):
        for c in controls:
            self.get_session().patch_control(c)

    def error(self, message: str) -> None:
        self.get_session().error(message)

    def before_event(self, e: ControlEvent):
        if isinstance(e, RouteChangeEvent):
            if self.__last_route == e.route:
                return False
            self.__last_route = e.route
            self.query()
        elif isinstance(e, ViewPopEvent):
            view = next((v for v in self.views if v.route == e.data), None)
            if view is None:
                return False
            e.view = view
            return True
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
        _session_page.set(self)
        assert asyncio.iscoroutinefunction(handler)

        future = asyncio.run_coroutine_threadsafe(
            handler(*args, **kwargs), self.get_session().connection.loop
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
            _session_page.set(self)
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
            loop = self.get_session().connection.loop
            loop.call_soon_threadsafe(
                loop.run_in_executor,
                self.executor,
                partial(handler_with_context, *args, **kwargs),
            )

    def go(
        self, route: str, skip_route_change_event: bool = False, **kwargs: Any
    ) -> None:
        """
        A helper method that updates [`page.route`](#route), calls
        [`page.on_route_change`](#on_route_change) event handler to update views and
        finally calls `page.update()`.
        """
        self.route = route if not kwargs else route + self.query.post(kwargs)

        if not skip_route_change_event:
            e = RouteChangeEvent(
                name="route_change", control=self, data=self.route, route=self.route
            )
            if self.on_route_change:
                if asyncio.iscoroutinefunction(self.on_route_change):
                    asyncio.create_task(self.on_route_change(e))
                elif callable(self.on_route_change):
                    self.on_route_change(e)

        self.update()
        self.query()  # Update query url (required when using go)

    def get_upload_url(self, file_name: str, expires: int) -> str:
        """
        Generates presigned upload URL for built-in upload storage:

        * `file_name` - a relative to upload storage path.
        * `expires` - a URL time-to-live in seconds.

        For example:

        ```python
        upload_url = page.get_upload_url("dir/filename.ext", 60)
        ```

        To enable built-in upload storage provide `upload_dir` argument to `flet.app()`
        call:

        ```python
        ft.app(main, upload_dir="uploads")
        ```
        """
        return self.get_session().connection.get_upload_url(file_name, expires)

    async def login_async(
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
        Starts OAuth flow. See [Authentication](/docs/cookbook/authentication) guide
        for more information and examples.
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
                    path=f"{self.get_session().connection.page_name}{self.route}"
                ).geturl()
            self.get_session().connection.oauth_authorize(auth_attrs)
            if on_open_authorization_url:
                await on_open_authorization_url(authorization_url)
            else:
                self.launch_url(
                    authorization_url, "flet_oauth_signin", web_popup_window=self.web
                )
        else:
            await self.__authorization.dehydrate_token_async(saved_token)

            e = LoginEvent(name="login", control=self, error="", error_description="")
            if self.on_login:
                if asyncio.iscoroutinefunction(self.on_login):
                    asyncio.create_task(self.on_login(e))
                elif callable(self.on_login):
                    self.on_login(e)

        return self.__authorization

    async def _authorize_callback_async(self, data: dict[str, Optional[str]]) -> None:
        assert self.__authorization
        state = data.get("state")
        assert state == self.__authorization.state

        if not self.web:
            if self.platform in ["ios", "android"]:
                # close web view on mobile
                self.close_in_app_web_view()
            else:
                # activate desktop window
                self.window.to_front()
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
                await self.__authorization.request_token_async(code)
            except Exception as ex:
                e.error = str(ex)
        if self.on_login:
            if asyncio.iscoroutinefunction(self.on_login):
                asyncio.create_task(self.on_login(e))
            elif callable(self.on_login):
                self.on_login(e)

    def logout(self) -> None:
        """
        Clears current authentication context. See
        [Authentication](/docs/cookbook/authentication#signing-out) guide for more
        information and examples.
        """
        self.__authorization = None
        e = ControlEvent(name="logout", control=self)
        if self.on_logout:
            if asyncio.iscoroutinefunction(self.on_logout):
                asyncio.create_task(self.on_logout(e))
            elif callable(self.on_logout):
                self.on_logout(e)

    def launch_url(
        self,
        url: str,
        web_window_name: Optional[str] = None,
        web_popup_window: Optional[bool] = False,
        window_width: Optional[int] = None,
        window_height: Optional[int] = None,
    ) -> None:
        """
        Opens `url` in a new browser window.

        Optional method arguments:

        * `web_window_name` - window tab/name to open URL in:
        [`UrlTarget.SELF`](https://flet.dev/docs/reference/types/urltarget#self) - the
        same browser tab, [`UrlTarget.BLANK`](/docs/reference/types/urltarget#blank) -
        a new browser tab (or in external
        application on mobile device) or `<your name>` - a named tab.
        * `web_popup_window` - set to `True` to display a URL in a browser popup
        window. Defaults to `False`.
        * `window_width` - optional, popup window width.
        * `window_height` - optional, popup window height.
        """
        self.url_launcher.launch_url(
            url,
            web_window_name=web_window_name,
            web_popup_window=web_popup_window,
            window_width=window_width,
            window_height=window_height,
        )

    async def launch_url_async(
        self,
        url: str,
        web_window_name: Optional[str] = None,
        web_popup_window: Optional[bool] = False,
        window_width: Optional[int] = None,
        window_height: Optional[int] = None,
    ) -> None:
        """
        Opens `url` in a new browser window.

        Optional method arguments:

        * `web_window_name` - window tab/name to open URL in: [`UrlTarget.SELF`](https://flet.dev//docs/reference/types/urltarget#self)
        - the same browser tab, [`UrlTarget.BLANK`](https://flet.dev//docs/reference/types/urltarget#blank)
        - a new browser tab (or in external
        application on mobile device) or `<your name>` - a named tab.
        * `web_popup_window` - set to `True` to display a URL in a browser popup
        window. Defaults to `False`.
        * `window_width` - optional, popup window width.
        * `window_height` - optional, popup window height.
        """
        await self.url_launcher.launch_url_async(
            url,
            web_window_name=web_window_name,
            web_popup_window=web_popup_window,
            window_width=window_width,
            window_height=window_height,
        )

    def can_launch_url_async(self, url: str):
        """
        Checks whether the specified URL can be handled by some app installed on the
        device.

        Returns `True` if it is possible to verify that there is a handler available.
        A `False` return value can indicate either that there is no handler available,
        or that the application does not have permission to check. For example:

        * On recent versions of Android and iOS, this will always return `False` unless
        the application has been configuration to allow querying the system for launch
        support.
        * On web, this will always return `False` except for a few specific schemes
        that are always assumed to be supported (such as http(s)), as web pages are
        never allowed to query installed applications.
        """
        return self.url_launcher.can_launch_url_async(url)

    def close_in_app_web_view(self) -> None:
        """
        Closes in-app web view opened with `launch_url()`.

        📱 Mobile only.
        """
        self.url_launcher.close_in_app_web_view()

    async def close_in_app_web_view_async(self) -> None:
        """
        Closes in-app web view opened with `launch_url()`.

        📱 Mobile only.
        """
        await self.url_launcher.close_in_app_web_view_async()

    # query
    @property
    def query(self) -> QueryString:
        return self.__query

    # url
    @property
    def url(self) -> Optional[str]:
        return self.get_session().connection.page_url

    # name
    @property
    def name(self) -> str:
        return self.get_session().connection.page_name

    # loop
    @property
    def loop(self) -> asyncio.AbstractEventLoop:
        return self.get_session().connection.loop

    # executor
    @property
    def executor(self) -> Optional[ThreadPoolExecutor]:
        return self.get_session().connection.executor

    # auth
    @property
    def auth(self) -> Optional[Authorization]:
        return self.__authorization

    # pubsub
    @property
    def pubsub(self) -> "PubSubClient":
        return self.get_session().pubsub_client

    # session_storage
    @property
    def session(self) -> SessionStorage:
        return self.__session_storage

    # services
    @property
    def services(self) -> list[Service]:
        return self._user_services.services

    @services.setter
    def services(self, value: list[Service]):
        self._user_services.services = value
