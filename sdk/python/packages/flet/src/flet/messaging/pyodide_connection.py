import asyncio
import inspect
import logging
import traceback
from collections.abc import Awaitable
from typing import TYPE_CHECKING, Any, Callable, Optional

import flet_js
import msgpack

from flet.controls.base_control import BaseControl
from flet.messaging.connection import Connection
from flet.messaging.protocol import (
    ClientAction,
    ClientMessage,
    ControlEventBody,
    InvokeMethodResponseBody,
    RegisterClientRequestBody,
    RegisterClientResponseBody,
    UpdateControlPropsBody,
    configure_encode_object_for_msgpack,
    decode_ext_from_msgpack,
)
from flet.messaging.session import Session
from flet.pubsub.pubsub_hub import PubSubHub

if TYPE_CHECKING:
    from flet.app import AppCallable

logger = logging.getLogger("flet")
transport_log = logging.getLogger("flet_transport")


class PyodideConnection(Connection):
    """
    Browser-side connection adapter used when Flet runs in Pyodide.

    This transport bridges JavaScript and Python message flow through `flet_js`,
    manages a session lifecycle, and routes protocol messages to session handlers.
    """

    def __init__(
        self,
        on_session_created: Optional[Callable[[Session], Awaitable[Any]]],
        before_main: Optional["AppCallable"],
    ):
        super().__init__()
        self.__receive_queue = asyncio.Queue()
        self.__on_session_created = on_session_created
        self.__before_main = before_main
        flet_js.start_connection = self.connect
        self.__running_tasks = set()
        self.pubsubhub = PubSubHub()
        self.loop = asyncio.get_running_loop()

    async def connect(self, send_callback):
        """
        Initializes JavaScript bridge callbacks and starts the receive loop.

        Args:
            send_callback: JavaScript callback used to send packed protocol messages
                from Python to the browser client.
        """
        logger.info("Starting Pyodide connection...")
        self.page_url = flet_js.documentUrl
        self.send_callback = send_callback
        asyncio.create_task(self.receive_loop())
        flet_js.send = self.send_from_js

    async def receive_loop(self):
        """
        Continuously receives, decodes, and dispatches inbound client messages.

        This loop waits for raw messages queued by `send_from_js()`, decodes MsgPack
        payloads, and forwards parsed protocol frames to `__on_message()`.
        """
        while True:
            data = await self.__receive_queue.get()
            message = msgpack.unpackb(data.to_py(), ext_hook=decode_ext_from_msgpack)
            await self.__on_message(message)

    def send_from_js(self, message: Any):
        """
        Enqueues a raw message delivered from JavaScript.

        Args:
            message: JS message payload object expected to expose `to_py()`.
        """
        self.__receive_queue.put_nowait(message)

    async def __on_message(self, data: Any):
        """
        Processes one decoded protocol frame from the client.

        Supported actions:
        - register client and create a new session;
        - dispatch control events;
        - apply control property updates;
        - deliver invoke-method results.

        Args:
            data: Decoded protocol frame `[action, body]`.

        Raises:
            RuntimeError: If the action type is unknown.
        """
        action = ClientAction(data[0])
        body = data[1]
        transport_log.debug(f"_on_message: {action} {body}")
        task = None
        if action == ClientAction.REGISTER_CLIENT:
            req = RegisterClientRequestBody(**body)

            # create new session
            self.session = Session(self)

            # apply page patch
            self.session.apply_page_patch(req.page)

            register_error = ""
            try:
                if inspect.iscoroutinefunction(self.__before_main):
                    await self.__before_main(self.session.page)
                elif callable(self.__before_main):
                    self.__before_main(self.session.page)
            except Exception as e:
                register_error = f"{e}\n{traceback.format_exc()}"
                logger.error("Unhandled error in before_main() handler", exc_info=True)

            # register response
            self.send_message(
                ClientMessage(
                    ClientAction.REGISTER_CLIENT,
                    RegisterClientResponseBody(
                        session_id=self.session.id,
                        page_patch=self.session.get_page_patch(),
                        error=register_error,
                    ),
                )
            )

            # start session
            if not register_error and self.__on_session_created is not None:
                task = asyncio.create_task(self.__on_session_created(self.session))
            elif register_error:
                self.session.error(register_error)

        elif action == ClientAction.CONTROL_EVENT:
            req = ControlEventBody(**body)
            task = asyncio.create_task(
                self.session.dispatch_event(req.target, req.name, req.data)
            )

        elif action == ClientAction.UPDATE_CONTROL_PROPS:
            req = UpdateControlPropsBody(**body)
            self.session.apply_patch(req.id, req.props)

        elif action == ClientAction.INVOKE_METHOD:
            req = InvokeMethodResponseBody(**body)
            self.session.handle_invoke_method_results(
                req.control_id, req.call_id, req.result, req.error
            )

        else:
            # it's something else
            raise RuntimeError(f'Unknown message "{action}": {body}')

        if task:
            self.__running_tasks.add(task)
            task.add_done_callback(self.__running_tasks.discard)

    def send_message(self, message: ClientMessage):
        """
        Serializes and sends an outbound protocol message to JavaScript.

        Args:
            message: Client message to serialize with MsgPack and send.
        """
        transport_log.debug(f"send_message: {message}")
        m = msgpack.packb(
            [message.action, message.body],
            default=configure_encode_object_for_msgpack(BaseControl),
        )
        self.send_callback(m)
