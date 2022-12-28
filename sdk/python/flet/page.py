import json
import logging
import threading
import time
import uuid
from dataclasses import dataclass
from typing import Any, cast
from urllib.parse import urlparse

from beartype import beartype
from beartype.typing import Dict, List, Optional

from flet import constants
from flet.app_bar import AppBar
from flet.auth.authorization import Authorization
from flet.auth.oauth_provider import OAuthProvider
from flet.banner import Banner
from flet.client_storage import ClientStorage
from flet.clipboard import Clipboard
from flet.connection import Connection
from flet.control import Control, OptionalNumber
from flet.control_event import ControlEvent
from flet.event import Event
from flet.event_handler import EventHandler
from flet.floating_action_button import FloatingActionButton
from flet.navigation_bar import NavigationBar
from flet.protocol import Command
from flet.pubsub import PubSub
from flet.querystring import QueryString
from flet.session_storage import SessionStorage
from flet.snack_bar import SnackBar
from flet.theme import Theme
from flet.types import (
    CrossAxisAlignment,
    MainAxisAlignment,
    PaddingValue,
    PageDesignLanguage,
    PageDesignString,
    ScrollMode,
    ThemeMode,
    ThemeModeString,
)
from flet.view import View

try:
    from typing import Literal
except ImportError:
    from typing_extensions import Literal


