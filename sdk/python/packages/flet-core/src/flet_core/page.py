import asyncio
import json
import logging
import threading
import time
import uuid
from asyncio import AbstractEventLoop
from concurrent.futures import ThreadPoolExecutor, Future
from contextvars import ContextVar
from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone
from functools import partial
from typing import (
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
    cast,
)
from urllib.parse import urlparse

try:
    from typing import ParamSpec
except ImportError:
    from typing_extensions import ParamSpec

import flet_core
from flet_core.adaptive_control import AdaptiveControl
from flet_core.alert_dialog import AlertDialog
from flet_core.alignment import Alignment
from flet_core.animation import AnimationCurve
from flet_core.app_bar import AppBar
from flet_core.banner import Banner
from flet_core.bottom_app_bar import BottomAppBar
from flet_core.bottom_sheet import BottomSheet
from flet_core.client_storage import ClientStorage
from flet_core.connection import Connection
from flet_core.control import Control
from flet_core.control_event import ControlEvent
from flet_core.cupertino_alert_dialog import CupertinoAlertDialog
from flet_core.cupertino_app_bar import CupertinoAppBar
from flet_core.cupertino_bottom_sheet import CupertinoBottomSheet
from flet_core.cupertino_navigation_bar import CupertinoNavigationBar
from flet_core.event import Event
from flet_core.event_handler import EventHandler
from flet_core.floating_action_button import FloatingActionButton
from flet_core.locks import NopeLock
from flet_core.navigation_bar import NavigationBar
from flet_core.navigation_drawer import NavigationDrawer, NavigationDrawerPosition
from flet_core.padding import Padding
from flet_core.protocol import Command
from flet_core.pubsub import PubSubClient
from flet_core.querystring import QueryString
from flet_core.scrollable_control import OnScrollEvent
from flet_core.session_storage import SessionStorage
from flet_core.snack_bar import SnackBar
from flet_core.theme import Theme
from flet_core.types import (
    AppLifecycleState,
    Brightness,
    CrossAxisAlignment,
    FloatingActionButtonLocation,
    MainAxisAlignment,
    OffsetValue,
    OptionalNumber,
    PaddingValue,
    PagePlatform,
    ScrollMode,
    ThemeMode,
    Wrapper,
    OptionalEventCallable,
    WindowEventType,
)
from flet_core.utils import classproperty, deprecated
from flet_core.utils.concurrency_utils import is_pyodide
from flet_core.view import View

logger = logging.getLogger(flet_core.__name__)

_session_page = ContextVar("flet_session_page", default=None)


class context:
    @classproperty
    def page(cls) -> "Page":
        return _session_page.get()


try:
    from flet_runtime.auth.authorization import Authorization
    from flet_runtime.auth.oauth_provider import OAuthProvider
except ImportError:

    class OAuthProvider:
        ...

    class Authorization:
        def __init__(
            self,
            provider: OAuthProvider,
            fetch_user: bool,
            fetch_groups: bool,
            scope: Optional[List[str]] = None,
        ):
            ...


AT = TypeVar("AT", bound=Authorization)

InputT = ParamSpec("InputT")
RetT = TypeVar("RetT")


@dataclass
class Locale:
    language_code: Optional[str] = field(default=None)
    country_code: Optional[str] = field(default=None)
    script_code: Optional[str] = field(default=None)


@dataclass
class LocaleConfiguration:
    supported_locales: Optional[List[Locale]] = field(default=None)
    current_locale: Optional[Locale] = field(default=None)


class PageDisconnectedException(Exception):
    def __init__(self, message):
        super().__init__(message)


class BrowserContextMenu:
    def __init__(self, page: "Page"):
        self.page = page
        self.disabled = False

    def enable(self, wait_timeout: Optional[float] = 10):
        self.page._invoke_method("enableBrowserContextMenu", wait_timeout=wait_timeout)
        self.disabled = False

    def disable(self, wait_timeout: Optional[float] = 10):
        self.page._invoke_method("disableBrowserContextMenu", wait_timeout=wait_timeout)
        self.disabled = True


