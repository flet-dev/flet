from typing import List, Optional

from flet_core.protocol import Command

try:
    from flet.pubsub import PubSubHub
except ImportError:

    class PubSubHub:
        pass


class Connection:
    def __init__(self):
        self.page_name: str = ""
        self.page_url: Optional[str] = None
        self.sessions = {}
        self.pubsubhub = PubSubHub()

    def send_command(self, session_id: str, command: Command):
        raise NotImplementedError()

    async def send_command_async(self, session_id: str, command: Command):
        raise NotImplementedError()

    def send_commands(self, session_id: str, commands: List[Command]):
        raise NotImplementedError()

    async def send_commands_async(self, session_id: str, commands: List[Command]):
        raise NotImplementedError()

    def _get_ws_url(self, server: str):
        url = server.rstrip("/")
        if server.startswith("https://"):
            url = url.replace("https://", "wss://")
        elif server.startswith("http://"):
            url = url.replace("http://", "ws://")
        else:
            url = "ws://" + url
        return url + "/ws"
