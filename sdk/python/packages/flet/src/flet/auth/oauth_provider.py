from typing import Callable, Optional

from flet.auth.group import Group
from flet.auth.user import User


class OAuthProvider:
    def __init__(
        self,
        client_id: str,
        client_secret: str,
        authorization_endpoint: str,
        token_endpoint: str,
        redirect_url: str,
        scopes: Optional[list[str]] = None,
        user_scopes: Optional[list[str]] = None,
        user_endpoint: Optional[str] = None,
        user_id_fn: Optional[Callable] = None,
        group_scopes: Optional[list[str]] = None,
        code_challenge: Optional[str] = None,
        code_challenge_method: Optional[str] = None,
        code_verifier: Optional[str] = None,
    ) -> None:
        self.client_id = client_id
        self.client_secret = client_secret
        self.authorization_endpoint = authorization_endpoint
        self.token_endpoint = token_endpoint
        self.redirect_url = redirect_url
        self.scopes = scopes if scopes is not None else []
        self.user_scopes = user_scopes if user_scopes is not None else []
        self.user_endpoint = user_endpoint
        self.user_id_fn = user_id_fn
        self.group_scopes = group_scopes if group_scopes is not None else []
        self.code_challenge = code_challenge
        self.code_challenge_method = code_challenge_method
        self.code_verifier = code_verifier

    def _name(self):
        raise NotImplementedError("Subclasses must implement _name()")

    async def _fetch_groups(self, access_token: str) -> list[Group]:
        return []

    async def _fetch_user(self, access_token: str) -> Optional[User]:
        return None
