import logging
from typing import Any, Callable

from flet.pubsub.pubsub_hub import PubSubHub

logger = logging.getLogger("flet")


class PubSubClient:
    """
    Session-scoped facade over [`PubSubHub`][flet.PubSubHub].

    This client binds all pub/sub operations to one session ID so callers can
    publish and subscribe without passing their session identity explicitly on
    each call.
    """

    def __init__(self, pubsub: PubSubHub, session_id: str):
        self.__pubsub = pubsub
        self.__session_id = session_id

    def send_all(self, message: Any):
        """
        Broadcasts a global message to all sessions.

        Args:
            message: Payload to publish.
        """
        self.__pubsub.send_all(message)

    def send_all_on_topic(self, topic: str, message: Any):
        """
        Broadcasts a topic message to all subscribers of `topic`.

        Args:
            topic: Topic name to publish on.
            message: Payload to publish.
        """
        self.__pubsub.send_all_on_topic(topic, message)

    def send_others(self, message: Any):
        """
        Broadcasts a global message to all sessions except this client session.

        Args:
            message: Payload to publish.
        """
        self.__pubsub.send_others(self.__session_id, message)

    def send_others_on_topic(self, topic: str, message: Any):
        """
        Broadcasts a topic message excluding this client session.

        Args:
            topic: Topic name to publish on.
            message: Payload to publish.
        """
        self.__pubsub.send_others_on_topic(self.__session_id, topic, message)

    def subscribe(self, handler: Callable):
        """
        Subscribes this session to global messages.

        The handler is invoked with one positional argument: `message`.

        Args:
            handler: Sync or async callback for global messages.
        """
        self.__pubsub.subscribe(self.__session_id, handler)

    def subscribe_topic(self, topic: str, handler: Callable):
        """
        Subscribes this session to a topic.

        The handler is invoked with two positional arguments:
        `(topic, message)`.

        Args:
            topic: Topic name to subscribe to.
            handler: Sync or async callback for topic messages.
        """
        self.__pubsub.subscribe_topic(self.__session_id, topic, handler)

    def unsubscribe(self):
        """
        Removes global subscriptions for this session.
        """
        self.__pubsub.unsubscribe(self.__session_id)

    def unsubscribe_topic(self, topic: str):
        """
        Removes this session's subscriptions for a specific topic.

        Args:
            topic: Topic to unsubscribe from.
        """
        self.__pubsub.unsubscribe_topic(self.__session_id, topic)

    def unsubscribe_all(self):
        """
        Removes all global and topic subscriptions for this session.
        """
        self.__pubsub.unsubscribe_all(self.__session_id)
