import logging
from typing import Any, Callable

import flet.core
from flet.core.pubsub.pubsub_hub import PubSubHub

logger = logging.getLogger(flet.__name__)


class PubSubClient:
    def __init__(self, pubsub: PubSubHub, session_id: str):
        self.__pubsub = pubsub
        self.__session_id = session_id

    def send_all(self, message: Any):
        self.__pubsub.send_all(message)

    def send_all_on_topic(self, topic: str, message: Any):
        self.__pubsub.send_all_on_topic(topic, message)

    def send_others(self, message: Any):
        self.__pubsub.send_others(self.__session_id, message)

    def send_others_on_topic(self, topic: str, message: Any):
        self.__pubsub.send_others_on_topic(self.__session_id, topic, message)

    def subscribe(self, handler: Callable):
        self.__pubsub.subscribe(self.__session_id, handler)

    def subscribe_topic(self, topic: str, handler: Callable):
        self.__pubsub.subscribe_topic(self.__session_id, topic, handler)

    def unsubscribe(self):
        self.__pubsub.unsubscribe(self.__session_id)

    def unsubscribe_topic(self, topic: str):
        self.__pubsub.unsubscribe_topic(self.__session_id, topic)

    def unsubscribe_all(self):
        self.__pubsub.unsubscribe_all(self.__session_id)
