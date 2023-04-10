import asyncio
import logging
import threading
from typing import Any, Callable, Dict, Iterable

import flet
from flet_core.locks import AsyncNopeLock, NopeLock
from flet_core.utils import is_asyncio

logger = logging.getLogger(flet.__name__)


class PubSubHub:
    def __init__(self):
        self.__lock = threading.Lock() if not is_asyncio() else NopeLock()
        self.__async_lock = asyncio.Lock() if is_asyncio() else AsyncNopeLock()
        self.__subscribers: Dict[str, Callable] = {}  # key: session_id, value: handler
        self.__topic_subscribers: Dict[
            str, Dict[str, Callable]
        ] = {}  # key: topic, value: dict[session_id, handler]
        self.__subscriber_topics: Dict[
            str, Dict[str, Callable]
        ] = {}  # key: session_id, value: dict[topic, handler]

    def send_all(self, message: Any):
        logger.debug(f"pubsub.send_all({message})")
        with self.__lock:
            for handler in self.__subscribers.values():
                self.__send(handler, [message])

    async def send_all_async(self, message: Any):
        logger.debug(f"pubsub.send_all_async({message})")
        async with self.__async_lock:
            for handler in self.__subscribers.values():
                await self.__send_async(handler, [message])

    def send_all_on_topic(self, topic: str, message: Any):
        logger.debug(f"pubsub.send_all_on_topic({topic}, {message})")
        with self.__lock:
            if topic in self.__topic_subscribers:
                for handler in self.__topic_subscribers[topic].values():
                    self.__send(handler, [topic, message])

    async def send_all_on_topic_async(self, topic: str, message: Any):
        logger.debug(f"pubsub.send_all_on_topic_async({topic}, {message})")
        async with self.__async_lock:
            if topic in self.__topic_subscribers:
                for handler in self.__topic_subscribers[topic].values():
                    await self.__send_async(handler, [topic, message])

    def send_others(self, except_session_id: str, message: Any):
        logger.debug(f"pubsub.send_others({except_session_id}, {message})")
        with self.__lock:
            for session_id, handler in self.__subscribers.items():
                if except_session_id != session_id:
                    self.__send(handler, [message])

    async def send_others_async(self, except_session_id: str, message: Any):
        logger.debug(f"pubsub.send_others_async({except_session_id}, {message})")
        async with self.__async_lock:
            for session_id, handler in self.__subscribers.items():
                if except_session_id != session_id:
                    await self.__send_async(handler, [message])

    def send_others_on_topic(self, except_session_id: str, topic: str, message: Any):
        logger.debug(
            f"pubsub.send_others_on_topic({except_session_id}, {topic}, {message})"
        )
        with self.__lock:
            if topic in self.__topic_subscribers:
                for session_id, handler in self.__topic_subscribers[topic].items():
                    if except_session_id != session_id:
                        self.__send(handler, [topic, message])

    async def send_others_on_topic_async(
        self, except_session_id: str, topic: str, message: Any
    ):
        logger.debug(
            f"pubsub.send_others_on_topic_async({except_session_id}, {topic}, {message})"
        )
        async with self.__async_lock:
            if topic in self.__topic_subscribers:
                for session_id, handler in self.__topic_subscribers[topic].items():
                    if except_session_id != session_id:
                        await self.__send_async(handler, [topic, message])

    def subscribe(self, session_id: str, handler: Callable):
        logger.debug(f"pubsub.subscribe({session_id})")
        with self.__lock:
            self.__subscribers[session_id] = handler

    async def subscribe_async(self, session_id: str, handler):
        logger.debug(f"pubsub.subscribe_async({session_id})")
        async with self.__async_lock:
            self.__subscribers[session_id] = handler

    def subscribe_topic(self, session_id: str, topic: str, handler: Callable):
        logger.debug(f"pubsub.subscribe_topic({session_id}, {topic})")
        with self.__lock:
            self.__subscribe_topic(session_id, topic, handler)

    async def subscribe_topic_async(self, session_id: str, topic: str, handler):
        logger.debug(f"pubsub.subscribe_topic_async({session_id}, {topic})")
        async with self.__async_lock:
            self.__subscribe_topic(session_id, topic, handler)

    def __subscribe_topic(self, session_id: str, topic: str, handler):
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

    async def unsubscribe_async(self, session_id: str):
        logger.debug(f"pubsub.unsubscribe_async({session_id})")
        async with self.__async_lock:
            self.__unsubscribe(session_id)

    def unsubscribe_topic(self, session_id: str, topic: str):
        logger.debug(f"pubsub.unsubscribe({session_id}, {topic})")
        with self.__lock:
            self.__unsubscribe_topic(session_id, topic)

    async def unsubscribe_topic_async(self, session_id: str, topic: str):
        logger.debug(f"pubsub.unsubscribe_topic_async({session_id}, {topic})")
        async with self.__async_lock:
            self.__unsubscribe_topic(session_id, topic)

    def unsubscribe_all(self, session_id: str):
        logger.debug(f"pubsub.unsubscribe_all({session_id})")
        with self.__lock:
            self.__unsubscribe(session_id)
            if session_id in self.__subscriber_topics:
                for topic in self.__subscriber_topics[session_id].keys():
                    self.__unsubscribe_topic(session_id, topic)

    async def unsubscribe_all_async(self, session_id: str):
        logger.debug(f"pubsub.unsubscribe_all_async({session_id})")
        async with self.__async_lock:
            self.__unsubscribe(session_id)
            if session_id in self.__subscriber_topics:
                for topic in self.__subscriber_topics[session_id].keys():
                    self.__unsubscribe_topic(session_id, topic)

    def __unsubscribe(self, session_id: str):
        logger.debug(f"pubsub.__unsubscribe({session_id})")
        self.__subscribers.pop(session_id)

    def __unsubscribe_topic(self, session_id: str, topic: str):
        logger.debug(f"pubsub.__unsubscribe_topic({session_id}, {topic})")
        topic_subscribers = self.__topic_subscribers.get(topic)
        if topic_subscribers is not None:
            topic_subscribers.pop(session_id)
            if len(topic_subscribers) == 0:
                self.__topic_subscribers.pop(topic)
        subscriber_topics = self.__subscriber_topics.get(session_id)
        if subscriber_topics is not None:
            subscriber_topics.pop(topic)
            if len(subscriber_topics) == 0:
                self.__subscriber_topics.pop(session_id)

    def __send(self, handler: Callable, args: Iterable):
        th = threading.Thread(
            target=handler,
            args=args,
            daemon=True,
        )
        th.start()

    async def __send_async(self, handler, args):
        asyncio.create_task(handler(*args))