class Window:
    def __init__(self, page: "Page"):
        self.page = page
        self.__alignment = None
        self.__on_event = EventHandler(lambda e: WindowEvent(e))
        self.page._add_event_handler(
            "window_event",
            self.__on_event.get_handler(),
        )

    # bgcolor
    @property
    def bgcolor(self) -> Optional[str]:
        return self.page._get_attr("windowBgcolor")

    @bgcolor.setter
    def bgcolor(self, value: Optional[str]):
        self.page._set_attr("windowBgcolor", value)

    # width
    @property
    def width(self) -> OptionalNumber:
        w = self.page._get_attr("windowWidth")
        return float(w) if w else 0

    @width.setter
    def width(self, value: OptionalNumber):
        self.page._set_attr("windowWidth", value)

    # height
    @property
    def height(self) -> OptionalNumber:
        h = self.page._get_attr("windowHeight")
        return float(h) if h else 0

    @height.setter
    def height(self, value: OptionalNumber):
        self.page._set_attr("windowHeight", value)

    # top
    @property
    def top(self) -> OptionalNumber:
        w = self.page._get_attr("windowTop")
        return float(w) if w else 0

    @top.setter
    def top(self, value: OptionalNumber):
        self.page._set_attr("windowTop", value)

    # left
    @property
    def left(self) -> OptionalNumber:
        h = self.page._get_attr("windowLeft")
        return float(h) if h else 0

    @left.setter
    def left(self, value: OptionalNumber):
        self.page._set_attr("windowLeft", value)

    # max_width
    @property
    def max_width(self) -> OptionalNumber:
        return self.page._get_attr("windowMaxWidth")

    @max_width.setter
    def max_width(self, value: OptionalNumber):
        self.page._set_attr("windowMaxWidth", value)

    # max_height
    @property
    def max_height(self) -> OptionalNumber:
        return self.page._get_attr("windowMaxHeight")

    @max_height.setter
    def max_height(self, value: OptionalNumber):
        self.page._set_attr("windowMaxHeight", value)

    # min_width
    @property
    def min_width(self) -> OptionalNumber:
        return self.page._get_attr("windowMinWidth")

    @min_width.setter
    def min_width(self, value: OptionalNumber):
        self.page._set_attr("windowMinWidth", value)

    # min_height
    @property
    def min_height(self) -> OptionalNumber:
        return self.page._get_attr("windowMinHeight")

    @min_height.setter
    def min_height(self, value: OptionalNumber):
        self.page._set_attr("windowMinHeight", value)

    # opacity
    @property
    def opacity(self) -> OptionalNumber:
        return self.page._get_attr("windowOpacity", data_type="float", def_value=1)

    @opacity.setter
    def opacity(self, value: OptionalNumber):
        self.page._set_attr("windowOpacity", value)

    # maximized
    @property
    def maximized(self) -> Optional[bool]:
        return self.page._get_attr("windowMaximized", data_type="bool", def_value=False)

    @maximized.setter
    def maximized(self, value: Optional[bool]):
        self.page._set_attr("windowMaximized", value)

    # minimized
    @property
    def minimized(self) -> Optional[bool]:
        return self.page._get_attr("windowMinimized", data_type="bool", def_value=False)

    @minimized.setter
    def minimized(self, value: Optional[bool]):
        self.page._set_attr("windowMinimized", value)

    # minimizable
    @property
    def minimizable(self) -> Optional[bool]:
        return self.page._get_attr(
            "windowMinimizable", data_type="bool", def_value=True
        )

    @minimizable.setter
    def minimizable(self, value: Optional[bool]):
        self.page._set_attr("windowMinimizable", value)

    # maximizable
    @property
    def maximizable(self) -> Optional[bool]:
        return self.page._get_attr(
            "windowMaximizable", data_type="bool", def_value=True
        )

    @maximizable.setter
    def maximizable(self, value: Optional[bool]):
        self.page._set_attr("windowMaximizable", value)

    # resizable
    @property
    def resizable(self) -> Optional[bool]:
        return self.page._get_attr("windowResizable", data_type="bool", def_value=True)

    @resizable.setter
    def resizable(self, value: Optional[bool]):
        self.page._set_attr("windowResizable", value)

    # movable
    @property
    def movable(self) -> Optional[bool]:
        return self.page._get_attr("windowMovable", data_type="bool", def_value=True)

    @movable.setter
    def movable(self, value: Optional[bool]):
        self.page._set_attr("windowMovable", value)

    # full_screen
    @property
    def full_screen(self) -> Optional[bool]:
        return self.page._get_attr(
            "windowFullScreen", data_type="bool", def_value=False
        )

    @full_screen.setter
    def full_screen(self, value: Optional[bool]):
        self.page._set_attr("windowFullScreen", value)

    # always_on_top
    @property
    def always_on_top(self) -> Optional[bool]:
        return self.page._get_attr(
            "windowAlwaysOnTop", data_type="bool", def_value=False
        )

    @always_on_top.setter
    def always_on_top(self, value: Optional[bool]):
        self.page._set_attr("windowAlwaysOnTop", value)

    # prevent_close
    @property
    def prevent_close(self) -> Optional[bool]:
        return self.page._get_attr(
            "windowPreventClose", data_type="bool", def_value=False
        )

    @prevent_close.setter
    def prevent_close(self, value: Optional[bool]):
        self.page._set_attr("windowPreventClose", value)

    # title_bar_hidden
    @property
    def title_bar_hidden(self) -> Optional[bool]:
        return self.page._get_attr(
            "windowTitleBarHidden", data_type="bool", def_value=False
        )

    @title_bar_hidden.setter
    def title_bar_hidden(self, value: Optional[bool]):
        self.page._set_attr("windowTitleBarHidden", value)

    # title_bar_buttons_hidden
    @property
    def title_bar_buttons_hidden(self) -> Optional[bool]:
        return self.page._get_attr(
            "windowTitleBarButtonsHidden", data_type="bool", def_value=False
        )

    @title_bar_buttons_hidden.setter
    def title_bar_buttons_hidden(self, value: Optional[bool]):
        self.page._set_attr("windowTitleBarButtonsHidden", value)

    # skip_task_bar
    @property
    def skip_task_bar(self) -> Optional[bool]:
        return self.page._get_attr(
            "windowSkipTaskBar", data_type="bool", def_value=False
        )

    @skip_task_bar.setter
    def skip_task_bar(self, value: Optional[bool]):
        self.page._set_attr("windowSkipTaskBar", value)

    # frameless
    @property
    def frameless(self) -> Optional[bool]:
        return self.page._get_attr("windowFrameless", data_type="bool", def_value=False)

    @frameless.setter
    def frameless(self, value: Optional[bool]):
        self.page._set_attr("windowFrameless", value)

    # progress_bar
    @property
    def progress_bar(self) -> OptionalNumber:
        return self.page._get_attr("windowProgressBar")

    @progress_bar.setter
    def progress_bar(self, value: OptionalNumber):
        self.page._set_attr("windowProgressBar", value)

    # focused
    @property
    def focused(self) -> Optional[bool]:
        return self.page._get_attr("windowFocused", data_type="bool", def_value=True)

    @focused.setter
    def focused(self, value: Optional[bool]):
        self.page._set_attr("windowFocused", value)

    # visible
    @property
    def visible(self) -> Optional[bool]:
        return self.page._get_attr("windowVisible", data_type="bool")

    @visible.setter
    def visible(self, value: Optional[bool]):
        self.page._set_attr("windowVisible", value)

    # always_on_bottom
    @property
    def always_on_bottom(self) -> Optional[bool]:
        return self.page._get_attr(
            "windowAlwaysOnBottom", data_type="bool", def_value=False
        )

    @always_on_bottom.setter
    def always_on_bottom(self, value: Optional[bool]):
        self.page._set_attr("windowAlwaysOnBottom", value)

    # wait_until_ready_to_show
    @property
    def wait_until_ready_to_show(self) -> Optional[bool]:
        return self.page._get_attr(
            "windowWaitUntilReadyToShow", data_type="bool", def_value=False
        )

    @wait_until_ready_to_show.setter
    def wait_until_ready_to_show(self, value: Optional[bool]):
        self.page._set_attr("windowWaitUntilReadyToShow", value)

    # shadow
    @property
    def shadow(self) -> Optional[bool]:
        return self.page._get_attr("windowShadow", data_type="bool", def_value=False)

    @shadow.setter
    def shadow(self, value: Optional[bool]):
        self.page._set_attr("windowShadow", value)

    # alignment
    @property
    def alignment(self) -> Optional[Alignment]:
        return self.__alignment

    @alignment.setter
    def alignment(self, value: Optional[Alignment]):
        self.__alignment = value

    # badge_label
    @property
    def badge_label(self) -> Optional[str]:
        return self.page._get_attr("windowBadgeLabel")

    @badge_label.setter
    def badge_label(self, value: Optional[str]):
        self.page._set_attr("windowBadgeLabel", value)

    # icon
    @property
    def icon(self) -> Optional[str]:
        return self.page._get_attr("windowIcon")

    @icon.setter
    def icon(self, value: Optional[str]):
        self.page._set_attr("windowIcon", value)

    # Methods
    def destroy(self):
        self.page._set_attr("windowDestroy", True)
        self.page.update()

    def center(self) -> None:
        self.page._set_attr("windowCenter", str(time.time()))
        self.page.update()

    def close(self) -> None:
        self.page._set_attr("windowClose", str(time.time()))
        self.page.update()

    def to_front(self) -> None:
        self.page._invoke_method("windowToFront")

    # Events
    # on_event
    @property
    def on_event(self):
        return self.__on_event

    @on_event.setter
    def on_event(self, handler: "Optional[Callable[[WindowEvent], None]]"):
        self.__on_event.subscribe(handler)


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

    def __init__(
        self,
        conn: Connection,
        session_id,
        loop: asyncio.AbstractEventLoop,
        executor: Optional[ThreadPoolExecutor] = None,
    ) -> None:
        Control.__init__(self)
        self._id = "page"
        self._Control__uid = "page"
        self.__window = Window(self)
        self.__browser_context_menu = BrowserContextMenu(self)
        self.__conn = conn
        self.__next_control_id = 1
        self.__snapshot: Dict[str, Dict[str, Any]] = {}
        self.__expires_at = None
        self.__query: QueryString = QueryString(page=self)  # Querystring
        self._session_id = session_id
        self.__loop = loop
        self.__executor = executor
        self._index = {self._Control__uid: self}  # index with all page controls

        self.__lock = threading.Lock() if not is_pyodide() else NopeLock()

        self.__views = [View()]
        self.__default_view = self.__views[0]
        self._controls = self.__default_view.controls

        self.__fonts: Optional[Dict[str, str]] = None
        self.__offstage = Offstage()
        self.__theme = None
        self.__dark_theme = None
        self.__locale_configuration = None
        self.__theme_mode = ThemeMode.SYSTEM  # Default Theme Mode
        self.__pubsub: PubSubClient = PubSubClient(conn.pubsubhub, session_id)
        self.__client_storage: ClientStorage = ClientStorage(self)
        self.__session_storage: SessionStorage = SessionStorage(self)
        self.__authorization: Optional[Authorization] = None

        self.__on_close = EventHandler()
        self._add_event_handler("close", self.__on_close.get_handler())
        self.__on_platform_brightness_change = EventHandler()
        self._add_event_handler(
            "platformBrightnessChange",
            self.__on_platform_brightness_change.get_handler(),
        )

        self.__on_app_lifecycle_state_change = EventHandler(
            lambda e: AppLifecycleStateChangeEvent(e)
        )
        self._add_event_handler(
            "app_lifecycle_state_change",
            self.__on_app_lifecycle_state_change.get_handler(),
        )
        self.__on_resized = EventHandler(lambda e: WindowResizeEvent(e))
        self._add_event_handler("resized", self.__on_resized.get_handler())

        self.__last_route = None

        # authorize/login/logout

        self.__on_login = EventHandler()
        self._add_event_handler("authorize", self.__on_authorize_async)
        self.__on_logout = EventHandler()

        # route_change

        def convert_route_change_event(e):
            if self.__last_route == e.data:
                return None  # avoid duplicate calls
            self.__last_route = e.data
            self._set_attr("route", e.data, False)
            self.query()  # Update query url (required when manually changed from browser)
            return RouteChangeEvent(route=e.data)

        self.__on_route_change: EventHandler = EventHandler(convert_route_change_event)
        self._add_event_handler("route_change", self.__on_route_change.get_handler())

        def convert_view_pop_event(e):
            return ViewPopEvent(view=cast(View, self.get_control(e.data)))

        self.__on_view_pop = EventHandler(convert_view_pop_event)
        self._add_event_handler("view_pop", self.__on_view_pop.get_handler())

        def convert_keyboard_event(e):
            d = json.loads(e.data)
            return KeyboardEvent(**d)

        self.__on_keyboard_event = EventHandler(convert_keyboard_event)
        self._add_event_handler(
            "keyboard_event", self.__on_keyboard_event.get_handler()
        )

        def convert_page_media_change_event(e):
            d = json.loads(e.data)
            return PageMediaData(**d)

        self.__on_page_media_change_event = EventHandler(
            convert_page_media_change_event
        )
        self._add_event_handler(
            "mediaChange", self.__on_page_media_change_event.get_handler()
        )

        self.__method_calls: Dict[str, Union[threading.Event, asyncio.Event]] = {}
        self.__method_call_results: Dict[
            Union[threading.Event, asyncio.Event], tuple[Optional[str], Optional[str]]
        ] = {}
        self._add_event_handler("invoke_method_result", self.__on_invoke_method_result)

        self.__on_connect = EventHandler()
        self._add_event_handler("connect", self.__on_connect.get_handler())
        self.__on_disconnect = EventHandler()
        self._add_event_handler("disconnect", self.__on_disconnect.get_handler())
        self.__on_error = EventHandler()
        self._add_event_handler("error", self.__on_error.get_handler())

        _session_page.set(self)

    def get_control(self, id: int) -> Control:
        return self._index.get(id)

    def before_update(self) -> None:
        super().before_update()
        self._set_attr_json("fonts", self.__fonts)
        self._set_attr_json("theme", self.__theme)
        self._set_attr_json("localeConfiguration", self.__locale_configuration)
        self._set_attr_json("darkTheme", self.__dark_theme)
        self._set_attr_json("windowAlignment", self.__window.alignment)

        # keyboard event
        if self.__on_keyboard_event.count() > 0:
            self._set_attr("onKeyboardEvent", True)

    def _get_control_name(self):
        return "page"

    def _get_children(self):
        children = []
        children.extend(self.__views)
        children.append(self.__offstage)
        return children

    def get_next_control_id(self) -> int:
        r = self.__next_control_id
        self.__next_control_id += 1
        return r

    async def fetch_page_details_async(self) -> None:
        assert self.__conn
        props = [
            "route",
            "pwa",
            "web",
            "debug",
            "platform",
            "platformBrightness",
            "media",
            "width",
            "height",
            "windowWidth",
            "windowHeight",
            "windowTop",
            "windowLeft",
            "clientIP",
            "clientUserAgent",
        ]
        values = (
            self.__conn.send_commands(
                self._session_id,
                [Command(0, "get", ["page", prop]) for prop in props],
            )
        ).results
        for i in range(len(props)):
            self._set_attr(props[i], values[i], False)

    async def _connect(self, conn: Connection) -> None:
        _session_page.set(self)
        self.__conn = conn
        self.__expires_at = None
        await self.on_event_async(Event("page", "connect", ""))

    async def _disconnect(self, session_timeout_seconds: int) -> None:
        self.__expires_at = datetime.now(timezone.utc) + timedelta(
            seconds=session_timeout_seconds
        )
        await self.on_event_async(Event("page", "disconnect", ""))

    def update(self, *controls) -> None:
        with self.__lock:
            if len(controls) == 0:
                r = self.__update(self)
            else:
                r = self.__update(*controls)
        self.__handle_mount_unmount(*r)

    @deprecated(
        reason="Use Page.update() method instead.",
        version="0.21.0",
        delete_version="0.26.0",
    )
    async def update_async(self, *controls):
        self.update(*controls)

    def add(self, *controls: Control) -> None:
        with self.__lock:
            self._controls.extend(controls)
            r = self.__update(self)
        self.__handle_mount_unmount(*r)

    @deprecated(
        reason="Use Page.add() method instead.",
        version="0.21.0",
        delete_version="0.26.0",
    )
    async def add_async(self, *controls):
        self.add(*controls)

    def insert(self, at: int, *controls: Control) -> None:
        with self.__lock:
            n = at
            for control in controls:
                self._controls.insert(n, control)
                n += 1
            r = self.__update(self)
        self.__handle_mount_unmount(*r)

    @deprecated(
        reason="Use Page.insert() method instead.",
        version="0.21.0",
        delete_version="0.26.0",
    )
    async def insert_async(self, at, *controls):
        self.insert(at, *controls)

    def remove(self, *controls: Control) -> None:
        with self.__lock:
            for control in controls:
                self._controls.remove(control)
            r = self.__update(self)
        self.__handle_mount_unmount(*r)

    @deprecated(
        reason="Use Page.remove() method instead.",
        version="0.21.0",
        delete_version="0.26.0",
    )
    async def remove_async(self, *controls):
        self.remove(*controls)

    def remove_at(self, index: int) -> None:
        with self.__lock:
            self._controls.pop(index)
            r = self.__update(self)
        self.__handle_mount_unmount(*r)

    @deprecated(
        reason="Use Page.remove_at() method instead.",
        version="0.21.0",
        delete_version="0.26.0",
    )
    async def remove_at_async(self, index):
        self.remove_at(index)

    def clean(self) -> None:
        self._clean(self)
        self._controls.clear()

    @deprecated(
        reason="Use Page.clean() method instead.",
        version="0.21.0",
        delete_version="0.26.0",
    )
    async def clean_async(self):
        self.clean()

    def _clean(self, control: Control) -> None:
        with self.__lock:
            control._previous_children.clear()
            assert control.uid is not None
            removed_controls = []
            for child in control._get_children():
                removed_controls.extend(
                    self._remove_control_recursively(self.index, child)
                )
            self._send_command("clean", [control.uid])
            for c in removed_controls:
                c.will_unmount()

    def _close(self) -> None:
        self.__pubsub.unsubscribe_all()
        removed_controls = self._remove_control_recursively(self.index, self)
        for c in removed_controls:
            c.will_unmount()
            c._dispose()
        self._controls.clear()
        self._previous_children.clear()
        self.__on_view_pop = None
        self.__client_storage = None
        self.__session_storage = None
        self.__conn = None

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

    @deprecated(
        reason="Use Page.error() method instead.",
        version="0.21.0",
        delete_version="0.26.0",
    )
    async def error_async(self, message=""):
        self.error(message)

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

    def run_task(
        self,
        handler: Callable[InputT, Awaitable[RetT]],
        *args: InputT.args,
        **kwargs: InputT.kwargs,
    ) -> "Future[RetT]":
        _session_page.set(self)
        assert asyncio.iscoroutinefunction(handler)

        future = asyncio.run_coroutine_threadsafe(handler(*args, **kwargs), self.__loop)

        def _on_completion(f):
            exception = f.exception()

            if exception:
                raise exception

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

    @deprecated(
        reason="Use Page.go() method instead.",
        version="0.21.0",
        delete_version="0.26.0",
    )
    async def go_async(self, route, skip_route_change_event=False, **kwargs):
        self.go(route, skip_route_change_event, **kwargs)

    def get_upload_url(self, file_name: str, expires: int) -> str:
        r = self._send_command(
            "getUploadUrl", attrs={"file": file_name, "expires": str(expires)}
        )
        if r.error:
            raise Exception(r.error)
        return r.result

    @deprecated(
        reason="Use Page.get_upload_url() method instead.",
        version="0.21.0",
        delete_version="0.26.0",
    )
    async def get_upload_url_async(self, file_name: str, expires: int):
        return self.get_upload_url(file_name, expires)

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
        state = d["state"]
        assert state == self.__authorization.state

        if not self.web:
            if self.platform in ["ios", "android"]:
                # close web view on mobile

                self.close_in_app_web_view()
            else:
                # activate desktop window

                self.window_to_front()
        login_evt = LoginEvent(
            error=d["error"],
            error_description=d["error_description"],
            page=self,
            control=self,
            target="page",
            name="on_login",
            data="",
        )
        if not login_evt.error:
            # perform token request

            code = d["code"]
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

    @deprecated(
        reason="Use Page.logout() method instead.",
        version="0.21.0",
        delete_version="0.26.0",
    )
    async def logout_async(self):
        self.logout()

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

    @deprecated(
        reason="Use Page.set_clipboard() method instead.",
        version="0.21.0",
        delete_version="0.26.0",
    )
    async def set_clipboard_async(self, value: str, wait_timeout: Optional[float] = 10):
        self.set_clipboard(value, wait_timeout=wait_timeout)

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

    @deprecated(
        reason="Use Page.launch_url() method instead.",
        version="0.21.0",
        delete_version="0.26.0",
    )
    async def launch_url_async(
        self,
        url: str,
        web_window_name: Optional[str] = None,
        web_popup_window: bool = False,
        window_width: Optional[int] = None,
        window_height: Optional[int] = None,
    ):
        self.launch_url(
            url, web_window_name, web_popup_window, window_width, window_height
        )

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

    @deprecated(
        reason="Use Page.close_in_app_web_view() method instead.",
        version="0.21.0",
        delete_version="0.26.0",
    )
    async def close_in_app_web_view_async(self):
        self.close_in_app_web_view()

    @deprecated(
        reason="Use Page.window.to_front() method instead.",
        version="0.21.0",
        delete_version="0.26.0",
    )
    def window_to_front(self) -> None:
        self.__window.to_front()

    @deprecated(
        reason="Use Page.window.to_front() method instead.",
        version="0.21.0",
        delete_version="0.26.0",
    )
    async def window_to_front_async(self):
        self.__window.to_front()

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

    @deprecated(
        reason="Use Page.scroll_to() method instead.",
        version="0.21.0",
        delete_version="0.26.0",
    )
    async def scroll_to_async(
        self,
        offset: Optional[float] = None,
        delta: Optional[float] = None,
        key: Optional[str] = None,
        duration: Optional[int] = None,
        curve: Optional[AnimationCurve] = None,
    ):
        self.scroll_to(offset, delta, key, duration, curve)

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
            raise ValueError("control has no open attribute")

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
            if control not in self.__offstage.controls:
                self.__offstage.controls.append(control)
                self.__offstage.update()

        control.update()

    @staticmethod
    def close(control: Control) -> None:
        if hasattr(control, "open"):
            control.open = False
            control.update()
        else:
            raise ValueError("control has no open attribute")

    #
    # SnackBar
    #
    @deprecated(
        reason="Use Page.open() method instead.",
        version="0.23.0",
        delete_version="0.26.0",
    )
    def show_snack_bar(self, snack_bar: SnackBar):
        self.__offstage.snack_bar = snack_bar
        self.__offstage.snack_bar.open = True
        self.__offstage.update()

    @deprecated(
        reason="Use Page.open() method instead.",
        version="0.21.0",
        delete_version="0.26.0",
    )
    async def show_snack_bar_async(self, snack_bar: SnackBar):
        self.show_snack_bar(snack_bar)

    #
    # Dialogs
    #
    @deprecated(
        reason="Use Page.open() method instead.",
        version="0.23.0",
        delete_version="0.26.0",
    )
    def show_dialog(self, dialog: Union[AlertDialog, CupertinoAlertDialog]):
        self.__offstage.dialog = dialog
        self.__offstage.dialog.open = True
        self.__offstage.update()

    @deprecated(
        reason="Use Page.open() method instead.",
        version="0.21.0",
        delete_version="0.26.0",
    )
    async def show_dialog_async(self, dialog: Union[AlertDialog, CupertinoAlertDialog]):
        self.show_dialog(dialog)

    @deprecated(
        reason="Use Page.close() method instead.",
        version="0.23.0",
        delete_version="0.26.0",
    )
    def close_dialog(self):
        if self.__offstage.dialog is not None:
            self.__offstage.dialog.open = False
            self.__offstage.update()

    @deprecated(
        reason="Use Page.close() method instead.",
        version="0.21.0",
        delete_version="0.26.0",
    )
    async def close_dialog_async(self):
        self.close_dialog()

    #
    # Banner
    #
    @deprecated(
        reason="Use Page.open() method instead.",
        version="0.23.0",
        delete_version="0.26.0",
    )
    def show_banner(self, banner: Banner):
        self.__offstage.banner = banner
        self.__offstage.banner.open = True
        self.__offstage.update()

    @deprecated(
        reason="Use Page.open() method instead.",
        version="0.21.0",
        delete_version="0.26.0",
    )
    async def show_banner_async(self, banner: Banner):
        self.show_banner(banner)

    @deprecated(
        reason="Use Page.close() method instead.",
        version="0.23.0",
        delete_version="0.26.0",
    )
    def close_banner(self):
        if self.__offstage.banner is not None:
            self.__offstage.banner.open = False
            self.__offstage.update()

    @deprecated(
        reason="Use Page.close() method instead.",
        version="0.21.0",
        delete_version="0.26.0",
    )
    async def close_banner_async(self):
        self.close_banner()

    #
    # BottomSheet
    #
    @deprecated(
        reason="Use Page.open() method instead.",
        version="0.23.0",
        delete_version="0.26.0",
    )
    def show_bottom_sheet(
        self,
        bottom_sheet: Union[BottomSheet, CupertinoBottomSheet],
    ):
        self.__offstage.bottom_sheet = bottom_sheet
        self.__offstage.bottom_sheet.open = True
        self.__offstage.update()

    @deprecated(
        reason="Use Page.open() method instead.",
        version="0.21.0",
        delete_version="0.26.0",
    )
    async def show_bottom_sheet_async(
        self,
        bottom_sheet: Union[BottomSheet, CupertinoBottomSheet],
    ):
        self.show_bottom_sheet(bottom_sheet)

    @deprecated(
        reason="Use Page.close() method instead.",
        version="0.23.0",
        delete_version="0.26.0",
    )
    def close_bottom_sheet(self):
        if self.__offstage.bottom_sheet is not None:
            self.__offstage.bottom_sheet.open = False
            self.__offstage.update()

    @deprecated(
        reason="Use Page.close() method instead.",
        version="0.21.0",
        delete_version="0.26.0",
    )
    async def close_bottom_sheet_async(self):
        self.close_bottom_sheet()

    #
    # Drawer
    #
    @deprecated(
        reason="Use Page.close() method instead.",
        version="0.23.0",
        delete_version="0.26.0",
    )
    def show_drawer(self, drawer: NavigationDrawer):
        self.drawer = drawer
        self.drawer.open = True
        self.update()

    @deprecated(
        reason="Use Page.open() method instead.",
        version="0.21.0",
        delete_version="0.26.0",
    )
    async def show_drawer_async(self, drawer: NavigationDrawer):
        self.show_drawer(drawer)

    @deprecated(
        reason="Use Page.close() method instead.",
        version="0.23.0",
        delete_version="0.26.0",
    )
    def close_drawer(self):
        if self.drawer is not None:
            self.drawer.open = False
            self.update()

    @deprecated(
        reason="Use Page.close() method instead.",
        version="0.21.0",
        delete_version="0.26.0",
    )
    async def close_drawer_async(self):
        self.close_drawer()

    #
    # End_drawer
    #
    @deprecated(
        reason="Use Page.close() method instead.",
        version="0.23.0",
        delete_version="0.26.0",
    )
    def show_end_drawer(self, end_drawer: NavigationDrawer):
        self.end_drawer = end_drawer
        self.end_drawer.open = True
        self.update()

    @deprecated(
        reason="Use Page.open() method instead.",
        version="0.21.0",
        delete_version="0.26.0",
    )
    async def show_end_drawer_async(self, end_drawer: NavigationDrawer):
        self.show_end_drawer(end_drawer)

    def close_end_drawer(self):
        if self.end_drawer is not None:
            self.end_drawer.open = False
            self.update()

    @deprecated(
        reason="Use Page.close() method instead.",
        version="0.21.0",
        delete_version="0.26.0",
    )
    async def close_end_drawer_async(self):
        self.close_end_drawer()

    @deprecated(
        reason="Use Page.window.destroy() method instead.",
        version="0.23.0",
        delete_version="0.26.0",
    )
    def window_destroy(self) -> None:
        self.__window.destroy()

    @deprecated(
        reason="Use Page.window.destroy() method instead.",
        version="0.21.0",
        delete_version="0.26.0",
    )
    async def window_destroy_async(self):
        self.__window.destroy()

    @deprecated(
        reason="Use Page.window.center() method instead.",
        version="0.23.0",
        delete_version="0.26.0",
    )
    def window_center(self) -> None:
        self.__window.center()

    @deprecated(
        reason="Use Page.window.center() method instead.",
        version="0.21.0",
        delete_version="0.26.0",
    )
    async def window_center_async(self):
        self.__window.center()

    @deprecated(
        reason="Use Page.window.close() method instead.",
        version="0.23.0",
        delete_version="0.26.0",
    )
    def window_close(self) -> None:
        self.__window.close()

    @deprecated(
        reason="Use Page.window.close() method instead.",
        version="0.21.0",
        delete_version="0.26.0",
    )
    async def window_close_async(self):
        self.__window.close()

    # query
    @property
    def query(self) -> QueryString:
        return self.__query

    # url
    @property
    def url(self) -> Optional[str]:
        return self.__conn.page_url

    # name
    @property
    def name(self) -> str:
        return self.__conn.page_name

    # connection
    @property
    def connection(self) -> Optional[Connection]:
        return self.__conn

    # snapshot
    @property
    def snapshot(self) -> Dict[str, Dict[str, Any]]:
        return self.__snapshot

    # loop
    @property
    def loop(self) -> AbstractEventLoop:
        return self.__loop

    # executor
    @property
    def executor(self) -> Optional[ThreadPoolExecutor]:
        return self.__executor

    # expires_at
    @property
    def expires_at(self) -> Optional[datetime]:
        return self.__expires_at

    # index
    @property
    def index(self) -> "Dict[str, Page]":
        return self._index

    # session_id
    @property
    def session_id(self) -> Any:
        return self._session_id

    # auth
    @property
    def auth(self) -> Optional[Authorization]:
        return self.__authorization

    # pubsub
    @property
    def pubsub(self) -> PubSubClient:
        return self.__pubsub

    # overlay
    @property
    def overlay(self) -> List[Control]:
        return self.__offstage.controls

    # title
    @property
    def title(self) -> str:
        return self._get_attr("title")

    @title.setter
    def title(self, value: str):
        self._set_attr("title", value)

    # route
    @property
    def route(self) -> str:
        return self._get_attr("route")

    @route.setter
    def route(self, value: str):
        self._set_attr("route", value)

    # pwa
    @property
    def pwa(self) -> bool:
        return self._get_attr("pwa", data_type="bool", def_value=False)

    # web
    @property
    def web(self) -> bool:
        return cast(bool, self._get_attr("web", data_type="bool", def_value=False))

    # debug
    @property
    def debug(self) -> bool:
        return cast(bool, self._get_attr("debug", data_type="bool", def_value=False))

    # platform
    @property
    def platform(self) -> PagePlatform:
        return PagePlatform(self._get_attr("platform"))

    @platform.setter
    def platform(self, value: PagePlatform):
        self._set_attr(
            "platform", value.value if isinstance(value, PagePlatform) else value
        )

    # platform_brightness
    @property
    def platform_brightness(self) -> Brightness:
        brightness = self._get_attr("platformBrightness")
        assert brightness
        return Brightness(brightness)

    # media
    @property
    def media(self) -> Optional["PageMediaData"]:
        m = self._get_attr("media")
        if not isinstance(m, str):
            return None
        d = json.loads(m)
        return PageMediaData(**d)

    # client_ip
    @property
    def client_ip(self):
        return self._get_attr("clientIP")

    # client_user_agent
    @property
    def client_user_agent(self):
        return self._get_attr("clientUserAgent")

    # fonts
    @property
    def fonts(self) -> Optional[Dict[str, str]]:
        return self.__fonts

    @fonts.setter
    def fonts(self, value: Optional[Dict[str, str]]):
        self.__fonts = value

    # views
    @property
    def views(self) -> List[View]:
        return self.__views

    # controls
    @property
    def controls(self) -> Optional[List[Control]]:
        return self.__default_view.controls

    @controls.setter
    def controls(self, value: Optional[List[Control]]):
        self.__default_view.controls = value if value is not None else []

    # appbar
    @property
    def appbar(self) -> Union[AppBar, CupertinoAppBar, None]:
        return self.__default_view.appbar

    @appbar.setter
    def appbar(self, value: Union[AppBar, CupertinoAppBar, None]):
        self.__default_view.appbar = value

    # bottom_appbar
    @property
    def bottom_appbar(self) -> Optional[BottomAppBar]:
        return self.__default_view.bottom_appbar

    @bottom_appbar.setter
    def bottom_appbar(self, value: Optional[BottomAppBar]):
        self.__default_view.bottom_appbar = value

    # navigation_bar
    @property
    def navigation_bar(self) -> Optional[Union[NavigationBar, CupertinoNavigationBar]]:
        return self.__default_view.navigation_bar

    @navigation_bar.setter
    def navigation_bar(
        self,
        value: Optional[Union[NavigationBar, CupertinoNavigationBar]],
    ):
        self.__default_view.navigation_bar = value

    # drawer
    @property
    def drawer(self) -> Optional[NavigationDrawer]:
        return self.__default_view.drawer

    @drawer.setter
    def drawer(self, value: Optional[NavigationDrawer]):
        self.__default_view.drawer = value

    # end_drawer
    @property
    def end_drawer(self) -> Optional[NavigationDrawer]:
        return self.__default_view.end_drawer

    @end_drawer.setter
    def end_drawer(self, value: Optional[NavigationDrawer]):
        self.__default_view.end_drawer = value

    # floating_action_button
    @property
    def floating_action_button(self) -> Optional[FloatingActionButton]:
        return self.__default_view.floating_action_button

    @floating_action_button.setter
    def floating_action_button(self, value: Optional[FloatingActionButton]):
        self.__default_view.floating_action_button = value

    # floating_action_button_location
    @property
    def floating_action_button_location(
        self,
    ) -> Union[FloatingActionButtonLocation, OffsetValue]:
        return self.__default_view.floating_action_button_location

    @floating_action_button_location.setter
    def floating_action_button_location(
        self, value: Union[FloatingActionButtonLocation, OffsetValue]
    ):
        self.__default_view.floating_action_button_location = value

    # horizontal_alignment
    @property
    def horizontal_alignment(self) -> CrossAxisAlignment:
        return self.__default_view.horizontal_alignment

    @horizontal_alignment.setter
    def horizontal_alignment(self, value: CrossAxisAlignment):
        self.__default_view.horizontal_alignment = value

    # vertical_alignment
    @property
    def vertical_alignment(self) -> MainAxisAlignment:
        return self.__default_view.vertical_alignment

    @vertical_alignment.setter
    def vertical_alignment(self, value: MainAxisAlignment):
        self.__default_view.vertical_alignment = value

    # window
    @property
    def window(self) -> Window:
        return self.__window

    # browser_context_menu
    @property
    def browser_context_menu(self) -> BrowserContextMenu:
        return self.__browser_context_menu

    # spacing
    @property
    def spacing(self) -> OptionalNumber:
        return self.__default_view.spacing

    @spacing.setter
    def spacing(self, value: OptionalNumber):
        self.__default_view.spacing = value

    # padding
    @property
    def padding(self) -> PaddingValue:
        return self.__default_view.padding

    @padding.setter
    def padding(self, value: PaddingValue):
        self.__default_view.padding = value

    # bgcolor
    @property
    def bgcolor(self) -> Optional[str]:
        return self.__default_view.bgcolor

    @bgcolor.setter
    def bgcolor(self, value: Optional[str]):
        self.__default_view.bgcolor = value

    # scroll
    @property
    def scroll(self) -> Optional[ScrollMode]:
        return self.__default_view.scroll

    @scroll.setter
    def scroll(self, value: Optional[ScrollMode]):
        self.__default_view.scroll = value

    # auto_scroll
    @property
    def auto_scroll(self) -> Optional[bool]:
        return self.__default_view.auto_scroll

    @auto_scroll.setter
    def auto_scroll(self, value: Optional[bool]):
        self.__default_view.auto_scroll = value

    # client_storage
    @property
    def client_storage(self) -> ClientStorage:
        return self.__client_storage

    # session_storage
    @property
    def session(self) -> SessionStorage:
        return self.__session_storage

    # splash
    @property
    def splash(self) -> Optional[Control]:
        return self.__offstage.splash

    @splash.setter
    @deprecated(
        reason="Use Page.overlay.append(splash) method instead.",
        version="0.23.0",
        delete_version="0.26.0",
        is_method=False,
    )
    def splash(self, value: Optional[Control]):
        self.__offstage.splash = value

    # banner
    @property
    def banner(self) -> Optional[Banner]:
        return self.__offstage.banner

    @banner.setter
    @deprecated(
        reason="Use Page.overlay.append(banner) instead.",
        version="0.23.0",
        delete_version="0.26.0",
        is_method=False,
    )
    def banner(self, value: Optional[Banner]):
        self.__offstage.banner = value

    # snack_bar
    @property
    def snack_bar(self) -> Optional[SnackBar]:
        return self.__offstage.snack_bar

    @snack_bar.setter
    @deprecated(
        reason="Use Page.overlay.append(snack_bar) instead.",
        version="0.23.0",
        delete_version="0.26.0",
        is_method=False,
    )
    def snack_bar(self, value: Optional[SnackBar]):
        self.__offstage.snack_bar = value

    # dialog
    @property
    def dialog(self) -> Optional[Control]:
        return self.__offstage.dialog

    @dialog.setter
    @deprecated(
        reason="Use Page.overlay.append(dialog) instead.",
        version="0.23.0",
        delete_version="0.26.0",
        is_method=False,
    )
    def dialog(self, value: Optional[Control]):
        self.__offstage.dialog = value

    # bottom_sheet
    @property
    def bottom_sheet(self) -> Optional[BottomSheet]:
        return self.__offstage.bottom_sheet

    @bottom_sheet.setter
    @deprecated(
        reason="Use Page.overlay.append(bottom_sheet) instead.",
        version="0.23.0",
        delete_version="0.26.0",
        is_method=False,
    )
    def bottom_sheet(self, value: Optional[BottomSheet]):
        self.__offstage.bottom_sheet = value

    # theme_mode
    @property
    def theme_mode(self) -> Optional[ThemeMode]:
        return self.__theme_mode

    @theme_mode.setter
    def theme_mode(self, value: Optional[ThemeMode]):
        self.__theme_mode = value
        self._set_attr(
            "themeMode", value.value if isinstance(value, ThemeMode) else value
        )

    # theme
    @property
    def theme(self) -> Optional[Theme]:
        return self.__theme

    @theme.setter
    def theme(self, value: Optional[Theme]):
        self.__theme = value

    # dark_theme
    @property
    def dark_theme(self) -> Optional[Theme]:
        return self.__dark_theme

    @dark_theme.setter
    def dark_theme(self, value: Optional[Theme]):
        self.__dark_theme = value

    # locale_configuration
    @property
    def locale_configuration(self) -> Optional[LocaleConfiguration]:
        return self.__locale_configuration

    @locale_configuration.setter
    def locale_configuration(self, value: Optional[LocaleConfiguration]):
        self.__locale_configuration = value

    # rtl
    @property
    def rtl(self) -> Optional[bool]:
        return self._get_attr("rtl")

    @rtl.setter
    def rtl(self, value: Optional[bool]):
        self._set_attr("rtl", value)

    # show_semantics_debugger
    @property
    def show_semantics_debugger(self) -> Optional[bool]:
        return self._get_attr("showSemanticsDebugger")

    @show_semantics_debugger.setter
    def show_semantics_debugger(self, value: Optional[bool]):
        self._set_attr("showSemanticsDebugger", value)

    # width
    @property
    def width(self) -> OptionalNumber:
        w = self._get_attr("width")
        return float(w) if w else 0

    # height
    @property
    def height(self) -> OptionalNumber:
        h = self._get_attr("height")
        return float(h) if h else 0

    # window_bgcolor
    @property
    @deprecated(
        reason="Use Page.window.bgcolor instead.",
        version="0.23.0",
        delete_version="0.26.0",
        is_method=False,
    )
    def window_bgcolor(self) -> Optional[str]:
        return self.__window.bgcolor

    @window_bgcolor.setter
    @deprecated(
        reason="Use Page.window.bgcolor instead.",
        version="0.23.0",
        delete_version="0.26.0",
        is_method=False,
    )
    def window_bgcolor(self, value: Optional[str]):
        self.__window.bgcolor = value

    # window_width
    @property
    @deprecated(
        reason="Use Page.window.width instead.",
        version="0.23.0",
        delete_version="0.26.0",
        is_method=False,
    )
    def window_width(self) -> OptionalNumber:
        return self.__window.width

    @window_width.setter
    @deprecated(
        reason="Use Page.window.width instead.",
        version="0.23.0",
        delete_version="0.26.0",
        is_method=False,
    )
    def window_width(self, value: OptionalNumber):
        self.__window.width = value

    # window_height
    @property
    @deprecated(
        reason="Use Page.window.height instead.",
        version="0.23.0",
        delete_version="0.26.0",
        is_method=False,
    )
    def window_height(self) -> OptionalNumber:
        return self.__window.height

    @window_height.setter
    @deprecated(
        reason="Use Page.window.height instead.",
        version="0.23.0",
        delete_version="0.26.0",
        is_method=False,
    )
    def window_height(self, value: OptionalNumber):
        self.__window.height = value

    # window_top
    @property
    @deprecated(
        reason="Use Page.window.top instead.",
        version="0.23.0",
        delete_version="0.26.0",
        is_method=False,
    )
    def window_top(self) -> OptionalNumber:
        return self.__window.top

    @window_top.setter
    @deprecated(
        reason="Use Page.window.top instead.",
        version="0.23.0",
        delete_version="0.26.0",
        is_method=False,
    )
    def window_top(self, value: OptionalNumber):
        self.__window.top = value

    # window_left
    @property
    @deprecated(
        reason="Use Page.window.left instead.",
        version="0.23.0",
        delete_version="0.26.0",
        is_method=False,
    )
    def window_left(self) -> OptionalNumber:
        return self.__window.left

    @window_left.setter
    @deprecated(
        reason="Use Page.window.left instead.",
        version="0.23.0",
        delete_version="0.26.0",
        is_method=False,
    )
    def window_left(self, value: OptionalNumber):
        self.__window.left = value

    # window_max_width
    @property
    @deprecated(
        reason="Use Page.window.max_width instead.",
        version="0.23.0",
        delete_version="0.26.0",
        is_method=False,
    )
    def window_max_width(self) -> OptionalNumber:
        return self.__window.max_width

    @window_max_width.setter
    @deprecated(
        reason="Use Page.window.max_width instead.",
        version="0.23.0",
        delete_version="0.26.0",
        is_method=False,
    )
    def window_max_width(self, value: OptionalNumber):
        self.__window.max_width = value

    # window_max_height
    @property
    @deprecated(
        reason="Use Page.window.max_height instead.",
        version="0.23.0",
        delete_version="0.26.0",
        is_method=False,
    )
    def window_max_height(self) -> OptionalNumber:
        return self.__window.max_height

    @window_max_height.setter
    @deprecated(
        reason="Use Page.window.max_height instead.",
        version="0.23.0",
        delete_version="0.26.0",
        is_method=False,
    )
    def window_max_height(self, value: OptionalNumber):
        self.__window.max_height = value

    # window_min_width
    @property
    @deprecated(
        reason="Use Page.window.min_width instead.",
        version="0.23.0",
        delete_version="0.26.0",
        is_method=False,
    )
    def window_min_width(self) -> OptionalNumber:
        return self.__window.min_width

    @window_min_width.setter
    @deprecated(
        reason="Use Page.window.min_width instead.",
        version="0.23.0",
        delete_version="0.26.0",
        is_method=False,
    )
    def window_min_width(self, value: OptionalNumber):
        self.__window.min_width = value

    # window_min_height
    @property
    @deprecated(
        reason="Use Page.window.min_height instead.",
        version="0.23.0",
        delete_version="0.26.0",
        is_method=False,
    )
    def window_min_height(self) -> OptionalNumber:
        return self.__window.min_height

    @window_min_height.setter
    @deprecated(
        reason="Use Page.window.min_height instead.",
        version="0.23.0",
        delete_version="0.26.0",
        is_method=False,
    )
    def window_min_height(self, value: OptionalNumber):
        self.__window.min_height = value

    # window_opacity
    @property
    @deprecated(
        reason="Use Page.window.opacity instead.",
        version="0.23.0",
        delete_version="0.26.0",
        is_method=False,
    )
    def window_opacity(self) -> OptionalNumber:
        return self.__window.opacity

    @window_opacity.setter
    @deprecated(
        reason="Use Page.window.opacity instead.",
        version="0.23.0",
        delete_version="0.26.0",
        is_method=False,
    )
    def window_opacity(self, value: OptionalNumber):
        self.__window.opacity = value

    # window_maximized
    @property
    @deprecated(
        reason="Use Page.window.maximized instead.",
        version="0.23.0",
        delete_version="0.26.0",
        is_method=False,
    )
    def window_maximized(self) -> Optional[bool]:
        return self.__window.maximized

    @window_maximized.setter
    @deprecated(
        reason="Use Page.window.maximized instead.",
        version="0.23.0",
        delete_version="0.26.0",
        is_method=False,
    )
    def window_maximized(self, value: Optional[bool]):
        self.__window.maximized = value

    # window_minimized
    @property
    @deprecated(
        reason="Use Page.window.minimized instead.",
        version="0.23.0",
        delete_version="0.26.0",
        is_method=False,
    )
    def window_minimized(self) -> Optional[bool]:
        return self.__window.minimized

    @window_minimized.setter
    @deprecated(
        reason="Use Page.window.minimized instead.",
        version="0.23.0",
        delete_version="0.26.0",
        is_method=False,
    )
    def window_minimized(self, value: Optional[bool]):
        self.__window.minimized = value

    # window_minimizable
    @property
    @deprecated(
        reason="Use Page.window.minimizable instead.",
        version="0.23.0",
        delete_version="0.26.0",
        is_method=False,
    )
    def window_minimizable(self) -> Optional[bool]:
        return self.__window.minimizable

    @window_minimizable.setter
    @deprecated(
        reason="Use Page.window.minimizable instead.",
        version="0.23.0",
        delete_version="0.26.0",
        is_method=False,
    )
    def window_minimizable(self, value: Optional[bool]):
        self.__window.minimizable = value

    # window_maximizable
    @property
    @deprecated(
        reason="Use Page.window.maximizable instead.",
        version="0.23.0",
        delete_version="0.26.0",
        is_method=False,
    )
    def window_maximizable(self) -> Optional[bool]:
        return self.__window.maximizable

    @window_maximizable.setter
    @deprecated(
        reason="Use Page.window.maximizable instead.",
        version="0.23.0",
        delete_version="0.26.0",
        is_method=False,
    )
    def window_maximizable(self, value: Optional[bool]):
        self.__window.maximizable = value

    # window_resizable
    @property
    @deprecated(
        reason="Use Page.window.resizable instead.",
        version="0.23.0",
        delete_version="0.26.0",
        is_method=False,
    )
    def window_resizable(self) -> Optional[bool]:
        return self.__window.resizable

    @window_resizable.setter
    @deprecated(
        reason="Use Page.window.resizable instead.",
        version="0.23.0",
        delete_version="0.26.0",
        is_method=False,
    )
    def window_resizable(self, value: Optional[bool]):
        self.__window.resizable = value

    # window_movable
    @property
    @deprecated(
        reason="Use Page.window.movable instead.",
        version="0.23.0",
        delete_version="0.26.0",
        is_method=False,
    )
    def window_movable(self) -> Optional[bool]:
        return self.__window.movable

    @window_movable.setter
    @deprecated(
        reason="Use Page.window.movable instead.",
        version="0.23.0",
        delete_version="0.26.0",
        is_method=False,
    )
    def window_movable(self, value: Optional[bool]):
        self.__window.movable = value

    # window_full_screen
    @property
    @deprecated(
        reason="Use Page.window.full_screen instead.",
        version="0.23.0",
        delete_version="0.26.0",
        is_method=False,
    )
    def window_full_screen(self) -> Optional[bool]:
        return self.__window.full_screen

    @window_full_screen.setter
    @deprecated(
        reason="Use Page.window.full_screen instead.",
        version="0.23.0",
        delete_version="0.26.0",
        is_method=False,
    )
    def window_full_screen(self, value: Optional[bool]):
        self.__window.full_screen = value

    # window_always_on_top
    @property
    @deprecated(
        reason="Use Page.window.always_on_top instead.",
        version="0.23.0",
        delete_version="0.26.0",
        is_method=False,
    )
    def window_always_on_top(self) -> Optional[bool]:
        return self.__window.always_on_top

    @window_always_on_top.setter
    @deprecated(
        reason="Use Page.window.always_on_top instead.",
        version="0.23.0",
        delete_version="0.26.0",
        is_method=False,
    )
    def window_always_on_top(self, value: Optional[bool]):
        self.__window.always_on_top = value

    # window_always_on_bottom
    @property
    @deprecated(
        reason="Use Page.window.always_on_bottom instead.",
        version="0.23.0",
        delete_version="0.26.0",
        is_method=False,
    )
    def window_always_on_bottom(self) -> Optional[bool]:
        return self.__window.always_on_bottom

    @window_always_on_bottom.setter
    @deprecated(
        reason="Use Page.window.always_on_bottom instead.",
        version="0.23.0",
        delete_version="0.26.0",
        is_method=False,
    )
    def window_always_on_bottom(self, value: Optional[bool]):
        self.window_always_on_bottom = value

    # window_prevent_close
    @property
    @deprecated(
        reason="Use Page.window.prevent_close instead.",
        version="0.23.0",
        delete_version="0.26.0",
        is_method=False,
    )
    def window_prevent_close(self) -> Optional[bool]:
        return self.__window.prevent_close

    @window_prevent_close.setter
    @deprecated(
        reason="Use Page.window.prevent_close instead.",
        version="0.23.0",
        delete_version="0.26.0",
        is_method=False,
    )
    def window_prevent_close(self, value: Optional[bool]):
        self.__window.prevent_close = value

    # window_title_bar_hidden
    @property
    @deprecated(
        reason="Use Page.window.title_bar_hidden instead.",
        version="0.23.0",
        delete_version="0.26.0",
        is_method=False,
    )
    def window_title_bar_hidden(self) -> Optional[bool]:
        return self.__window.title_bar_hidden

    @window_title_bar_hidden.setter
    @deprecated(
        reason="Use Page.window.title_bar_hidden instead.",
        version="0.23.0",
        delete_version="0.26.0",
        is_method=False,
    )
    def window_title_bar_hidden(self, value: Optional[bool]):
        self.__window.title_bar_hidden = value

    # window_title_bar_buttons_hidden
    @property
    @deprecated(
        reason="Use Page.window.title_bar_buttons_hidden instead.",
        version="0.23.0",
        delete_version="0.26.0",
        is_method=False,
    )
    def window_title_bar_buttons_hidden(self) -> Optional[bool]:
        return self.__window.title_bar_buttons_hidden

    @window_title_bar_buttons_hidden.setter
    @deprecated(
        reason="Use Page.window.title_bar_buttons_hidden instead.",
        version="0.23.0",
        delete_version="0.26.0",
        is_method=False,
    )
    def window_title_bar_buttons_hidden(self, value: Optional[bool]):
        self.__window.title_bar_buttons_hidden = value

    # window_skip_task_bar
    @property
    @deprecated(
        reason="Use Page.window.skip_task_bar instead.",
        version="0.23.0",
        delete_version="0.26.0",
        is_method=False,
    )
    def window_skip_task_bar(self) -> Optional[bool]:
        return self.__window.skip_task_bar

    @window_skip_task_bar.setter
    @deprecated(
        reason="Use Page.window.skip_task_bar instead.",
        version="0.23.0",
        delete_version="0.26.0",
        is_method=False,
    )
    def window_skip_task_bar(self, value: Optional[bool]):
        self.__window.skip_taskbar = value

    # window_frameless
    @property
    @deprecated(
        reason="Use Page.window.frameless instead.",
        version="0.23.0",
        delete_version="0.26.0",
        is_method=False,
    )
    def window_frameless(self) -> Optional[bool]:
        return self.__window.frameless

    @window_frameless.setter
    @deprecated(
        reason="Use Page.window.frameless instead.",
        version="0.23.0",
        delete_version="0.26.0",
        is_method=False,
    )
    def window_frameless(self, value: Optional[bool]):
        self.__window.frameless = value

    # window_progress_bar
    @property
    @deprecated(
        reason="Use Page.window.progress_bar instead.",
        version="0.23.0",
        delete_version="0.26.0",
        is_method=False,
    )
    def window_progress_bar(self) -> OptionalNumber:
        return self.__window.progress_bar

    @window_progress_bar.setter
    @deprecated(
        reason="Use Page.window.progress_bar instead.",
        version="0.23.0",
        delete_version="0.26.0",
        is_method=False,
    )
    def window_progress_bar(self, value: OptionalNumber):
        self.__window.progress_bar = value

    # window_focused
    @property
    @deprecated(
        reason="Use Page.window.focused instead.",
        version="0.23.0",
        delete_version="0.26.0",
        is_method=False,
    )
    def window_focused(self) -> Optional[bool]:
        return self.__window.focused

    @window_focused.setter
    @deprecated(
        reason="Use Page.window.focused instead.",
        version="0.23.0",
        delete_version="0.26.0",
        is_method=False,
    )
    def window_focused(self, value: Optional[bool]):
        self.__window.focused = value

    # window_visible
    @property
    @deprecated(
        reason="Use Page.window.visible instead.",
        version="0.23.0",
        delete_version="0.26.0",
        is_method=False,
    )
    def window_visible(self) -> Optional[bool]:
        return self.__window.visible

    @window_visible.setter
    @deprecated(
        reason="Use Page.window.visible instead.",
        version="0.23.0",
        delete_version="0.26.0",
        is_method=False,
    )
    def window_visible(self, value: Optional[bool]):
        self.__window.visible = value

    # on_scroll_interval
    @property
    def on_scroll_interval(self) -> OptionalNumber:
        return self.__default_view.on_scroll_interval

    @on_scroll_interval.setter
    def on_scroll_interval(self, value: OptionalNumber):
        self.__default_view.on_scroll_interval = value

    # on_close
    @property
    def on_close(self):
        return self.__on_close

    @on_close.setter
    def on_close(self, handler: OptionalEventCallable):
        self.__on_close.subscribe(handler)

    # on_resize
    @property
    @deprecated(
        reason="Use Page.on_resized instead.",
        version="0.23.0",
        delete_version="0.26.0",
        is_method=False,
    )
    def on_resize(self):
        return self.__on_resized

    @on_resize.setter
    @deprecated(
        reason="Use on_resized instead.",
        version="0.23.0",
        delete_version="0.26.0",
        is_method=False,
    )
    def on_resize(self, handler: "Optional[Callable[[WindowResizeEvent], None]]"):
        self.__on_resized.subscribe(handler)

    @property
    def on_resized(self):
        return self.__on_resized

    @on_resized.setter
    def on_resized(self, handler: "Optional[Callable[[WindowResizeEvent], None]]"):
        self.__on_resized.subscribe(handler)

    # on_platform_brightness_change
    @property
    def on_platform_brightness_change(self):
        return self.__on_platform_brightness_change

    @on_platform_brightness_change.setter
    def on_platform_brightness_change(self, handler: OptionalEventCallable):
        self.__on_platform_brightness_change.subscribe(handler)

    # on_app_lifecycle_change
    @property
    def on_app_lifecycle_state_change(self):
        return self.__on_app_lifecycle_state_change

    @on_app_lifecycle_state_change.setter
    def on_app_lifecycle_state_change(
        self, handler: "Optional[Callable[[AppLifecycleStateChangeEvent], None]]"
    ):
        self.__on_app_lifecycle_state_change.subscribe(handler)

    # on_route_change
    @property
    def on_route_change(self):
        return self.__on_route_change

    @on_route_change.setter
    def on_route_change(self, handler: "Optional[Callable[[RouteChangeEvent], None]]"):
        self.__on_route_change.subscribe(handler)

    # on_view_pop
    @property
    def on_view_pop(self):
        return self.__on_view_pop

    @on_view_pop.setter
    def on_view_pop(self, handler: "Optional[Callable[[ViewPopEvent], None]]"):
        self.__on_view_pop.subscribe(handler)

    # on_keyboard_event
    @property
    def on_keyboard_event(self):
        return self.__on_keyboard_event

    @on_keyboard_event.setter
    def on_keyboard_event(self, handler: "Optional[Callable[[KeyboardEvent], None]]"):
        self.__on_keyboard_event.subscribe(handler)

    # on_window_event
    @property
    @deprecated(
        reason="Use Page.on_window_event instead.",
        version="0.23.0",
        delete_version="0.26.0",
        is_method=False,
    )
    def on_window_event(self):
        return self.__window.on_event

    @on_window_event.setter
    @deprecated(
        "Use Page.on_window_event instead.",
        version="0.23.0",
        delete_version="0.26.0",
        is_method=False,
    )
    def on_window_event(self, handler: "Optional[Callable[[WindowEvent], None]]"):
        self.__window.on_event.subscribe(handler)

    # on_media_change
    @property
    def on_media_change(self):
        return self.__on_page_media_change_event

    @on_media_change.setter
    def on_media_change(self, handler: "Optional[Callable[[PageMediaData], None]]"):
        self.__on_page_media_change_event.subscribe(handler)

    # on_connect
    @property
    def on_connect(self):
        return self.__on_connect

    @on_connect.setter
    def on_connect(self, handler: OptionalEventCallable):
        self.__on_connect.subscribe(handler)

    # on_disconnect
    @property
    def on_disconnect(self):
        return self.__on_disconnect

    @on_disconnect.setter
    def on_disconnect(self, handler: OptionalEventCallable):
        self.__on_disconnect.subscribe(handler)

    # on_login
    @property
    def on_login(self):
        return self.__on_login

    @on_login.setter
    def on_login(self, handler: "Optional[Callable[[LoginEvent], None]]"):
        self.__on_login.subscribe(handler)

    # on_logout
    @property
    def on_logout(self):
        return self.__on_logout

    @on_logout.setter
    def on_logout(self, handler: OptionalEventCallable):
        self.__on_logout.subscribe(handler)

    # on_error
    @property
    def on_error(self):
        return self.__on_error

    @on_error.setter
    def on_error(self, handler: OptionalEventCallable):
        self.__on_error.subscribe(handler)

    # on_scroll
    @property
    def on_scroll(self):
        return self.__default_view.on_scroll

    @on_scroll.setter
    def on_scroll(self, handler: Optional[Callable[[OnScrollEvent], None]]):
        self.__default_view.on_scroll = handler

    # Magic methods
    def __contains__(self, item: Control) -> bool:
        return item in self._controls


