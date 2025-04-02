import json
from dataclasses import dataclass, fields, is_dataclass
from enum import Enum
from typing import Any, Dict


def encode_object_for_msgpack(obj):
    if is_dataclass(obj):
        r = {}
        for field in fields(obj):
            if "skip" in field.metadata:  # or hasattr(obj, f"_prev_{field.name}"):
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
            elif field.name.startswith("on_"):
                v = v is not None
                if v:
                    r[field.name] = v
            elif v != field.default:
                r[field.name] = v
            setattr(obj, f"_prev_{field.name}", v)
        return r
    elif isinstance(obj, Enum):
        return obj.value
    return obj


class ClientAction(Enum):
    REGISTER_CLIENT = 1
    PATCH_CONTROL = 2
    CONTROL_EVENT = 3
    UPDATE_CONTROL_PROPS = 4
    INVOKE_METHOD = 5
    SESSION_CRASHED = 6


@dataclass
class ClientMessage:
    action: ClientAction
    body: Any


@dataclass
class RegisterClientRequestBody:
    session_id: str
    page_name: str
    page: dict[str, Any]


@dataclass
class SessionPayload:
    id: str
    controls: Dict[str, Dict[str, Any]]


@dataclass
class RegisterClientResponseBody:
    session_id: str
    page_patch: Any
    error: str


@dataclass
class PatchControlBody:
    id: int
    patch: Any


@dataclass
class UpdateControlPropsBody:
    id: int
    props: Any


@dataclass
class ControlEventBody:
    target: int
    name: str
    data: Any


@dataclass
class SessionCrashedBody:
    message: str


@dataclass
class InvokeMethodRequestBody:
    control_id: int
    call_id: str
    name: str
    args: Dict[str, Any]


@dataclass
class InvokeMethodResponseBody:
    control_id: int
    call_id: str
    result: Any
    error: str
