import asyncio
import inspect
import logging
import threading
from collections.abc import Awaitable, Iterable
from concurrent.futures import ThreadPoolExecutor
from typing import Any, Callable, Optional, Union

from flet.utils import is_pyodide
from flet.utils.locks import NopeLock

logger = logging.getLogger("flet")


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
        self.__subscribers: dict[
            str, set[Union[Callable, Callable[..., Awaitable[Any]]]]
        ] = {}  # key: session_id, value: handler
        self.__topic_subscribers: dict[
            str, dict[str, set[Union[Callable, Callable[..., Awaitable[Any]]]]]
        ] = {}  # key: topic, value: dict[session_id, handler]
        self.__subscriber_topics: dict[
            str, dict[str, set[Union[Callable, Callable[..., Awaitable[Any]]]]]
        ] = {}  # key: session_id, value: dict[topic, handler]

    def send_all(self, message: Any):
        logger.debug(f"pubsub.send_all({message})")
        with self.__lock:
            for handlers in self.__subscribers.values():
                for handler in handlers:
                    self.__send(handler, [message])

    def send_all_on_topic(self, topic: str, message: Any):
        logger.debug(f"pubsub.send_all_on_topic({topic}, {message})")
        with self.__lock:
            if topic in self.__topic_subscribers:
                for handlers in self.__topic_subscribers[topic].values():
                    for handler in handlers:
                        self.__send(handler, [topic, message])

    def send_others(self, except_session_id: str, message: Any):
        logger.debug(f"pubsub.send_others({except_session_id}, {message})")
        with self.__lock:
            for session_id, handlers in self.__subscribers.items():
                if except_session_id != session_id:
                    for handler in handlers:
                        self.__send(handler, [message])

    def send_others_on_topic(self, except_session_id: str, topic: str, message: Any):
        logger.debug(
            f"pubsub.send_others_on_topic({except_session_id}, {topic}, {message})"
        )
        with self.__lock:
            if topic in self.__topic_subscribers:
                for session_id, handlers in self.__topic_subscribers[topic].items():
                    if except_session_id != session_id:
                        for handler in handlers:
                            self.__send(handler, [topic, message])

    def subscribe(self, session_id: str, handler: Callable):
        logger.debug(f"pubsub.subscribe({session_id})")
        with self.__lock:
            handlers = self.__subscribers.get(session_id)
            if handlers is None:
                handlers = set()
                self.__subscribers[session_id] = handlers
            handlers.add(handler)

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
        handlers = topic_subscribers.get(session_id)
        if handlers is None:
            handlers = set()
            topic_subscribers[session_id] = handlers
        handlers.add(handler)
        subscriber_topics = self.__subscriber_topics.get(session_id)
        if subscriber_topics is None:
            subscriber_topics = {}
            self.__subscriber_topics[session_id] = subscriber_topics
        handlers = subscriber_topics.get(topic)
        if handlers is None:
            handlers = set()
            subscriber_topics[topic] = handlers
        handlers.add(handler)

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
                for topic in list(self.__subscriber_topics[session_id].keys()):
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
        if not self.__loop:
            raise RuntimeError("PubSub event loop is not set")

        if inspect.iscoroutinefunction(handler):
            asyncio.run_coroutine_threadsafe(handler(*args), self.__loop)
        else:
            if self.__executor:
                self.__loop.call_soon_threadsafe(
                    self.__loop.run_in_executor, self.__executor, handler, *args
                )
            else:
                handler(*args)
