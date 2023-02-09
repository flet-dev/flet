import json
import logging
import os
import socket
import struct
import tempfile
import threading
from pathlib import Path
from typing import List, Optional

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


class SyncLocalSocketConnection(LocalConnection):
    def __init__(
        self,
        port: int = 0,
        uds_path: Optional[str] = None,
        on_event=None,
        on_session_created=None,
    ):
        super().__init__()
        self.__port = port
        self.__uds_path = uds_path
        self.__on_event = on_event
        self.__on_session_created = on_session_created

    def connect(self):
        if is_windows() or self.__port > 0:
            # TCP
            port = self.__port if self.__port > 0 else get_free_tcp_port()
            self.page_url = f"tcp://localhost:{port}"
            server_address = ("localhost", port)
            self.__sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.__sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            logging.info(f"Starting up TCP server on {server_address}")
            self.__sock.bind(server_address)
        else:
            # UDS
            if not self.__uds_path:
                self.__uds_path = str(
                    Path(tempfile.gettempdir()).joinpath(random_string(10))
                )
            self.page_url = self.__uds_path
            self.__sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
            logging.info(f"Starting up UDS server on {self.__uds_path}")
            self.__sock.bind(self.__uds_path)

        # Listen for incoming connections
        self.__sock.listen(1)

        # start connect loop
        th = threading.Thread(target=self.__connection_loop, args=(), daemon=True)
        th.start()

    def __on_message(self, data):
        logging.debug(f"_on_message: {data}")
        msg_dict = json.loads(data)
        msg = ClientMessage(**msg_dict)
        if msg.action == ClientActions.REGISTER_WEB_CLIENT:
            self._client_details = RegisterWebClientRequestPayload(**msg.payload)

            # register response
            self.__send(self._create_register_web_client_response())

            # start a new session
            if self.__on_session_created is not None:
                th = threading.Thread(
                    target=self.__on_session_created,
                    args=(
                        self,
                        self._create_session_handler_arg(),
                    ),
                    daemon=True,
                )
                th.start()
        elif msg.action == ClientActions.PAGE_EVENT_FROM_WEB:
            if self.__on_event is not None:
                th = threading.Thread(
                    target=self.__on_event,
                    args=(self, self._create_page_event_handler_arg(msg)),
                    daemon=True,
                )
                th.start()
        elif msg.action == ClientActions.UPDATE_CONTROL_PROPS:
            if self.__on_event is not None:
                th = threading.Thread(
                    target=self.__on_event,
                    args=(self, self._create_update_control_props_handler_arg(msg)),
                    daemon=True,
                )
                th.start()
        else:
            # it's something else
            raise Exception('Unknown message "{}": {}'.format(msg.action, msg.payload))

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
            self.__send(ClientMessage(ClientActions.PAGE_CONTROLS_BATCH, messages))
        return PageCommandsBatchResponsePayload(results=results, error="")

    def close(self):
        logging.debug("Closing connection...")
        # close socket
        if self.__sock:
            self.__sock.close()

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
                logging.debug("Closing connection")
                self.__connection.close()

    def __send(self, message: ClientMessage):
        j = json.dumps(message, cls=CommandEncoder, separators=(",", ":"))
        logging.debug(f"__send: {j}")
        self.__send_msg(self.__connection, j.encode("utf-8"))

    def __send_msg(self, sock, msg):
        # Prefix each message with a 4-byte length (network byte order)
        msg = struct.pack(">I", len(msg)) + msg
        sock.sendall(msg)
        logging.debug("Sent: {}".format(len(msg)))

    def __recv_msg(self, sock):
        # Read message length and unpack it into an integer
        raw_msglen = self.__recvall(sock, 4)
        if not raw_msglen:
            return None
        msglen = struct.unpack(">I", raw_msglen)[0]
        logging.debug("Message size: {}".format(msglen))
        # Read the message data
        return self.__recvall(sock, msglen)

    def __recvall(self, sock, n):
        # Helper function to recv n bytes or return None if EOF is hit
        data = bytearray()
        while len(data) < n:
            try:
                packet = sock.recv(n - len(data))
            except:
                return None
            # print("packet received:", len(packet))
            if not packet:
                return None
            data.extend(packet)
        return data
