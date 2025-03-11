import asyncio
import json
import logging
import os
import struct
import sys
import tempfile
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from typing import Any, List, Optional

import flet
import msgpack
from flet.messaging.connection import Connection
from flet.messaging.protocol import (
    ClientAction,
    ClientMessage,
    Command,
    CommandEncoder,
    PageCommandResponsePayload,
    PageCommandsBatchResponsePayload,
    RegisterWebClientRequestPayload,
    encode_object_for_msgpack,
)
from flet.pubsub.pubsub_hub import PubSubHub
from flet.utils import get_free_tcp_port, is_windows, random_string

logger = logging.getLogger(flet.__name__)


class FletSocketServer(Connection):
    def __init__(
        self,
        loop: asyncio.AbstractEventLoop,
        port: int = 0,
        uds_path: Optional[str] = None,
        on_event=None,
        on_session_created=None,
        blocking=False,
        executor: Optional[ThreadPoolExecutor] = None,
    ):
        super().__init__()
        self.__send_queue = asyncio.Queue()
        self.__port = port
        self.__uds_path = uds_path
        self.__on_event = on_event
        self.__on_session_created = on_session_created
        self.__blocking = blocking
        self.__loop = loop
        self.__executor = executor
        self.pubsubhub = PubSubHub(loop=loop, executor=executor)
        self.__running_tasks = set()

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
        unpacker = msgpack.Unpacker()
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
                # await writer.drain()
                print(f"sent to TCP: {len(message)}")
            except Exception:
                # re-enqueue the message to repeat it when re-connected
                self.__send_queue.put_nowait(message)
                raise

    async def __on_message(self, data: Any):
        msg = ClientMessage(action=data[0], payload=data[1])
        print(f"_on_message: {data}", ClientAction(msg.action))
        task = None
        if ClientAction(msg.action) == ClientAction.REGISTER_CLIENT:
            print("REGISTER CLIENT")
            self._client_details = RegisterWebClientRequestPayload(**msg.payload)

            # register response
            self.__send(self._create_register_web_client_response())

            # start session
            if self.__on_session_created is not None:
                task = asyncio.create_task(
                    self.__on_session_created(self._create_session_handler_arg())
                )

        elif ClientAction(msg.action) == ClientAction.CONTROL_EVENT:
            if self.__on_event is not None:
                task = asyncio.create_task(
                    self.__on_event(self._create_page_event_handler_arg(msg))
                )

        elif ClientAction(msg.action) == ClientAction.UPDATE_CONTROL_PROPS:
            if self.__on_event is not None:
                task = asyncio.create_task(
                    self.__on_event(self._create_update_control_props_handler_arg(msg))
                )
        else:
            # it's something else
            raise Exception(f'Unknown message "{msg.action}": {msg.payload}')

        if task:
            self.__running_tasks.add(task)
            task.add_done_callback(self.__running_tasks.discard)

    def send_command(self, session_id: str, command: Command):
        result, message = self._process_command(command)
        if message:
            self.__send(message)
        return PageCommandResponsePayload(result=result, error="")

    def send_commands(self, session_id: str, commands: List[Command]):
        results = []
        messages = []
        for command in commands:
            result, message = self._process_command(command)
            if command.name in ["add", "get"]:
                results.append(result)
            if message:
                messages.append(message)
        if len(messages) > 0:
            self.__send(ClientMessage(ClientAction.PAGE_CONTROLS_BATCH, messages))
        return PageCommandsBatchResponsePayload(results=results, error="")

    def __send(self, message: ClientMessage):
        m = msgpack.packb(
            [message.action, message.payload], default=encode_object_for_msgpack
        )
        print(f"__send: {m}")
        self.__loop.call_soon_threadsafe(self.__send_queue.put_nowait, m)

    async def close(self):
        logger.debug("Closing connection...")

        logger.debug(f"Disconnecting all pages...")
        while self.sessions:
            _, page = self.sessions.popitem()
            await page._disconnect(0)

        if self.__executor:
            logger.debug("Shutting down thread pool...")
            if sys.version_info >= (3, 9):
                self.__executor.shutdown(wait=False, cancel_futures=True)
            else:
                self.__executor.shutdown(wait=False)

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
