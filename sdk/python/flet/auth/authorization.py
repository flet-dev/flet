import json
import secrets
import threading
import time
from typing import List, Optional, Tuple

import requests
from oauthlib.oauth2 import WebApplicationClient
from oauthlib.oauth2.rfc6749.tokens import OAuth2Token

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
        saved_token: Optional[str] = None,
    ) -> None:
        self.fetch_user = fetch_user
        self.fetch_groups = fetch_groups
        self.scope = scope if scope is not None else []
        self.provider = provider
        self.__token: Optional[OAuthToken] = None
        self.user: Optional[User] = None
        self._lock = threading.Lock()

        # fix scopes
        self.scope.extend(self.provider.scopes)
        if self.fetch_user:
            for s in self.provider.user_scopes:
                if s not in self.scope:
                    self.scope.append(s)
        if self.fetch_groups:
            for s in self.provider.group_scopes:
                if s not in self.scope:
                    self.scope.append(s)

        if saved_token != None:
            self.__token = OAuthToken.from_json(saved_token)
            self.__refresh_token()
            self.__fetch_user_and_groups()

    # token
    @property
    def token(self) -> Optional[OAuthToken]:
        with self._lock:
            self.__refresh_token()
            return self.__token

    def get_authorization_data(self) -> Tuple[str, str]:
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
        self.__token = self.__convert_token(t)
        self.__fetch_user_and_groups()

    def __fetch_user_and_groups(self):
        assert self.__token is not None
        if self.fetch_user:
            self.user = self.provider._fetch_user(self.__token.access_token)
            if self.user == None and self.provider.user_endpoint != None:
                if self.provider.user_id_fn == None:
                    raise Exception(
                        "user_id_fn must be specified too if user_endpoint is not None"
                    )
                self.user = self.__get_user()
            if self.fetch_groups and self.user != None:
                self.user.groups = self.provider._fetch_groups(
                    self.__token.access_token
                )

    def __convert_token(self, t: OAuth2Token):
        return OAuthToken(
            access_token=t["access_token"],
            scope=t.get("scope"),
            token_type=t.get("token_type"),
            expires_in=t.get("expires_in"),
            expires_at=t.get("expires_at"),
            refresh_token=t.get("refresh_token"),
        )

    def __refresh_token(self):
        if (
            self.__token is None
            or self.__token.expires_at is None
            or self.__token.refresh_token is None
            or time.time() < self.__token.expires_at
        ):
            return

        assert self.__token is not None
        client = WebApplicationClient(self.provider.client_id)
        data = client.prepare_refresh_body(
            client_id=self.provider.client_id,
            client_secret=self.provider.client_secret,
            refresh_token=self.__token.refresh_token,
            redirect_uri=self.provider.redirect_url,
        )
        headers = {"content-type": "application/x-www-form-urlencoded"}
        response = requests.post(
            self.provider.token_endpoint, data=data, headers=headers
        )
        t = client.parse_request_body_response(response.text)
        if t.get("refresh_token") == None:
            t["refresh_token"] = self.__token.refresh_token
        self.__token = self.__convert_token(t)

    def __get_user(self):
        assert self.token is not None
        assert self.provider.user_endpoint is not None
        assert self.provider.user_id_fn is not None
        headers = {"Authorization": "Bearer {}".format(self.token.access_token)}
        user_resp = requests.get(self.provider.user_endpoint, headers=headers)
        uj = json.loads(user_resp.text)
        return User(uj, str(self.provider.user_id_fn(uj)))
