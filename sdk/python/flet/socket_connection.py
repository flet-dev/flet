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
        self.__control_id = 1

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

    def __on_message(self, data):
        logging.debug(f"_on_message: {data}")
        msg_dict = json.loads(data)
        msg = ClientMessage(**msg_dict)
        if msg.action == ClientActions.REGISTER_WEB_CLIENT:
            self.__client_details = RegisterWebClientRequestPayload(**msg.payload)

            # register response
            self.__send(
                ClientMessage(
                    ClientActions.REGISTER_WEB_CLIENT,
                    RegisterWebClientResponsePayload(
                        session=SessionPayload(
                            id=self.__client_details.sessionId,
                            controls={
                                "page": {
                                    "i": "page",
                                    "t": "page",
                                    "p": "",
                                    "c": [],
                                    "route": self.__client_details.pageRoute,
                                    "width": self.__client_details.pageWidth,
                                    "height": self.__client_details.pageHeight,
                                    "windowwidth": self.__client_details.windowWidth,
                                    "windowheight": self.__client_details.windowHeight,
                                    "windowtop": self.__client_details.windowTop,
                                    "windowleft": self.__client_details.windowLeft,
                                    "pwa": self.__client_details.isPWA,
                                    "web": self.__client_details.isWeb,
                                    "platform": self.__client_details.platform,
                                }
                            },
                        ),
                        appInactive=False,
                        error="",
                    ),
                )
            )

            # start session
            if self.__on_session_created is not None:
                th = threading.Thread(
                    target=self.__on_session_created,
                    args=(
                        self,
                        PageSessionCreatedPayload(
                            pageName=self.__client_details.pageName,
                            sessionID=self.__client_details.sessionId,
                        ),
                    ),
                    daemon=True,
                )
                th.start()
        elif msg.action == ClientActions.PAGE_EVENT_FROM_WEB:
            if self.__on_event is not None:
                web_event = PageEventFromWebPayload(**msg.payload)
                th = threading.Thread(
                    target=self.__on_event,
                    args=(
                        self,
                        PageEventPayload(
                            pageName=self.__client_details.pageName,
                            sessionID=self.__client_details.sessionId,
                            eventTarget=web_event.eventTarget,
                            eventName=web_event.eventName,
                            eventData=web_event.eventData,
                        ),
                    ),
                    daemon=True,
                )
                th.start()
        elif msg.action == ClientActions.UPDATE_CONTROL_PROPS:
            if self.__on_event is not None:
                th = threading.Thread(
                    target=self.__on_event,
                    args=(
                        self,
                        PageEventPayload(
                            pageName=self.__client_details.pageName,
                            sessionID=self.__client_details.sessionId,
                            eventTarget="page",
                            eventName="change",
                            eventData=json.dumps(
                                msg.payload["props"], separators=(",", ":")
                            ),
                        ),
                    ),
                    daemon=True,
                )
                th.start()
        else:
            # it's something else
            print("Unknown message:", msg.action, msg.payload)

    def send_command(self, session_id: str, command: Command):
        result, message = self.__process_command(command)
        if message:
            self.__send(message)
        return PageCommandResponsePayload(result=result, error="")

    def send_commands(self, session_id: str, commands: List[Command]):
        results = []
        messages = []
        for command in commands:
            result, message = self.__process_command(command)
            if command.name in ["add", "get"]:
                results.append(result)
            if message:
                messages.append(message)
        if len(messages) > 0:
            self.__send(ClientMessage(ClientActions.PAGE_CONTROLS_BATCH, messages))
        return PageCommandsBatchResponsePayload(results=results, error="")

    def __process_command(self, command: Command):
        logging.debug("__process_command: {}".format(command))
        if command.name == "get":
            return self.__process_get_command(command.values)
        elif command.name == "add":
            return self.__process_add_command(command)
        elif command.name == "set":
            return self.__process_set_command(command.values, command.attrs)
        elif command.name == "remove":
            return self.__process_remove_command(command.values)
        elif command.name == "clean":
            return self.__process_clean_command(command.values)
        elif command.name == "invokeMethod":
            return self.__process_invoke_method_command(command.values, command.attrs)
        elif command.name == "error":
            return self.__process_error_command(command.values)
        raise Exception("Unsupported command: {}".format(command.name))

    def __process_add_command(self, command: Command):

        top_parent_id = command.attrs.get("to", "page")
        top_parent_at = int(command.attrs.get("at", "-1"))

        batch: List[Command] = []
        if len(command.values) > 0:
            batch.append(command)

        for sub_cmd in command.commands:
            sub_cmd.name = "add"
            batch.append(sub_cmd)

        ids = []
        controls = []
        controls_idx = {}

        i = 0
        for cmd in batch:
            assert len(cmd.values) > 0, "control type is not specified"
            control_type = cmd.values[0].lower()

            parent_id = ""
            parent_at = -1

            # find nearest parentID
            pi = i - 1
            while pi >= 0:
                if batch[pi].indent < cmd.indent:
                    parent_id = batch[pi].attrs.get("id", "")
                    break
                pi -= 1

            # parent wasn't found - use the topmost one
            if parent_id == "":
                parent_id = top_parent_id
                parent_at = top_parent_at

            id = cmd.attrs.get("id", "")
            if not id:
                id = "_{}".format(self.__control_id)
                self.__control_id += 1
                cmd.attrs["id"] = id

            ids.append(id)

            control = {"t": control_type, "i": id, "p": parent_id, "c": []}
            controls.append(control)
            controls_idx[id] = control

            if parent_at != -1:
                control["at"] = str(parent_at)
                top_parent_at += 1

            parent_control = controls_idx.get(parent_id)
            if parent_control:
                if parent_at != -1:
                    parent_control["c"].insert(parent_at, id)
                else:
                    parent_control["c"].append(id)

            system_attrs = ["id", "to", "from", "at", "t", "p", "i", "c"]
            for k, v in cmd.attrs.items():
                if k not in system_attrs and v:
                    control[k] = v

            i += 1

        return " ".join(ids), ClientMessage(
            ClientActions.ADD_PAGE_CONTROLS, AddPageControlsPayload(controls=controls)
        )

    def __process_set_command(self, values, attrs):
        assert len(values) == 1, '"set" command has wrong number of values'
        props = {"i": values[0]}
        for k, v in attrs.items():
            props[k] = v

        return "", ClientMessage(
            ClientActions.UPDATE_CONTROL_PROPS, UpdateControlPropsPayload(props=[props])
        )

    def __process_remove_command(self, values):
        assert len(values) > 0, '"remove" command has wrong number of values'
        return "", ClientMessage(
            ClientActions.REMOVE_CONTROL, RemoveControlPayload(ids=values)
        )

    def __process_clean_command(self, values):
        assert len(values) > 0, '"clean" command has wrong number of values'
        return "", ClientMessage(
            ClientActions.CLEAN_CONTROL, CleanControlPayload(ids=values)
        )

    def __process_error_command(self, values):
        assert len(values) == 1, '"error" command has wrong number of values'
        return "", ClientMessage(
            ClientActions.SESSION_CRASHED, SessionCrashedPayload(message=values[0])
        )

    def __process_invoke_method_command(self, values, attrs):
        # "invokeMethod", values=[method_id, method_name], attrs=arguments
        assert len(values) == 2, '"invokeMethod" command has wrong number of values'
        return "", ClientMessage(
            ClientActions.INVOKE_METHOD,
            InvokeMethodPayload(
                methodId=values[0], methodName=values[1], arguments=attrs
            ),
        )

    def __process_get_command(self, values: List[str]):
        assert len(values) == 2, '"get" command has wrong number of values'
        ctrl_id = values[0]
        prop_name = values[1]
        r = ""
        if ctrl_id == "page":
            if prop_name == "route":
                r = self.__client_details.pageRoute
            elif prop_name == "pwa":
                r = self.__client_details.isPWA
            elif prop_name == "web":
                r = self.__client_details.isWeb
            elif prop_name == "platform":
                r = self.__client_details.platform
            elif prop_name == "width":
                r = self.__client_details.pageWidth
            elif prop_name == "height":
                r = self.__client_details.pageHeight
            elif prop_name == "windowWidth":
                r = self.__client_details.windowWidth
            elif prop_name == "windowHeight":
                r = self.__client_details.windowHeight
            elif prop_name == "windowTop":
                r = self.__client_details.windowTop
            elif prop_name == "windowLeft":
                r = self.__client_details.windowLeft
        return r, None

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
                logging.debug("Cloding connection")
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
            packet = sock.recv(n - len(data))
            # print("packet received:", len(packet))
            if not packet:
                return None
            data.extend(packet)
        return data
