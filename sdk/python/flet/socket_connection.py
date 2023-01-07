import json
import logging
import os
import socket
import struct
import tempfile
import threading
from pathlib import Path
from typing import List

from flet.connection import Connection
from flet.protocol import *
from flet.reconnecting_websocket import ReconnectingWebSocket
from flet.utils import get_free_tcp_port, is_windows, random_string


class SocketConnection(Connection):
    def __init__(
        self,
        on_event=None,
        on_session_created=None,
    ):
        super().__init__()
        self.__on_event = on_event
        self.__on_session_created = on_session_created

    def connect(self):
        if is_windows():
            # TCP
            port = get_free_tcp_port()
            self.page_url = f"tcp://localhost:{port}"
            server_address = ("localhost", port)
            self.__sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            logging.info(f"Starting up TCP server on {server_address}")
            self.__sock.bind(server_address)
        else:
            # UDS
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

    def __on_ws_message(self, data):
        logging.debug(f"_on_message: {data}")
        msg_dict = json.loads(data)
        msg = SimpleMessage(**msg_dict)
        if msg.action == Actions.PAGE_EVENT_TO_HOST:
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
        return PageCommandResponsePayload(result="", error="")

    def send_commands(self, session_id: str, commands: List[Command]):
        return PageCommandsBatchResponsePayload(results=[], error="")

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
                    self.__on_ws_message(message.decode("utf-8"))

            finally:
                logging.debug("Cloding connection")
                self.__connection.close()

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
            packet = sock.recv(n - len(data))
            # print("packet received:", len(packet))
            if not packet:
                return None
            data.extend(packet)
        return data
