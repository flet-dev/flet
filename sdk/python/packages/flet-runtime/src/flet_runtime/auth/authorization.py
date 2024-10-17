import asyncio
import json
import secrets
import threading
import time
from typing import List, Optional, Tuple

import httpx
from flet.version import version
from flet_core.locks import AsyncNopeLock, NopeLock
from flet_core.utils import is_asyncio
from oauthlib.oauth2 import WebApplicationClient
from oauthlib.oauth2.rfc6749.tokens import OAuth2Token

from flet_runtime.auth.oauth_provider import OAuthProvider
from flet_runtime.auth.oauth_token import OAuthToken
from flet_runtime.auth.user import User


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
        self.scope = scope if scope is not None else []
        self.provider = provider
        self.__token: Optional[OAuthToken] = None
        self.user: Optional[User] = None
        self.__lock = threading.Lock() if not is_asyncio() else NopeLock()
        self.__async_lock = asyncio.Lock() if is_asyncio() else AsyncNopeLock()

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

    def dehydrate_token(self, saved_token: str):
        self.__token = OAuthToken.from_json(saved_token)
        self.__refresh_token()
        self.__fetch_user_and_groups()

    async def dehydrate_token_async(self, saved_token: str):
        self.__token = OAuthToken.from_json(saved_token)
        await self.__refresh_token_async()
        await self.__fetch_user_and_groups_async()

    # token
    @property
    def token(self) -> Optional[OAuthToken]:
        with self.__lock:
            self.__refresh_token()
            return self.__token

    # token_async
    @property
    async def token_async(self) -> Optional[OAuthToken]:
        async with self.__async_lock:
            await self.__refresh_token_async()
            return self.__token

    def get_authorization_data(self) -> Tuple[str, str]:
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

    def request_token(self, code: str):
        req = self.__get_request_token_request(code)
        with httpx.Client(follow_redirects=True) as client:
            resp = client.send(req)
            resp.raise_for_status()
            client = WebApplicationClient(self.provider.client_id)
            t = client.parse_request_body_response(resp.text)
            self.__token = self.__convert_token(t)
            self.__fetch_user_and_groups()

    async def request_token_async(self, code: str):
        req = self.__get_request_token_request(code)
        async with httpx.AsyncClient(follow_redirects=True) as client:
            resp = await client.send(req)
            resp.raise_for_status()
            client = WebApplicationClient(self.provider.client_id)
            t = client.parse_request_body_response(resp.text)
            self.__token = self.__convert_token(t)
            await self.__fetch_user_and_groups_async()

    def __get_request_token_request(self, code: str):
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
        return httpx.Request(
            "POST", self.provider.token_endpoint, content=data, headers=headers
        )

    def __fetch_user_and_groups(self):
        assert self.__token is not None
        if self.fetch_user:
            self.user = self.provider._fetch_user(self.__token.access_token)
            if self.user is None and self.provider.user_endpoint is not None:
                if self.provider.user_id_fn is None:
                    raise Exception(
                        "user_id_fn must be specified too if user_endpoint is not None"
                    )
                self.user = self.__get_user()
            if self.fetch_groups and self.user is not None:
                self.user.groups = self.provider._fetch_groups(
                    self.__token.access_token
                )

    async def __fetch_user_and_groups_async(self):
        assert self.__token is not None
        if self.fetch_user:
            self.user = await self.provider._fetch_user_async(self.__token.access_token)
            if self.user is None and self.provider.user_endpoint is not None:
                if self.provider.user_id_fn is None:
                    raise Exception(
                        "user_id_fn must be specified too if user_endpoint is not None"
                    )
                self.user = await self.__get_user_async()
            if self.fetch_groups and self.user is not None:
                self.user.groups = await self.provider._fetch_groups_async(
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
        refresh_req = self.__get_refresh_token_request()
        if refresh_req:
            with httpx.Client(follow_redirects=True) as client:
                refresh_resp = client.send(refresh_req)
                self.__complete_refresh_token_request(refresh_resp)

    async def __refresh_token_async(self):
        refresh_req = self.__get_refresh_token_request()
        if refresh_req:
            async with httpx.AsyncClient(follow_redirects=True) as client:
                refresh_resp = await client.send(refresh_req)
                self.__complete_refresh_token_request(refresh_resp)

    def __get_refresh_token_request(self):
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
        return httpx.Request(
            "POST", url=self.provider.token_endpoint, content=data, headers=headers
        )

    def __complete_refresh_token_request(self, refresh_resp):
        refresh_resp.raise_for_status()
        assert self.__token is not None
        client = WebApplicationClient(self.provider.client_id)
        t = client.parse_request_body_response(refresh_resp.text)
        if t.get("refresh_token") is None:
            t["refresh_token"] = self.__token.refresh_token
        self.__token = self.__convert_token(t)

    def __get_user(self):
        user_req = self.__get_user_request()
        with httpx.Client() as client:
            user_resp = client.send(user_req)
            return self.__complete_user_request(user_resp)

    async def __get_user_async(self):
        user_req = self.__get_user_request()
        async with httpx.AsyncClient(follow_redirects=True) as client:
            user_resp = await client.send(user_req)
            return self.__complete_user_request(user_resp)

    def __get_user_request(self):
        assert self.token is not None
        assert self.provider.user_endpoint is not None
        headers = self.__get_default_headers()
        headers["Authorization"] = f"Bearer {self.token.access_token}"
        return httpx.Request("GET", self.provider.user_endpoint, headers=headers)

    def __complete_user_request(self, user_resp):
        user_resp.raise_for_status()
        assert self.provider.user_id_fn is not None
        uj = json.loads(user_resp.text)
        return User(uj, str(self.provider.user_id_fn(uj)))

    def __get_default_headers(self):
        return {
            "User-Agent": f"Flet/{version}",
        }
