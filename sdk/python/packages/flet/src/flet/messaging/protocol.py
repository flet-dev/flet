import json
from dataclasses import dataclass, field, fields, is_dataclass
from enum import Enum
from typing import Any, Dict, List, Optional


def encode_object_for_msgpack(obj):
    if is_dataclass(obj):
        r = {}
        for field in fields(obj):
            if "skip" in field.metadata:
                continue
            v = getattr(obj, field.name)
            if isinstance(v, list):
                v = v[:]
                if len(v) > 0:
                    r[field.name] = v
            elif isinstance(v, dict):
                v = v.copy()
                if len(v) > 0:
                    r[field.name] = v
            elif field.name.startswith("on_") and v is not None:
                v = True
                r[field.name] = v
            elif v is not None:
                r[field.name] = v
            setattr(obj, f"_prev_{field.name}", v)
        return r
    elif isinstance(obj, Enum):
        return obj.value
    return obj


class CommandEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, ClientMessage):
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


@dataclass
class Command:
    indent: int
    name: Optional[str]
    values: List[str] = field(default_factory=list)
    attrs: Dict[str, str] = field(default_factory=dict)
    commands: List[Any] = field(default_factory=list)

    def __str__(self):
        return f"{self.name} {self.values} {self.attrs}"


@dataclass
class PageCommandResponsePayload:
    result: str
    error: str


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
class PageSessionCreatedPayload:
    pageName: str
    sessionID: str


class ClientAction:
    REGISTER_CLIENT = 1
    PATCH_CLIENT = 2
    CONTROL_EVENT = 3
    CONTROL_PROPS = 4
    INVOKE_METHOD = 5
    SESSION_CRASHED = 6


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
    isDebug: str
    platform: str
    platformBrightness: str
    media: str
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
    controlId: str
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
