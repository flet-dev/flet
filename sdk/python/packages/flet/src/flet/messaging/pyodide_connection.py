import asyncio
import logging
from typing import Any

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

logger = logging.getLogger("flet")


class PyodideConnection(Connection):
    def __init__(self, on_session_created):
        super().__init__()
        self.__receive_queue = asyncio.Queue()
        self.__on_session_created = on_session_created
        flet_js.start_connection = self.connect
        self.__running_tasks = set()
        self.pubsubhub = PubSubHub()

    async def connect(self, send_callback):
        logger.info("Starting Pyodide connection...")
        self.page_url = flet_js.documentUrl
        self.send_callback = send_callback
        asyncio.create_task(self.receive_loop())
        flet_js.send = self.send_from_js

    async def receive_loop(self):
        while True:
            data = await self.__receive_queue.get()
            message = msgpack.unpackb(data.to_py(), ext_hook=decode_ext_from_msgpack)
            await self.__on_message(message)

    def send_from_js(self, message: Any):
        self.__receive_queue.put_nowait(message)

    async def __on_message(self, data: Any):
        action = ClientAction(data[0])
        body = data[1]
        # print(f"_on_message: {action} {body}")
        task = None
        if action == ClientAction.REGISTER_CLIENT:
            req = RegisterClientRequestBody(**body)

            try:
                # create new session
                self.session = Session(self)

                # apply page patch
                self.session.apply_page_patch(req.page)

                # register response
                self.send_message(
                    ClientMessage(
                        ClientAction.REGISTER_CLIENT,
                        RegisterClientResponseBody(
                            session_id=self.session.id,
                            page_patch=self.session.get_page_patch(),
                            error="",
                        ),
                    )
                )

                # start session
                if self.__on_session_created is not None:
                    task = asyncio.create_task(self.__on_session_created(self.session))
            except Exception as ex:
                logger.debug(f"Error creating session: {ex}", exc_info=True)

        elif action == ClientAction.CONTROL_EVENT:
            req = ControlEventBody(**body)
            await self.session.dispatch_event(
                req.target, req.name, req.data, req.fields
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
            raise Exception(f'Unknown message "{action}": {body}')

        if task:
            self.__running_tasks.add(task)
            task.add_done_callback(self.__running_tasks.discard)

    def send_message(self, message: ClientMessage):
        # print(f"Sending: {message}")
        m = msgpack.packb(
            [message.action, message.body],
            default=configure_encode_object_for_msgpack(BaseControl),
        )
        self.send_callback(m)
