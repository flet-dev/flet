import logging
import threading
import uuid

from flet.protocol import *
from flet.pubsub import PubSubHub
from flet.reconnecting_websocket import ReconnectingWebSocket


class Connection:
    def __init__(self, ws: ReconnectingWebSocket):
        self._ws = ws
        self._ws.on_message = self._on_message
        self._ws_callbacks = {}
        self._on_event = None
        self._on_session_created = None
        self.host_client_id: Optional[str] = None
        self.page_name: Optional[str] = None
        self.page_url: Optional[str] = None
        self.sessions = {}
        self.pubsubhub = PubSubHub()

    @property
    def on_event(self):
        return self._on_event

    @on_event.setter
    def on_event(self, handler):
        self._on_event = handler

    @property
    def on_session_created(self):
        return self._on_session_created

    @on_session_created.setter
    def on_session_created(self, handler):
        self._on_session_created = handler

    def _on_message(self, data):
        logging.debug(f"_on_message: {data}")
        msg_dict = json.loads(data)
        msg = Message(**msg_dict)
        if msg.id:
            # callback
            evt = self._ws_callbacks[msg.id][0]
            self._ws_callbacks[msg.id] = (None, msg.payload)
            evt.set()
        elif msg.action == Actions.PAGE_EVENT_TO_HOST:
            if self._on_event is not None:
                th = threading.Thread(
                    target=self._on_event,
                    args=(
                        self,
                        PageEventPayload(**msg.payload),
                    ),
                    daemon=True,
                )
                th.start()
                # self._on_event(self, PageEventPayload(**msg.payload))
        elif msg.action == Actions.SESSION_CREATED:
            if self._on_session_created is not None:
                th = threading.Thread(
                    target=self._on_session_created,
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

    def register_host_client(
        self,
        host_client_id: Optional[str],
        page_name: str,
        is_app: bool,
        update: bool,
        auth_token: Optional[str],
        permissions: Optional[str],
    ):
        payload = RegisterHostClientRequestPayload(
            host_client_id, page_name, is_app, update, auth_token, permissions
        )
        response = self._send_message_with_result(Actions.REGISTER_HOST_CLIENT, payload)
        return RegisterHostClientResponsePayload(**response)

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
        logging.debug(f"_send_message_with_result: {j}")
        evt = threading.Event()
        self._ws_callbacks[msg_id] = (evt, None)
        self._ws.send(j)
        evt.wait()
        return self._ws_callbacks.pop(msg_id)[1]

    def close(self):
        logging.debug("Closing connection...")
        if self._ws is not None:
            self._ws.close()
