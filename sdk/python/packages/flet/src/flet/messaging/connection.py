import logging
from asyncio import AbstractEventLoop
from concurrent.futures import ThreadPoolExecutor
from typing import Any, Optional

from flet.messaging.protocol import ClientMessage
from flet.pubsub.pubsub_hub import PubSubHub

logger = logging.getLogger("flet")


class Connection:
    def __init__(self):
        self.page_name: str = ""
        self.page_url: Optional[str] = None
        self.__pubsubhub = None
        self.__loop: Optional[AbstractEventLoop] = None
        self.__executor: Optional[ThreadPoolExecutor] = None

    @property
    def loop(self) -> AbstractEventLoop:
        if self.__loop is None:
            raise RuntimeError("Loop not initialized")
        return self.__loop

    @loop.setter
    def loop(self, value):
        self.__loop = value

    @property
    def executor(self) -> ThreadPoolExecutor:
        if self.__executor is None:
            raise RuntimeError("Executor not initialized")
        return self.__executor

    @executor.setter
    def executor(self, value):
        self.__executor = value

    @property
    def pubsubhub(self) -> PubSubHub:
        if self.__pubsubhub is None:
            raise RuntimeError("PubSubHub not initialized")
        return self.__pubsubhub

    @pubsubhub.setter
    def pubsubhub(self, value: PubSubHub):
        self.__pubsubhub = value

    def send_message(self, message: ClientMessage):
        raise NotImplementedError()

    def get_upload_url(self, file_name: str, expires: int) -> str:
        raise NotImplementedError()

    def oauth_authorize(self, attrs: dict[str, Any]):
        raise NotImplementedError()

    def dispose(self):
        pass
