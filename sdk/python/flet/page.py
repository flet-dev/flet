import json
import logging
import threading

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
from flet.control_event import ControlEvent
from flet.floating_action_button import FloatingActionButton
from flet.protocol import Command
from flet.pubsub import PubSub
from flet.snack_bar import SnackBar
from flet.theme import Theme

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
        self._controls = []  # page controls
        self._index = {}  # index with all page controls
        self._index[self._Control__uid] = self
        self._last_event = None
        self._event_available = threading.Event()
        self._fetch_page_details()

        self.__fonts: Dict[str, str] = None
        self.__offstage = Offstage()
        self.__appbar = None
        self.__theme = None
        self.__dark_theme = None
        self.__pubsub = PubSub(conn.pubsubhub, session_id)

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        self.close()

    def get_control(self, id):
        return self._index.get(id)

    def _get_children(self):
        children = [self.__offstage]
        if self.__appbar:
            children.append(self.__appbar)
        children.extend(self._controls)
        return children

    def _fetch_page_details(self):
        values = self.__conn.send_commands(
            self.__conn.page_name,
            self._session_id,
            [
                Command(0, "get", ["page", "winWidth"], None, None),
                Command(0, "get", ["page", "winHeight"], None, None),
            ],
        ).results
        self._set_attr("winWidth", values[0], False)
        self._set_attr("winHeight", values[1], False)

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

    def on_event(self, e):
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

    # controls
    @property
    def controls(self):
        return self._controls

    @controls.setter
    @beartype
    def controls(self, value: List[Control]):
        self._controls = value or []

    # title
    @property
    def title(self):
        return self._get_attr("title")

    @title.setter
    def title(self, value):
        self._set_attr("title", value)

    # horizontal_alignment
    @property
    def horizontal_alignment(self):
        return self._get_attr("horizontalAlignment")

    @horizontal_alignment.setter
    @beartype
    def horizontal_alignment(self, value: CrossAxisAlignment):
        self._set_attr("horizontalAlignment", value)

    # vertical_alignment
    @property
    def vertical_alignment(self):
        return self._get_attr("verticalAlignment")

    @vertical_alignment.setter
    @beartype
    def vertical_alignment(self, value: MainAxisAlignment):
        self._set_attr("verticalAlignment", value)

    # spacing
    @property
    def spacing(self):
        return self._get_attr("spacing")

    @spacing.setter
    @beartype
    def spacing(self, value: OptionalNumber):
        self._set_attr("spacing", value)

    # padding
    @property
    def padding(self):
        return self.__padding

    @padding.setter
    @beartype
    def padding(self, value: PaddingValue):
        self.__padding = value
        if value and isinstance(value, (int, float)):
            value = padding.all(value)
        self._set_attr_json("padding", value)

    # bgcolor
    @property
    def bgcolor(self):
        return self._get_attr("bgcolor")

    @bgcolor.setter
    def bgcolor(self, value):
        self._set_attr("bgcolor", value)

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

    # splash
    @property
    def splash(self):
        return self.__offstage.splash

    @splash.setter
    @beartype
    def splash(self, value: Optional[Control]):
        self.__offstage.splash = value

    # appbar
    @property
    def appbar(self):
        return self.__appbar

    @appbar.setter
    @beartype
    def appbar(self, value: Optional[AppBar]):
        self.__appbar = value

    # floating_action_button
    @property
    def floating_action_button(self):
        return self.__offstage.floating_action_button

    @floating_action_button.setter
    @beartype
    def floating_action_button(self, value: Optional[FloatingActionButton]):
        self.__offstage.floating_action_button = value

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

    # scroll
    @property
    def scroll(self):
        return self.__scroll

    @scroll.setter
    @beartype
    def scroll(self, value: ScrollMode):
        self.__scroll = value
        if value == True:
            value = "auto"
        elif value == False:
            value = "none"
        self._set_attr("scroll", value)

    # auto_scroll
    @property
    def auto_scroll(self):
        return self._get_attr("autoScroll")

    @auto_scroll.setter
    @beartype
    def auto_scroll(self, value: Optional[bool]):
        self._set_attr("autoScroll", value)

    # window_width
    @property
    def window_width(self):
        w = self._get_attr("winWidth")
        if w != None and w != "":
            return float(w)
        return 0

    # window_height
    @property
    def window_height(self):
        h = self._get_attr("winHeight")
        if h != None and h != "":
            return float(h)
        return 0

    # on_close
    @property
    def on_close(self):
        return self._get_event_handler("close")

    @on_close.setter
    def on_close(self, handler):
        self._add_event_handler("close", handler)

    # on_resize
    @property
    def on_resize(self):
        return self._get_event_handler("resize")

    @on_resize.setter
    def on_resize(self, handler):
        self._add_event_handler("resize", handler)

    # on_connect
    @property
    def on_connect(self):
        return self._get_event_handler("connect")

    @on_connect.setter
    def on_connect(self, handler):
        self._add_event_handler("connect", handler)

    # on_disconnect
    @property
    def on_disconnect(self):
        return self._get_event_handler("disconnect")

    @on_disconnect.setter
    def on_disconnect(self, handler):
        self._add_event_handler("disconnect", handler)


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
        self.__fab = None
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
        if self.__fab:
            children.append(self.__fab)
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

    # floating_action_button
    @property
    def floating_action_button(self):
        return self.__fab

    @floating_action_button.setter
    @beartype
    def floating_action_button(self, value: Optional[FloatingActionButton]):
        self.__fab = value

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
