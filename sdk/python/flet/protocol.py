import json
from dataclasses import dataclass, field
from typing import Any, List, Optional

from beartype.typing import Dict


class CommandEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Message):
            return obj.__dict__
        elif isinstance(obj, Command):
            d = {}
            if obj.indent > 0:
                d["i"] = obj.indent
            if obj.name is not None:
                d["n"] = obj.name
            if obj.values and len(obj.values) > 0:
                d["v"] = obj.values
            if obj.attrs and len(obj.attrs) > 0:
                d["a"] = obj.attrs
            if obj.commands and len(obj.commands) > 0:
                d["c"] = obj.commands
            return d
        elif isinstance(obj, object):
            return obj.__dict__
        return json.JSONEncoder.default(self, obj)


class Actions:
    REGISTER_HOST_CLIENT = "registerHostClient"
    SESSION_CREATED = "sessionCreated"
    PAGE_COMMAND_FROM_HOST = "pageCommandFromHost"
    PAGE_COMMANDS_BATCH_FROM_HOST = "pageCommandsBatchFromHost"
    PAGE_EVENT_TO_HOST = "pageEventToHost"


@dataclass
class Command:
    indent: int
    name: Optional[str]
    values: List[str] = field(default_factory=list)
    attrs: Dict[str, str] = field(default_factory=dict)
    commands: List[Any] = field(default_factory=list)


@dataclass
class Message:
    id: str
    action: str
    payload: Any


@dataclass
class PageCommandRequestPayload:
    pageName: str
    sessionID: str
    command: Command


@dataclass
class PageCommandResponsePayload:
    result: str
    error: str


@dataclass
class PageCommandsBatchRequestPayload:
    pageName: str
    sessionID: str
    commands: List[Command]


@dataclass
class PageCommandsBatchResponsePayload:
    results: List[str]
    error: str


@dataclass
class PageEventPayload:
    pageName: str
    sessionID: str
    eventTarget: str
    eventName: str
    eventData: str


@dataclass
class RegisterHostClientRequestPayload:
    hostClientID: Optional[str]
    pageName: str
    isApp: bool
    update: bool
    authToken: Optional[str]
    permissions: Optional[str]


@dataclass
class RegisterHostClientResponsePayload:
    hostClientID: str
    pageName: str
    sessionID: str
    error: str


@dataclass
class PageSessionCreatedPayload:
    pageName: str
    sessionID: str
