import asyncio
import json
import logging
import os
import socket
import struct
import tempfile
import threading
from pathlib import Path
from typing import List

from flet.local_connection import LocalConnection
from flet.protocol import *
from flet.utils import get_free_tcp_port, is_windows, random_string


class AsyncLocalSocketConnection(LocalConnection):
    def __init__(
        self,
        on_event=None,
        on_session_created=None,
    ):
        super().__init__()
        self.__on_event = on_event
        self.__on_session_created = on_session_created
        self._control_id = 1

    async def connect(self):
        if is_windows():
            # TCP
            host = "localhost"
            port = get_free_tcp_port()
            self.page_url = f"tcp://{host}:{port}"
            logging.info(f"Starting up TCP server on {host}:{port}")
            server = await asyncio.start_server(self.handle_connection, host, port)
            self.__server = asyncio.create_task(server.serve_forever())
        else:
            # UDS
            self.__uds_path = str(
                Path(tempfile.gettempdir()).joinpath(random_string(10))
            )
            self.page_url = self.__uds_path
            logging.info(f"Starting up UDS server on {self.__uds_path}")
            server = await asyncio.start_unix_server(
                self.handle_connection, self.__uds_path
            )
            self.__server = asyncio.create_task(server.serve_forever())

    async def handle_connection(
        self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter
    ):
        pass

    async def __on_message(self, data: str):
        logging.debug(f"_on_message: {data}")
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
            raise Exception('Unknown message "{}": {}'.format(msg.action, msg.payload))

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

    async def close_async(self):
        logging.debug("Closing connection...")
        # close socket
        if self.__server:
            self.__server.cancel()

        # remove UDS path
        if self.__uds_path and os.path.exists(self.__uds_path):
            os.unlink(self.__uds_path)

    def __connection_loop(self):
        while True:
            logging.debug("Waiting for a client connection")
            self.__connection, client_address = self.__sock.accept()
            try:
                logging.debug(f"Connection from {client_address}")

                # receive loop
                while True:
                    message = self.__recv_msg(self.__connection)
                    if message:
                        self.__on_message(message.decode("utf-8"))

            finally:
                logging.debug("Cloding connection")
                self.__connection.close()

    async def __send(self, message: ClientMessage):
        j = json.dumps(message, cls=CommandEncoder, separators=(",", ":"))
        logging.debug(f"__send: {j}")
        self.__send_msg(self.__connection, j.encode("utf-8"))
