import asyncio
import json
import logging
import traceback
from typing import List

import flet
from fastapi import WebSocket, WebSocketDisconnect
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

logger = logging.getLogger(flet.__name__)


class SessionManager:
    def __init__(self):
        self.sessions: dict[str, Page] = {}

    def create(self, session_id: str, conn: Page):
        logger.info(f"New session created: {session_id}")
        self.sessions[session_id] = conn

    def disconnect(self, session_id: str):
        logger.info(f"Session disconnected: {session_id}")
        # self.active_connections.remove(websocket)

    def delete(self, session_id: str):
        logger.info(f"Delete session: {session_id}")
        pass


manager = SessionManager()


class FletConnection(LocalConnection):
    def __init__(self, websocket: WebSocket, target):
        super().__init__()
        self.__websocket = websocket
        self.__target = target

    async def accept(self):
        await self.__websocket.accept()
        await self.__receive_loop()

    async def __on_event(self, e):
        if e.sessionID in manager.sessions:
            await manager.sessions[e.sessionID].on_event_async(
                Event(e.eventTarget, e.eventName, e.eventData)
            )
            if e.eventTarget == "page" and e.eventName == "close":
                logger.info(f"Session closed: {e.sessionID}")
                manager.delete(e.sessionID)

    async def __on_session_created(self, session_data):
        logger.info(f"Start session: {session_data.sessionID}")
        try:
            assert self.__target is not None
            if is_coroutine(self.__target):
                await self.__target(self.page)
            else:
                self.__target(self.page)
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
                manager.disconnect(self.page.session_id)

    async def __on_message(self, data: str):
        logger.debug(f"_on_message: {data}")
        msg_dict = json.loads(data)
        msg = ClientMessage(**msg_dict)
        if msg.action == ClientActions.REGISTER_WEB_CLIENT:
            self._client_details = RegisterWebClientRequestPayload(**msg.payload)

            new_session = True
            if (
                not self._client_details.sessionId
                or self._client_details.sessionId not in manager.sessions
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
                self.page._set_attr("clientIP", "", False)
                self.page._set_attr("clientUserAgent", "", False)

                # register session
                manager.create(self._client_details.sessionId, self.page)
            else:
                logger.info(
                    f"Existing session requested: {self._client_details.sessionId}"
                )
                self.page = manager.sessions[self._client_details.sessionId]
                new_session = False

            # send register response
            await self.__send(self._create_register_web_client_response())

            # start session
            if new_session and self.__on_session_created is not None:
                asyncio.create_task(
                    self.__on_session_created(self._create_session_handler_arg())
                )

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
