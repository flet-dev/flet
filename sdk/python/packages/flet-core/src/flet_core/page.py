import asyncio
import json
import logging
import threading
import time
import uuid
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Tuple, Union, cast
from urllib.parse import urlparse

from flet_core.app_bar import AppBar
from flet_core.banner import Banner
from flet_core.client_storage import ClientStorage
from flet_core.clipboard import Clipboard
from flet_core.connection import Connection
from flet_core.control import Control, OptionalNumber
from flet_core.control_event import ControlEvent
from flet_core.event import Event
from flet_core.event_handler import EventHandler
from flet_core.floating_action_button import FloatingActionButton
from flet_core.navigation_bar import NavigationBar
from flet_core.protocol import Command
from flet_core.querystring import QueryString
from flet_core.session_storage import SessionStorage
from flet_core.snack_bar import SnackBar
from flet_core.theme import Theme
from flet_core.types import (
    CrossAxisAlignment,
    MainAxisAlignment,
    PaddingValue,
    PageDesignLanguage,
    PageDesignString,
    ScrollMode,
    ThemeMode,
    ThemeModeString,
)
from flet_core.utils import is_asyncio, is_coroutine
from flet_core.view import View

try:
    from flet.auth.authorization import Authorization
    from flet.auth.oauth_provider import OAuthProvider
    from flet.pubsub import PubSub
except ImportError:

    class Authorization:
        pass

    class OAuthProvider:
        pass

    class PubSub:
        def __init__(self, pubsubhub, session_id) -> None:
            pass


try:
    from typing import Literal
except ImportError:
    from typing_extensions import Literal


class NopeLock(object):
    def __enter__(self):
        pass

    def __exit__(self, *args):
        pass


