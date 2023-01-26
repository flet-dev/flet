import json
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


class CommandEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Message):
            return obj.__dict__
        elif isinstance(obj, ClientMessage):
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


#
# Local client protocol for desktop apps
#


class ClientActions:
    REGISTER_WEB_CLIENT = "registerWebClient"
    PAGE_EVENT_FROM_WEB = "pageEventFromWeb"
    SESSION_CRASHED = "sessionCrashed"
    INVOKE_METHOD = "invokeMethod"
    PAGE_CONTROLS_BATCH = "pageControlsBatch"
    ADD_PAGE_CONTROLS = "addPageControls"
    UPDATE_CONTROL_PROPS = "updateControlProps"
    CLEAN_CONTROL = "cleanControl"
    REMOVE_CONTROL = "removeControl"


@dataclass
class ClientMessage:
    action: str
    payload: Any


@dataclass
class RegisterWebClientRequestPayload:
    pageName: str
    pageRoute: str
    pageWidth: str
    pageHeight: str
    windowWidth: str
    windowHeight: str
    windowTop: str
    windowLeft: str
    isPWA: str
    isWeb: str
    platform: str
    sessionId: str


@dataclass
class SessionPayload:
    id: str
    controls: Dict[str, Dict[str, Any]]


@dataclass
class RegisterWebClientResponsePayload:
    session: SessionPayload
    error: str
    appInactive: bool


@dataclass
class PageEventFromWebPayload:
    eventTarget: str
    eventName: str
    eventData: str


@dataclass
class SessionCrashedPayload:
    message: str


@dataclass
class InvokeMethodPayload:
    methodId: str
    methodName: str
    arguments: Dict[str, str]


@dataclass
class AddPageControlsPayload:
    controls: List[Dict[str, Any]]
    trimIDs: List[str] = field(default_factory=lambda: [])


@dataclass
class UpdateControlPropsPayload:
    props: List[Dict[str, str]]


@dataclass
class CleanControlPayload:
    ids: List[str]


@dataclass
class RemoveControlPayload:
    ids: List[str]
