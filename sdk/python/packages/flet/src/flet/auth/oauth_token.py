import json
from typing import Optional

from flet.controls.embed_json_encoder import EmbedJsonEncoder

__all__ = ["OAuthToken"]


class OAuthToken:
    """
    OAuth token payload used by Flet authentication flows.

    Stores access/refresh token fields and expiry metadata returned by OAuth
    token endpoints.
    """

    def __init__(
        self,
        access_token: str,
        scope: Optional[list[str]] = None,
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

    def to_json(self) -> str:
        """
        Serializes this token to a compact JSON string.

        Returns:
            JSON representation suitable for persistence and later hydration via
                [`from_json()`][(c).from_json].
        """
        return json.dumps(self, cls=EmbedJsonEncoder, separators=(",", ":"))

    @staticmethod
    def from_json(data: str) -> "OAuthToken":
        """
        Deserializes a token from JSON.

        Args:
            data: JSON produced by [`to_json()`][(c).to_json].

        Returns:
            A new `OAuthToken` instance.
        """
        t = json.loads(data)
        return OAuthToken(**t)
