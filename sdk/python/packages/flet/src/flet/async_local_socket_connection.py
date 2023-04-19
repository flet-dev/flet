import asyncio
import json
import logging
import os
import struct
import tempfile
from pathlib import Path
from typing import List, Optional

import flet
from flet.utils import get_free_tcp_port, is_windows
from flet_core.local_connection import LocalConnection
from flet_core.protocol import (
    ClientActions,
    ClientMessage,
    Command,
    CommandEncoder,
    PageCommandResponsePayload,
    PageCommandsBatchResponsePayload,
    RegisterWebClientRequestPayload,
)
from flet_core.utils import random_string

logger = logging.getLogger(flet.__name__)


class AsyncLocalSocketConnection(LocalConnection):
    def __init__(
        self,
        port: int = 0,
        uds_path: Optional[str] = None,
        on_event=None,
        on_session_created=None,
    ):
        super().__init__()
        self.__send_queue = asyncio.Queue(1)
        self.__port = port
        self.__uds_path = uds_path
        self.__on_event = on_event
        self.__on_session_created = on_session_created

    async def connect(self):
        self.__connected = False
        if is_windows() or self.__port > 0:
            # TCP
            host = "localhost"
            port = self.__port if self.__port > 0 else get_free_tcp_port()
            self.page_url = f"tcp://{host}:{port}"
            logger.info(f"Starting up TCP server on {host}:{port}")
            server = await asyncio.start_server(self.handle_connection, host, port)
            self.__server = asyncio.create_task(server.serve_forever())
        else:
            # UDS
            if not self.__uds_path:
                self.__uds_path = str(
                    Path(tempfile.gettempdir()).joinpath(random_string(10))
                )
            self.page_url = self.__uds_path
            logger.info(f"Starting up UDS server on {self.__uds_path}")
            server = await asyncio.start_unix_server(
                self.handle_connection, self.__uds_path
            )
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
        while True:
            try:
                raw_msglen = await reader.readexactly(4)
            except Exception:
                return None

            if not raw_msglen:
                return None
            msglen = struct.unpack(">I", raw_msglen)[0]

            data = await reader.readexactly(msglen)
            await self.__on_message(data.decode("utf-8"))

    async def __send_loop(self, writer: asyncio.StreamWriter):
        while True:
            message = await self.__send_queue.get()
            try:
                data = message.encode("utf-8")
                msg = struct.pack(">I", len(data)) + data
                writer.write(msg)
                # await writer.drain()
                logger.debug(f"sent to TCP: {len(msg)}")
            except Exception:
                # re-enqueue the message to repeat it when re-connected
                self.__send_queue.put_nowait(message)
                raise

    async def __on_message(self, data: str):
        logger.debug(f"_on_message: {data}")
        msg_dict = json.loads(data)
        msg = ClientMessage(**msg_dict)
        if msg.action == ClientActions.REGISTER_WEB_CLIENT:
            self._client_details = RegisterWebClientRequestPayload(**msg.payload)

            # register response
            await self.__send(self._create_register_web_client_response())

            # start session
            if self.__on_session_created is not None:
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
        await self.__send_queue.put(j)

    async def close(self):
        logger.debug("Closing connection...")
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
