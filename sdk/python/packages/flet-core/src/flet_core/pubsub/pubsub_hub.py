import asyncio
import logging
import threading
from concurrent.futures import ThreadPoolExecutor
from typing import Any, Awaitable, Callable, Dict, Iterable, Optional, Union

import flet_core
from flet_core.locks import NopeLock
from flet_core.utils.concurrency_utils import is_pyodide

logger = logging.getLogger(flet_core.__name__)


class PubSubHub:
    def __init__(
        self,
        loop: Optional[asyncio.AbstractEventLoop] = None,
        executor: Optional[ThreadPoolExecutor] = None,
    ):
        logger.debug("Creating new PubSubHub instance")
        self.__loop = loop
        self.__executor = executor
        self.__lock = threading.Lock() if not is_pyodide() else NopeLock()
        self.__subscribers: Dict[
            str, Union[Callable, Callable[..., Awaitable[Any]]]
        ] = {}  # key: session_id, value: handler
        self.__topic_subscribers: Dict[
            str, Dict[str, Union[Callable, Callable[..., Awaitable[Any]]]]
        ] = {}  # key: topic, value: dict[session_id, handler]
        self.__subscriber_topics: Dict[
            str, Dict[str, Union[Callable, Callable[..., Awaitable[Any]]]]
        ] = {}  # key: session_id, value: dict[topic, handler]

    def send_all(self, message: Any):
        logger.debug(f"pubsub.send_all({message})")
        with self.__lock:
            for handler in self.__subscribers.values():
                self.__send(handler, [message])

    def send_all_on_topic(self, topic: str, message: Any):
        logger.debug(f"pubsub.send_all_on_topic({topic}, {message})")
        with self.__lock:
            if topic in self.__topic_subscribers:
                for handler in self.__topic_subscribers[topic].values():
                    self.__send(handler, [topic, message])

    def send_others(self, except_session_id: str, message: Any):
        logger.debug(f"pubsub.send_others({except_session_id}, {message})")
        with self.__lock:
            for session_id, handler in self.__subscribers.items():
                if except_session_id != session_id:
                    self.__send(handler, [message])

    def send_others_on_topic(self, except_session_id: str, topic: str, message: Any):
        logger.debug(
            f"pubsub.send_others_on_topic({except_session_id}, {topic}, {message})"
        )
        with self.__lock:
            if topic in self.__topic_subscribers:
                for session_id, handler in self.__topic_subscribers[topic].items():
                    if except_session_id != session_id:
                        self.__send(handler, [topic, message])

    def subscribe(self, session_id: str, handler: Callable):
        logger.debug(f"pubsub.subscribe({session_id})")
        with self.__lock:
            self.__subscribers[session_id] = handler

    def subscribe_topic(
        self,
        session_id: str,
        topic: str,
        handler: Union[Callable, Callable[..., Awaitable[Any]]],
    ):
        logger.debug(f"pubsub.subscribe_topic({session_id}, {topic})")
        with self.__lock:
            self.__subscribe_topic(session_id, topic, handler)

    def __subscribe_topic(
        self,
        session_id: str,
        topic: str,
        handler: Union[Callable, Callable[..., Awaitable[Any]]],
    ):
        topic_subscribers = self.__topic_subscribers.get(topic)
        if topic_subscribers is None:
            topic_subscribers = {}
            self.__topic_subscribers[topic] = topic_subscribers
        topic_subscribers[session_id] = handler
        subscriber_topics = self.__subscriber_topics.get(session_id)
        if subscriber_topics is None:
            subscriber_topics = {}
            self.__subscriber_topics[session_id] = subscriber_topics
        subscriber_topics[topic] = handler

    def unsubscribe(self, session_id: str):
        logger.debug(f"pubsub.unsubscribe({session_id})")
        with self.__lock:
            self.__unsubscribe(session_id)

    def unsubscribe_topic(self, session_id: str, topic: str):
        logger.debug(f"pubsub.unsubscribe({session_id}, {topic})")
        with self.__lock:
            self.__unsubscribe_topic(session_id, topic)

    def unsubscribe_all(self, session_id: str):
        logger.debug(f"pubsub.unsubscribe_all({session_id})")
        with self.__lock:
            self.__unsubscribe(session_id)
            if session_id in self.__subscriber_topics:
                for topic in self.__subscriber_topics[session_id].keys():
                    self.__unsubscribe_topic(session_id, topic)

    def __unsubscribe(self, session_id: str):
        logger.debug(f"pubsub.__unsubscribe({session_id})")
        self.__subscribers.pop(session_id, None)

    def __unsubscribe_topic(self, session_id: str, topic: str):
        logger.debug(f"pubsub.__unsubscribe_topic({session_id}, {topic})")
        topic_subscribers = self.__topic_subscribers.get(topic)
        if topic_subscribers is not None:
            topic_subscribers.pop(session_id, None)
            if len(topic_subscribers) == 0:
                self.__topic_subscribers.pop(topic, None)
        subscriber_topics = self.__subscriber_topics.get(session_id)
        if subscriber_topics is not None:
            subscriber_topics.pop(topic, None)
            if len(subscriber_topics) == 0:
                self.__subscriber_topics.pop(session_id, None)

    def __send(
        self, handler: Union[Callable, Callable[..., Awaitable[Any]]], args: Iterable
    ):
        assert self.__loop, "PubSub event loop is not set"

        if asyncio.iscoroutinefunction(handler):
            asyncio.run_coroutine_threadsafe(handler(*args), self.__loop)
        else:
            if self.__executor:
                self.__loop.call_soon_threadsafe(
                    self.__loop.run_in_executor, self.__executor, handler, *args
                )
            else:
                handler(*args)
