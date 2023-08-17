import asyncio
import json
import logging
import traceback
from typing import List, Optional

import flet
from fastapi import WebSocket, WebSocketDisconnect
from flet_core.connection import Connection
from flet_core.event import Event
from flet_core.local_connection import LocalConnection
from flet_core.page import Page
from flet_core.protocol import (
    ClientActions,
    ClientMessage,
    Command,
    CommandEncoder,
    PageCommandResponsePayload,
    PageCommandsBatchResponsePayload,
    RegisterWebClientRequestPayload,
)
from flet_core.utils import is_coroutine, random_string
from flet_runtime.uploads import build_upload_url

logger = logging.getLogger(flet.__name__)


class SessionManager:
    def __init__(self):
        self.sessions: dict[str, Page] = {}

    def create(self, session_id: str, conn: Page):
        logger.info(f"New session created: {session_id}")
        self.sessions[session_id] = conn

    async def reconnect(self, session_id: str, conn: Connection):
        logger.info(f"Session reconnected: {session_id}")
        if session_id in self.sessions:
            await self.sessions[session_id]._connect(conn)

    async def disconnect(self, session_id: str):
        logger.info(f"Session disconnected: {session_id}")
        if session_id in self.sessions:
            await self.sessions[session_id]._disconnect()

    def delete(self, session_id: str):
        logger.info(f"Delete session: {session_id}")
        pass


session_manager = SessionManager()


class FletApp(LocalConnection):
    def __init__(self, session_handler, upload_path: Optional[str] = None):
        super().__init__()
        logger.info("New FletConnection")

        self.__session_handler = session_handler
        self.__upload_path = upload_path

    async def handle(self, websocket: WebSocket):
        self.__websocket = websocket
        await self.__websocket.accept()
        await self.__receive_loop()

    async def __on_event(self, e):
        if e.sessionID in session_manager.sessions:
            await session_manager.sessions[e.sessionID].on_event_async(
                Event(e.eventTarget, e.eventName, e.eventData)
            )
            if e.eventTarget == "page" and e.eventName == "close":
                logger.info(f"Session closed: {e.sessionID}")
                session_manager.delete(e.sessionID)

    async def __on_session_created(self, session_data):
        logger.info(f"Start session: {session_data.sessionID}")
        try:
            assert self.__session_handler is not None
            if is_coroutine(self.__session_handler):
                await self.__session_handler(self.page)
            else:
                self.__session_handler(self.page)
        except Exception as e:
            print(
                f"Unhandled error processing page session {self.page.session_id}:",
                traceback.format_exc(),
            )
            await self.page.error_async(
                f"There was an error while processing your request: {e}"
            )

    async def __receive_loop(self):
        try:
            while True:
                await self.__on_message(await self.__websocket.receive_text())
        except WebSocketDisconnect:
            if self.page:
                await session_manager.disconnect(self.page.session_id)

    async def __on_message(self, data: str):
        logger.debug(f"_on_message: {data}")
        msg_dict = json.loads(data)
        msg = ClientMessage(**msg_dict)
        if msg.action == ClientActions.REGISTER_WEB_CLIENT:
            self._client_details = RegisterWebClientRequestPayload(**msg.payload)

            new_session = True
            if (
                not self._client_details.sessionId
                or self._client_details.sessionId not in session_manager.sessions
            ):
                # generate session ID
                self._client_details.sessionId = random_string(16)

                # create new Page object
                self.page = Page(self, self._client_details.sessionId)
                self.page._set_attr("route", self._client_details.pageRoute, False)
                self.page._set_attr("pwa", self._client_details.isPWA, False)
                self.page._set_attr("web", self._client_details.isWeb, False)
                self.page._set_attr("debug", self._client_details.isDebug, False)
                self.page._set_attr("platform", self._client_details.platform, False)
                self.page._set_attr(
                    "platformBrightness", self._client_details.platformBrightness, False
                )
                self.page._set_attr("width", self._client_details.pageWidth, False)
                self.page._set_attr("height", self._client_details.pageHeight, False)
                self.page._set_attr(
                    "windowWidth", self._client_details.windowWidth, False
                )
                self.page._set_attr(
                    "windowHeight", self._client_details.windowHeight, False
                )
                self.page._set_attr("windowTop", self._client_details.windowTop, False)
                self.page._set_attr(
                    "windowLeft", self._client_details.windowLeft, False
                )

                # TODO
                self.page._set_attr(
                    "clientIP",
                    self.__websocket.client.host if self.__websocket.client else "",
                    False,
                )
                self.page._set_attr(
                    "clientUserAgent",
                    self.__websocket.headers["user-agent"]
                    if "user-agent" in self.__websocket.headers
                    else "",
                    False,
                )

                # register session
                session_manager.create(self._client_details.sessionId, self.page)
            else:
                # existing session
                logger.info(
                    f"Existing session requested: {self._client_details.sessionId}"
                )
                self.page = session_manager.sessions[self._client_details.sessionId]
                new_session = False

            # send register response
            controls = {}
            self.page.serialize_to_json(controls)
            await self.__send(
                self._create_register_web_client_response(controls=controls)
            )

            # start session
            if new_session:
                asyncio.create_task(
                    self.__on_session_created(self._create_session_handler_arg())
                )
            else:
                await session_manager.reconnect(self._client_details.sessionId, self)

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
        assert self.__upload_path, "upload_path should be specified to enable uploads"
        return (
            build_upload_url(self.__upload_path, attrs["file"], int(attrs["expires"])),
            None,
        )

    async def send_command_async(self, session_id: str, command: Command):
        result, message = self._process_command(command)
        if message:
            await self.__send(message)
        return PageCommandResponsePayload(result=result, error="")

    async def send_commands_async(self, session_id: str, commands: List[Command]):
        results = []
        messages = []
        for command in commands:
            result, message = self._process_command(command)
            if command.name in ["add", "get"]:
                results.append(result)
            if message:
                messages.append(message)
        if len(messages) > 0:
            await self.__send(
                ClientMessage(ClientActions.PAGE_CONTROLS_BATCH, messages)
            )
        return PageCommandsBatchResponsePayload(results=results, error="")

    async def __send(self, message: ClientMessage):
        j = json.dumps(message, cls=CommandEncoder, separators=(",", ":"))
        logger.debug(f"__send: {j}")
        await self.__websocket.send_text(j)
