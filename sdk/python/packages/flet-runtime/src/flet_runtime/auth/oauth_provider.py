from typing import Callable, List, Optional

from flet_runtime.auth.group import Group
from flet_runtime.auth.user import User


class OAuthProvider:
    def __init__(
        self,
        client_id: str,
        client_secret: str,
        authorization_endpoint: str,
        token_endpoint: str,
        redirect_url: str,
        scopes: Optional[List[str]] = None,
        user_scopes: Optional[List[str]] = None,
        user_endpoint: Optional[str] = None,
        user_id_fn: Optional[Callable] = None,
        group_scopes: Optional[List[str]] = None,
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

    def _name(self):
        raise Exception("Not implemented")

    def _fetch_groups(self, access_token: str) -> List[Group]:
        return []

    async def _fetch_groups_async(self, access_token: str) -> List[Group]:
        return []

    def _fetch_user(self, access_token: str) -> Optional[User]:
        return None

    async def _fetch_user_async(self, access_token: str) -> Optional[User]:
        return None
