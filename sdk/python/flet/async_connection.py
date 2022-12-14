from asyncio import sleep
import asyncio
import json
import logging
from typing import List, Optional
import uuid
from flet import constants
from flet.connection import Connection

from flet.protocol import *


class AsyncConnection(Connection):
    def __init__(
        self,
        server_address: str,
        page_name: str,
        token: Optional[str],
        on_event=None,
        on_session_created=None,
    ):
        super().__init__()
        self.page_name = page_name
        self.__host_client_id: Optional[str] = None
        self.__token = token
        self.__server_address = server_address
        self.__on_event = on_event
        self.__on_session_created = on_session_created

    async def connect(self):
        print("Connecting async...")
        self.page_url = "http://localhost:8550"
        self.task = asyncio.get_event_loop().create_task(self.__connect_async())

    async def __connect_async(self):
        i = 1
        while True:
            print(i)
            await sleep(1)
            i += 1

    async def send_command_async(self, session_id: str, command: Command):
        pass

    async def send_commands_async(self, session_id: str, commands: List[Command]):
        pass

    def close(self):
        logging.debug("Closing connection...")
        self.task.cancel()
