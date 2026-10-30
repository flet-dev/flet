"""Encode notification arguments through Flet's real transport serializer."""

import msgpack

from flet.controls.base_control import BaseControl
from flet.messaging.protocol import (
    configure_encode_object_for_msgpack,
    decode_ext_from_msgpack,
)


def encode_wire(value):
    return msgpack.unpackb(
        msgpack.packb(value, default=configure_encode_object_for_msgpack(BaseControl)),
        raw=False,
        ext_hook=decode_ext_from_msgpack,
    )
