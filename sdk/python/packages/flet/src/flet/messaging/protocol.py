import datetime
from dataclasses import dataclass, fields, is_dataclass
from enum import Enum
from typing import Any

import msgpack

from flet.controls.duration import Duration


def _get_root_dataclass_field(cls, field_name):
    """
    Returns the field definition from the earliest dataclass in the MRO
    that declares `field_name`. This lets us recover defaults configured
    on base controls before subclasses override them.
    """

    for base in reversed(cls.__mro__):
        dataclass_fields = getattr(base, "__dataclass_fields__", None)
        if dataclass_fields and field_name in dataclass_fields:
            return dataclass_fields[field_name]
    return None


def configure_encode_object_for_msgpack(control_cls):
    def encode_object_for_msgpack(obj):
        """Encode object for MessagePack."""
        if is_dataclass(obj):
            r = {}
            prev_lists = {}
            prev_dicts = {}
            prev_classes = {}
            for field in fields(obj):
                if "skip" in field.metadata:  # or hasattr(obj, f"_prev_{field.name}"):
                    continue
                v = getattr(obj, field.name)
                if isinstance(v, list):
                    v = v[:]
                    if len(v) > 0:
                        r[field.name] = v
                    prev_lists[field.name] = v
                elif isinstance(v, dict):
                    v = v.copy()
                    if len(v) > 0:
                        r[field.name] = v
                    prev_dicts[field.name] = v
                elif field.name.startswith("on_") and field.metadata.get("event", True):
                    v = v is not None
                    if v:
                        r[field.name] = v
                elif is_dataclass(v):
                    r[field.name] = v
                    prev_classes[field.name] = v
                else:
                    default_value = field.default
                    if isinstance(obj, control_cls):
                        root_field = _get_root_dataclass_field(
                            obj.__class__, field.name
                        )
                        if root_field is not None:
                            default_value = root_field.default
                    if v is not None and (
                        v != default_value or not isinstance(obj, control_cls)
                    ):
                        r[field.name] = v

            if not hasattr(obj, "_frozen"):
                setattr(obj, "__prev_lists", prev_lists)
                setattr(obj, "__prev_dicts", prev_dicts)
                setattr(obj, "__prev_classes", prev_classes)
            # print("__prev_cols", obj.__class__.__name__, prev_cols.keys())

            return r
        elif isinstance(obj, Enum):
            return obj.value
        elif isinstance(obj, (datetime.datetime, datetime.date)):
            if isinstance(obj, datetime.datetime):
                if obj.tzinfo is None:  # naive
                    try:
                        # May fail on Windows for out-of-range values.
                        # See: https://github.com/flet-dev/flet/issues/5895
                        obj = obj.astimezone()
                    except Exception:
                        # Attach current local tzinfo or UTC if that fails.
                        try:
                            tz = datetime.datetime.now().astimezone().tzinfo
                        except Exception:
                            tz = datetime.timezone.utc
                        obj = obj.replace(tzinfo=tz)
                # Normalize to UTC to ensure cross-platform consistency.
                obj = obj.astimezone(datetime.timezone.utc)
            return msgpack.ExtType(1, obj.isoformat().encode("utf-8"))
        elif isinstance(obj, datetime.time):
            return msgpack.ExtType(2, obj.strftime("%H:%M").encode("utf-8"))
        elif isinstance(obj, Duration):
            return msgpack.ExtType(3, obj.in_microseconds)
        elif callable(obj):
            raise RuntimeError(f"Cannot serialize method: {obj}") from None
        return obj

    return encode_object_for_msgpack


def decode_ext_from_msgpack(code, data):
    """Decode MessagePack extension types used in Flet protocol."""
    if code == 1:
        return datetime.datetime.fromisoformat(data.decode("utf-8"))
    elif code == 2:
        return datetime.time(*map(int, data.decode("utf-8").split(":")))
    elif code == 3:
        return Duration.from_unit(microseconds=int(data))
    elif code == 4:
        return data.decode("utf-8")
    return msgpack.ExtType(code, data)


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
    controls: dict[str, dict[str, Any]]


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
    args: dict[str, Any]


@dataclass
class InvokeMethodResponseBody:
    control_id: int
    call_id: str
    result: Any
    error: str