class PubSub:
    def __init__(self, pubsub: PubSubHub, session_id: str):
        self.__pubsub = pubsub
        self.__session_id = session_id

    def send_all(self, message: Any):
        self.__pubsub.send_all(message)

    async def send_all_async(self, message: Any):
        await self.__pubsub.send_all_async(message)

    def send_all_on_topic(self, topic: str, message: Any):
        self.__pubsub.send_all_on_topic(topic, message)

    async def send_all_on_topic_async(self, topic: str, message: Any):
        await self.__pubsub.send_all_on_topic_async(topic, message)

    def send_others(self, message: Any):
        self.__pubsub.send_others(self.__session_id, message)

    async def send_others_async(self, message: Any):
        await self.__pubsub.send_others_async(self.__session_id, message)

    def send_others_on_topic(self, topic: str, message: Any):
        self.__pubsub.send_others_on_topic(self.__session_id, topic, message)

    async def send_others_on_topic_async(self, topic: str, message: Any):
        await self.__pubsub.send_others_on_topic_async(
            self.__session_id, topic, message
        )

    def subscribe(self, handler: Callable):
        self.__pubsub.subscribe(self.__session_id, handler)

    async def subscribe_async(self, handler: Callable):
        await self.__pubsub.subscribe_async(self.__session_id, handler)

    def subscribe_topic(self, topic: str, handler: Callable):
        self.__pubsub.subscribe_topic(self.__session_id, topic, handler)

    async def subscribe_topic_async(self, topic: str, handler: Callable):
        await self.__pubsub.subscribe_topic_async(self.__session_id, topic, handler)

    def unsubscribe(self):
        self.__pubsub.unsubscribe(self.__session_id)

    async def unsubscribe_async(self):
        await self.__pubsub.unsubscribe_async(self.__session_id)

    def unsubscribe_topic(self, topic: str):
        self.__pubsub.unsubscribe_topic(self.__session_id, topic)

    async def unsubscribe_topic_async(self, topic: str):
        await self.__pubsub.unsubscribe_topic_async(self.__session_id, topic)

    def unsubscribe_all(self):
        self.__pubsub.unsubscribe_all(self.__session_id)

    async def unsubscribe_all_async(self):
        await self.__pubsub.unsubscribe_all_async(self.__session_id)
