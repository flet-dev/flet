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
from flet.controls.control_event import ControlEvent
from flet.controls.core.view import View
from flet.controls.core.window import Window
from flet.controls.multi_view import MultiView
from flet.controls.page_view import PageView
from flet.controls.query_string import QueryString
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
    OptionalControlEventCallable,
    OptionalEventCallable,
    PagePlatform,
    Wrapper,
)
from flet.utils import classproperty, is_pyodide

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


class PageDisconnectedException(Exception):
    def __init__(self, message):
        super().__init__(message)


@control("Page", isolated=True, post_init_args=2)
class Page(PageView):
    """
    Page is a container for `View` (https://flet.dev/docs/controls/view) controls.

    A page instance and the root view are automatically created when a new
    user session started.

    Example:

    ```
    import flet as ft


    def main(page: ft.Page):
        page.title = "New page"
        page.add(ft.Text("Hello"))


    ft.app(target=main)
    ```

    -----

    Online docs: https://flet.dev/docs/controls/page
    """

    sess: InitVar["Session"]

    multi_views: list[MultiView] = field(default_factory=list)
    window: Window = field(default_factory=lambda: Window())
    browser_context_menu: BrowserContextMenu = field(
        default_factory=lambda: BrowserContextMenu()
    )
    shared_preferences: SharedPreferences = field(
        default_factory=lambda: SharedPreferences()
    )
    clipboard: Clipboard = field(default_factory=lambda: Clipboard())
    storage_paths: StoragePaths = field(default_factory=lambda: StoragePaths())
    url_launcher: UrlLauncher = field(default_factory=lambda: UrlLauncher())
    _user_services: "ServiceRegistry" = field(default_factory=lambda: ServiceRegistry())
    _page_services: "ServiceRegistry" = field(default_factory=lambda: ServiceRegistry())

    route: Optional[str] = None
    web: bool = field(default=False)
    pwa: bool = field(default=False)
    debug: bool = field(default=False)
    wasm: bool = field(default=False)
    multi_view: bool = field(default=False)
    platform: Optional[PagePlatform] = None
    platform_brightness: Optional[Brightness] = None
    client_ip: Optional[str] = None
    client_user_agent: Optional[str] = None
    fonts: Optional[dict[str, str]] = None

    on_platform_brightness_change: OptionalControlEventCallable = None
    on_app_lifecycle_state_change: OptionalEventCallable[
        "AppLifecycleStateChangeEvent"
    ] = None
    on_route_change: OptionalEventCallable["RouteChangeEvent"] = None
    on_view_pop: OptionalEventCallable["ViewPopEvent"] = None
    on_keyboard_event: OptionalEventCallable["KeyboardEvent"] = None
    on_connect: OptionalControlEventCallable = None
    on_disconnect: OptionalControlEventCallable = None
    on_close: OptionalControlEventCallable = None
    on_login: OptionalEventCallable["LoginEvent"] = None
    on_logout: OptionalControlEventCallable = None
    on_error: OptionalControlEventCallable = None
    on_multi_view_add: OptionalEventCallable["MultiViewAddEvent"] = None
    on_multi_view_remove: OptionalEventCallable["MultiViewRemoveEvent"] = None

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
        self.__query: QueryString = QueryString(self)
        self.__session_storage: SessionStorage = SessionStorage()
        self.__authorization: Optional[Authorization] = None

    def get_control(self, id: int) -> Optional[BaseControl]:
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
            if self.route == e.route:
                return False
            self.query()
        return super().before_event(e)

    def run_task(
        self,
        handler: Callable[InputT, Awaitable[RetT]],
        *args: InputT.args,
        **kwargs: InputT.kwargs,
    ) -> Future[RetT]:
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
        def wrapper(*args):
            _session_page.set(self)
            handler(*args)

        return wrapper

    def run_thread(
        self,
        handler: Callable[InputT, Any],
        *args: InputT.args,
        **kwargs: InputT.kwargs,
    ) -> None:
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
        self.route = route if not kwargs else route + self.query.post(kwargs)

        if not skip_route_change_event:
            e = RouteChangeEvent(
                name="route_change", control=self, data=self.route, route=self.route
            )
            if self.on_route_change:
                if asyncio.iscoroutinefunction(self.on_route_change):
                    self.run_task(self.on_route_change, e)
                elif callable(self.on_route_change):
                    self.on_route_change(e)

        self.update()
        self.query()  # Update query url (required when using go)

    def get_upload_url(self, file_name: str, expires: int) -> str:
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
                    self.run_task(self.on_login, e)
                elif callable(self.on_login):
                    self.on_login(e)

        return self.__authorization

    async def _authorize_callback_async(self, data: dict[str, str]) -> None:
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
                self.run_task(self.on_login, e)
            elif callable(self.on_login):
                self.on_login(e)

    def logout(self) -> None:
        self.__authorization = None
        e = ControlEvent(name="logout", control=self)
        if self.on_logout:
            if asyncio.iscoroutinefunction(self.on_logout):
                self.run_task(self.on_logout, e)
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
        await self.url_launcher.launch_url_async(
            url,
            web_window_name=web_window_name,
            web_popup_window=web_popup_window,
            window_width=window_width,
            window_height=window_height,
        )

    def can_launch_url_async(self, url: str):
        return self.url_launcher.can_launch_url_async(url)

    def close_in_app_web_view(self) -> None:
        self.url_launcher.close_in_app_web_view()

    async def close_in_app_web_view_async(self) -> None:
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


@control("ServiceRegistry")
class ServiceRegistry(Service):
    services: list[Service] = field(default_factory=list)


@dataclass
class RouteChangeEvent(ControlEvent):
    route: str


@dataclass
class ViewPopEvent(ControlEvent):
    view: View


@dataclass
class KeyboardEvent(ControlEvent):
    key: str
    shift: bool
    ctrl: bool
    alt: bool
    meta: bool


@dataclass
class LoginEvent(ControlEvent):
    error: Optional[str]
    error_description: Optional[str]


@dataclass
class InvokeMethodResults:
    method_id: str
    result: Optional[str]
    error: Optional[str]


@dataclass
class AppLifecycleStateChangeEvent(ControlEvent):
    state: AppLifecycleState


@dataclass
class MultiViewAddEvent(ControlEvent):
    view_id: int
    initial_data: Any


@dataclass
class MultiViewRemoveEvent(ControlEvent):
    view_id: int
