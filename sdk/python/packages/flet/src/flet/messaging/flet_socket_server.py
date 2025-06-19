import asyncio
import logging
import os
import tempfile
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from typing import Any, Optional

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
from flet.utils import get_free_tcp_port, is_windows, random_string

logger = logging.getLogger("flet")
transport_log = logging.getLogger("flet_transport")


class FletSocketServer(Connection):
    def __init__(
        self,
        loop: asyncio.AbstractEventLoop,
        port: int = 0,
        uds_path: Optional[str] = None,
        on_session_created=None,
        before_main=None,
        blocking=False,
        executor: Optional[ThreadPoolExecutor] = None,
    ):
        super().__init__()
        self.__send_loop_task = None
        self.__receive_loop_task = None
        self.__connected = None
        self.session = None
        self.__send_queue = asyncio.Queue()
        self.__port = port
        self.__uds_path = uds_path
        self.__on_session_created = on_session_created
        self.__before_main = before_main
        self.__blocking = blocking
        self.__running_tasks = set()
        self.loop = loop
        self.executor = executor
        self.pubsubhub = PubSubHub(loop=loop, executor=executor)

    async def start(self):
        self.__connected = False
        self.__receive_loop_task = None
        self.__send_loop_task = None
        if is_windows() or self.__port > 0:
            # TCP
            host = "localhost"
            port = self.__port if self.__port > 0 else get_free_tcp_port()
            self.page_url = f"tcp://{host}:{port}"
            logger.info(f"Starting up TCP server on {host}:{port}")
            server = await asyncio.start_server(self.handle_connection, host, port)
        else:
            # UDS
            if not self.__uds_path:
                self.__uds_path = str(
                    Path(tempfile.gettempdir()).joinpath(random_string(10))
                )
            if os.path.exists(self.__uds_path):
                os.remove(self.__uds_path)
            self.page_url = self.__uds_path
            logger.info(f"Starting up UDS server on {self.__uds_path}")
            server = await asyncio.start_unix_server(
                self.handle_connection, self.__uds_path
            )

        if self.__blocking:
            self.__server = None
            await server.serve_forever()
        else:
            self.__server = asyncio.create_task(server.serve_forever())

    async def handle_connection(
        self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter
    ):
        if not self.__connected:
            self.__connected = True
            logger.debug("Connected new TCP client")
            self.__receive_loop_task = asyncio.create_task(self.__receive_loop(reader))
            self.__send_loop_task = asyncio.create_task(self.__send_loop(writer))

    async def __receive_loop(self, reader: asyncio.StreamReader):
        unpacker = msgpack.Unpacker(ext_hook=decode_ext_from_msgpack)
        while True:
            try:
                buf = await reader.read(1024**2)
                if not buf:
                    return None
                unpacker.feed(buf)
            except Exception as e:
                logger.debug(f"Error receiving socket data from Flet client: {e}")
                return None

            for msg in unpacker:
                await self.__on_message(msg)

    async def __send_loop(self, writer: asyncio.StreamWriter):
        while True:
            message = await self.__send_queue.get()
            try:
                writer.write(message)
            except Exception:
                # re-enqueue the message to repeat it when re-connected
                self.__send_queue.put_nowait(message)
                raise

    async def __on_message(self, data: Any):
        action = ClientAction(data[0])
        body = data[1]
        transport_log.debug(f"_on_message: {action} {body}")
        task = None
        if action == ClientAction.REGISTER_CLIENT:
            req = RegisterClientRequestBody(**body)

            # create new session
            self.session = Session(self)

            try:
                # apply page patch
                if not req.session_id:
                    self.session.apply_page_patch(req.page)

                if asyncio.iscoroutinefunction(self.__before_main):
                    await self.__before_main(self.session.page)
                elif callable(self.__before_main):
                    self.__before_main(self.session.page)

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
            raise Exception(f'Unknown message "{action}": {body}')

        if task:
            self.__running_tasks.add(task)
            task.add_done_callback(self.__running_tasks.discard)

    def send_message(self, message: ClientMessage):
        transport_log.debug(f"send_message: {message}")
        m = msgpack.packb(
            [message.action, message.body],
            default=configure_encode_object_for_msgpack(BaseControl),
        )
        self.__send_queue.put_nowait(m)

    async def close(self):
        logger.debug("Closing connection...")

        if self.executor:
            logger.debug("Shutting down thread pool...")
            self.executor.shutdown(wait=False, cancel_futures=True)

        # close socket
        if self.__receive_loop_task:
            self.__receive_loop_task.cancel()
        if self.__send_loop_task:
            self.__send_loop_task.cancel()
        if self.__server:
            self.__server.cancel()

        # remove UDS path
        if self.__uds_path and os.path.exists(self.__uds_path):
            os.unlink(self.__uds_path)
