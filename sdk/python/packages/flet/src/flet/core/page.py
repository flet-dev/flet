from __future__ import annotations

import asyncio
import json
import logging
import threading
import uuid
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
    Sequence,
    Tuple,
    Type,
    TypeVar,
    Union,
    cast,
)
from urllib.parse import urlparse

import flet.core
from flet.core.adaptive_control import AdaptiveControl
from flet.core.alignment import Alignment
from flet.core.animation import AnimationCurve
from flet.core.app_bar import AppBar
from flet.core.bottom_app_bar import BottomAppBar
from flet.core.box import BoxDecoration
from flet.core.client_storage import ClientStorage
from flet.core.control import Control, control
from flet.core.control_event import ControlEvent
from flet.core.cupertino_app_bar import CupertinoAppBar
from flet.core.cupertino_navigation_bar import CupertinoNavigationBar
from flet.core.event import Event
from flet.core.floating_action_button import FloatingActionButton
from flet.core.navigation_bar import NavigationBar
from flet.core.navigation_drawer import NavigationDrawer, NavigationDrawerPosition
from flet.core.padding import Padding
from flet.core.querystring import QueryString
from flet.core.scrollable_control import OnScrollEvent
from flet.core.session_storage import SessionStorage
from flet.core.theme import Theme
from flet.core.types import (
    AppLifecycleState,
    Brightness,
    ColorValue,
    CrossAxisAlignment,
    FloatingActionButtonLocation,
    LocaleConfiguration,
    MainAxisAlignment,
    OffsetValue,
    OptionalControlEventCallable,
    OptionalEventCallable,
    OptionalNumber,
    PaddingValue,
    PagePlatform,
    ScrollMode,
    ThemeMode,
    WindowEventType,
    Wrapper,
)
from flet.core.view import View
from flet.messaging.protocol import Command
from flet.utils import classproperty, is_pyodide
from flet.utils.locks import NopeLock

if TYPE_CHECKING:
    from flet.messaging.session import Session
    from flet.pubsub.pubsub_client import PubSubClient

try:
    from typing import ParamSpec
except ImportError:
    from typing_extensions import ParamSpec


logger = logging.getLogger(flet.__name__)
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


@control("browser_context_menu")
class BrowserContextMenu:

    def __init__(self, page: Page):
        self.__page = weakref.ref(page)
        self.__disabled = False

    def enable(self, wait_timeout: Optional[float] = 10):
        if page := self.__page():
            page.invoke_method("enableBrowserContextMenu", wait_timeout=wait_timeout)
            self.__disabled = False

    def disable(self, wait_timeout: Optional[float] = 10):
        if page := self.__page():
            page.invoke_method("disableBrowserContextMenu", wait_timeout=wait_timeout)
            self.__disabled = True

    @property
    def disabled(self):
        return self.__disabled


@control("window")
class Window(Control):
    bgcolor: Optional[ColorValue] = None
    width: OptionalNumber = None
    height: OptionalNumber = None
    top: OptionalNumber = None
    left: OptionalNumber = None
    max_width: OptionalNumber = None
    max_height: OptionalNumber = None
    min_width: OptionalNumber = None
    min_height: OptionalNumber = None
    opacity: OptionalNumber = field(default=1.0)
    maximized: Optional[bool] = field(default=False)
    minimized: Optional[bool] = field(default=False)
    minimizable: Optional[bool] = field(default=True)
    maximizable: Optional[bool] = field(default=True)
    resizable: Optional[bool] = field(default=True)
    movable: Optional[bool] = field(default=True)
    full_screen: Optional[bool] = field(default=False)
    always_on_top: Optional[bool] = field(default=False)
    prevent_close: Optional[bool] = field(default=False)
    title_bar_hidden: Optional[bool] = field(default=False)
    title_bar_buttons_hidden: Optional[bool] = field(default=False)
    skip_task_bar: Optional[bool] = field(default=False)
    frameless: Optional[bool] = field(default=False)
    progress_bar: OptionalNumber = None
    focused: Optional[bool] = field(default=True)
    visible: Optional[bool] = field(default=True)
    always_on_bottom: Optional[bool] = field(default=False)
    wait_until_ready_to_show: Optional[bool] = field(default=False)
    shadow: Optional[bool] = field(default=False)
    alignment: Optional[Alignment] = None
    badge_label: Optional[str] = None
    icon: Optional[str] = None
    ignore_mouse_events: Optional[bool] = field(default=False)
    on_event: OptionalEventCallable["WindowEvent"] = None

    def destroy(self):
        self.invoke_method("destroy")

    def center(self):
        self.invoke_method("center")

    def close(self):
        self.invoke_method("close")

    def to_front(self):
        self.invoke_method("to_front")


