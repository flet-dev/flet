import logging
from typing import Any, Callable

import flet_core
from flet_core.pubsub.pubsub_hub import PubSubHub
from flet_core.utils.deprecated import deprecated

logger = logging.getLogger(flet_core.__name__)


class PubSubClient:
    def __init__(self, pubsub: PubSubHub, session_id: str):
        self.__pubsub = pubsub
        self.__session_id = session_id

    def send_all(self, message: Any):
        self.__pubsub.send_all(message)

    @deprecated(
        reason="Use send_all() method instead.",
        version="0.21.0",
        delete_version="1.0",
    )
    async def send_all_async(self, message: Any):
        self.send_all(message)

    def send_all_on_topic(self, topic: str, message: Any):
        self.__pubsub.send_all_on_topic(topic, message)

    @deprecated(
        reason="Use send_all_on_topic() method instead.",
        version="0.21.0",
        delete_version="1.0",
    )
    async def send_all_on_topic_async(self, topic: str, message: Any):
        self.send_all_on_topic(topic, message)

    def send_others(self, message: Any):
        self.__pubsub.send_others(self.__session_id, message)

    @deprecated(
        reason="Use send_others() method instead.",
        version="0.21.0",
        delete_version="1.0",
    )
    async def send_others_async(self, message: Any):
        self.send_others(message)

    def send_others_on_topic(self, topic: str, message: Any):
        self.__pubsub.send_others_on_topic(self.__session_id, topic, message)

    @deprecated(
        reason="Use send_others_on_topic() method instead.",
        version="0.21.0",
        delete_version="1.0",
    )
    async def send_others_on_topic_async(self, topic: str, message: Any):
        self.send_others_on_topic(topic, message)

    def subscribe(self, handler: Callable):
        self.__pubsub.subscribe(self.__session_id, handler)

    @deprecated(
        reason="Use subscribe() method instead.",
        version="0.21.0",
        delete_version="1.0",
    )
    async def subscribe_async(self, handler: Callable):
        self.subscribe(handler)

    def subscribe_topic(self, topic: str, handler: Callable):
        self.__pubsub.subscribe_topic(self.__session_id, topic, handler)

    @deprecated(
        reason="Use subscribe_topic() method instead.",
        version="0.21.0",
        delete_version="1.0",
    )
    async def subscribe_topic_async(self, topic: str, handler: Callable):
        self.subscribe_topic(topic, handler)

    def unsubscribe(self):
        self.__pubsub.unsubscribe(self.__session_id)

    @deprecated(
        reason="Use unsubscribe() method instead.",
        version="0.21.0",
        delete_version="1.0",
    )
    async def unsubscribe_async(self):
        self.unsubscribe()

    def unsubscribe_topic(self, topic: str):
        self.__pubsub.unsubscribe_topic(self.__session_id, topic)

    @deprecated(
        reason="Use unsubscribe_topic() method instead.",
        version="0.21.0",
        delete_version="1.0",
    )
    async def unsubscribe_topic_async(self, topic: str):
        self.unsubscribe_topic(topic)

    def unsubscribe_all(self):
        self.__pubsub.unsubscribe_all(self.__session_id)

    @deprecated(
        reason="Use unsubscribe_all() method instead.",
        version="0.21.0",
        delete_version="1.0",
    )
    async def unsubscribe_all_async(self):
        self.unsubscribe_all()
