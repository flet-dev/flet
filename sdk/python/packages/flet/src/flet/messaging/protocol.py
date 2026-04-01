import datetime
from dataclasses import dataclass, fields, is_dataclass
from enum import Enum
from typing import Any

import msgpack

from flet.controls.duration import Duration
from flet.controls.value_types import _UNSET, Value


def _get_root_dataclass_field(cls, field_name):
    """
    Returns the field definition from the earliest dataclass in the MRO that declares \
    `field_name`. This lets us recover defaults configured on base controls before \
    subclasses override them.
    """

    for base in reversed(cls.__mro__):
        dataclass_fields = getattr(base, "__dataclass_fields__", None)
        if dataclass_fields and field_name in dataclass_fields:
            return dataclass_fields[field_name]
    return None


def configure_encode_object_for_msgpack(control_cls):
    """
    Builds an object encoder callback for Flet's MessagePack transport.

    The returned function is passed to `msgpack.packb(..., default=...)` and handles
    protocol-specific serialization rules for dataclasses, enums, date/time objects,
    :class:`~flet.Duration`, and extension values exchanged with Dart.

    Encoding behavior highlights:
    - dataclasses are converted to dictionaries with control-aware default pruning;
    - event handler fields (`on_*`) are serialized as booleans (`True` when set);
    - list/dict/dataclass snapshots are captured into `__prev_*` attributes for patch
      diffing unless the object is frozen (`_frozen`);
    - datetime/date/time and duration values are encoded as MsgPack extension types;
    - callables are rejected to prevent accidental method serialization.

    Args:
        control_cls: Base control type used to apply root-dataclass default comparison
            rules for Flet controls.

    Returns:
        Callable that serializes unsupported objects for MsgPack packing.
    """

    def encode_object_for_msgpack(obj):
        """Encode object for MessagePack."""
        if is_dataclass(obj):
            r = {}
            prev_lists = {}
            prev_dicts = {}
            prev_classes = {}

            _values = getattr(obj, "_values", None)
            _structural_fields = getattr(type(obj), "_structural_fields", None)
            is_control = isinstance(obj, control_cls)

            if (
                _values is not None
                and _structural_fields is not None
                and (is_control or isinstance(obj, Value))
            ):
                # ── Fast path for @control / @value types ────────────────────
                # Only non-default values are in _values; structural fields
                # (lists, dicts, nested dataclasses, and internal scalars like
                # _i / _c) are iterated separately — there are typically very
                # few of them.
                _event_fields = getattr(type(obj), "_event_fields", frozenset())
                _root_defaults = getattr(type(obj), "_root_defaults", {})

                # 1. Emit sparse non-default Prop values.
                #    Even though these are Prop-tracked scalars, their runtime
                #    value may be a dataclass, list, or dict (e.g. content=…).
                #    Those must be added to the prev_* snapshots so that the
                #    next diff can compare old vs new correctly.
                for fname, v in _values.items():
                    if v is None:
                        continue
                    # Skip if the value happens to equal the Dart-side root
                    # default (e.g. a subclass Prop was set to the base value).
                    root_def = _root_defaults.get(fname, _UNSET)
                    if root_def is not _UNSET and v == root_def:
                        continue
                    if is_dataclass(v):
                        r[fname] = v
                        prev_classes[fname] = v
                    elif isinstance(v, list):
                        v = v[:]
                        if len(v) > 0:
                            r[fname] = v
                        prev_lists[fname] = v
                    elif isinstance(v, dict):
                        v = v.copy()
                        if len(v) > 0:
                            r[fname] = v
                        prev_dicts[fname] = v
                    else:
                        r[fname] = True if fname in _event_fields else v

                # 2. Emit subclass-overridden defaults that are absent from
                #    _values because they equal the subclass Prop.default.
                for fname, v in getattr(type(obj), "_override_props", {}).items():
                    if fname not in r and v is not None:
                        r[fname] = v

                # 3. Structural fields: lists, dicts, nested dataclasses, and
                #    fixed-scalar internals (_i, _c, …).
                obj_dc_fields = type(obj).__dataclass_fields__
                for fname in _structural_fields:
                    v = getattr(obj, fname)
                    if isinstance(v, list):
                        v = v[:]
                        if len(v) > 0:
                            r[fname] = v
                        prev_lists[fname] = v
                    elif isinstance(v, dict):
                        v = v.copy()
                        if len(v) > 0:
                            r[fname] = v
                        prev_dicts[fname] = v
                    elif is_dataclass(v):
                        r[fname] = v
                        prev_classes[fname] = v
                    elif v is not None:
                        # Scalar structural field (e.g. _i, _c).
                        fmeta = obj_dc_fields.get(fname)
                        default_value = fmeta.default if fmeta is not None else _UNSET
                        root_field = _get_root_dataclass_field(type(obj), fname)
                        if root_field is not None:
                            default_value = root_field.default
                        if v != default_value:
                            r[fname] = v
            else:
                # ── Slow path for plain @dataclass types ─────────────────────
                for field in fields(obj):
                    if "skip" in field.metadata:
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
                    elif field.name.startswith("on_") and field.metadata.get(
                        "event", True
                    ):
                        v = v is not None
                        if v:
                            r[field.name] = v
                    elif is_dataclass(v):
                        r[field.name] = v
                        prev_classes[field.name] = v
                    else:
                        default_value = field.default
                        if is_control:
                            root_field = _get_root_dataclass_field(
                                type(obj), field.name
                            )
                            if root_field is not None:
                                default_value = root_field.default
                        if v is not None and (v != default_value or not is_control):
                            r[field.name] = v

            if not hasattr(obj, "_frozen"):
                setattr(obj, "__prev_lists", prev_lists)
                setattr(obj, "__prev_dicts", prev_dicts)
                setattr(obj, "__prev_classes", prev_classes)

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
    """
    Wire-level action codes exchanged between Python and Dart clients.

    Integer values must stay in sync with Dart `MessageAction` values because
    protocol frames are encoded as `[action_code, body]`.
    """

    REGISTER_CLIENT = 1
    """
    Client registration handshake request/response.
    """

    PATCH_CONTROL = 2
    """
    Server-to-client control tree patch payload.
    """

    CONTROL_EVENT = 3
    """
    Client-to-server control event notification.
    """

    UPDATE_CONTROL_PROPS = 4
    """
    Client-to-server incremental control property update.
    """

    INVOKE_METHOD = 5
    """
    Bidirectional control method invocation and result payload.
    """

    SESSION_CRASHED = 6
    """
    Server-to-client fatal session error notification.
    """


