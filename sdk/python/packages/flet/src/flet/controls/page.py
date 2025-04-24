import asyncio
import json
import logging
import weakref
from concurrent.futures import CancelledError, Future, ThreadPoolExecutor
from contextvars import ContextVar
from dataclasses import InitVar, dataclass, field
from functools import partial
from typing import (
    TYPE_CHECKING,
    Any,
    Awaitable,
    Callable,
    Coroutine,
    Dict,
    List,
    Optional,
    Tuple,
    Type,
    TypeVar,
    Union,
)
from urllib.parse import urlparse

from flet.controls.adaptive_control import AdaptiveControl
from flet.controls.animation import AnimationCurve
from flet.controls.base_control import BaseControl, control
from flet.controls.box import BoxDecoration
from flet.controls.control import Control
from flet.controls.control_event import ControlEvent
from flet.controls.core.browser_context_menu import BrowserContextMenu
from flet.controls.core.clipboard import Clipboard
from flet.controls.core.shared_preferences import SharedPreferences
from flet.controls.core.storage_paths import StoragePaths
from flet.controls.core.url_launcher import UrlLauncher
from flet.controls.core.view import View
from flet.controls.core.window import Window
from flet.controls.cupertino.cupertino_app_bar import CupertinoAppBar
from flet.controls.cupertino.cupertino_navigation_bar import CupertinoNavigationBar
from flet.controls.dialog_control import DialogControl
from flet.controls.duration import OptionalDurationValue
from flet.controls.material.app_bar import AppBar
from flet.controls.material.bottom_app_bar import BottomAppBar
from flet.controls.material.floating_action_button import FloatingActionButton
from flet.controls.material.navigation_bar import NavigationBar
from flet.controls.material.navigation_drawer import NavigationDrawer
from flet.controls.padding import OptionalPaddingValue, Padding
from flet.controls.query_string import QueryString
from flet.controls.scrollable_control import OnScrollEvent
from flet.controls.service import Service
from flet.controls.session_storage import SessionStorage
from flet.controls.theme import Theme
from flet.controls.transform import OffsetValue
from flet.controls.types import (
    AppLifecycleState,
    Brightness,
    CrossAxisAlignment,
    FloatingActionButtonLocation,
    LocaleConfiguration,
    MainAxisAlignment,
    OptionalColorValue,
    OptionalControlEventCallable,
    OptionalEventCallable,
    OptionalNumber,
    PagePlatform,
    ScrollMode,
    ThemeMode,
    Wrapper,
)
from flet.utils import classproperty, is_pyodide

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
    def page(cls) -> "Page":
        return _session_page.get()


try:
    from flet.auth.authorization import Authorization
    from flet.auth.oauth_provider import OAuthProvider
except ImportError as e:

    class OAuthProvider: ...

    class Authorization:
        def __init__(
            self,
            provider: OAuthProvider,
            fetch_user: bool,
            fetch_groups: bool,
            scope: Optional[List[str]] = None,
        ): ...


AT = TypeVar("AT", bound=Authorization)

InputT = ParamSpec("InputT")
RetT = TypeVar("RetT")


class PageDisconnectedException(Exception):
    def __init__(self, message):
        super().__init__(message)


