import json
from typing import List, Optional

from flet.core.embed_json_encoder import EmbedJsonEncoder


class OAuthToken:
    def __init__(
        self,
        access_token: str,
        scope: Optional[List[str]] = None,
        token_type: Optional[str] = None,
        expires_in: Optional[int] = None,
        expires_at: Optional[float] = None,
        refresh_token: Optional[str] = None,
    ) -> None:
        self.access_token = access_token
        self.scope = scope
        self.token_type = token_type
        self.expires_in = expires_in
        self.expires_at = expires_at
        self.refresh_token = refresh_token

    def to_json(self):
        return json.dumps(self, cls=EmbedJsonEncoder, separators=(",", ":"))

    @staticmethod
    def from_json(data: str):
        t = json.loads(data)
        return OAuthToken(**t)
