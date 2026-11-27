"""Tests for `PubSubHub`."""

import asyncio
import threading

import pytest

from flet.pubsub.pubsub_hub import PubSubHub

# Upper bound for a publish to return.
TIMEOUT = 5.0


class TestPubSubDelivery:
    """PubSub calls its subscribers after releasing its lock."""

    @pytest.mark.asyncio
    async def test_subscriber_can_unsubscribe_while_receiving(self):
        """A subscriber called inline can unsubscribe without blocking the publish."""
        hub = PubSubHub(loop=asyncio.get_running_loop())
        received = []

        def subscriber(message):
            received.append(message)
            hub.unsubscribe("session")

        hub.subscribe("session", subscriber)
        publish = threading.Thread(target=hub.send_all, args=["hello"], daemon=True)
        publish.start()
        publish.join(TIMEOUT)

        assert not publish.is_alive()
        assert received == ["hello"]