@dataclass
class ClientMessage:
    """
    Top-level protocol frame with action and payload.

    Messages are serialized as a two-item sequence: `[action_code, body]`.
    """

    action: ClientAction
    """
    Action discriminator for this message.
    """

    body: Any
    """
    Action-specific payload object.
    """


@dataclass
class RegisterClientRequestBody:
    """
    Payload sent by the client to register with the backend session.

    This is emitted from Dart during startup/reconnect and includes a current page
    snapshot that can be used for rehydration.
    """

    session_id: str
    """
    Previously assigned session ID, if any.

    Initial registration may provide an empty or null-equivalent value.
    """

    page_name: str
    """
    Logical page name derived from the current app URL.
    """

    page: dict[str, Any]
    """
    Initial page state snapshot (route, media, window, and related metadata).
    """


@dataclass
class SessionPayload:
    """
    Session snapshot payload model.

    This structure represents a session identifier plus serialized controls map and is
    currently reserved/legacy in the active transport flow.
    """

    id: str
    """
    Session identifier.
    """

    controls: dict[str, dict[str, Any]]
    """
    Serialized controls keyed by control ID.
    """


@dataclass
class RegisterClientResponseBody:
    """
    Payload returned by the backend after client registration.

    Contains the active session ID, an initial page patch, and optional startup error
    text.
    """

    session_id: str
    """
    Assigned backend session ID.
    """

    page_patch: Any
    """
    Patch payload used to initialize/update client page state.
    """

    error: str
    """
    Startup error details, or empty string when registration succeeded.
    """


@dataclass
class PatchControlBody:
    """
    Server-to-client control patch message body.

    Applies one patch operation list to the control subtree rooted at `id`.
    """

    id: int
    """
    Target root control ID for patch application.
    """

    patch: Any
    """
    Serialized patch operations generated by object diffing.
    """


@dataclass
class UpdateControlPropsBody:
    """
    Client-to-server control property update payload.

    Used when the client updates selected control properties and sends them back to
    Python.
    """

    id: int
    """
    Target control ID.
    """

    props: Any
    """
    Property mapping to apply to the target control.
    """


@dataclass
class ControlEventBody:
    """
    Client-to-server control event payload.
    """

    target: int
    """
    ID of the control that emitted the event.
    """

    name: str
    """
    Event name without `on_` prefix.
    """

    data: Any
    """
    Event-specific payload.
    """


@dataclass
class SessionCrashedBody:
    """
    Fatal session error payload sent from server to client.
    """

    message: str
    """
    Human-readable crash/error description.
    """


@dataclass
class InvokeMethodRequestBody:
    """
    Server-to-client method invocation request payload.

    The client resolves `control_id`, invokes `name(args)`, then returns an
    `InvokeMethodResponseBody`.
    """

    control_id: int
    """
    Target control ID.
    """

    call_id: str
    """
    Unique invocation correlation ID.
    """

    name: str
    """
    Method name to invoke on the target control.
    """

    args: dict[str, Any]
    """
    Invocation arguments payload.
    """


@dataclass
class InvokeMethodResponseBody:
    """
    Client-to-server method invocation result payload.

    This message correlates to a prior invoke request by `call_id`.
    """

    control_id: int
    """
    Target control ID from the original request.
    """

    call_id: str
    """
    Correlation ID matching the original invoke request.
    """

    result: Any
    """
    Returned method result value.
    """

    error: str
    """
    Error message if invocation failed; otherwise null/empty.
    """