class Offstage(Control):
    def __init__(
        self,
        visible: Optional[bool] = None,
        disabled: Optional[bool] = None,
        data: Any = None,
    ) -> None:
        Control.__init__(
            self,
            visible=visible,
            disabled=disabled,
            data=data,
        )

        self.__controls: List[Control] = []
        self.__banner = None
        self.__snack_bar = None
        self.__dialog = None
        self.__bottom_sheet = None
        self.__splash = None

    def _get_control_name(self):
        return "offstage"

    def _get_children(self):
        return self.__controls

    # controls
    @property
    def controls(self) -> List[Control]:
        return self.__controls

    # splash
    @property
    def splash(self) -> Optional[Control]:
        return self.__splash

    @splash.setter
    def splash(self, value: Optional[Control]):
        self.__splash = value
        if value is not None:
            self.__controls.append(value)

    # banner
    @property
    def banner(self) -> Optional[Banner]:
        return self.__banner

    @banner.setter
    def banner(self, value: Optional[Banner]):
        self.__banner = value
        if value is not None:
            self.__controls.append(value)

    # snack_bar
    @property
    def snack_bar(self) -> Optional[SnackBar]:
        return self.__snack_bar

    @snack_bar.setter
    def snack_bar(self, value: Optional[SnackBar]):
        self.__snack_bar = value
        if value is not None:
            self.__controls.append(value)

    # dialog
    @property
    def dialog(self) -> Optional[Union[AlertDialog, CupertinoAlertDialog]]:
        return self.__dialog

    @dialog.setter
    def dialog(self, value: Optional[Union[AlertDialog, CupertinoAlertDialog]]):
        self.__dialog = value
        if value is not None:
            self.__controls.append(value)

    # bottom_sheet
    @property
    def bottom_sheet(self) -> Optional[Union[BottomSheet, CupertinoBottomSheet]]:
        return self.__bottom_sheet

    @bottom_sheet.setter
    def bottom_sheet(self, value: Optional[Union[BottomSheet, CupertinoBottomSheet]]):
        self.__bottom_sheet = value
        if value is not None:
            self.__controls.append(value)


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


