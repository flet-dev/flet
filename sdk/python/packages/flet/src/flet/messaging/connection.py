import logging
from asyncio import AbstractEventLoop
from concurrent.futures import ThreadPoolExecutor
from typing import Any, Optional

from flet.messaging.protocol import ClientMessage
from flet.pubsub.pubsub_hub import PubSubHub

logger = logging.getLogger("flet")


class Connection:
    """
    Base messaging connection interface used by a Flet session.

    Concrete implementations provide transport-specific behavior (for example,
    socket or browser-backed messaging) and must implement message sending and
    platform-specific service methods.
    """

    def __init__(self):
        self.page_name: str = ""
        self.page_url: Optional[str] = None
        self.__pubsubhub = None
        self.__loop: Optional[AbstractEventLoop] = None
        self.__executor: Optional[ThreadPoolExecutor] = None

    @property
    def loop(self) -> AbstractEventLoop:
        """
        Returns the event loop associated with this connection.

        Returns:
            Initialized asyncio event loop.

        Raises:
            RuntimeError: If the loop has not been assigned.
        """
        if self.__loop is None:
            raise RuntimeError("Loop not initialized")
        return self.__loop

    @loop.setter
    def loop(self, value):
        self.__loop = value

    @property
    def executor(self) -> ThreadPoolExecutor:
        """
        Returns the thread pool executor used by this connection.

        Returns:
            Initialized thread pool executor.

        Raises:
            RuntimeError: If the executor has not been assigned.
        """
        if self.__executor is None:
            raise RuntimeError("Executor not initialized")
        return self.__executor

    @executor.setter
    def executor(self, value):
        self.__executor = value

    @property
    def pubsubhub(self) -> PubSubHub:
        """
        Returns the pub/sub hub used to broadcast session messages.

        Returns:
            Initialized pub/sub hub instance.

        Raises:
            RuntimeError: If the pub/sub hub has not been assigned.
        """
        if self.__pubsubhub is None:
            raise RuntimeError("PubSubHub not initialized")
        return self.__pubsubhub

    @pubsubhub.setter
    def pubsubhub(self, value: PubSubHub):
        self.__pubsubhub = value

    def send_message(self, message: ClientMessage):
        """
        Sends a message to the connected Flet client.

        Args:
            message: Client message to send.
        """
        raise NotImplementedError()

    def get_upload_url(self, file_name: str, expires: int) -> str:
        """
        Returns an upload URL for built-in file upload storage.

        Args:
            file_name: Relative path of the file in upload storage.
            expires: URL expiration time in seconds.

        Returns:
            The upload URL.
        """
        raise NotImplementedError()

    def oauth_authorize(self, attrs: dict[str, Any]):
        """
        Initiates OAuth authorization on the client side.

        Args:
            attrs: Authorization attributes passed to the client transport.
        """
        raise NotImplementedError()

    def dispose(self):
        """
        Releases connection resources associated with the current session.

        Subclasses can override this method to clean up transport-specific state.
        """
        pass