@control("page", post_init_args=2)
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

    sess: InitVar[Session]

    views: List[View] = field(default_factory=lambda: [View()])
    offstage: Offstage = field(default_factory=lambda: Offstage())
    window: Window = field(default_factory=lambda: Window())

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
    platform: Optional[PagePlatform] = None
    platform_brightness: Optional[Brightness] = None
    media: Optional["PageMediaData"] = None
    client_ip: Optional[str] = None
    client_user_agent: Optional[str] = None
    fonts: Optional[Dict[str, str]] = None

    on_scroll_interval: OptionalNumber = None
    on_close: OptionalControlEventCallable = None
    on_resized: OptionalEventCallable["WindowResizeEvent"] = None
    on_platform_brightness_change: OptionalControlEventCallable = None
    on_app_lifecycle_state_change: OptionalEventCallable[
        "AppLifecycleStateChangeEvent"
    ] = None
    on_route_change: OptionalEventCallable["RouteChangeEvent"] = None
    on_view_pop: OptionalEventCallable["ViewPopEvent"] = None
    on_keyboard_event: OptionalEventCallable["KeyboardEvent"] = None
    on_media_change: OptionalEventCallable["PageMediaData"] = None
    on_connect: OptionalControlEventCallable = None
    on_disconnect: OptionalControlEventCallable = None
    on_login: OptionalEventCallable["LoginEvent"] = None
    on_logout: OptionalControlEventCallable = None
    on_error: OptionalControlEventCallable = None
    on_scroll: OptionalEventCallable["OnScrollEvent"] = None

    def __post_init__(
        self,
        ref,
        sess: Session,
    ) -> None:
        AdaptiveControl.__post_init__(self, ref)
        self.__session = weakref.ref(sess)
        self.__lock = threading.Lock() if not is_pyodide() else NopeLock()

        self.__browser_context_menu = BrowserContextMenu(self)
        self.__query: QueryString = QueryString(self)
        self.__client_storage: ClientStorage = ClientStorage(self)
        self.__session_storage: SessionStorage = SessionStorage()
        self.__authorization: Optional[Authorization] = None

        self.__last_route = None

        self.__method_calls: Dict[str, Union[threading.Event, asyncio.Event]] = {}
        self.__method_call_results: Dict[
            Union[threading.Event, asyncio.Event], tuple[Optional[str], Optional[str]]
        ] = {}

    def get_control(self, id: int) -> Optional[Control]:
        return self.__get_session().index.get(id)

    def __default_view(self):
        assert len(self.views) > 0, "views list is empty."
        return self.views[0]

    # async def fetch_page_details_async(self) -> None:
    #     assert self.__conn
    #     props = [
    #         "route",
    #         "pwa",
    #         "web",
    #         "debug",
    #         "platform",
    #         "platformBrightness",
    #         "media",
    #         "width",
    #         "height",
    #         "windowWidth",
    #         "windowHeight",
    #         "windowTop",
    #         "windowLeft",
    #         "clientIP",
    #         "clientUserAgent",
    #     ]
    #     values = (
    #         self.__conn.send_commands(
    #             self._session_id,
    #             [Command(0, "get", ["page", prop]) for prop in props],
    #         )
    #     ).results
    #     for i in range(len(props)):
    #         self._set_attr(props[i], values[i], False)

    def update(self, *controls) -> None:
        with self.__lock:
            if len(controls) == 0:
                r = self.__update(self)
            else:
                r = self.__update(*controls)
        self.__handle_mount_unmount(*r)

    def add(self, *controls: Control) -> None:
        with self.__lock:
            self.controls.extend(controls)
            r = self.__update(self)
        self.__handle_mount_unmount(*r)

    def insert(self, at: int, *controls: Control) -> None:
        with self.__lock:
            n = at
            for control in controls:
                self.controls.insert(n, control)
                n += 1
            r = self.__update(self)
        self.__handle_mount_unmount(*r)

    def remove(self, *controls: Control) -> None:
        with self.__lock:
            for control in controls:
                self.controls.remove(control)
            r = self.__update(self)
        self.__handle_mount_unmount(*r)

    def remove_at(self, index: int) -> None:
        with self.__lock:
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

    def _close(self) -> None:
        # self.__pubsub.unsubscribe_all()
        # removed_controls = self._remove_control_recursively(self.index, self)
        # for c in removed_controls:
        #     c.will_unmount()
        #     c._dispose()
        # self._controls.clear()
        # self.__on_view_pop = None
        # self.__client_storage = None
        # self.__session_storage = None
        # self.__conn = None
        pass

    def __get_session(self):
        if sess := self.__session():
            return sess
        raise Exception("An attempt to fetch destroyed session.")

    def __update(self, *controls: Control) -> Tuple[List[Control], List[Control]]:
        if not self.__conn:
            raise PageDisconnectedException("Page has been disconnected")
        commands, added_controls, removed_controls = self.__prepare_update(*controls)
        self.__validate_controls_page(added_controls)
        results = self.__conn.send_commands(self._session_id, commands).results
        self.__update_control_ids(added_controls, results)
        return added_controls, removed_controls

    def __prepare_update(
        self, *controls: Control
    ) -> Tuple[List[Any], List[Control], List[Control]]:
        added_controls = []
        removed_controls = []
        commands = []

        # build commands

        for control in controls:
            control.build_update_commands(
                self._index, commands, added_controls, removed_controls
            )
        return commands, added_controls, removed_controls

    def __validate_controls_page(self, added_controls: List[Control]) -> None:
        for ctrl in added_controls:
            if ctrl.page and ctrl.page != self:
                raise Exception(
                    f"Control has already been added to another page: {ctrl}"
                )

    def __update_control_ids(
        self, added_controls: List[Control], results: List[Any]
    ) -> None:
        if len(results) > 0:
            n = 0
            for line in results:
                for id in line.split(" "):
                    added_controls[n]._Control__uid = id

                    # add to index
                    self._index[id] = added_controls[n]

                    n += 1

    def __handle_mount_unmount(self, added_controls, removed_controls) -> None:
        for ctrl in removed_controls:
            ctrl.will_unmount()
            ctrl.parent = None  # remove parent reference
            ctrl.page = None
        for ctrl in added_controls:
            ctrl.did_mount()

    def error(self, message: str = "") -> None:
        with self.__lock:
            self._send_command("error", [message])

    async def on_event_async(self, e: Event) -> None:
        logger.debug(f"page.on_event_async: {e.target} {e.name} {e.data}")

        if e.target == "page" and e.name == "change":
            with self.__lock:
                self.__on_page_change_event(e.data)
        elif e.target in self._index:
            ce = ControlEvent(e.target, e.name, e.data, self._index[e.target], self)
            handler = self._index[e.target].event_handlers.get(e.name)
            if handler:
                if asyncio.iscoroutinefunction(handler):
                    await handler(ce)
                else:
                    self.run_thread(handler, ce)

    def __on_page_change_event(self, data: str) -> None:
        for props in json.loads(data):
            id = props["i"]
            if id in self._index:
                for name in props:
                    if name != "i":
                        self._index[id]._set_attr(name, props[name], dirty=False)
                        if id in self.__snapshot:
                            self.__snapshot[id][name] = props[name]

    def run_task(
        self,
        handler: Callable[InputT, Awaitable[RetT]],
        *args: InputT.args,
        **kwargs: InputT.kwargs,
    ) -> Future[RetT]:
        _session_page.set(self)
        assert asyncio.iscoroutinefunction(handler)

        future = asyncio.run_coroutine_threadsafe(handler(*args, **kwargs), self.__loop)

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
            assert self.__loop
            self.__loop.call_soon_threadsafe(
                self.__loop.run_in_executor,
                self.__executor,
                partial(handler_with_context, *args, **kwargs),
            )

    def go(
        self, route: str, skip_route_change_event: bool = False, **kwargs: Any
    ) -> None:
        self.route = route if not kwargs else route + self.query.post(kwargs)

        if not skip_route_change_event:
            self.run_task(
                self.__on_route_change.get_handler(),
                ControlEvent(
                    target="page",
                    name="route_change",
                    data=self.route,
                    page=self,
                    control=self,
                ),
            )
        self.update()
        self.query()  # Update query url (required when using go)

    def get_upload_url(self, file_name: str, expires: int) -> str:
        r = self._send_command(
            "getUploadUrl", attrs={"file": file_name, "expires": str(expires)}
        )
        if r.error:
            raise Exception(r.error)
        return r.result

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
        await self.on_event_async(Event("page", "authorize", json.dumps(data)))

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

    def _send_command(
        self,
        name: str,
        values: Optional[List[str]] = None,
        attrs: Optional[Dict[str, str]] = None,
    ):
        return self.__conn.send_command(
            self._session_id,
            Command(
                indent=0,
                name=name,
                values=values if values is not None else [],
                attrs=attrs or {},
            ),
        )

    def set_clipboard(self, value: str, wait_timeout: Optional[float] = 10) -> None:
        self._invoke_method("setClipboard", {"data": value}, wait_timeout=wait_timeout)

    def get_clipboard(self, wait_timeout: Optional[float] = 10) -> Optional[str]:
        return self._invoke_method(
            "getClipboard", wait_for_result=True, wait_timeout=wait_timeout
        )

    async def get_clipboard_async(
        self, wait_timeout: Optional[float] = 10
    ) -> Optional[str]:
        return await self._invoke_method_async(
            "getClipboard", wait_for_result=True, wait_timeout=wait_timeout
        )

    def launch_url(
        self,
        url: str,
        web_window_name: Optional[str] = None,
        web_popup_window: Optional[bool] = False,
        window_width: Optional[int] = None,
        window_height: Optional[int] = None,
    ) -> None:
        args = {"url": url}
        if web_window_name:
            args["web_window_name"] = web_window_name
        if web_popup_window:
            args["web_popup_window"] = str(web_popup_window)
        if window_width:
            args["window_width"] = str(window_width)
        if window_height:
            args["window_height"] = str(window_height)
        self._invoke_method("launchUrl", args)

    def can_launch_url(self, url: str) -> bool:
        args = {"url": url}
        return self._invoke_method("canLaunchUrl", args, wait_for_result=True) == "true"

    async def can_launch_url_async(self, url: str) -> bool:
        args = {"url": url}
        return (
            await self._invoke_method_async("canLaunchUrl", args, wait_for_result=True)
            == "true"
        )

    def close_in_app_web_view(self) -> None:
        self._invoke_method("closeInAppWebView")

    def scroll_to(
        self,
        offset: Optional[float] = None,
        delta: Optional[float] = None,
        key: Optional[str] = None,
        duration: Optional[int] = None,
        curve: Optional[AnimationCurve] = None,
    ) -> None:
        self.__default_view.scroll_to(
            offset=offset, delta=delta, key=key, duration=duration, curve=curve
        )

    def _invoke_method(
        self,
        method_name: str,
        arguments: Optional[Dict[str, str]] = None,
        control_id: Optional[str] = "",
        wait_for_result: Optional[bool] = False,
        wait_timeout: Optional[float] = 5,
    ) -> Optional[str]:
        method_id = uuid.uuid4().hex

        # register callback
        evt: Optional[threading.Event] = None
        if wait_for_result:
            evt = threading.Event()
            self.__method_calls[method_id] = evt

        # call method
        result = self._send_command(
            "invokeMethod", values=[method_id, method_name, control_id], attrs=arguments
        )

        if result.error != "":
            if wait_for_result:
                del self.__method_calls[method_id]
            raise Exception(result.error)
        if not wait_for_result:
            return
        assert evt is not None

        if not evt.wait(wait_timeout):
            del self.__method_calls[method_id]
            raise TimeoutError(
                f"Timeout waiting for invokeMethod {method_name}({arguments}) call"
            )

        result, err = self.__method_call_results.pop(evt)
        if err:
            raise Exception(err)
        if result is None or result == "null":
            return None
        return result

    async def _invoke_method_async(
        self,
        method_name: str,
        arguments: Optional[Dict[str, str]] = None,
        control_id: Optional[str] = "",
        wait_for_result: Optional[bool] = False,
        wait_timeout: Optional[float] = 5,
    ) -> Optional[str]:
        method_id = uuid.uuid4().hex

        # register callback
        evt: Optional[asyncio.Event] = None
        if wait_for_result:
            evt = asyncio.Event()
            self.__method_calls[method_id] = evt

        # call method
        result = self._send_command(
            "invokeMethod", values=[method_id, method_name, control_id], attrs=arguments
        )

        if result.error != "":
            if wait_for_result:
                del self.__method_calls[method_id]
            raise Exception(result.error)
        if not wait_for_result:
            return
        assert evt is not None

        try:
            await asyncio.wait_for(evt.wait(), timeout=wait_timeout)
        except TimeoutError:
            del self.__method_calls[method_id]
            raise TimeoutError(
                f"Timeout waiting for invokeMethod {method_name}({arguments}) call"
            )

        result, err = self.__method_call_results.pop(evt)
        if err:
            raise Exception(err)
        if result == "null":
            return None
        return result

    def __on_invoke_method_result(self, e) -> None:
        d = json.loads(e.data)
        result = InvokeMethodResults(**d)
        evt = self.__method_calls.pop(result.method_id, None)
        if evt is None:
            return
        self.__method_call_results[evt] = (result.result, result.error)
        evt.set()

    def open(self, control: Control) -> None:
        if not hasattr(control, "open"):
            raise ValueError(f"{control.__class__.__qualname__} has no open attribute")

        control.open = True

        if isinstance(control, NavigationDrawer):
            if control.position == NavigationDrawerPosition.END:
                if self.end_drawer != control:
                    self.end_drawer = control
                    self.update()
            else:
                if self.drawer != control:
                    self.drawer = control
                    self.update()
        else:
            if control not in self.offstage.controls:
                self.offstage.controls.append(control)
                self.offstage.update()

        control.update()

    @staticmethod
    def close(control: Control) -> None:
        if hasattr(control, "open"):
            control.open = False
            control.update()
        else:
            raise ValueError(f"{control.__class__.__qualname__} has no open attribute")

    # query
    @property
    def query(self) -> QueryString:
        return self.__query

    # url
    @property
    def url(self) -> Optional[str]:
        return self.__get_session().connection.page_url

    # name
    @property
    def name(self) -> str:
        return self.__get_session().connection.page_name

    # loop
    @property
    def loop(self) -> asyncio.AbstractEventLoop:
        return self.__loop

    # executor
    @property
    def executor(self) -> Optional[ThreadPoolExecutor]:
        return self.__executor

    # auth
    @property
    def auth(self) -> Optional[Authorization]:
        return self.__authorization

    # pubsub
    @property
    def pubsub(self) -> PubSubClient:
        return self.__get_session().pubsub_client

    # overlay
    @property
    def overlay(self) -> List[Control]:
        return self.offstage.controls

    # browser_context_menu
    @property
    def browser_context_menu(self) -> BrowserContextMenu:
        return self.__browser_context_menu

    # controls
    @property
    def controls(self) -> List[Control]:
        return self.__default_view().controls

    @controls.setter
    def controls(self, value: List[Control]):
        self.__default_view().controls = value

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
    def padding(self) -> Optional[PaddingValue]:
        return self.__default_view().padding

    @padding.setter
    def padding(self, value: Optional[PaddingValue]):
        self.__default_view().padding = value

    # bgcolor
    @property
    def bgcolor(self) -> Optional[ColorValue]:
        return self.__default_view().bgcolor

    @bgcolor.setter
    def bgcolor(self, value: Optional[ColorValue]):
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
    def auto_scroll(self) -> bool:
        return self.__default_view().auto_scroll

    @auto_scroll.setter
    def auto_scroll(self, value: Optional[bool]):
        self.__default_view().auto_scroll = value

    # client_storage
    @property
    def client_storage(self) -> ClientStorage:
        return self.__client_storage

    # session_storage
    @property
    def session(self) -> SessionStorage:
        return self.__session_storage

    # Magic methods
    def __contains__(self, item: Control) -> bool:
        return item in self.controls


@control("offstage")
class Offstage(Control):
    controls: List[Control] = field(default_factory=lambda: [])


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
class PageMediaData(ControlEvent):
    padding: Padding
    view_padding: Padding
    view_insets: Padding


@dataclass
class AppLifecycleStateChangeEvent(ControlEvent):
    state: AppLifecycleState


@dataclass
class WindowEvent(ControlEvent):
    type: WindowEventType


@dataclass
class WindowResizeEvent(ControlEvent):
    width: float
    sheight: float
