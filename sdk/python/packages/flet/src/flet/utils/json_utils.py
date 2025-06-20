import json
from typing import Optional

from flet.controls.embed_json_encoder import EmbedJsonEncoder


def to_json(value) -> Optional[str]:
    return (
        json.dumps(value, cls=EmbedJsonEncoder, separators=(",", ":"))
        if value is not None
        else None
    )