class Page(Control):
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

    def __init__(self, conn: Connection, session_id):
        Control.__init__(self)

        self._id = "page"
        self._Control__uid = "page"
        self.__conn = conn
        self.__query = QueryString(page=self)  # Querystring
        self._session_id = session_id
        self._index = {self._Control__uid: self}  # index with all page controls
        self._last_event = None
        self._event_available = threading.Event()
        self._fetch_page_details()

        self.__views = [View()]
        self.__default_view = self.__views[0]
        self._controls = self.__default_view.controls

        self.__fonts: Optional[Dict[str, str]] = None
        self.__offstage = Offstage()
        self.__theme = None
        self.__dark_theme = None
        self.__pubsub = PubSub(conn.pubsubhub, session_id)
        self.__client_storage = ClientStorage(self)
        self.__session_storage = SessionStorage(self)
        self.__authorization: Optional[Authorization] = None

        self.__on_close = EventHandler()
        self._add_event_handler("close", self.__on_close.handler)
        self.__on_resize = EventHandler()
        self._add_event_handler("resize", self.__on_resize.handler)

        self.__last_route = None

        # authorize/login/logout
        self.__on_login = EventHandler()
        self._add_event_handler("authorize", self.__on_authorize)
        self.__on_logout = EventHandler()

        # route_change
        def convert_route_change_event(e):
            if self.__last_route == e.data:
                return None  # avoid duplicate calls
            self.__last_route = e.data
            self.query()  # Update query url (required when manually changed from browser)
            return RouteChangeEvent(route=e.data)

        self.__on_route_change = EventHandler(convert_route_change_event)
        self._add_event_handler("route_change", self.__on_route_change.handler)

        def convert_view_pop_event(e):
            return ViewPopEvent(view=cast(View, self.get_control(e.data)))

        self.__on_view_pop = EventHandler(convert_view_pop_event)
        self._add_event_handler("view_pop", self.__on_view_pop.handler)

        def convert_keyboard_event(e):
            d = json.loads(e.data)
            return KeyboardEvent(**d)

        self.__on_keyboard_event = EventHandler(convert_keyboard_event)
        self._add_event_handler("keyboard_event", self.__on_keyboard_event.handler)

        self.__method_calls: Dict[str, threading.Event] = {}
        self.__method_call_results: Dict[
            threading.Event, tuple[Optional[str], Optional[str]]
        ] = {}
        self._add_event_handler("invoke_method_result", self._on_invoke_method_result)

        self.__on_window_event = EventHandler()
        self._add_event_handler("window_event", self.__on_window_event.handler)
        self.__on_connect = EventHandler()
        self._add_event_handler("connect", self.__on_connect.handler)
        self.__on_disconnect = EventHandler()
        self._add_event_handler("disconnect", self.__on_disconnect.handler)
        self.__on_error = EventHandler()
        self._add_event_handler("error", self.__on_error.handler)

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        self.close()

    def get_control(self, id):
        return self._index.get(id)

    def _before_build_command(self):
        super()._before_build_command()
        # fonts
        self._set_attr_json("fonts", self.__fonts)

        # light theme
        self._set_attr_json("theme", self.__theme)

        # dark theme
        self._set_attr_json("darkTheme", self.__dark_theme)

        # keyboard event
        if self.__on_keyboard_event.count() > 0:
            self._set_attr("onKeyboardEvent", True)

    def _get_children(self):
        children = []
        children.extend(self.__views)
        children.append(self.__offstage)
        return children

    def _fetch_page_details(self):
        assert self.__conn.page_name is not None
        values = self.__conn.send_commands(
            self._session_id,
            [
                Command(0, "get", ["page", "route"]),
                Command(
                    0,
                    "get",
                    ["page", "pwa"],
                ),
                Command(0, "get", ["page", "web"]),
                Command(0, "get", ["page", "platform"]),
                Command(0, "get", ["page", "width"]),
                Command(0, "get", ["page", "height"]),
                Command(0, "get", ["page", "windowWidth"]),
                Command(0, "get", ["page", "windowHeight"]),
                Command(0, "get", ["page", "windowTop"]),
                Command(0, "get", ["page", "windowLeft"]),
            ],
        ).results
        self._set_attr("route", values[0], False)
        self._set_attr("pwa", values[1], False)
        self._set_attr("web", values[2], False)
        self._set_attr("platform", values[3], False)
        self._set_attr("width", values[4], False)
        self._set_attr("height", values[5], False)
        self._set_attr("windowWidth", values[6], False)
        self._set_attr("windowHeight", values[7], False)
        self._set_attr("windowTop", values[8], False)
        self._set_attr("windowLeft", values[9], False)

    def update(self, *controls):
        added_controls = []
        with self._lock:
            if len(controls) == 0:
                added_controls = self.__update(self)
            else:
                added_controls = self.__update(*controls)
        for ctrl in added_controls:
            ctrl.did_mount()

    def __update(self, *controls) -> List[Control]:
        added_controls = []
        commands = []

        # build commands
        for control in controls:
            control.build_update_commands(self._index, added_controls, commands)

        if len(commands) == 0:
            return added_controls

        # execute commands
        results = self.__conn.send_commands(self._session_id, commands).results

        if len(results) > 0:
            n = 0
            for line in results:
                for id in line.split(" "):
                    added_controls[n]._Control__uid = id
                    added_controls[n].page = self

                    # add to index
                    self._index[id] = added_controls[n]

                    n += 1
        return added_controls

    def add(self, *controls):
        added_controls = []
        with self._lock:
            self._controls.extend(controls)
            added_controls = self.__update(self)
        for ctrl in added_controls:
            ctrl.did_mount()

    def insert(self, at, *controls):
        added_controls = []
        with self._lock:
            n = at
            for control in controls:
                self._controls.insert(n, control)
                n += 1
            added_controls = self.__update(self)
        for ctrl in added_controls:
            ctrl.did_mount()

    def remove(self, *controls):
        added_controls = []
        with self._lock:
            for control in controls:
                self._controls.remove(control)
            added_controls = self.__update(self)
        for ctrl in added_controls:
            ctrl.did_mount()

    def remove_at(self, index):
        added_controls = []
        with self._lock:
            self._controls.pop(index)
            added_controls = self.__update(self)
        for ctrl in added_controls:
            ctrl.did_mount()

    def clean(self):
        with self._lock:
            self._previous_children.clear()
            for child in self._get_children():
                self._remove_control_recursively(self._index, child)
            self._controls.clear()
            assert self.uid is not None
            return self._send_command("clean", [self.uid])

    def error(self, message=""):
        with self._lock:
            self._send_command("error", [message])

    def on_event(self, e: Event):
        logging.info(f"page.on_event: {e.target} {e.name} {e.data}")

        with self._lock:
            if e.target == "page" and e.name == "change":
                for props in json.loads(e.data):
                    id = props["i"]
                    if id in self._index:
                        for name in props:
                            if name != "i":
                                self._index[id]._set_attr(
                                    name, props[name], dirty=False
                                )

            elif e.target in self._index:
                self._last_event = ControlEvent(
                    e.target, e.name, e.data, self._index[e.target], self
                )
                handler = self._index[e.target].event_handlers.get(e.name)
                if handler:
                    t = threading.Thread(
                        target=handler, args=(self._last_event,), daemon=True
                    )
                    t.start()
                self._event_available.set()

    def wait_event(self) -> ControlEvent:
        self._event_available.clear()
        self._event_available.wait()
        assert self._last_event is not None
        return self._last_event

    def go(self, route, **kwargs):
        self.route = route if kwargs == {} else route + self.query.post(kwargs)

        self.__on_route_change.handler(
            ControlEvent(
                target="page",
                name="route_change",
                data=self.route,
                page=self,
                control=self,
            )
        )
        self.update()
        self.query()  # Update query url (required when using go)

    def get_upload_url(self, file_name: str, expires: int):
        r = self._send_command(
            "getUploadUrl", attrs={"file": file_name, "expires": str(expires)}
        )
        if r.error:
            raise Exception(r.error)

        return r.result

    def login(
        self,
        provider: OAuthProvider,
        fetch_user=True,
        fetch_groups=False,
        scope: Optional[List[str]] = None,
        saved_token: Optional[str] = None,
        on_open_authorization_url=None,
        complete_page_html: Optional[str] = None,
        redirect_to_page=False,
        authorization=Authorization
    ):
        self.__authorization = authorization(
            provider,
            fetch_user=fetch_user,
            fetch_groups=fetch_groups,
            scope=scope,
            saved_token=saved_token,
        )
        if saved_token == None:
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
            self.__on_login.handler(LoginEvent(error="", error_description=""))
        return self.__authorization

    def __on_authorize(self, e):
        assert self.__authorization is not None
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
            error=d["error"], error_description=d["error_description"]
        )
        if login_evt.error == "":
            # perform token request
            code = d["code"]
            assert code not in [None, ""]
            try:
                self.__authorization.request_token(code)
            except Exception as ex:
                login_evt.error = str(ex)
        self.__on_login.handler(login_evt)

    def logout(self):
        self.__authorization = None
        self.__on_logout.handler(
            ControlEvent(target="page", name="logout", data="", control=self, page=self)
        )

    def close(self):
        if self._session_id == constants.ZERO_SESSION:
            self.__conn.close()

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

    @beartype
    def set_clipboard(self, value: str):
        self.__offstage.clipboard.set_data(value)

    def get_clipboard(self):
        return self.__offstage.clipboard.get_data()

    @beartype
    def launch_url(
        self,
        url: str,
        web_window_name: Optional[str] = None,
        web_popup_window: bool = False,
        window_width: Optional[int] = None,
        window_height: Optional[int] = None,
    ):
        args = {"url": url}
        if web_window_name != None:
            args["web_window_name"] = web_window_name
        if web_popup_window != None:
            args["web_popup_window"] = str(web_popup_window)
        if window_width != None:
            args["window_width"] = str(window_width)
        if window_height != None:
            args["window_height"] = str(window_height)
        self.invoke_method("launchUrl", args)

    @beartype
    def can_launch_url(self, url: str):
        args = {"url": url}
        return self.invoke_method("canLaunchUrl", args, wait_for_result=True) == "true"

    def close_in_app_web_view(self):
        self.invoke_method("closeInAppWebView")

    @beartype
    def window_to_front(self):
        self.invoke_method("windowToFront")

    def invoke_method(
        self,
        method_name: str,
        arguments: Optional[Dict[str, str]] = None,
        wait_for_result: bool = False,
    ) -> Optional[str]:
        method_id = uuid.uuid4().hex

        # register callback
        evt: Optional[threading.Event] = None
        if wait_for_result:
            evt = threading.Event()
            self.__method_calls[method_id] = evt

        # call method
        result = self._send_command(
            "invokeMethod", values=[method_id, method_name], attrs=arguments
        )

        if result.error != "":
            if wait_for_result:
                del self.__method_calls[method_id]
            raise Exception(result.error)

        if not wait_for_result:
            return

        assert evt is not None

        if not evt.wait(5):
            del self.__method_calls[method_id]
            raise Exception(
                f"Timeout waiting for invokeMethod {method_name}({arguments}) call"
            )

        result, err = self.__method_call_results.pop(evt)
        if err != None:
            raise Exception(err)
        if result == None:
            return None
        return result

    def _on_invoke_method_result(self, e):
        d = json.loads(e.data)
        result = InvokeMethodResults(**d)
        evt = self.__method_calls.pop(result.method_id, None)
        if evt == None:
            return
        self.__method_call_results[evt] = (result.result, result.error)
        evt.set()

    @beartype
    def show_snack_bar(self, snack_bar: SnackBar):
        self.__offstage.snack_bar = snack_bar
        self.__offstage.update()

    def window_destroy(self):
        self._set_attr("windowDestroy", "true")
        self.update()

    def window_center(self):
        self._set_attr("windowCenter", str(time.time()))
        self.update()

    def window_close(self):
        self._set_attr("windowClose", str(time.time()))
        self.update()

    # QueryString
    @property
    def query(self):
        return self.__query

    # url
    @property
    def url(self):
        return self.__conn.page_url

    # name
    @property
    def name(self):
        return self.__conn.page_name

    # connection
    @property
    def connection(self):
        return self.__conn

    # index
    @property
    def index(self):
        return self._index

    # session_id
    @property
    def session_id(self):
        return self._session_id

    # auth
    @property
    def auth(self):
        return self.__authorization

    # pubsub
    @property
    def pubsub(self):
        return self.__pubsub

    # overlay
    @property
    def overlay(self):
        return self.__offstage.controls

    # title
    @property
    def title(self):
        return self._get_attr("title")

    @title.setter
    def title(self, value):
        self._set_attr("title", value)

    # route
    @property
    def route(self):
        return self._get_attr("route")

    @route.setter
    def route(self, value):
        self._set_attr("route", value)

    # pwa
    @property
    def pwa(self):
        return self._get_attr("pwa", data_type="bool", def_value=False)

    # web
    @property
    def web(self) -> bool:
        return cast(bool, self._get_attr("web", data_type="bool", def_value=False))

    # platform
    @property
    def platform(self):
        return self._get_attr("platform")

    # design
    @property
    def design(self) -> Optional[PageDesignLanguage]:
        return self.__design

    @design.setter
    def design(self, value: Optional[PageDesignLanguage]):
        self.__design = value
        if isinstance(value, PageDesignLanguage):
            self._set_attr("design", value.value)
        else:
            self.__set_design(value)

    @beartype
    def __set_design(self, value: PageDesignString):
        self._set_attr("design", value)

    # fonts
    @property
    def fonts(self) -> Optional[Dict[str, str]]:
        return self.__fonts

    @fonts.setter
    @beartype
    def fonts(self, value: Optional[Dict[str, str]]):
        self.__fonts = value

    # views
    @property
    def views(self):
        return self.__views

    # controls
    @property
    def controls(self) -> Optional[List[Control]]:
        return self.__default_view.controls

    @controls.setter
    @beartype
    def controls(self, value: Optional[List[Control]]):
        self.__default_view.controls = value if value is not None else []

    # appbar
    @property
    def appbar(self) -> Optional[AppBar]:
        return self.__default_view.appbar

    @appbar.setter
    @beartype
    def appbar(self, value: Optional[AppBar]):
        self.__default_view.appbar = value

    # navigation_bar
    @property
    def navigation_bar(self) -> Optional[NavigationBar]:
        return self.__default_view.navigation_bar

    @navigation_bar.setter
    @beartype
    def navigation_bar(self, value: Optional[NavigationBar]):
        self.__default_view.navigation_bar = value

    # floating_action_button
    @property
    def floating_action_button(self) -> Optional[FloatingActionButton]:
        return self.__default_view.floating_action_button

    @floating_action_button.setter
    @beartype
    def floating_action_button(self, value: Optional[FloatingActionButton]):
        self.__default_view.floating_action_button = value

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

    # spacing
    @property
    def spacing(self) -> OptionalNumber:
        return self.__default_view.spacing

    @spacing.setter
    @beartype
    def spacing(self, value: OptionalNumber):
        self.__default_view.spacing = value

    # padding
    @property
    def padding(self) -> PaddingValue:
        return self.__default_view.padding

    @padding.setter
    @beartype
    def padding(self, value: PaddingValue):
        self.__default_view.padding = value

    # bgcolor
    @property
    def bgcolor(self):
        return self.__default_view.bgcolor

    @bgcolor.setter
    def bgcolor(self, value):
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
    @beartype
    def auto_scroll(self, value: Optional[bool]):
        self.__default_view.auto_scroll = value

    # client_storage
    @property
    def client_storage(self):
        return self.__client_storage

    # session_storage
    @property
    def session(self):
        return self.__session_storage

    # splash
    @property
    def splash(self) -> Optional[Control]:
        return self.__offstage.splash

    @splash.setter
    @beartype
    def splash(self, value: Optional[Control]):
        self.__offstage.splash = value

    # banner
    @property
    def banner(self) -> Optional[Banner]:
        return self.__offstage.banner

    @banner.setter
    @beartype
    def banner(self, value: Optional[Banner]):
        self.__offstage.banner = value

    # snack_bar
    @property
    def snack_bar(self) -> Optional[SnackBar]:
        return self.__offstage.snack_bar

    @snack_bar.setter
    @beartype
    def snack_bar(self, value: Optional[SnackBar]):
        self.__offstage.snack_bar = value

    # dialog
    @property
    def dialog(self) -> Optional[Control]:
        return self.__offstage.dialog

    @dialog.setter
    @beartype
    def dialog(self, value: Optional[Control]):
        self.__offstage.dialog = value

    # theme_mode
    @property
    def theme_mode(self) -> Optional[ThemeMode]:
        return self.__theme_mode

    @theme_mode.setter
    def theme_mode(self, value: Optional[ThemeMode]):
        self.__theme_mode = value
        if isinstance(value, ThemeMode):
            self._set_attr("themeMode", value.value)
        else:
            self.__set_theme_mode(value)

    @beartype
    def __set_theme_mode(self, value: ThemeModeString):
        self._set_attr("themeMode", value)

    # theme
    @property
    def theme(self) -> Optional[Theme]:
        return self.__theme

    @theme.setter
    @beartype
    def theme(self, value: Optional[Theme]):
        self.__theme = value

    # dark_theme
    @property
    def dark_theme(self) -> Optional[Theme]:
        return self.__dark_theme

    @dark_theme.setter
    @beartype
    def dark_theme(self, value: Optional[Theme]):
        self.__dark_theme = value

    # rtl
    @property
    def rtl(self) -> Optional[bool]:
        return self._get_attr("rtl")

    @rtl.setter
    @beartype
    def rtl(self, value: Optional[bool]):
        self._set_attr("rtl", value)

    # show_semantics_debugger
    @property
    def show_semantics_debugger(self) -> Optional[bool]:
        return self._get_attr("showSemanticsDebugger")

    @show_semantics_debugger.setter
    @beartype
    def show_semantics_debugger(self, value: Optional[bool]):
        self._set_attr("showSemanticsDebugger", value)

    # width
    @property
    def width(self):
        w = self._get_attr("width")
        if w:
            return float(w)
        return 0

    # height
    @property
    def height(self):
        h = self._get_attr("height")
        if h:
            return float(h)
        return 0

    # window_bgcolor
    @property
    def window_bgcolor(self):
        return self._get_attr("windowBgcolor")

    @window_bgcolor.setter
    @beartype
    def window_bgcolor(self, value):
        self._set_attr("windowBgcolor", value)

    # window_width
    @property
    def window_width(self) -> OptionalNumber:
        w = self._get_attr("windowWidth")
        if w:
            return float(w)
        return 0

    @window_width.setter
    @beartype
    def window_width(self, value: OptionalNumber):
        self._set_attr("windowWidth", value)

    # window_height
    @property
    def window_height(self) -> OptionalNumber:
        h = self._get_attr("windowHeight")
        if h:
            return float(h)
        return 0

    @window_height.setter
    @beartype
    def window_height(self, value: OptionalNumber):
        self._set_attr("windowHeight", value)

    # window_top
    @property
    def window_top(self) -> OptionalNumber:
        w = self._get_attr("windowTop")
        if w:
            return float(w)
        return 0

    @window_top.setter
    @beartype
    def window_top(self, value: OptionalNumber):
        self._set_attr("windowTop", value)

    # window_left
    @property
    def window_left(self) -> OptionalNumber:
        h = self._get_attr("windowLeft")
        if h:
            return float(h)
        return 0

    @window_left.setter
    @beartype
    def window_left(self, value: OptionalNumber):
        self._set_attr("windowLeft", value)

    # window_max_width
    @property
    def window_max_width(self) -> OptionalNumber:
        return self._get_attr("windowMaxWidth")

    @window_max_width.setter
    @beartype
    def window_max_width(self, value: OptionalNumber):
        self._set_attr("windowMaxWidth", value)

    # window_max_height
    @property
    def window_max_height(self) -> OptionalNumber:
        return self._get_attr("windowMaxHeight")

    @window_max_height.setter
    @beartype
    def window_max_height(self, value: OptionalNumber):
        self._set_attr("windowMaxHeight", value)

    # window_min_width
    @property
    def window_min_width(self) -> OptionalNumber:
        return self._get_attr("windowMinWidth")

    @window_min_width.setter
    @beartype
    def window_min_width(self, value: OptionalNumber):
        self._set_attr("windowMinWidth", value)

    # window_min_height
    @property
    def window_min_height(self) -> OptionalNumber:
        return self._get_attr("windowMinHeight")

    @window_min_height.setter
    @beartype
    def window_min_height(self, value: OptionalNumber):
        self._set_attr("windowMinHeight", value)

    # window_opacity
    @property
    def window_opacity(self) -> OptionalNumber:
        return self._get_attr("windowOpacity", data_type="float", def_value=1)

    @window_opacity.setter
    @beartype
    def window_opacity(self, value: OptionalNumber):
        self._set_attr("windowOpacity", value)

    # window_maximized
    @property
    def window_maximized(self) -> Optional[bool]:
        return self._get_attr("windowMaximized", data_type="bool", def_value=False)

    @window_maximized.setter
    @beartype
    def window_maximized(self, value: Optional[bool]):
        self._set_attr("windowMaximized", value)

    # window_minimized
    @property
    def window_minimized(self) -> Optional[bool]:
        return self._get_attr("windowMinimized", data_type="bool", def_value=False)

    @window_minimized.setter
    @beartype
    def window_minimized(self, value: Optional[bool]):
        self._set_attr("windowMinimized", value)

    # window_minimizable
    @property
    def window_minimizable(self) -> Optional[bool]:
        return self._get_attr("windowMinimizable", data_type="bool", def_value=True)

    @window_minimizable.setter
    @beartype
    def window_minimizable(self, value: Optional[bool]):
        self._set_attr("windowMinimizable", value)

    # window_maximizable
    @property
    def window_maximizable(self) -> Optional[bool]:
        return self._get_attr("windowMaximizable", data_type="bool", def_value=True)

    @window_maximizable.setter
    @beartype
    def window_maximizable(self, value: Optional[bool]):
        self._set_attr("windowMaximizable", value)

    # window_resizable
    @property
    def window_resizable(self) -> Optional[bool]:
        return self._get_attr("windowResizable", data_type="bool", def_value=True)

    @window_resizable.setter
    @beartype
    def window_resizable(self, value: Optional[bool]):
        self._set_attr("windowResizable", value)

    # window_movable
    @property
    def window_movable(self) -> Optional[bool]:
        return self._get_attr("windowMovable", data_type="bool", def_value=True)

    @window_movable.setter
    @beartype
    def window_movable(self, value: Optional[bool]):
        self._set_attr("windowMovable", value)

    # window_full_screen
    @property
    def window_full_screen(self) -> Optional[bool]:
        return self._get_attr("windowFullScreen", data_type="bool", def_value=False)

    @window_full_screen.setter
    @beartype
    def window_full_screen(self, value: Optional[bool]):
        self._set_attr("windowFullScreen", value)

    # window_always_on_top
    @property
    def window_always_on_top(self) -> Optional[bool]:
        return self._get_attr("windowAlwaysOnTop", data_type="bool", def_value=False)

    @window_always_on_top.setter
    @beartype
    def window_always_on_top(self, value: Optional[bool]):
        self._set_attr("windowAlwaysOnTop", value)

    # window_prevent_close
    @property
    def window_prevent_close(self) -> Optional[bool]:
        return self._get_attr("windowPreventClose", data_type="bool", def_value=False)

    @window_prevent_close.setter
    @beartype
    def window_prevent_close(self, value: Optional[bool]):
        self._set_attr("windowPreventClose", value)

    # window_title_bar_hidden
    @property
    def window_title_bar_hidden(self) -> Optional[bool]:
        return self._get_attr("windowTitleBarHidden", data_type="bool", def_value=False)

    @window_title_bar_hidden.setter
    @beartype
    def window_title_bar_hidden(self, value: Optional[bool]):
        self._set_attr("windowTitleBarHidden", value)

    # window_title_bar_buttons_hidden
    @property
    def window_title_bar_buttons_hidden(self) -> Optional[bool]:
        return self._get_attr(
            "windowTitleBarButtonsHidden", data_type="bool", def_value=False
        )

    @window_title_bar_buttons_hidden.setter
    @beartype
    def window_title_bar_buttons_hidden(self, value: Optional[bool]):
        self._set_attr("windowTitleBarButtonsHidden", value)

    # window_skip_task_bar
    @property
    def window_skip_task_bar(self) -> Optional[bool]:
        return self._get_attr("windowSkipTaskBar", data_type="bool", def_value=False)

    @window_skip_task_bar.setter
    @beartype
    def window_skip_task_bar(self, value: Optional[bool]):
        self._set_attr("windowSkipTaskBar", value)

    # window_frameless
    @property
    def window_frameless(self) -> Optional[bool]:
        return self._get_attr("windowFrameless", data_type="bool", def_value=False)

    @window_frameless.setter
    @beartype
    def window_frameless(self, value: Optional[bool]):
        self._set_attr("windowFrameless", value)

    # window_progress_bar
    @property
    def window_progress_bar(self) -> OptionalNumber:
        return self._get_attr("windowProgressBar")

    @window_progress_bar.setter
    @beartype
    def window_progress_bar(self, value: OptionalNumber):
        self._set_attr("windowProgressBar", value)

    # window_focused
    @property
    def window_focused(self) -> Optional[bool]:
        return self._get_attr("windowFocused", data_type="bool", def_value=True)

    @window_focused.setter
    @beartype
    def window_focused(self, value: Optional[bool]):
        self._set_attr("windowFocused", value)

    # window_visible
    @property
    def window_visible(self) -> Optional[bool]:
        return self._get_attr("windowVisible", data_type="bool")

    @window_visible.setter
    @beartype
    def window_visible(self, value: Optional[bool]):
        self._set_attr("windowVisible", value)

    # on_close
    @property
    def on_close(self):
        return self.__on_close

    @on_close.setter
    def on_close(self, handler):
        self.__on_close.subscribe(handler)

    # on_resize
    @property
    def on_resize(self):
        return self.__on_resize

    @on_resize.setter
    def on_resize(self, handler):
        self.__on_resize.subscribe(handler)

    # on_route_change
    @property
    def on_route_change(self):
        return self.__on_route_change

    @on_route_change.setter
    def on_route_change(self, handler):
        self.__on_route_change.subscribe(handler)

    # on_view_pop
    @property
    def on_view_pop(self):
        return self.__on_view_pop

    @on_view_pop.setter
    def on_view_pop(self, handler):
        self.__on_view_pop.subscribe(handler)

    # on_keyboard_event
    @property
    def on_keyboard_event(self):
        return self.__on_keyboard_event

    @on_keyboard_event.setter
    def on_keyboard_event(self, handler):
        self.__on_keyboard_event.subscribe(handler)

    # on_window_event
    @property
    def on_window_event(self):
        return self.__on_window_event

    @on_window_event.setter
    def on_window_event(self, handler):
        self.__on_window_event.subscribe(handler)

    # on_connect
    @property
    def on_connect(self):
        return self.__on_connect

    @on_connect.setter
    def on_connect(self, handler):
        self.__on_connect.subscribe(handler)

    # on_disconnect
    @property
    def on_disconnect(self):
        return self.__on_disconnect

    @on_disconnect.setter
    def on_disconnect(self, handler):
        self.__on_disconnect.subscribe(handler)

    # on_login
    @property
    def on_login(self):
        return self.__on_login

    @on_login.setter
    def on_login(self, handler):
        self.__on_login.subscribe(handler)

    # on_logout
    @property
    def on_logout(self):
        return self.__on_logout

    @on_logout.setter
    def on_logout(self, handler):
        self.__on_logout.subscribe(handler)

    # on_error
    @property
    def on_error(self):
        return self.__on_error

    @on_error.setter
    def on_error(self, handler):
        self.__on_error.subscribe(handler)


