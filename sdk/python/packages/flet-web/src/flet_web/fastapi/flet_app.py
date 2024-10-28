import asyncio
import copy
import json
import logging
import os
import traceback
from datetime import datetime, timedelta, timezone
from typing import Any, Dict, List, Optional

import flet_web.fastapi as flet_fastapi
from fastapi import WebSocket, WebSocketDisconnect
from flet.core.event import Event
from flet.core.local_connection import LocalConnection
from flet.core.page import Page, PageDisconnectedException
from flet.core.protocol import (
    ClientActions,
    ClientMessage,
    Command,
    CommandEncoder,
    PageCommandResponsePayload,
    PageCommandsBatchResponsePayload,
    RegisterWebClientRequestPayload,
)
from flet.core.pubsub.pubsub_hub import PubSubHub
from flet.utils import random_string, sha1
from flet_web.fastapi.flet_app_manager import app_manager
from flet_web.fastapi.oauth_state import OAuthState
from flet_web.uploads import build_upload_url

logger = logging.getLogger(flet_fastapi.__name__)

DEFAULT_FLET_SESSION_TIMEOUT = 3600
DEFAULT_FLET_OAUTH_STATE_TIMEOUT = 600


class FletApp(LocalConnection):
    def __init__(
        self,
        loop: asyncio.AbstractEventLoop,
        session_handler,
        session_timeout_seconds: int = DEFAULT_FLET_SESSION_TIMEOUT,
        oauth_state_timeout_seconds: int = DEFAULT_FLET_OAUTH_STATE_TIMEOUT,
        upload_endpoint_path: Optional[str] = None,
        secret_key: Optional[str] = None,
    ):
        """
        Handle Flet app WebSocket connections.

        Parameters:

        * `session_handler` (Coroutine) - application entry point - an async method called for newly connected user. Handler coroutine must have 1 parameter: `page` - `Page` instance.
        * `session_timeout_seconds` (int, optional) - session lifetime, in seconds, after user disconnected.
        * `oauth_state_timeout_seconds` (int, optional) - OAuth state lifetime, in seconds, which is a maximum allowed time between starting OAuth flow and redirecting to OAuth callback URL.
        * `upload_endpoint_path` (str, optional) - absolute URL of upload endpoint, e.g. `/upload`.
        * `secret_key` (str, optional) - secret key to sign upload requests.
        """
        super().__init__()
        self.__id = random_string(8)
        logger.info(f"New FletApp: {self.__id}")

        self.__page = None
        self.__loop = loop
        self.__session_handler = session_handler
        self.__session_timeout_seconds = session_timeout_seconds
        self.__oauth_state_timeout_seconds = oauth_state_timeout_seconds

        env_session_timeout_seconds = os.getenv("FLET_SESSION_TIMEOUT")
        if env_session_timeout_seconds:
            self.__session_timeout_seconds = int(env_session_timeout_seconds)

        env_oauth_state_timeout_seconds = os.getenv("FLET_OAUTH_STATE_TIMEOUT")
        if env_oauth_state_timeout_seconds:
            self.__oauth_state_timeout_seconds = int(env_oauth_state_timeout_seconds)

        self.__upload_endpoint_path = upload_endpoint_path
        self.__secret_key = secret_key

    async def handle(self, websocket: WebSocket):
        """
        Handle WebSocket connection.

        Parameters:

        * `websocket` (WebSocket) - Websocket instance.
        """
        self.__websocket = websocket

        self.client_ip = (
            self.__websocket.client.host if self.__websocket.client else ""
        ).split(":")[0]
        self.client_user_agent = (
            self.__websocket.headers["user-agent"]
            if "user-agent" in self.__websocket.headers
            else ""
        )

        self.pubsubhub = app_manager.get_pubsubhub(
            self.__session_handler, loop=self.__loop
        )
        self.page_url = str(websocket.url).rsplit("/", 1)[0]
        self.page_name = websocket.url.path.rsplit("/", 1)[0].lstrip("/")

        if not self.__upload_endpoint_path:
            self.__upload_endpoint_path = (
                f"{'' if self.page_name == '' else '/'}{self.page_name}/upload"
            )

        await self.__websocket.accept()
        self.__send_queue = asyncio.Queue()
        st = asyncio.create_task(self.__send_loop())
        await self.__receive_loop()
        st.cancel()

    async def __on_event(self, e):
        session = await app_manager.get_session(
            self.__get_unique_session_id(e.sessionID)
        )
        if session is not None:
            try:
                await session.on_event_async(
                    Event(e.eventTarget, e.eventName, e.eventData)
                )
            except PageDisconnectedException:
                logger.debug(
                    f"Event handler attempted to update disconnected page: {e.sessionID}"
                )
            if e.eventTarget == "page" and e.eventName == "close":
                logger.info(f"Session closed: {e.sessionID}")
                await app_manager.delete_session(
                    self.__get_unique_session_id(e.sessionID)
                )

    async def __on_session_created(self, session_data):
        logger.info(f"Start session: {session_data.sessionID}")
        session_id = session_data.sessionID
        try:
            assert self.__session_handler is not None
            if asyncio.iscoroutinefunction(self.__session_handler):
                await self.__session_handler(self.__page)
            else:
                # run in thread pool
                await asyncio.get_running_loop().run_in_executor(
                    app_manager.executor, self.__session_handler, self.__page
                )
        except PageDisconnectedException:
            logger.debug(
                f"Session handler attempted to update disconnected page: {session_id}"
            )
        except BrokenPipeError:
            logger.info(f"Session handler terminated: {session_id}")
        except Exception as e:
            print(
                f"Unhandled error processing page session {session_id}:",
                traceback.format_exc(),
            )
            assert self.__page
            self.__page.error(f"There was an error while processing your request: {e}")

    async def __send_loop(self):
        assert self.__websocket
        assert self.__send_queue
        while True:
            message = await self.__send_queue.get()
            try:
                await self.__websocket.send_text(message)
            except Exception:
                # re-enqueue the message to repeat it when re-connected
                self.__send_queue.put_nowait(message)
                raise

    async def __receive_loop(self):
        assert self.__websocket
        try:
            while True:
                await self.__on_message(await self.__websocket.receive_text())
        except Exception as e:
            if not isinstance(e, WebSocketDisconnect):
                logger.warning(f"Receive loop error: {e}")
            if self.__page:
                await app_manager.disconnect_session(
                    self.__get_unique_session_id(self.__page.session_id),
                    self.__session_timeout_seconds,
                )
        self.__websocket = None
        self.__send_queue = None

    async def __on_message(self, data: str):
        logger.debug(f"_on_message: {data}")
        msg_dict = json.loads(data)
        msg = ClientMessage(**msg_dict)
        if msg.action == ClientActions.REGISTER_WEB_CLIENT:
            self._client_details = RegisterWebClientRequestPayload(**msg.payload)

            new_session = True
            if (
                not self._client_details.sessionId
                or await app_manager.get_session(
                    self.__get_unique_session_id(self._client_details.sessionId)
                )
                is None
            ):
                # generate session ID
                self._client_details.sessionId = random_string(16)

                # create new Page object
                self.__page = Page(
                    self,
                    self._client_details.sessionId,
                    executor=app_manager.executor,
                    loop=asyncio.get_running_loop(),
                )

                # register session
                await app_manager.add_session(
                    self.__get_unique_session_id(self._client_details.sessionId),
                    self.__page,
                )
            else:
                # existing session
                logger.info(
                    f"Existing session requested: {self._client_details.sessionId}"
                )
                self.__page = await app_manager.get_session(
                    self.__get_unique_session_id(self._client_details.sessionId)
                )
                new_session = False

            # update page props
            assert self.__page
            original_route = self.__page.route
            self.__page._set_attr("route", self._client_details.pageRoute, False)
            self.__page._set_attr("pwa", self._client_details.isPWA, False)
            self.__page._set_attr("web", self._client_details.isWeb, False)
            self.__page._set_attr("debug", self._client_details.isDebug, False)
            self.__page._set_attr("platform", self._client_details.platform, False)
            self.__page._set_attr(
                "platformBrightness", self._client_details.platformBrightness, False
            )
            self.__page._set_attr("media", self._client_details.media, False)
            self.__page._set_attr("width", self._client_details.pageWidth, False)
            self.__page._set_attr("height", self._client_details.pageHeight, False)
            self.__page._set_attr(
                "windowWidth", self._client_details.windowWidth, False
            )
            self.__page._set_attr(
                "windowHeight", self._client_details.windowHeight, False
            )
            self.__page._set_attr("windowTop", self._client_details.windowTop, False)
            self.__page._set_attr("windowLeft", self._client_details.windowLeft, False)
            self.__page._set_attr("clientIP", self.client_ip, False)
            self.__page._set_attr("clientUserAgent", self.client_user_agent, False)

            p = self.__page.snapshot.get("page")
            if not p:
                p = {
                    "i": "page",
                    "t": "page",
                    "p": "",
                    "c": [],
                }
                self.__page.snapshot["page"] = p
            self.__page.copy_attrs(p)

            # send register response
            self.__send(
                self._create_register_web_client_response(controls=self.__page.snapshot)
            )

            # start session
            if new_session:
                asyncio.create_task(
                    self.__on_session_created(self._create_session_handler_arg())
                )
            else:
                await app_manager.reconnect_session(
                    self.__get_unique_session_id(self._client_details.sessionId), self
                )

                if original_route != self.__page.route:
                    self.__page.go(self.__page.route)

        elif msg.action == ClientActions.PAGE_EVENT_FROM_WEB:
            if self.__on_event is not None:
                asyncio.create_task(
                    self.__on_event(self._create_page_event_handler_arg(msg))
                )

        elif msg.action == ClientActions.UPDATE_CONTROL_PROPS:
            if self.__on_event is not None:
                asyncio.create_task(
                    self.__on_event(self._create_update_control_props_handler_arg(msg))
                )
        else:
            # it's something else
            raise Exception(f'Unknown message "{msg.action}": {msg.payload}')

    def _process_get_upload_url_command(self, attrs):
        assert len(attrs) == 2, '"getUploadUrl" command has wrong number of attrs'
        assert (
            self.__upload_endpoint_path
        ), "upload_path should be specified to enable uploads"
        return (
            build_upload_url(
                self.__upload_endpoint_path,
                attrs["file"],
                int(attrs["expires"]),
                self.__secret_key,
            ),
            None,
        )

    def __process_oauth_authorize_command(self, attrs: Dict[str, Any]):
        state_id = attrs["state"]
        state = OAuthState(
            session_id=self.__get_unique_session_id(self._client_details.sessionId),
            expires_at=datetime.now(timezone.utc)
            + timedelta(seconds=self.__oauth_state_timeout_seconds),
            complete_page_html=attrs.get("completePageHtml", None),
            complete_page_url=attrs.get("completePageUrl", None),
        )
        app_manager.store_state(state_id, state)
        return (
            "",
            None,
        )

    def _process_add_command(self, command: Command):
        assert self.__page
        result, message = super()._process_add_command(command)
        if message:
            for oc in message.payload.controls:
                control = copy.deepcopy(oc)
                id = control["i"]
                pid = control["p"]
                parent = self.__page.snapshot[pid]
                assert parent, f"parent control not found: {pid}"
                if id not in parent["c"]:
                    if "at" in control:
                        parent["c"].insert(int(control["at"]), id)
                    else:
                        parent["c"].append(id)
                self.__page.snapshot[id] = control
        return result, message

    def _process_set_command(self, values, attrs):
        assert self.__page
        result, message = super()._process_set_command(values, attrs)
        control = self.__page.snapshot.get(values[0])
        if control:
            for k, v in attrs.items():
                control[k] = v
        return result, message

    def _process_remove_command(self, values):
        assert self.__page
        result, message = super()._process_remove_command(values)
        for id in values:
            control = self.__page.snapshot.get(id)
            assert (
                control is not None
            ), f"_process_remove_command: control with ID '{id}' not found."
            for cid in self.__get_all_descendant_ids(id):
                self.__page.snapshot.pop(cid, None)
            # delete control itself
            self.__page.snapshot.pop(id, None)
            # remove id from parent
            parent = self.__page.snapshot.get(control["p"])
            if parent:
                parent["c"].remove(id)
        return result, message

    def _process_clean_command(self, values):
        assert self.__page
        result, message = super()._process_clean_command(values)
        for id in values:
            for cid in self.__get_all_descendant_ids(id):
                self.__page.snapshot.pop(cid, None)
        return result, message

    def __get_all_descendant_ids(self, id):
        assert self.__page
        ids = []
        control = self.__page.snapshot.get(id)
        if control:
            for cid in control["c"]:
                ids.append(cid)
                ids.extend(self.__get_all_descendant_ids(cid))
        return ids

    def send_command(self, session_id: str, command: Command):
        if command.name == "oauthAuthorize":
            result, message = self.__process_oauth_authorize_command(command.attrs)
        else:
            result, message = self._process_command(command)
        if message:
            self.__send(message)
        return PageCommandResponsePayload(result=result, error="")

    def send_commands(self, session_id: str, commands: List[Command]):
        results = []
        messages = []
        for command in commands:
            if command.name == "oauthAuthorize":
                result, message = self.__process_oauth_authorize_command(command.attrs)
            else:
                result, message = self._process_command(command)
            if command.name in ["add", "get"]:
                results.append(result)
            if message:
                messages.append(message)
        if len(messages) > 0:
            self.__send(ClientMessage(ClientActions.PAGE_CONTROLS_BATCH, messages))
        return PageCommandsBatchResponsePayload(results=results, error="")

    def __send(self, message: ClientMessage):
        m = json.dumps(message, cls=CommandEncoder, separators=(",", ":"))
        logger.debug(f"__send: {m}")
        if self.__send_queue:
            self.__loop.call_soon_threadsafe(self.__send_queue.put_nowait, m)

    def _get_next_control_id(self):
        assert self.__page
        return self.__page.get_next_control_id()

    def __get_unique_session_id(self, session_id: str):
        client_hash = sha1(f"{self.client_ip}{self.client_user_agent}")
        return f"{self.page_name}_{session_id}_{client_hash}"

    def dispose(self):
        logger.info(f"Disposing FletApp: {self.__id}")
        self.__page = None
