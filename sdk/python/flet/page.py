import json
import logging
import threading
import time

from beartype import beartype
from beartype.typing import Dict, List, Optional

from flet import constants, padding
from flet.app_bar import AppBar
from flet.banner import Banner
from flet.clipboard import Clipboard
from flet.connection import Connection
from flet.control import (
    Control,
    CrossAxisAlignment,
    MainAxisAlignment,
    OptionalNumber,
    PaddingValue,
    ScrollMode,
)
from flet.event import Event
from flet.event_handler import EventHandler
from flet.floating_action_button import FloatingActionButton
from flet.protocol import Command
from flet.pubsub import PubSub
from flet.snack_bar import SnackBar
from flet.theme import Theme
from flet.view import View

try:
    from typing import Literal
except:
    from typing_extensions import Literal


PageDesign = Literal[None, "material", "cupertino", "fluent", "macos", "adaptive"]
ThemeMode = Literal[None, "system", "light", "dark"]


class Page(Control):
    def __init__(self, conn: Connection, session_id):
        Control.__init__(self)

        self._id = "page"
        self._Control__uid = "page"
        self.__conn = conn
        self._session_id = session_id
        self._index = {}  # index with all page controls
        self._index[self._Control__uid] = self
        self._last_event = None
        self._event_available = threading.Event()
        self._fetch_page_details()

        self.__views = [View()]
        self.__default_view = self.__views[0]
        self._controls = self.__default_view.controls

        self.__fonts: Dict[str, str] = None
        self.__offstage = Offstage()
        self.__theme = None
        self.__dark_theme = None
        self.__pubsub = PubSub(conn.pubsubhub, session_id)

        self.__on_close = EventHandler()
        self._add_event_handler("close", self.__on_close.handler)
        self.__on_resize = EventHandler()
        self._add_event_handler("resize", self.__on_resize.handler)

        self.__on_route_change = EventHandler(lambda e: e.data)
        self._add_event_handler("route_change", self.__on_route_change.handler)
        self.__on_view_pop = EventHandler(lambda e: self.get_control(e.data))
        self._add_event_handler("view_pop", self.__on_view_pop.handler)
        self.__on_window_event = EventHandler()
        self._add_event_handler("window_event", self.__on_window_event.handler)
        self.__on_connect = EventHandler()
        self._add_event_handler("connect", self.__on_connect.handler)
        self.__on_disconnect = EventHandler()
        self._add_event_handler("disconnect", self.__on_disconnect.handler)

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        self.close()

    def get_control(self, id):
        return self._index.get(id)

    def _get_children(self):
        children = []
        children.extend(self.__views)
        children.append(self.__offstage)
        return children

    def _fetch_page_details(self):
        values = self.__conn.send_commands(
            self.__conn.page_name,
            self._session_id,
            [
                Command(0, "get", ["page", "route"], None, None),
                Command(0, "get", ["page", "pwa"], None, None),
                Command(0, "get", ["page", "width"], None, None),
                Command(0, "get", ["page", "height"], None, None),
                Command(0, "get", ["page", "windowWidth"], None, None),
                Command(0, "get", ["page", "windowHeight"], None, None),
                Command(0, "get", ["page", "windowTop"], None, None),
                Command(0, "get", ["page", "windowLeft"], None, None),
            ],
        ).results
        self._set_attr("route", values[0], False)
        self._set_attr("pwa", values[1], False)
        self._set_attr("width", values[2], False)
        self._set_attr("height", values[3], False)
        self._set_attr("windowWidth", values[4], False)
        self._set_attr("windowHeight", values[5], False)
        self._set_attr("windowTop", values[6], False)
        self._set_attr("windowLeft", values[7], False)

    def update(self, *controls):
        with self._lock:
            if len(controls) == 0:
                return self.__update(self)
            else:
                return self.__update(*controls)

    def __update(self, *controls):
        added_controls = []
        commands = []

        # build commands
        for control in controls:
            control.build_update_commands(self._index, added_controls, commands)

        if len(commands) == 0:
            return

        # execute commands
        results = self.__conn.send_commands(
            self.__conn.page_name, self._session_id, commands
        ).results

        if len(results) > 0:
            n = 0
            for line in results:
                for id in line.split(" "):
                    added_controls[n]._Control__uid = id
                    added_controls[n].page = self

                    # add to index
                    self._index[id] = added_controls[n]

                    # call Control.did_mount
                    added_controls[n].did_mount()

                    n += 1

    def add(self, *controls):
        with self._lock:
            self._controls.extend(controls)
            return self.__update(self)

    def insert(self, at, *controls):
        with self._lock:
            n = at
            for control in controls:
                self._controls.insert(n, control)
                n += 1
            return self.__update(self)

    def remove(self, *controls):
        with self._lock:
            for control in controls:
                self._controls.remove(control)
            return self.__update(self)

    def remove_at(self, index):
        with self._lock:
            self._controls.pop(index)
            return self.__update(self)

    def clean(self):
        with self._lock:
            self._previous_children.clear()
            for child in self._get_children():
                self._remove_control_recursively(self._index, child)
            self._controls.clear()
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

    def wait_event(self):
        self._event_available.clear()
        self._event_available.wait()
        return self._last_event

    def show_signin(self, auth_providers="*", auth_groups=False, allow_dismiss=False):
        with self._lock:
            self.signin = auth_providers
            self.signin_groups = auth_groups
            self.signin_allow_dismiss = allow_dismiss
            self.__update(self)

        while True:
            e = self.wait_event()
            if e.control == self and e.name.lower() == "signin":
                return True
            elif e.control == self and e.name.lower() == "dismisssignin":
                return False

    def go(self, route):
        self.route = route
        self.__on_route_change.handler(Event("page", "route_change", self.route))
        self.update()

    def signout(self):
        return self._send_command("signout", None)

    def can_access(self, users_and_groups):
        return (
            self._send_command("canAccess", [users_and_groups]).result.lower() == "true"
        )

    def close(self):
        if self._session_id == constants.ZERO_SESSION:
            self.__conn.close()

    def _send_command(self, name: str, values: List[str]):
        return self.__conn.send_command(
            self.__conn.page_name,
            self._session_id,
            Command(0, name, values, None, None),
        )

    @beartype
    def set_clipboard(self, value: str):
        self.__offstage.clipboard.value = value
        self.__offstage.clipboard.update()

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

    # pubsub
    @property
    def pubsub(self):
        return self.__pubsub

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

    # design
    @property
    def design(self):
        return self._get_attr("design")

    @design.setter
    @beartype
    def design(self, value: PageDesign):
        self._set_attr("design", value)

    # fonts
    @property
    def fonts(self):
        return self.__fonts

    @fonts.setter
    @beartype
    def fonts(self, value: Optional[Dict[str, str]]):
        self.__fonts = value
        self._set_attr_json("fonts", value)

    # views
    @property
    def views(self):
        return self.__views

    # controls
    @property
    def controls(self):
        return self.__default_view.controls

    @controls.setter
    @beartype
    def controls(self, value: List[Control]):
        self.__default_view.controls = value or []

    # appbar
    @property
    def appbar(self):
        return self.__default_view.appbar

    @appbar.setter
    @beartype
    def appbar(self, value: Optional[AppBar]):
        self.__default_view.appbar = value

    # floating_action_button
    @property
    def floating_action_button(self):
        return self.__default_view.floating_action_button

    @floating_action_button.setter
    @beartype
    def floating_action_button(self, value: Optional[FloatingActionButton]):
        self.__default_view.floating_action_button = value

    # horizontal_alignment
    @property
    def horizontal_alignment(self):
        return self.__default_view.horizontal_alignment

    @horizontal_alignment.setter
    @beartype
    def horizontal_alignment(self, value: CrossAxisAlignment):
        self.__default_view.horizontal_alignment = value

    # vertical_alignment
    @property
    def vertical_alignment(self):
        return self.__default_view.vertical_alignment

    @vertical_alignment.setter
    @beartype
    def vertical_alignment(self, value: MainAxisAlignment):
        self.__default_view.vertical_alignment = value

    # spacing
    @property
    def spacing(self):
        return self.__default_view.spacing

    @spacing.setter
    @beartype
    def spacing(self, value: OptionalNumber):
        self.__default_view.spacing = value

    # padding
    @property
    def padding(self):
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
    def scroll(self):
        return self.__default_view.scroll

    @scroll.setter
    @beartype
    def scroll(self, value: ScrollMode):
        self.__default_view.scroll = value

    # auto_scroll
    @property
    def auto_scroll(self):
        return self.__default_view.auto_scroll

    @auto_scroll.setter
    @beartype
    def auto_scroll(self, value: Optional[bool]):
        self.__default_view.auto_scroll = value

    # splash
    @property
    def splash(self):
        return self.__offstage.splash

    @splash.setter
    @beartype
    def splash(self, value: Optional[Control]):
        self.__offstage.splash = value

    # banner
    @property
    def banner(self):
        return self.__offstage.banner

    @banner.setter
    @beartype
    def banner(self, value: Optional[Banner]):
        self.__offstage.banner = value

    # snack_bar
    @property
    def snack_bar(self):
        return self.__offstage.snack_bar

    @snack_bar.setter
    @beartype
    def snack_bar(self, value: Optional[SnackBar]):
        self.__offstage.snack_bar = value

    # dialog
    @property
    def dialog(self):
        return self.__offstage.dialog

    @dialog.setter
    @beartype
    def dialog(self, value: Optional[Control]):
        self.__offstage.dialog = value

    # theme_mode
    @property
    def theme_mode(self):
        return self._get_attr("themeMode")

    @theme_mode.setter
    @beartype
    def theme_mode(self, value: Optional[ThemeMode]):
        self._set_attr("themeMode", value)

    # theme
    @property
    def theme(self):
        return self.__theme

    @theme.setter
    @beartype
    def theme(self, value: Optional[Theme]):
        self.__theme = value
        if self.__theme:
            self.__theme.brightness = "light"
        self._set_attr_json("theme", value)

    # dark_theme
    @property
    def dark_theme(self):
        return self.__dark_theme

    @dark_theme.setter
    @beartype
    def dark_theme(self, value: Optional[Theme]):
        self.__dark_theme = value
        if self.__dark_theme:
            self.__dark_theme.brightness = "dark"
        self._set_attr_json("darkTheme", value)

    # rtl
    @property
    def rtl(self):
        return self._get_attr("rtl")

    @rtl.setter
    @beartype
    def rtl(self, value: Optional[bool]):
        self._set_attr("rtl", value)

    # width
    @property
    def width(self):
        w = self._get_attr("width")
        if w != None and w != "":
            return float(w)
        return 0

    # height
    @property
    def height(self):
        h = self._get_attr("height")
        if h != None and h != "":
            return float(h)
        return 0

    # window_width
    @property
    def window_width(self):
        w = self._get_attr("windowWidth")
        if w != None and w != "":
            return float(w)
        return 0

    @window_width.setter
    @beartype
    def window_width(self, value: OptionalNumber):
        self._set_attr("windowWidth", value)

    # window_height
    @property
    def window_height(self):
        h = self._get_attr("windowHeight")
        if h != None and h != "":
            return float(h)
        return 0

    @window_height.setter
    @beartype
    def window_height(self, value: OptionalNumber):
        self._set_attr("windowHeight", value)

    # window_top
    @property
    def window_top(self):
        w = self._get_attr("windowTop")
        if w != None and w != "":
            return float(w)
        return 0

    @window_top.setter
    @beartype
    def window_top(self, value: OptionalNumber):
        self._set_attr("windowTop", value)

    # window_left
    @property
    def window_left(self):
        h = self._get_attr("windowLeft")
        if h != None and h != "":
            return float(h)
        return 0

    @window_left.setter
    @beartype
    def window_left(self, value: OptionalNumber):
        self._set_attr("windowLeft", value)

    # window_max_width
    @property
    def window_max_width(self):
        return self._get_attr("windowMaxWidth")

    @window_max_width.setter
    @beartype
    def window_max_width(self, value: OptionalNumber):
        self._set_attr("windowMaxWidth", value)

    # window_max_height
    @property
    def window_max_height(self):
        return self._get_attr("windowMaxHeight")

    @window_max_height.setter
    @beartype
    def window_max_height(self, value: OptionalNumber):
        self._set_attr("windowMaxHeight", value)

    # window_min_width
    @property
    def window_min_width(self):
        return self._get_attr("windowMinWidth")

    @window_min_width.setter
    @beartype
    def window_min_width(self, value: OptionalNumber):
        self._set_attr("windowMinWidth", value)

    # window_min_height
    @property
    def window_min_height(self):
        return self._get_attr("windowMinHeight")

    @window_min_height.setter
    @beartype
    def window_min_height(self, value: OptionalNumber):
        self._set_attr("windowMinHeight", value)

    # window_opacity
    @property
    def window_opacity(self):
        return self._get_attr("windowOpacity", data_type="float", def_value=1)

    @window_opacity.setter
    @beartype
    def window_opacity(self, value: OptionalNumber):
        self._set_attr("windowOpacity", value)

    # window_maximized
    @property
    def window_maximized(self):
        return self._get_attr("windowMaximized", data_type="bool", def_value=False)

    @window_maximized.setter
    @beartype
    def window_maximized(self, value: Optional[bool]):
        self._set_attr("windowMaximized", value)

    # window_minimized
    @property
    def window_minimized(self):
        return self._get_attr("windowMinimized", data_type="bool", def_value=False)

    @window_minimized.setter
    @beartype
    def window_minimized(self, value: Optional[bool]):
        self._set_attr("windowMinimized", value)

    # window_minimizable
    @property
    def window_minimizable(self):
        return self._get_attr("windowMinimizable", data_type="bool", def_value=True)

    @window_minimizable.setter
    @beartype
    def window_minimizable(self, value: Optional[bool]):
        self._set_attr("windowMinimizable", value)

    # window_resizable
    @property
    def window_resizable(self):
        return self._get_attr("windowResizable", data_type="bool", def_value=True)

    @window_resizable.setter
    @beartype
    def window_resizable(self, value: Optional[bool]):
        self._set_attr("windowResizable", value)

    # window_movable
    @property
    def window_movable(self):
        return self._get_attr("windowMovable", data_type="bool", def_value=True)

    @window_movable.setter
    @beartype
    def window_movable(self, value: Optional[bool]):
        self._set_attr("windowMovable", value)

    # window_full_screen
    @property
    def window_full_screen(self):
        return self._get_attr("windowFullScreen", data_type="bool", def_value=False)

    @window_full_screen.setter
    @beartype
    def window_full_screen(self, value: Optional[bool]):
        self._set_attr("windowFullScreen", value)

    # window_always_on_top
    @property
    def window_always_on_top(self):
        return self._get_attr("windowAlwaysOnTop", data_type="bool", def_value=False)

    @window_always_on_top.setter
    @beartype
    def window_always_on_top(self, value: Optional[bool]):
        self._set_attr("windowAlwaysOnTop", value)

    # window_prevent_close
    @property
    def window_prevent_close(self):
        return self._get_attr("windowPreventClose", data_type="bool", def_value=False)

    @window_prevent_close.setter
    @beartype
    def window_prevent_close(self, value: Optional[bool]):
        self._set_attr("windowPreventClose", value)

    # window_focused
    @property
    def window_focused(self):
        return self._get_attr("windowFocused", data_type="bool", def_value=True)

    @window_focused.setter
    @beartype
    def window_focused(self, value: Optional[bool]):
        self._set_attr("windowFocused", value)

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


