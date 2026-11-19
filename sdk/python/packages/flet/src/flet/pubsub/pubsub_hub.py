import asyncio
import inspect
import logging
import threading
from collections.abc import Awaitable, Iterable
from concurrent.futures import Future, ThreadPoolExecutor
from functools import partial
from typing import Any, Callable, Optional, Union

from flet.utils import is_pyodide
from flet.utils.locks import NopeLock

logger = logging.getLogger("flet")


def _log_subscriber_error(handler: Callable, exception: BaseException) -> None:
    """Log an exception raised by a subscriber on the `flet` logger."""
    logger.error(
        "Unhandled error in PubSub subscriber %s",
        getattr(handler, "__qualname__", None) or repr(handler),
        exc_info=exception,
    )


def _on_async_subscriber_done(handler: Callable, future: Future) -> None:
    """Log the exception an async subscriber raised, if any."""
    if not future.cancelled() and (exception := future.exception()) is not None:
        _log_subscriber_error(handler, exception)


def _call_subscriber(handler: Callable, *args: Any) -> None:
    """Call a sync subscriber, logging an exception it raises."""
    try:
        handler(*args)
    except Exception as e:
        _log_subscriber_error(handler, e)


class PubSubHub:
    """
    Thread-safe in-memory pub/sub router scoped to a Flet server process.

    Subscribers are grouped by session ID and optionally by topic. Handlers can
    be synchronous callables or async coroutine functions:
    - global subscribers receive `(message)`;
    - topic subscribers receive `(topic, message)`.

    This hub is used by session-scoped `PubSubClient`
    instances to fan out messages between connected sessions.
    """

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
        """
        Sends a message to all global subscribers across all sessions.

        Args:
            message: Payload to deliver.
        """
        logger.debug("pubsub.send_all(%s)", message)
        with self.__lock:
            handlers = [h for hs in self.__subscribers.values() for h in hs]
        self.__send_to(handlers, [message])

    def send_all_on_topic(self, topic: str, message: Any):
        """
        Sends a topic message to all subscribers of `topic`.

        Args:
            topic: Topic name to broadcast on.
            message: Payload to deliver.
        """
        logger.debug("pubsub.send_all_on_topic(%s, %s)", topic, message)
        with self.__lock:
            handlers = [
                h for hs in self.__topic_subscribers.get(topic, {}).values() for h in hs
            ]
        self.__send_to(handlers, [topic, message])

    def send_others(self, except_session_id: str, message: Any):
        """
        Sends a global message to all sessions except one.

        Args:
            except_session_id: Session ID to exclude from delivery.
            message: Payload to deliver.
        """
        logger.debug("pubsub.send_others(%s, %s)", except_session_id, message)
        with self.__lock:
            handlers = [
                h
                for session_id, hs in self.__subscribers.items()
                if session_id != except_session_id
                for h in hs
            ]
        self.__send_to(handlers, [message])

    def send_others_on_topic(self, except_session_id: str, topic: str, message: Any):
        """
        Sends a topic message to all subscribers except one session.

        Args:
            except_session_id: Session ID to exclude from delivery.
            topic: Topic name to publish on.
            message: Payload to deliver.
        """
        logger.debug(
            "pubsub.send_others_on_topic(%s, %s, %s)", except_session_id, topic, message
        )
        with self.__lock:
            handlers = [
                h
                for session_id, hs in self.__topic_subscribers.get(topic, {}).items()
                if session_id != except_session_id
                for h in hs
            ]
        self.__send_to(handlers, [topic, message])

    def subscribe(self, session_id: str, handler: Callable):
        """
        Registers a global subscriber for a session.

        The handler will receive one positional argument: `message`.
        Duplicate registrations of the same handler are ignored because
        handlers are stored in a set.

        Args:
            session_id: Session identifier that owns this subscription.
            handler: Sync or async callback invoked for global messages.
        """
        logger.debug("pubsub.subscribe(%s)", session_id)
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
        """
        Registers a topic subscriber for a session.

        The handler will receive two positional arguments: `(topic, message)`.

        Args:
            session_id: Session identifier that owns this subscription.
            topic: Topic name to subscribe to.
            handler: Sync or async callback invoked for topic messages.
        """
        logger.debug("pubsub.subscribe_topic(%s, %s)", session_id, topic)
        with self.__lock:
            self.__subscribe_topic(session_id, topic, handler)

    def __subscribe_topic(
        self,
        session_id: str,
        topic: str,
        handler: Union[Callable, Callable[..., Awaitable[Any]]],
    ):
        """
        Internal implementation of topic subscription bookkeeping.

        Maintains both forward (`topic -> session -> handlers`) and reverse
        (`session -> topic -> handlers`) indexes for efficient publish and
        cleanup operations.

        Args:
            session_id: Session identifier that owns this subscription.
            topic: Topic name to subscribe to.
            handler: Sync or async callback invoked for topic messages.
        """
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
        """
        Removes all global subscribers for a session.

        This does not remove topic subscriptions; use
        :meth:`unsubscribe_all` to remove both.

        Args:
            session_id: Session identifier to remove.
        """
        logger.debug("pubsub.unsubscribe(%s)", session_id)
        with self.__lock:
            self.__unsubscribe(session_id)

    def unsubscribe_topic(self, session_id: str, topic: str):
        """
        Removes all handlers for a specific session/topic pair.

        Args:
            session_id: Session identifier to remove from the topic.
            topic: Topic to unsubscribe from.
        """
        logger.debug("pubsub.unsubscribe(%s, %s)", session_id, topic)
        with self.__lock:
            self.__unsubscribe_topic(session_id, topic)

    def unsubscribe_all(self, session_id: str):
        """
        Removes both global and topic subscriptions for a session.

        Args:
            session_id: Session identifier to fully unsubscribe.
        """
        logger.debug("pubsub.unsubscribe_all(%s)", session_id)
        with self.__lock:
            self.__unsubscribe(session_id)
            if session_id in self.__subscriber_topics:
                for topic in list(self.__subscriber_topics[session_id].keys()):
                    self.__unsubscribe_topic(session_id, topic)

    def __unsubscribe(self, session_id: str):
        """
        Internal helper that removes global subscribers for a session.

        Args:
            session_id: Session identifier to remove.
        """
        logger.debug("pubsub.__unsubscribe(%s)", session_id)
        self.__subscribers.pop(session_id, None)

    def __unsubscribe_topic(self, session_id: str, topic: str):
        """
        Internal helper that removes one session/topic subscription entry.

        Cleans up empty topic and session containers after removal.

        Args:
            session_id: Session identifier to remove from the topic.
            topic: Topic to unsubscribe from.
        """
        logger.debug("pubsub.__unsubscribe_topic(%s, %s)", session_id, topic)
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

    def __send_to(
        self,
        handlers: list[Union[Callable, Callable[..., Awaitable[Any]]]],
        args: Iterable,
    ):
        """
        Dispatches a message to each of `handlers`.

        Called after releasing the hub lock, so subscribers and the logging of
        their errors can subscribe and unsubscribe.

        Args:
            handlers: Subscriber callbacks to invoke.
            args: Positional arguments to pass to each callback.
        """
        for handler in handlers:
            self.__send(handler, args)

    def __send(
        self, handler: Union[Callable, Callable[..., Awaitable[Any]]], args: Iterable
    ):
        """
        Dispatches a message to a handler in the configured execution context.

        Async handlers are scheduled on the hub event loop using
        `run_coroutine_threadsafe`. Sync handlers are either submitted to the
        configured executor or invoked inline when no executor is provided.

        Args:
            handler: Subscriber callback to invoke.
            args: Positional arguments to pass to the callback.

        Raises:
            RuntimeError: If the hub has no event loop configured.
        """
        if not self.__loop:
            raise RuntimeError("PubSub event loop is not set")

        if inspect.iscoroutinefunction(handler):
            try:
                coroutine = handler(*args)
            except Exception as e:
                # E.g. a subscriber that takes other arguments than it's sent.
                _log_subscriber_error(handler, e)
                return
            future = asyncio.run_coroutine_threadsafe(coroutine, self.__loop)
            future.add_done_callback(partial(_on_async_subscriber_done, handler))
        else:
            call = partial(_call_subscriber, handler, *args)
            if self.__executor:
                self.__loop.call_soon_threadsafe(
                    self.__loop.run_in_executor, self.__executor, call
                )
            else:
                call()