class Offstage(Control):
    def __init__(
        self,
        visible: Optional[bool] = None,
        disabled: Optional[bool] = None,
        data: Any = None,
    ):

        Control.__init__(
            self,
            visible=visible,
            disabled=disabled,
            data=data,
        )

        self.__controls: List[Control] = []
        self.__clipboard = Clipboard()
        self.__banner = None
        self.__snack_bar = None
        self.__dialog = None
        self.__splash = None

    def _get_control_name(self):
        return "offstage"

    def _get_children(self):
        children = []
        children.extend(self.__controls)
        if self.__clipboard:
            children.append(self.__clipboard)
        if self.__banner:
            children.append(self.__banner)
        if self.__snack_bar:
            children.append(self.__snack_bar)
        if self.__dialog:
            children.append(self.__dialog)
        if self.__splash:
            children.append(self.__splash)
        return children

    # controls
    @property
    def controls(self):
        return self.__controls

    # clipboard
    @property
    def clipboard(self):
        return self.__clipboard

    # splash
    @property
    def splash(self) -> Optional[Control]:
        return self.__splash

    @splash.setter
    @beartype
    def splash(self, value: Optional[Control]):
        self.__splash = value

    # banner
    @property
    def banner(self) -> Optional[Banner]:
        return self.__banner

    @banner.setter
    @beartype
    def banner(self, value: Optional[Banner]):
        self.__banner = value

    # snack_bar
    @property
    def snack_bar(self) -> Optional[SnackBar]:
        return self.__snack_bar

    @snack_bar.setter
    @beartype
    def snack_bar(self, value: Optional[SnackBar]):
        self.__snack_bar = value

    # dialog
    @property
    def dialog(self) -> Optional[Control]:
        return self.__dialog

    @dialog.setter
    @beartype
    def dialog(self, value: Optional[Control]):
        self.__dialog = value


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