class Offstage(Control):
    def __init__(
        self,
        visible: bool = None,
        disabled: bool = None,
        data: any = None,
    ):

        Control.__init__(
            self,
            visible=visible,
            disabled=disabled,
            data=data,
        )

        self.__clipboard = Clipboard()
        self.__banner = None
        self.__snack_bar = None
        self.__dialog = None
        self.__splash = None

    def _get_control_name(self):
        return "offstage"

    def _get_children(self):
        children = []
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

    # clipboard
    @property
    def clipboard(self):
        return self.__clipboard

    # splash
    @property
    def splash(self):
        return self.__splash

    @splash.setter
    @beartype
    def splash(self, value: Optional[Control]):
        self.__splash = value

    # banner
    @property
    def banner(self):
        return self.__banner

    @banner.setter
    @beartype
    def banner(self, value: Optional[Banner]):
        self.__banner = value

    # snack_bar
    @property
    def snack_bar(self):
        return self.__snack_bar

    @snack_bar.setter
    @beartype
    def snack_bar(self, value: Optional[SnackBar]):
        self.__snack_bar = value

    # dialog
    @property
    def dialog(self):
        return self.__dialog

    @dialog.setter
    @beartype
    def dialog(self, value: Optional[Control]):
        self.__dialog = value


class ControlEvent(Event):
    def __init__(self, target: str, name: str, data: str, control: Control, page: Page):
        Event.__init__(self, target=target, name=name, data=data)

        self.control: Control = control
        self.page: Page = page