class LoginEvent(ControlEvent):
    def __init__(
        self,
        error: str,
        error_description: str,
        target: str,
        name: str,
        data: str,
        control,
        page,
    ) -> None:
        super().__init__(target, name, data, control, page)

        self.error = error
        self.error_description = error_description


@dataclass
class InvokeMethodResults:
    method_id: str
    result: Optional[str]
    error: Optional[str]


class PageMediaData(ControlEvent):
    def __init__(self, padding, view_padding, view_insets) -> None:
        self.padding = Padding(
            left=padding["left"],
            top=padding["top"],
            right=padding["right"],
            bottom=padding["bottom"],
        )
        self.view_padding = Padding(
            left=view_padding["left"],
            top=view_padding["top"],
            right=view_padding["right"],
            bottom=view_padding["bottom"],
        )
        self.view_insets = Padding(
            left=view_insets["left"],
            top=view_insets["top"],
            right=view_insets["right"],
            bottom=view_insets["bottom"],
        )

    def __str__(self) -> str:
        return f"PageMediaData(padding={self.padding}, view_padding={self.view_padding}, view_insets={self.view_insets})"


class AppLifecycleStateChangeEvent(ControlEvent):
    def __init__(self, e: ControlEvent) -> None:
        super().__init__(e.target, e.name, e.data, e.control, e.page)
        self.state = AppLifecycleState(e.data)


class WindowEvent(ControlEvent):
    def __init__(self, e: ControlEvent):
        super().__init__(e.target, e.name, e.data, e.control, e.page)
        self.type = WindowEventType(e.data)


class WindowResizeEvent(ControlEvent):
    def __init__(self, e: ControlEvent):
        super().__init__(e.target, e.name, e.data, e.control, e.page)
        size = json.loads(e.data)
        self.width: float = size["width"]
        self.height: float = size["height"]
