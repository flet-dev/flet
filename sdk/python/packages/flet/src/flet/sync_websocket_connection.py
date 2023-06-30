import json
import logging
import threading
import uuid
from time import sleep
from typing import List, Optional

import flet
from flet import constants
from flet.reconnecting_websocket import ReconnectingWebSocket
from flet_core.connection import Connection
from flet_core.protocol import (
    Actions,
    Command,
    CommandEncoder,
    Message,
    PageCommandRequestPayload,
    PageCommandResponsePayload,
    PageCommandsBatchRequestPayload,
    PageCommandsBatchResponsePayload,
    PageEventPayload,
    PageSessionCreatedPayload,
    RegisterHostClientRequestPayload,
    RegisterHostClientResponsePayload,
)

logger = logging.getLogger(flet.__name__)


class SyncWebSocketConnection(Connection):
    def __init__(
        self,
        server_address: str,
        page_name: str,
        assets_dir: Optional[str],
        token: Optional[str],
        on_event=None,
        on_session_created=None,
    ):
        super().__init__()
        self.page_name = page_name
        self.__host_client_id: Optional[str] = None
        self.__token = token
        self.__assets_dir = assets_dir
        self.__server_address = server_address
        self.__ws = ReconnectingWebSocket(
            self._get_ws_url(server_address),
            on_connect=self.__on_ws_connect,
            on_message=self.__on_ws_message,
        )
        self.__ws_callbacks = {}
        self.__on_event = on_event
        self.__on_session_created = on_session_created

    def connect(self):
        self.__connected = threading.Event()
        self.__ws.connect()
        for n in range(0, constants.CONNECT_TIMEOUT_SECONDS):
            if not self.__connected.is_set():
                sleep(1)
        if not self.__connected.is_set():
            self.__ws.close()
            raise Exception(
                f"Could not connected to Flet server in {constants.CONNECT_TIMEOUT_SECONDS} seconds."
            )

    def __on_ws_connect(self):
        payload = RegisterHostClientRequestPayload(
            hostClientID=self.__host_client_id,
            pageName=self.page_name,
            assetsDir=self.__assets_dir,
            authToken=self.__token,
            permissions=None,
        )
        response = self._send_message_with_result(Actions.REGISTER_HOST_CLIENT, payload)
        register_result = RegisterHostClientResponsePayload(**response)
        self.__host_client_id = register_result.hostClientID
        self.page_name = register_result.pageName
        self.page_url = self.__server_address.rstrip("/")
        if self.page_name != constants.INDEX_PAGE:
            self.page_url += f"/{self.page_name}"
        self.__connected.set()

    def __on_ws_message(self, data):
        logger.debug(f"_on_message: {data}")
        msg_dict = json.loads(data)
        msg = Message(**msg_dict)
        if msg.id:
            # callback
            evt = self.__ws_callbacks[msg.id][0]
            self.__ws_callbacks[msg.id] = (None, msg.payload)
            evt.set()
        elif msg.action == Actions.PAGE_EVENT_TO_HOST:
            if self.__on_event is not None:
                th = threading.Thread(
                    target=self.__on_event,
                    args=(
                        self,
                        PageEventPayload(**msg.payload),
                    ),
                    daemon=True,
                )
                th.start()
                # self._on_event(self, PageEventPayload(**msg.payload))
        elif msg.action == Actions.SESSION_CREATED:
            if self.__on_session_created is not None:
                th = threading.Thread(
                    target=self.__on_session_created,
                    args=(
                        self,
                        PageSessionCreatedPayload(**msg.payload),
                    ),
                    daemon=True,
                )
                th.start()
        else:
            # it's something else
            print(msg.payload)

    def send_command(self, session_id: str, command: Command):
        assert self.page_name is not None
        payload = PageCommandRequestPayload(self.page_name, session_id, command)
        response = self._send_message_with_result(
            Actions.PAGE_COMMAND_FROM_HOST, payload
        )
        result = PageCommandResponsePayload(**response)
        if result.error:
            raise Exception(result.error)
        return result

    def send_commands(self, session_id: str, commands: List[Command]):
        assert self.page_name is not None
        payload = PageCommandsBatchRequestPayload(self.page_name, session_id, commands)
        response = self._send_message_with_result(
            Actions.PAGE_COMMANDS_BATCH_FROM_HOST, payload
        )
        result = PageCommandsBatchResponsePayload(**response)
        if result.error:
            raise Exception(result.error)
        return result

    def _send_message_with_result(self, action_name, payload):
        msg_id = uuid.uuid4().hex
        msg = Message(msg_id, action_name, payload)
        j = json.dumps(msg, cls=CommandEncoder, separators=(",", ":"))
        logger.debug(f"_send_message_with_result: {j}")
        evt = threading.Event()
        self.__ws_callbacks[msg_id] = (evt, None)
        self.__ws.send(j)
        evt.wait()
        return self.__ws_callbacks.pop(msg_id)[1]

    def close(self):
        logger.debug("Closing connection...")
        if self.__ws is not None:
            self.__ws.close()
