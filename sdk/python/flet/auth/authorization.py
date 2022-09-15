import secrets
from typing import List, Optional, Tuple

import requests
from oauthlib.oauth2 import WebApplicationClient

from flet.auth.oauth_provider import OAuthProvider
from flet.auth.oauth_token import OAuthToken
from flet.auth.user import User


class Authorization:
    def __init__(
        self,
        provider: OAuthProvider,
        fetch_user: bool,
        fetch_groups: bool,
        scope: Optional[List[str]] = None,
    ) -> None:
        self.fetch_user = fetch_user
        self.fetch_groups = fetch_groups
        self.scope = scope or []
        self.provider = provider
        self.token: Optional[OAuthToken] = None
        self.user: Optional[User] = None

        # fix scopes
        if self.fetch_user:
            for s in self.provider.user_scopes:
                if s not in self.scope:
                    self.scope.append(s)
        if self.fetch_groups:
            for s in self.provider.group_scopes:
                if s not in self.scope:
                    self.scope.append(s)

    def authorize(self) -> Tuple[str, str]:
        self.state = secrets.token_urlsafe(16)
        client = WebApplicationClient(self.provider.client_id)
        authorization_url = client.prepare_request_uri(
            self.provider.authorization_endpoint,
            self.provider.redirect_url,
            scope=self.scope,
            state=self.state,
        )
        return (authorization_url, self.state)

    def request_token(self, code: str):
        client = WebApplicationClient(self.provider.client_id)
        data = client.prepare_request_body(
            code=code,
            redirect_uri=self.provider.redirect_url,
            client_id=self.provider.client_id,
            client_secret=self.provider.client_secret,
        )
        headers = {"content-type": "application/x-www-form-urlencoded"}
        response = requests.post(
            self.provider.token_endpoint, data=data, headers=headers
        )
        t = client.parse_request_body_response(response.text)
        self.token = OAuthToken(
            access_token=t["access_token"],
            scope=t["scope"],
            token_type=t["token_type"],
            expires_in=t.get("expires_in"),
            refresh_token=t.get("refresh_token"),
        )
        if self.fetch_user:
            self.user = self.provider._get_user(
                self.token.access_token, self.fetch_groups
            )
