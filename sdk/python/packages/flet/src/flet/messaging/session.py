import weakref
from datetime import datetime, timedelta, timezone
from typing import Any, Optional

from flet.core.control import BaseControl, Control
from flet.core.object_patch import ObjectPatch
from flet.core.page import Page, _session_page
from flet.messaging.connection import Connection
from flet.messaging.protocol import (
    ClientAction,
    ClientMessage,
    PatchControlBody,
    SessionCrashedBody,
)
from flet.pubsub.pubsub_client import PubSubClient
from flet.utils.patch_dataclass import patch_dataclass
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
    def connection(self) -> Connection:
        if conn := self.__conn():
            return conn
        raise Exception("An attempt to use destroyed connection.")

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
    def page(self):
        return self.__page

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

    def patch_control(self, control: BaseControl):
        patch = self.__get_update_control_patch(control=control, prev_control=control)
        self.connection.send_message(
            ClientMessage(
                ClientAction.PATCH_CONTROL, PatchControlBody(control._i, patch)
            )
        )

    def apply_patch(self, control_id: int, patch: dict[str, Any]):
        if control := self.__index.get(control_id):
            patch_dataclass(control, patch)
            # print("patch_dataclass:", control)

    def apply_page_patch(self, patch: dict[str, Any]):
        self.apply_patch(self.__page._i, patch)

    def get_page_patch(self):
        return self.__get_update_control_patch(self.__page, prev_control=None)[""]

    def error(self, message: str):
        self.connection.send_message(
            ClientMessage(ClientAction.SESSION_CRASHED, SessionCrashedBody(message))
        )

    def __get_update_control_patch(
        self, control: BaseControl, prev_control: Optional[BaseControl]
    ):
        # calculate patch
        patch = ObjectPatch.from_diff(
            prev_control,
            control,
            in_place=True,
            controls_index=self.__index,
            control_cls=BaseControl,
        )

        return patch.to_graph()