@control("Page", isolated=True, post_init_args=2)
class Page(AdaptiveControl):
    """
    Page is a container for `View` (https://flet.dev/docs/controls/view) controls.

    A page instance and the root view are automatically created when a new user session started.

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

    views: List[View] = field(default_factory=lambda: [View()])
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
    _overlay: "Overlay" = field(default_factory=lambda: Overlay())
    _dialogs: "Dialogs" = field(default_factory=lambda: Dialogs())

    theme_mode: Optional[ThemeMode] = field(default=ThemeMode.SYSTEM)
    theme: Optional[Theme] = None
    dark_theme: Optional[Theme] = None
    locale_configuration: Optional[LocaleConfiguration] = None
    show_semantics_debugger: Optional[bool] = None
    width: OptionalNumber = None
    height: OptionalNumber = None
    title: Optional[str] = None
    route: Optional[str] = None
    web: Optional[bool] = field(default=False)
    pwa: Optional[bool] = field(default=False)
    debug: Optional[bool] = field(default=False)
    wasm: Optional[bool] = field(default=False)
    platform: Optional[PagePlatform] = None
    platform_brightness: Optional[Brightness] = None
    media: Optional["PageMediaData"] = None
    client_ip: Optional[str] = None
    client_user_agent: Optional[str] = None
    fonts: Optional[Dict[str, str]] = None
    scroll_event_interval: OptionalNumber = None

    on_close: OptionalControlEventCallable = None
    on_resized: OptionalEventCallable["PageResizeEvent"] = None
    on_platform_brightness_change: OptionalControlEventCallable = None
    on_app_lifecycle_state_change: OptionalEventCallable[
        "AppLifecycleStateChangeEvent"
    ] = None
    on_route_change: OptionalEventCallable["RouteChangeEvent"] = None
    on_view_pop: OptionalEventCallable["ViewPopEvent"] = None
    on_keyboard_event: OptionalEventCallable["KeyboardEvent"] = None
    on_media_change: OptionalControlEventCallable = None
    on_connect: OptionalControlEventCallable = None
    on_disconnect: OptionalControlEventCallable = None
    on_login: OptionalEventCallable["LoginEvent"] = None
    on_logout: OptionalControlEventCallable = None
    on_error: OptionalControlEventCallable = None
    on_scroll: OptionalEventCallable["OnScrollEvent"] = None

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

        self.__last_route = None

    def get_control(self, id: int) -> Optional[Control]:
        return self.get_session().index.get(id)

    def __default_view(self) -> View:
        assert len(self.views) > 0, "views list is empty."
        return self.views[0]

    def update(self, *controls) -> None:
        if len(controls) == 0:
            r = self.__update(self)
        else:
            r = self.__update(*controls)
        self.__handle_mount_unmount(*r)

    def add(self, *controls: Control) -> None:
        self.controls.extend(controls)
        r = self.__update(self)
        self.__handle_mount_unmount(*r)

    def insert(self, at: int, *controls: Control) -> None:
        n = at
        for control in controls:
            self.controls.insert(n, control)
            n += 1
        r = self.__update(self)
        self.__handle_mount_unmount(*r)

    def remove(self, *controls: Control) -> None:
        for control in controls:
            self.controls.remove(control)
        r = self.__update(self)
        self.__handle_mount_unmount(*r)

    def remove_at(self, index: int) -> None:
        self.controls.pop(index)
        r = self.__update(self)
        self.__handle_mount_unmount(*r)

    def clean(self) -> None:
        self._clean(self)
        self.controls.clear()

    def _clean(self, control: Control) -> None:
        # with self.__lock:
        #     control._previous_children.clear()
        #     assert control.uid is not None
        #     removed_controls = []
        #     for child in control._get_children():
        #         removed_controls.extend(
        #             self._remove_control_recursively(self.index, child)
        #         )
        #     self._send_command("clean", [control.uid])
        #     for c in removed_controls:
        #         c.will_unmount()
        pass

    def get_session(self):
        if sess := self.__session():
            return sess
        raise Exception("An attempt to fetch destroyed session.")

    def __update(self, *controls: Control) -> Tuple[List[Control], List[Control]]:
        # if not self.__get_session().is_connected:
        #     raise PageDisconnectedException("Page has been disconnected")
        # commands, added_controls, removed_controls = self.__prepare_update(*controls)
        # self.__validate_controls_page(added_controls)
        # results = self.__conn.send_commands(self._session_id, commands).results
        for control in controls:
            self.get_session().patch_control(control)
        return [], []  # added_controls, removed_controls

    def __validate_controls_page(self, added_controls: List[Control]) -> None:
        for ctrl in added_controls:
            if ctrl.page and ctrl.page != self:
                raise Exception(
                    f"Control has already been added to another page: {ctrl}"
                )

    def __handle_mount_unmount(self, added_controls, removed_controls) -> None:
        # for ctrl in removed_controls:
        #     ctrl.will_unmount()
        #     ctrl.parent = None  # remove parent reference
        #     ctrl.page = None
        # for ctrl in added_controls:
        #     ctrl.did_mount()
        pass

    def error(self, message: str) -> None:
        self.get_session().error(message)

    def run_task(
        self,
        handler: Callable[InputT, Awaitable[RetT]],
        *args: InputT.args,
        **kwargs: InputT.kwargs,
    ) -> Future[RetT]:
        _session_page.set(self)
        assert asyncio.iscoroutinefunction(handler)

        future = asyncio.run_coroutine_threadsafe(handler(*args, **kwargs), self.loop)

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
            self.loop.call_soon_threadsafe(
                self.loop.run_in_executor,
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

    def login(
        self,
        provider: OAuthProvider,
        fetch_user: Optional[bool] = True,
        fetch_groups: Optional[bool] = False,
        scope: Optional[List[str]] = None,
        saved_token: Optional[str] = None,
        on_open_authorization_url: Optional[Callable[[str], None]] = None,
        complete_page_html: Optional[str] = None,
        redirect_to_page: Optional[bool] = False,
        authorization: Type[AT] = Authorization,
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
                    path=self.__conn.page_name
                ).geturl()
            result = self._send_command("oauthAuthorize", attrs=auth_attrs)
            if result.error != "":
                raise Exception(result.error)
            if on_open_authorization_url:
                on_open_authorization_url(authorization_url)
            else:
                self.launch_url(
                    authorization_url, "flet_oauth_signin", web_popup_window=self.web
                )
        else:
            self.__authorization.dehydrate_token(saved_token)
            self.run_task(
                self.__on_login.get_handler(),
                LoginEvent(
                    error="",
                    error_description="",
                    page=self,
                    control=self,
                    target="page",
                    name="on_login",
                    data="",
                ),
            )
        return self.__authorization

    async def login_async(
        self,
        provider: OAuthProvider,
        fetch_user: Optional[bool] = True,
        fetch_groups: Optional[bool] = False,
        scope: Optional[List[str]] = None,
        saved_token: Optional[str] = None,
        on_open_authorization_url: Optional[
            Callable[[str], Coroutine[Any, Any, None]]
        ] = None,
        complete_page_html: Optional[str] = None,
        redirect_to_page: Optional[bool] = False,
        authorization: Type[AT] = Authorization,
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
                    path=f"{self.__conn.page_name}{self.route}"
                ).geturl()
            result = self._send_command("oauthAuthorize", attrs=auth_attrs)
            if result.error != "":
                raise Exception(result.error)
            if on_open_authorization_url:
                await on_open_authorization_url(authorization_url)
            else:
                self.launch_url(
                    authorization_url, "flet_oauth_signin", web_popup_window=self.web
                )
        else:
            await self.__authorization.dehydrate_token_async(saved_token)
            self.run_task(
                self.__on_login.get_handler(),
                LoginEvent(
                    error="",
                    error_description="",
                    page=self,
                    control=self,
                    target="page",
                    name="on_login",
                    data="",
                ),
            )
        return self.__authorization

    async def _authorize_callback_async(self, data: str) -> None:
        await self.on_event_async(ControlEvent("page", "authorize", json.dumps(data)))

    async def __on_authorize_async(self, e) -> None:
        assert self.__authorization
        d = json.loads(e.data)
        state = d.get("state")
        assert state == self.__authorization.state

        if not self.web:
            if self.platform in ["ios", "android"]:
                # close web view on mobile
                self.close_in_app_web_view()
            else:
                # activate desktop window
                self.window.to_front()
        login_evt = LoginEvent(
            error=d.get("error"),
            error_description=d.get("error_description"),
            page=self,
            control=self,
            target="page",
            name="on_login",
            data="",
        )
        if not login_evt.error:
            # perform token request

            code = d.get("code")
            assert code not in [None, ""]
            try:
                await self.__authorization.request_token_async(code)
            except Exception as ex:
                login_evt.error = str(ex)
        self.run_task(
            self.__on_login.get_handler(),
            login_evt,
        )

    def logout(self) -> None:
        self.__authorization = None
        self.run_task(
            self.__on_logout.get_handler(),
            ControlEvent(
                target="page", name="logout", data="", control=self, page=self
            ),
        )

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

    def scroll_to(
        self,
        offset: Optional[float] = None,
        delta: Optional[float] = None,
        key: Optional[str] = None,
        duration: OptionalDurationValue = None,
        curve: Optional[AnimationCurve] = None,
    ) -> None:
        self.__default_view().scroll_to(
            offset=offset, delta=delta, key=key, duration=duration, curve=curve
        )

    def show_dialog(self, dialog: DialogControl) -> None:
        if dialog in self._dialogs.controls:
            raise Exception("Dialog is already opened")

        original_on_dismiss = dialog.on_dismiss

        def wrapped_on_dismiss(*args, **kwargs):
            if dialog in self._dialogs.controls:
                self._dialogs.controls.remove(dialog)
                self._dialogs.update()
            if (
                original_on_dismiss
                and not hasattr(dialog, "_force_close")
                and args[0].data
                != False  # e.data == False for TimePicker and DatePicker if they were dismissed without changing the value
            ):
                original_on_dismiss(*args, **kwargs)
            dialog.on_dismiss = original_on_dismiss
            if hasattr(dialog, "_force_close"):
                del dialog._force_close

        dialog.open = True
        dialog.on_dismiss = wrapped_on_dismiss

        self._dialogs.controls.append(dialog)
        self._dialogs.update()

    def pop_dialog(self) -> Optional[DialogControl]:
        # get the top most opened dialog
        dialog = next(
            (dlg for dlg in reversed(self._dialogs.controls) if dlg.open), None
        )
        if not dialog:
            return None
        dialog.open = False
        setattr(dialog, "_force_close", True)
        dialog.update()
        return dialog

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

    # overlay
    @property
    def overlay(self) -> List[Control]:
        return self._overlay.controls

    # session_storage
    @property
    def session(self) -> SessionStorage:
        return self.__session_storage

    # controls
    @property
    def controls(self) -> List[Control]:
        return self.__default_view().controls

    @controls.setter
    def controls(self, value: List[Control]):
        self.__default_view().controls = value

    # services
    @property
    def services(self) -> List[Service]:
        return self._user_services.services

    @services.setter
    def services(self, value: List[Service]):
        self._user_services.services = value

    # appbar
    @property
    def appbar(self) -> Union[AppBar, CupertinoAppBar, None]:
        return self.__default_view().appbar

    @appbar.setter
    def appbar(self, value: Union[AppBar, CupertinoAppBar, None]):
        self.__default_view().appbar = value

    # bottom_appbar
    @property
    def bottom_appbar(self) -> Optional[BottomAppBar]:
        return self.__default_view().bottom_appbar

    @bottom_appbar.setter
    def bottom_appbar(self, value: Optional[BottomAppBar]):
        self.__default_view().bottom_appbar = value

    # navigation_bar
    @property
    def navigation_bar(self) -> Optional[Union[NavigationBar, CupertinoNavigationBar]]:
        return self.__default_view().navigation_bar

    @navigation_bar.setter
    def navigation_bar(
        self,
        value: Optional[Union[NavigationBar, CupertinoNavigationBar]],
    ):
        self.__default_view().navigation_bar = value

    # drawer
    @property
    def drawer(self) -> Optional[NavigationDrawer]:
        return self.__default_view().drawer

    @drawer.setter
    def drawer(self, value: Optional[NavigationDrawer]):
        self.__default_view().drawer = value

    # end_drawer
    @property
    def end_drawer(self) -> Optional[NavigationDrawer]:
        return self.__default_view().end_drawer

    @end_drawer.setter
    def end_drawer(self, value: Optional[NavigationDrawer]):
        self.__default_view().end_drawer = value

    # decoration
    @property
    def decoration(self) -> Optional[BoxDecoration]:
        return self.__default_view().decoration

    @decoration.setter
    def decoration(self, value: Optional[BoxDecoration]):
        self.__default_view().decoration = value

    # foreground_decoration
    @property
    def foreground_decoration(self) -> Optional[BoxDecoration]:
        return self.__default_view().foreground_decoration

    @foreground_decoration.setter
    def foreground_decoration(self, value: Optional[BoxDecoration]):
        self.__default_view().foreground_decoration = value

    # floating_action_button
    @property
    def floating_action_button(self) -> Optional[FloatingActionButton]:
        return self.__default_view().floating_action_button

    @floating_action_button.setter
    def floating_action_button(self, value: Optional[FloatingActionButton]):
        self.__default_view().floating_action_button = value

    # floating_action_button_location
    @property
    def floating_action_button_location(
        self,
    ) -> Optional[Union[FloatingActionButtonLocation, OffsetValue]]:
        return self.__default_view().floating_action_button_location

    @floating_action_button_location.setter
    def floating_action_button_location(
        self, value: Optional[Union[FloatingActionButtonLocation, OffsetValue]]
    ):
        self.__default_view().floating_action_button_location = value

    # horizontal_alignment
    @property
    def horizontal_alignment(self) -> Optional[CrossAxisAlignment]:
        return self.__default_view().horizontal_alignment

    @horizontal_alignment.setter
    def horizontal_alignment(self, value: Optional[CrossAxisAlignment]):
        self.__default_view().horizontal_alignment = value

    # vertical_alignment
    @property
    def vertical_alignment(self) -> Optional[MainAxisAlignment]:
        return self.__default_view().vertical_alignment

    @vertical_alignment.setter
    def vertical_alignment(self, value: Optional[MainAxisAlignment]):
        self.__default_view().vertical_alignment = value

    # spacing
    @property
    def spacing(self) -> OptionalNumber:
        return self.__default_view().spacing

    @spacing.setter
    def spacing(self, value: OptionalNumber):
        self.__default_view().spacing = value

    # padding
    @property
    def padding(self) -> OptionalPaddingValue:
        return self.__default_view().padding

    @padding.setter
    def padding(self, value: OptionalPaddingValue):
        self.__default_view().padding = value

    # bgcolor
    @property
    def bgcolor(self) -> OptionalColorValue:
        return self.__default_view().bgcolor

    @bgcolor.setter
    def bgcolor(self, value: OptionalColorValue):
        self.__default_view().bgcolor = value

    # scroll
    @property
    def scroll(self) -> Optional[ScrollMode]:
        return self.__default_view().scroll

    @scroll.setter
    def scroll(self, value: Optional[ScrollMode]):
        self.__default_view().scroll = value

    # auto_scroll
    @property
    def auto_scroll(self):
        return self.__default_view().auto_scroll

    @auto_scroll.setter
    def auto_scroll(self, value: Optional[bool]):
        self.__default_view().auto_scroll = value

    # Magic methods
    def __contains__(self, item: Control) -> bool:
        return item in self.controls


@control("Overlay")
class Overlay(BaseControl):
    controls: List[Control] = field(default_factory=list)


@control("Dialogs")
class Dialogs(BaseControl):
    controls: List[DialogControl] = field(default_factory=list)


@control("ServiceRegistry")
class ServiceRegistry(Service):
    services: List[Service] = field(default_factory=list)


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
    error: str
    error_description: str


@dataclass
class InvokeMethodResults:
    method_id: str
    result: Optional[str]
    error: Optional[str]


@dataclass
class PageMediaData:
    padding: Padding
    view_padding: Padding
    view_insets: Padding


@dataclass
class AppLifecycleStateChangeEvent(ControlEvent):
    state: AppLifecycleState


@dataclass
class PageResizeEvent(ControlEvent):
    width: float
    height: float