class AsyncNopeLock(object):
    async def __aenter__(self):
        pass

    async def __aexit__(self, *args):
        pass


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

        self.__lock = threading.Lock() if not is_asyncio() else NopeLock()
        self.__async_lock = asyncio.Lock() if is_asyncio() else AsyncNopeLock()

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
        self._add_event_handler("close", self.__on_close.get_handler())
        self.__on_resize = EventHandler()
        self._add_event_handler("resize", self.__on_resize.get_handler())

        self.__last_route = None

        # authorize/login/logout
        self.__on_login = EventHandler()
        self._add_event_handler(
            "authorize",
            self.__on_authorize if not is_asyncio() else self.__on_authorize_async,
        )
        self.__on_logout = EventHandler()

        # route_change
        def convert_route_change_event(e):
            if self.__last_route == e.data:
                return None  # avoid duplicate calls
            self.__last_route = e.data
            self.query()  # Update query url (required when manually changed from browser)
            return RouteChangeEvent(route=e.data)

        self.__on_route_change = EventHandler(convert_route_change_event)
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

        self.__method_calls: Dict[str, Union[threading.Event, asyncio.Event]] = {}
        self.__method_call_results: Dict[
            Union[threading.Event, asyncio.Event], tuple[Optional[str], Optional[str]]
        ] = {}
        self._add_event_handler("invoke_method_result", self.__on_invoke_method_result)

        self.__on_window_event = EventHandler()
        self._add_event_handler("window_event", self.__on_window_event.get_handler())
        self.__on_connect = EventHandler()
        self._add_event_handler("connect", self.__on_connect.get_handler())
        self.__on_disconnect = EventHandler()
        self._add_event_handler("disconnect", self.__on_disconnect.get_handler())
        self.__on_error = EventHandler()
        self._add_event_handler("error", self.__on_error.get_handler())

    def get_control(self, id):
        return self._index.get(id)

    def _before_build_command(self):
        super()._before_build_command()
        self._set_attr_json("fonts", self.__fonts)
        self._set_attr_json("theme", self.__theme)
        self._set_attr_json("darkTheme", self.__dark_theme)

        # keyboard event
        if self.__on_keyboard_event.count() > 0:
            self._set_attr("onKeyboardEvent", True)

    def _get_children(self):
        children = []
        children.extend(self.__views)
        children.append(self.__offstage)
        return children

    def fetch_page_details(self):
        assert self.__conn.page_name is not None
        values = self.__conn.send_commands(
            self._session_id,
            self.__get_page_detail_commands(),
        ).results
        self.__set_page_details(values)

    async def fetch_page_details_async(self):
        assert self.__conn.page_name is not None
        values = (
            await self.__conn.send_commands_async(
                self._session_id,
                self.__get_page_detail_commands(),
            )
        ).results
        self.__set_page_details(values)

    def __get_page_detail_commands(self):
        return [
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
        ]

    def __set_page_details(self, values):
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
        with self.__lock:
            if len(controls) == 0:
                r = self.__update(self)
            else:
                r = self.__update(*controls)
        self.__handle_mount_unmount(*r)

    async def update_async(self, *controls):
        async with self.__async_lock:
            if len(controls) == 0:
                r = await self.__update_async(self)
            else:
                r = await self.__update_async(*controls)
        await self.__handle_mount_unmount_async(*r)

    def add(self, *controls):
        with self.__lock:
            self._controls.extend(controls)
            r = self.__update(self)
        self.__handle_mount_unmount(*r)

    async def add_async(self, *controls):
        async with self.__async_lock:
            self._controls.extend(controls)
            r = await self.__update_async(self)
        await self.__handle_mount_unmount_async(*r)

    def insert(self, at, *controls):
        with self.__lock:
            n = at
            for control in controls:
                self._controls.insert(n, control)
                n += 1
            r = self.__update(self)
        self.__handle_mount_unmount(*r)

    async def insert_async(self, at, *controls):
        async with self.__async_lock:
            n = at
            for control in controls:
                self._controls.insert(n, control)
                n += 1
            r = await self.__update_async(self)
        await self.__handle_mount_unmount_async(*r)

    def remove(self, *controls):
        with self.__lock:
            for control in controls:
                self._controls.remove(control)
            r = self.__update(self)
        self.__handle_mount_unmount(*r)

    async def remove_async(self, *controls):
        async with self.__async_lock:
            for control in controls:
                self._controls.remove(control)
            r = await self.__update_async(self)
        await self.__handle_mount_unmount_async(*r)

    def remove_at(self, index):
        with self.__lock:
            self._controls.pop(index)
            r = self.__update(self)
        self.__handle_mount_unmount(*r)

    async def remove_at_async(self, index):
        async with self.__async_lock:
            self._controls.pop(index)
            r = await self.__update_async(self)
        await self.__handle_mount_unmount_async(*r)

    def clean(self):
        self._clean(self)
        self._controls.clear()

    async def clean_async(self):
        await self._clean_async(self)
        self._controls.clear()

    def _clean(self, control: Control):
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

    async def _clean_async(self, control: Control):
        async with self.__async_lock:
            control._previous_children.clear()
            assert control.uid is not None
            removed_controls = []
            for child in control._get_children():
                removed_controls.extend(
                    self._remove_control_recursively(self.index, child)
                )
            await self._send_command_async("clean", [control.uid])
            for c in removed_controls:
                await c.will_unmount_async()

    def __update(self, *controls) -> Tuple[List[Control], List[Control]]:
        commands, added_controls, removed_controls = self.__prepare_update(*controls)
        self.__validate_controls_page(added_controls)
        results = self.__conn.send_commands(self._session_id, commands).results
        self.__update_control_ids(added_controls, results)
        return added_controls, removed_controls

    async def __update_async(self, *controls) -> Tuple[List[Control], List[Control]]:
        commands, added_controls, removed_controls = self.__prepare_update(*controls)
        self.__validate_controls_page(added_controls)
        results = (
            await self.__conn.send_commands_async(self._session_id, commands)
        ).results
        self.__update_control_ids(added_controls, results)
        return added_controls, removed_controls

    def __prepare_update(self, *controls):
        added_controls = []
        removed_controls = []
        commands = []

        # build commands
        for control in controls:
            control.build_update_commands(
                self._index, commands, added_controls, removed_controls
            )

        if len(commands) == 0:
            return commands, added_controls, removed_controls

        return commands, added_controls, removed_controls

    def __validate_controls_page(self, added_controls):
        for ctrl in added_controls:
            if ctrl.page and ctrl.page != self:
                raise Exception(
                    "Control has already been added to another page: {}".format(ctrl)
                )

    def __update_control_ids(self, added_controls, results):
        if len(results) > 0:
            n = 0
            for line in results:
                for id in line.split(" "):
                    added_controls[n]._Control__uid = id
                    added_controls[n].page = self

                    # add to index
                    self._index[id] = added_controls[n]

                    n += 1

    def __handle_mount_unmount(self, added_controls, removed_controls):
        for ctrl in removed_controls:
            ctrl.will_unmount()
        for ctrl in added_controls:
            ctrl.did_mount()

    async def __handle_mount_unmount_async(self, added_controls, removed_controls):
        for ctrl in removed_controls:
            await ctrl.will_unmount_async()
        for ctrl in added_controls:
            await ctrl.did_mount_async()

    def error(self, message=""):
        with self.__lock:
            self._send_command("error", [message])

    async def error_async(self, message=""):
        async with self.__async_lock:
            await self._send_command_async("error", [message])

    def on_event(self, e: Event):
        logging.info(f"page.on_event: {e.target} {e.name} {e.data}")
        with self.__lock:
            if e.target == "page" and e.name == "change":
                self.__on_page_change_event(e.data)

            elif e.target in self._index:
                ce = ControlEvent(e.target, e.name, e.data, self._index[e.target], self)
                handler = self._index[e.target].event_handlers.get(e.name)
                if handler:
                    t = threading.Thread(target=handler, args=(ce,), daemon=True)
                    t.start()

    async def on_event_async(self, e: Event):
        logging.info(f"page.on_event_async: {e.target} {e.name} {e.data}")

        if e.target == "page" and e.name == "change":
            async with self.__async_lock:
                self.__on_page_change_event(e.data)

        elif e.target in self._index:
            ce = ControlEvent(e.target, e.name, e.data, self._index[e.target], self)
            handler = self._index[e.target].event_handlers.get(e.name)
            if handler:
                if is_coroutine(handler):
                    await handler(ce)
                else:
                    handler(ce)

    def __on_page_change_event(self, data):
        for props in json.loads(data):
            id = props["i"]
            if id in self._index:
                for name in props:
                    if name != "i":
                        self._index[id]._set_attr(name, props[name], dirty=False)

    def go(self, route, **kwargs):
        self.route = route if kwargs == {} else route + self.query.post(kwargs)

        self.__on_route_change.get_sync_handler()(
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

    async def go_async(self, route, **kwargs):
        self.route = route if kwargs == {} else route + self.query.post(kwargs)

        await self.__on_route_change.get_handler()(
            ControlEvent(
                target="page",
                name="route_change",
                data=self.route,
                page=self,
                control=self,
            )
        )
        await self.update_async()
        self.query()

    def get_upload_url(self, file_name: str, expires: int):
        r = self._send_command(
            "getUploadUrl", attrs={"file": file_name, "expires": str(expires)}
        )
        if r.error:
            raise Exception(r.error)
        return r.result

    async def get_upload_url_async(self, file_name: str, expires: int):
        r = await self._send_command_async(
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
        authorization=Authorization,
    ):
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
            self.__on_login.get_sync_handler()(
                LoginEvent(error="", error_description="")
            )
        return self.__authorization

    async def login_async(
        self,
        provider: OAuthProvider,
        fetch_user=True,
        fetch_groups=False,
        scope: Optional[List[str]] = None,
        saved_token: Optional[str] = None,
        on_open_authorization_url=None,
        complete_page_html: Optional[str] = None,
        redirect_to_page=False,
        authorization=Authorization,
    ):
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
            result = await self._send_command_async("oauthAuthorize", attrs=auth_attrs)
            if result.error != "":
                raise Exception(result.error)
            if on_open_authorization_url:
                await on_open_authorization_url(authorization_url)
            else:
                await self.launch_url_async(
                    authorization_url, "flet_oauth_signin", web_popup_window=self.web
                )
        else:
            await self.__authorization.dehydrate_token_async(saved_token)
            await self.__on_login.get_handler()(
                LoginEvent(error="", error_description="")
            )
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
        self.__on_login.get_sync_handler()(login_evt)

    async def __on_authorize_async(self, e):
        assert self.__authorization is not None
        d = json.loads(e.data)
        state = d["state"]
        assert state == self.__authorization.state

        if not self.web:
            if self.platform in ["ios", "android"]:
                # close web view on mobile
                await self.close_in_app_web_view_async()
            else:
                # activate desktop window
                await self.window_to_front_async()

        login_evt = LoginEvent(
            error=d["error"], error_description=d["error_description"]
        )
        if login_evt.error == "":
            # perform token request
            code = d["code"]
            assert code not in [None, ""]
            try:
                await self.__authorization.request_token_async(code)
            except Exception as ex:
                login_evt.error = str(ex)
        await self.__on_login.get_handler()(login_evt)

    def logout(self):
        self.__authorization = None
        self.__on_logout.get_sync_handler()(
            ControlEvent(target="page", name="logout", data="", control=self, page=self)
        )

    async def logout_async(self):
        self.__authorization = None
        await self.__on_logout.get_handler()(
            ControlEvent(target="page", name="logout", data="", control=self, page=self)
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

    async def _send_command_async(
        self,
        name: str,
        values: Optional[List[str]] = None,
        attrs: Optional[Dict[str, str]] = None,
    ):
        return await self.__conn.send_command_async(
            self._session_id,
            Command(
                indent=0,
                name=name,
                values=values if values is not None else [],
                attrs=attrs or {},
            ),
        )

    def set_clipboard(self, value: str):
        self.__offstage.clipboard.set_data(value)

    async def set_clipboard_async(self, value: str):
        await self.__offstage.clipboard.set_data_async(value)

    def get_clipboard(self):
        return self.__offstage.clipboard.get_data()

    async def get_clipboard_async(self):
        return await self.__offstage.clipboard.get_data_async()

    def launch_url(
        self,
        url: str,
        web_window_name: Optional[str] = None,
        web_popup_window: bool = False,
        window_width: Optional[int] = None,
        window_height: Optional[int] = None,
    ):
        self.invoke_method(
            "launchUrl",
            self.__get_launch_url_args(
                url=url,
                web_window_name=web_window_name,
                web_popup_window=web_popup_window,
                window_width=window_width,
                window_height=window_height,
            ),
        )

    async def launch_url_async(
        self,
        url: str,
        web_window_name: Optional[str] = None,
        web_popup_window: bool = False,
        window_width: Optional[int] = None,
        window_height: Optional[int] = None,
    ):
        await self.invoke_method_async(
            "launchUrl",
            self.__get_launch_url_args(
                url=url,
                web_window_name=web_window_name,
                web_popup_window=web_popup_window,
                window_width=window_width,
                window_height=window_height,
            ),
        )

    def __get_launch_url_args(
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
        return args

    def can_launch_url(self, url: str):
        args = {"url": url}
        return self.invoke_method("canLaunchUrl", args, wait_for_result=True) == "true"

    async def can_launch_url_async(self, url: str):
        args = {"url": url}
        return (
            await self.invoke_method_async("canLaunchUrl", args, wait_for_result=True)
            == "true"
        )

    def close_in_app_web_view(self):
        self.invoke_method("closeInAppWebView")

    async def close_in_app_web_view_async(self):
        await self.invoke_method_async("closeInAppWebView")

    def window_to_front(self):
        self.invoke_method("windowToFront")

    async def window_to_front_async(self):
        await self.invoke_method_async("windowToFront")

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

    async def invoke_method_async(
        self,
        method_name: str,
        arguments: Optional[Dict[str, str]] = None,
        wait_for_result: bool = False,
    ) -> Optional[str]:
        method_id = uuid.uuid4().hex

        # register callback
        evt: Optional[asyncio.Event] = None
        if wait_for_result:
            evt = asyncio.Event()
            self.__method_calls[method_id] = evt

        # call method
        result = await self._send_command_async(
            "invokeMethod", values=[method_id, method_name], attrs=arguments
        )

        if result.error != "":
            if wait_for_result:
                del self.__method_calls[method_id]
            raise Exception(result.error)

        if not wait_for_result:
            return

        assert evt is not None

        try:
            await asyncio.wait_for(evt.wait(), timeout=5)
        except TimeoutError:
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

    def __on_invoke_method_result(self, e):
        d = json.loads(e.data)
        result = InvokeMethodResults(**d)
        evt = self.__method_calls.pop(result.method_id, None)
        if evt == None:
            return
        self.__method_call_results[evt] = (result.result, result.error)
        evt.set()

    def show_snack_bar(self, snack_bar: SnackBar):
        self.__offstage.snack_bar = snack_bar
        self.__offstage.update()

    async def show_snack_bar_async(self, snack_bar: SnackBar):
        self.__offstage.snack_bar = snack_bar
        await self.__offstage.update_async()

    def window_destroy(self):
        self._set_attr("windowDestroy", "true")
        self.update()

    async def window_destroy_async(self):
        self._set_attr("windowDestroy", "true")
        await self.update_async()

    def window_center(self):
        self._set_attr("windowCenter", str(time.time()))
        self.update()

    async def window_center_async(self):
        self._set_attr("windowCenter", str(time.time()))
        await self.update_async()

    def window_close(self):
        self._set_attr("windowClose", str(time.time()))
        self.update()

    async def window_close_async(self):
        self._set_attr("windowClose", str(time.time()))
        await self.update_async()

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

    def __set_design(self, value: PageDesignString):
        self._set_attr("design", value)

    # fonts
    @property
    def fonts(self) -> Optional[Dict[str, str]]:
        return self.__fonts

    @fonts.setter
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
    def controls(self, value: Optional[List[Control]]):
        self.__default_view.controls = value if value is not None else []

    # appbar
    @property
    def appbar(self) -> Optional[AppBar]:
        return self.__default_view.appbar

    @appbar.setter
    def appbar(self, value: Optional[AppBar]):
        self.__default_view.appbar = value

    # navigation_bar
    @property
    def navigation_bar(self) -> Optional[NavigationBar]:
        return self.__default_view.navigation_bar

    @navigation_bar.setter
    def navigation_bar(self, value: Optional[NavigationBar]):
        self.__default_view.navigation_bar = value

    # floating_action_button
    @property
    def floating_action_button(self) -> Optional[FloatingActionButton]:
        return self.__default_view.floating_action_button

    @floating_action_button.setter
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
    def splash(self, value: Optional[Control]):
        self.__offstage.splash = value

    # banner
    @property
    def banner(self) -> Optional[Banner]:
        return self.__offstage.banner

    @banner.setter
    def banner(self, value: Optional[Banner]):
        self.__offstage.banner = value

    # snack_bar
    @property
    def snack_bar(self) -> Optional[SnackBar]:
        return self.__offstage.snack_bar

    @snack_bar.setter
    def snack_bar(self, value: Optional[SnackBar]):
        self.__offstage.snack_bar = value

    # dialog
    @property
    def dialog(self) -> Optional[Control]:
        return self.__offstage.dialog

    @dialog.setter
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

    def __set_theme_mode(self, value: ThemeModeString):
        self._set_attr("themeMode", value)

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
    def window_left(self, value: OptionalNumber):
        self._set_attr("windowLeft", value)

    # window_max_width
    @property
    def window_max_width(self) -> OptionalNumber:
        return self._get_attr("windowMaxWidth")

    @window_max_width.setter
    def window_max_width(self, value: OptionalNumber):
        self._set_attr("windowMaxWidth", value)

    # window_max_height
    @property
    def window_max_height(self) -> OptionalNumber:
        return self._get_attr("windowMaxHeight")

    @window_max_height.setter
    def window_max_height(self, value: OptionalNumber):
        self._set_attr("windowMaxHeight", value)

    # window_min_width
    @property
    def window_min_width(self) -> OptionalNumber:
        return self._get_attr("windowMinWidth")

    @window_min_width.setter
    def window_min_width(self, value: OptionalNumber):
        self._set_attr("windowMinWidth", value)

    # window_min_height
    @property
    def window_min_height(self) -> OptionalNumber:
        return self._get_attr("windowMinHeight")

    @window_min_height.setter
    def window_min_height(self, value: OptionalNumber):
        self._set_attr("windowMinHeight", value)

    # window_opacity
    @property
    def window_opacity(self) -> OptionalNumber:
        return self._get_attr("windowOpacity", data_type="float", def_value=1)

    @window_opacity.setter
    def window_opacity(self, value: OptionalNumber):
        self._set_attr("windowOpacity", value)

    # window_maximized
    @property
    def window_maximized(self) -> Optional[bool]:
        return self._get_attr("windowMaximized", data_type="bool", def_value=False)

    @window_maximized.setter
    def window_maximized(self, value: Optional[bool]):
        self._set_attr("windowMaximized", value)

    # window_minimized
    @property
    def window_minimized(self) -> Optional[bool]:
        return self._get_attr("windowMinimized", data_type="bool", def_value=False)

    @window_minimized.setter
    def window_minimized(self, value: Optional[bool]):
        self._set_attr("windowMinimized", value)

    # window_minimizable
    @property
    def window_minimizable(self) -> Optional[bool]:
        return self._get_attr("windowMinimizable", data_type="bool", def_value=True)

    @window_minimizable.setter
    def window_minimizable(self, value: Optional[bool]):
        self._set_attr("windowMinimizable", value)

    # window_maximizable
    @property
    def window_maximizable(self) -> Optional[bool]:
        return self._get_attr("windowMaximizable", data_type="bool", def_value=True)

    @window_maximizable.setter
    def window_maximizable(self, value: Optional[bool]):
        self._set_attr("windowMaximizable", value)

    # window_resizable
    @property
    def window_resizable(self) -> Optional[bool]:
        return self._get_attr("windowResizable", data_type="bool", def_value=True)

    @window_resizable.setter
    def window_resizable(self, value: Optional[bool]):
        self._set_attr("windowResizable", value)

    # window_movable
    @property
    def window_movable(self) -> Optional[bool]:
        return self._get_attr("windowMovable", data_type="bool", def_value=True)

    @window_movable.setter
    def window_movable(self, value: Optional[bool]):
        self._set_attr("windowMovable", value)

    # window_full_screen
    @property
    def window_full_screen(self) -> Optional[bool]:
        return self._get_attr("windowFullScreen", data_type="bool", def_value=False)

    @window_full_screen.setter
    def window_full_screen(self, value: Optional[bool]):
        self._set_attr("windowFullScreen", value)

    # window_always_on_top
    @property
    def window_always_on_top(self) -> Optional[bool]:
        return self._get_attr("windowAlwaysOnTop", data_type="bool", def_value=False)

    @window_always_on_top.setter
    def window_always_on_top(self, value: Optional[bool]):
        self._set_attr("windowAlwaysOnTop", value)

    # window_prevent_close
    @property
    def window_prevent_close(self) -> Optional[bool]:
        return self._get_attr("windowPreventClose", data_type="bool", def_value=False)

    @window_prevent_close.setter
    def window_prevent_close(self, value: Optional[bool]):
        self._set_attr("windowPreventClose", value)

    # window_title_bar_hidden
    @property
    def window_title_bar_hidden(self) -> Optional[bool]:
        return self._get_attr("windowTitleBarHidden", data_type="bool", def_value=False)

    @window_title_bar_hidden.setter
    def window_title_bar_hidden(self, value: Optional[bool]):
        self._set_attr("windowTitleBarHidden", value)

    # window_title_bar_buttons_hidden
    @property
    def window_title_bar_buttons_hidden(self) -> Optional[bool]:
        return self._get_attr(
            "windowTitleBarButtonsHidden", data_type="bool", def_value=False
        )

    @window_title_bar_buttons_hidden.setter
    def window_title_bar_buttons_hidden(self, value: Optional[bool]):
        self._set_attr("windowTitleBarButtonsHidden", value)

    # window_skip_task_bar
    @property
    def window_skip_task_bar(self) -> Optional[bool]:
        return self._get_attr("windowSkipTaskBar", data_type="bool", def_value=False)

    @window_skip_task_bar.setter
    def window_skip_task_bar(self, value: Optional[bool]):
        self._set_attr("windowSkipTaskBar", value)

    # window_frameless
    @property
    def window_frameless(self) -> Optional[bool]:
        return self._get_attr("windowFrameless", data_type="bool", def_value=False)

    @window_frameless.setter
    def window_frameless(self, value: Optional[bool]):
        self._set_attr("windowFrameless", value)

    # window_progress_bar
    @property
    def window_progress_bar(self) -> OptionalNumber:
        return self._get_attr("windowProgressBar")

    @window_progress_bar.setter
    def window_progress_bar(self, value: OptionalNumber):
        self._set_attr("windowProgressBar", value)

    # window_focused
    @property
    def window_focused(self) -> Optional[bool]:
        return self._get_attr("windowFocused", data_type="bool", def_value=True)

    @window_focused.setter
    def window_focused(self, value: Optional[bool]):
        self._set_attr("windowFocused", value)

    # window_visible
    @property
    def window_visible(self) -> Optional[bool]:
        return self._get_attr("windowVisible", data_type="bool")

    @window_visible.setter
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
    def splash(self, value: Optional[Control]):
        self.__splash = value

    # banner
    @property
    def banner(self) -> Optional[Banner]:
        return self.__banner

    @banner.setter
    def banner(self, value: Optional[Banner]):
        self.__banner = value

    # snack_bar
    @property
    def snack_bar(self) -> Optional[SnackBar]:
        return self.__snack_bar

    @snack_bar.setter
    def snack_bar(self, value: Optional[SnackBar]):
        self.__snack_bar = value

    # dialog
    @property
    def dialog(self) -> Optional[Control]:
        return self.__dialog

    @dialog.setter
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
