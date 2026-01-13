import json
from typing import Optional

import httpx

from flet.auth.group import Group
from flet.auth.oauth_provider import OAuthProvider
from flet.auth.user import User
from flet.version import flet_version


class GitHubOAuthProvider(OAuthProvider):
    def __init__(self, client_id: str, client_secret: str, redirect_url: str) -> None:
        super().__init__(
            client_id=client_id,
            client_secret=client_secret,
            authorization_endpoint="https://github.com/login/oauth/authorize",
            token_endpoint="https://github.com/login/oauth/access_token",
            redirect_url=redirect_url,
            user_scopes=["read:user", "user:email"],
            group_scopes=["read:org"],
        )

    async def _fetch_groups(self, access_token: str) -> list[Group]:
        async with httpx.AsyncClient(follow_redirects=True) as client:
            teams_resp = await client.send(
                httpx.Request(
                    "GET",
                    "https://api.github.com/user/teams",
                    headers=self.__get_client_headers(access_token),
                )
            )
            teams_resp.raise_for_status()
            groups = []
            tj = json.loads(teams_resp.text)
            for t in tj:
                groups.append(
                    Group(
                        t,
                        name=t["name"],
                    )
                )
            return groups

    async def _fetch_user(self, access_token: str) -> Optional[User]:
        async with httpx.AsyncClient(follow_redirects=True) as client:
            user_resp = await client.send(
                httpx.Request(
                    "GET",
                    "https://api.github.com/user",
                    headers=self.__get_client_headers(access_token),
                )
            )
            user_resp.raise_for_status()
            uj = json.loads(user_resp.text)

            emails_resp = await client.send(
                httpx.Request(
                    "GET",
                    "https://api.github.com/user/emails",
                    headers=self.__get_client_headers(access_token),
                )
            )
            emails_resp.raise_for_status()
            ej = json.loads(emails_resp.text)
            for e in ej:
                if e["primary"]:
                    uj["email"] = e["email"]
                    break
            return User(uj, id=str(uj["id"]))

    def __get_client_headers(self, access_token):
        return {
            "Authorization": f"Bearer {access_token}",
            "User-Agent": f"Flet/{flet_version}",
        }
