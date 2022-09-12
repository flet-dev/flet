from typing import List, Optional

from flet.auth.user import User


class OAuthProvider:
    def __init__(
        self,
        client_id: str,
        client_secret: str,
        authorization_endpoint: str,
        token_endpoint: str,
        redirect_url: str,
        user_scopes: Optional[List[str]] = None,
        group_scopes: Optional[List[str]] = None,
    ) -> None:
        self.client_id = client_id
        self.client_secret = client_secret
        self.authorization_endpoint = authorization_endpoint
        self.token_endpoint = token_endpoint
        self.redirect_url = redirect_url
        self.user_scopes = user_scopes or []
        self.group_scopes = group_scopes or []

    def _name(self):
        raise Exception("Not implemented")

    def _get_user(self, access_token: str, fetch_groups: bool) -> Optional[User]:
        return
