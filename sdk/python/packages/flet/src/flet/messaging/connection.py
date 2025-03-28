import logging
from typing import Optional

import flet.core
from flet.messaging.protocol import ClientMessage
from flet.pubsub.pubsub_hub import PubSubHub

logger = logging.getLogger(flet.__name__)


class Connection:
    def __init__(self):
        self.page_name: str = ""
        self.page_url: Optional[str] = None
        self.pubsubhub = PubSubHub()

    def send_message(self, message: ClientMessage):
        raise NotImplementedError()

    def dispose(self):
        pass
