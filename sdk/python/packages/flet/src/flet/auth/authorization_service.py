import json
import secrets
import time
from typing import Optional

import httpx
from oauthlib.oauth2 import WebApplicationClient
from oauthlib.oauth2.rfc6749.tokens import OAuth2Token

from flet.auth.authorization import Authorization
from flet.auth.oauth_provider import OAuthProvider
from flet.auth.oauth_token import OAuthToken
from flet.auth.user import User
from flet.version import flet_version


class AuthorizationService(Authorization):
    def __init__(
        self,
        provider: OAuthProvider,
        fetch_user: bool,
        fetch_groups: bool,
        scope: Optional[list[str]] = None,
    ) -> None:
        self.fetch_user = fetch_user
        self.fetch_groups = fetch_groups
        self.scope = scope if scope is not None else []
        self.provider = provider
        self.__token: Optional[OAuthToken] = None
        self.user: Optional[User] = None

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

    async def dehydrate_token(self, saved_token: str):
        self.__token = OAuthToken.from_json(saved_token)
        await self.__refresh_token()
        await self.__fetch_user_and_groups()

    async def get_token(self):
        await self.__refresh_token()
        return self.__token

    def get_authorization_data(self) -> tuple[str, str]:
        self.state = secrets.token_urlsafe(16)
        client = WebApplicationClient(self.provider.client_id)
        authorization_url = client.prepare_request_uri(
            self.provider.authorization_endpoint,
            self.provider.redirect_url,
            scope=self.scope,
            state=self.state,
            code_challenge=self.provider.code_challenge,
            code_challenge_method=self.provider.code_challenge_method,
        )
        return authorization_url, self.state

    async def request_token(self, code: str):
        client = WebApplicationClient(self.provider.client_id)
        data = client.prepare_request_body(
            code=code,
            redirect_uri=self.provider.redirect_url,
            client_secret=self.provider.client_secret,
            include_client_id=True,
            code_verifier=self.provider.code_verifier,
        )
        headers = self.__get_default_headers()
        headers["content-type"] = "application/x-www-form-urlencoded"
        req = httpx.Request(
            "POST", self.provider.token_endpoint, content=data, headers=headers
        )
        async with httpx.AsyncClient(follow_redirects=True) as client:
            resp = await client.send(req)
            resp.raise_for_status()
            client = WebApplicationClient(self.provider.client_id)
            t = client.parse_request_body_response(resp.text)
            self.__token = self.__convert_token(t)
            await self.__fetch_user_and_groups()

    async def __fetch_user_and_groups(self):
        assert self.__token is not None
        if self.fetch_user:
            self.user = await self.provider._fetch_user(self.__token.access_token)
            if self.user is None and self.provider.user_endpoint is not None:
                if self.provider.user_id_fn is None:
                    raise ValueError(
                        "user_id_fn must be specified too if user_endpoint is not None"
                    )
                self.user = await self.__get_user()
            if self.fetch_groups and self.user is not None:
                self.user.groups = await self.provider._fetch_groups(
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

    async def __refresh_token(self):
        if (
            self.__token is None
            or self.__token.expires_at is None
            or self.__token.refresh_token is None
            or time.time() < self.__token.expires_at
        ):
            return None

        assert self.__token is not None
        client = WebApplicationClient(self.provider.client_id)
        data = client.prepare_refresh_body(
            client_id=self.provider.client_id,
            client_secret=self.provider.client_secret,
            refresh_token=self.__token.refresh_token,
            redirect_uri=self.provider.redirect_url,
        )
        headers = self.__get_default_headers()
        headers["content-type"] = "application/x-www-form-urlencoded"
        refresh_req = httpx.Request(
            "POST", url=self.provider.token_endpoint, content=data, headers=headers
        )
        if refresh_req:
            async with httpx.AsyncClient(follow_redirects=True) as client:
                refresh_resp = await client.send(refresh_req)
                refresh_resp.raise_for_status()
                assert self.__token is not None
                client = WebApplicationClient(self.provider.client_id)
                t = client.parse_request_body_response(refresh_resp.text)
                if t.get("refresh_token") is None:
                    t["refresh_token"] = self.__token.refresh_token
                self.__token = self.__convert_token(t)

    async def __get_user(self):
        assert self.__token is not None
        assert self.provider.user_endpoint is not None
        headers = self.__get_default_headers()
        headers["Authorization"] = f"Bearer {self.__token.access_token}"
        user_req = httpx.Request("GET", self.provider.user_endpoint, headers=headers)
        async with httpx.AsyncClient(follow_redirects=True) as client:
            user_resp = await client.send(user_req)
            user_resp.raise_for_status()
            assert self.provider.user_id_fn is not None
            uj = json.loads(user_resp.text)
            return User(uj, str(self.provider.user_id_fn(uj)))

    def __get_default_headers(self):
        return {
            "User-Agent": f"Flet/{flet_version}",
        }
