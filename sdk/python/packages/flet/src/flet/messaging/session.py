import weakref
from datetime import datetime, timedelta, timezone
from typing import Optional

from flet.core.control import Control
from flet.core.page import Page, _session_page
from flet.messaging.connection import Connection
from flet.pubsub.pubsub_client import PubSubClient
from flet.utils.strings import random_string


class Session:
    def __init__(self, conn: Connection):
        self.__conn: weakref.ReferenceType = weakref.ref(conn)
        self.__id = random_string(16)
        self.__expires_at = None
        self.__index: weakref.WeakValueDictionary[int, Control] = (
            weakref.WeakValueDictionary()
        )
        self.__page = Page(self)
        self.__index[self.__page._i] = self.__page
        self.__pubsub_client = PubSubClient(conn.pubsubhub, self.__id)

    @property
    def connection(self):
        if conn := self.__conn():
            return conn
        raise Exception("An attempt to fetch destroyed connection.")

    @property
    def id(self):
        return self.__id

    @property
    def expires_at(self) -> Optional[datetime]:
        return self.__expires_at

    @property
    def index(self):
        return self.__index

    @property
    def pubsub_client(self) -> PubSubClient:
        return self.__pubsub_client

    async def connect(self, conn: Connection) -> None:
        _session_page.set(self.__page)
        self.__conn = weakref.ref(conn)
        self.__expires_at = None
        # await self.on_event_async(Event("page", "connect", ""))

    async def disconnect(self, session_timeout_seconds: int) -> None:
        self.__expires_at = datetime.now(timezone.utc) + timedelta(
            seconds=session_timeout_seconds
        )
        # await self.on_event_async(Event("page", "disconnect", ""))
