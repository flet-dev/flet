from typing import List, Optional
from flet.protocol import Command
from flet.pubsub import PubSubHub


class Connection:
    def __init__(self):
        self.host_client_id: Optional[str] = None
        self.page_name: Optional[str] = None
        self.page_url: Optional[str] = None
        self.sessions = {}
        self.pubsubhub = PubSubHub()

    def send_command(self, session_id: str, command: Command):
        raise NotImplementedError()

    def send_commands(self, session_id: str, commands: List[Command]):
        raise NotImplementedError()

    def close(self):
        raise NotImplementedError()
