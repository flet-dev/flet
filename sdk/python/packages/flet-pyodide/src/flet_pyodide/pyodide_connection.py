import asyncio
import json
import logging
from typing import List

import flet_js
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


class PyodideConnection(LocalConnection):
    def __init__(
        self,
        on_event,
        on_session_created,
    ):
        super().__init__()
        self.__send_queue = asyncio.Queue(1)
        self.__receive_queue = asyncio.Queue()
        self.__on_event = on_event
        self.__on_session_created = on_session_created
        flet_js.start_connection = self.connect

    async def connect(self):
        print("Starting Pyodide connection...")
        asyncio.create_task(self.receive_loop())
        flet_js.send = self.send_from_js
        flet_js.receive_async = self.receive_from_js_async

    async def receive_loop(self):
        while True:
            message = await self.__receive_queue.get()
            await self.__on_message(message)

    def send_from_js(self, message: str):
        print("Sending data from JavaScript to Python:", message)
        self.__receive_queue.put_nowait(message)

    async def receive_from_js_async(self):
        return await self.__send_queue.get()

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

    async def __send(self, message: ClientMessage):
        j = json.dumps(message, cls=CommandEncoder, separators=(",", ":"))
        logging.debug(f"__send: {j}")
        await self.__send_queue.put(j)
