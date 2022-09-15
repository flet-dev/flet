import json
from typing import Optional

import requests

from flet.auth.oauth_provider import OAuthProvider
from flet.auth.user import User


class Auth0OAuthProvider(OAuthProvider):
    def __init__(
        self, domain: str, client_id: str, client_secret: str, redirect_url: str
    ) -> None:
        super().__init__(
            client_id=client_id,
            client_secret=client_secret,
            authorization_endpoint=f"https://{domain}/authorize",
            token_endpoint=f"https://{domain}/oauth/token",
            redirect_url=redirect_url,
            user_scopes=["openid", "profile", "email"],
            group_scopes=[],
        )
        self.domain = domain

    def _get_user(self, access_token: str, fetch_groups: bool) -> Optional[User]:
        headers = {"Authorization": "Bearer {}".format(access_token)}
        user_resp = requests.get(f"https://{self.domain}/userinfo", headers=headers)
        uj = json.loads(user_resp.text)
        return User(uj, "")
