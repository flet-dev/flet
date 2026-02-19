import json
from typing import Optional

from flet.controls.embed_json_encoder import EmbedJsonEncoder


def to_json(value) -> Optional[str]:
    """
    Serializes a value to compact JSON using Flet's embedded encoder.

    Args:
        value: Value to serialize.

    Returns:
        JSON string without extra whitespace, or `None` when `value` is `None`.
    """
    return (
        json.dumps(value, cls=EmbedJsonEncoder, separators=(",", ":"))
        if value is not None
        else None
    )
