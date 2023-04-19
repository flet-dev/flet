import json
from typing import List, Optional

import httpx

from flet.auth.group import Group
from flet.auth.oauth_provider import OAuthProvider
from flet.auth.user import User

from flet.version import version


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

    def _fetch_groups(self, access_token: str) -> List[Group]:
        with httpx.Client(follow_redirects=True) as client:
            teams_resp = client.send(self.__get_user_teams_request(access_token))
            return self.__complete_fetch_groups(teams_resp)

    async def _fetch_groups_async(self, access_token: str) -> List[Group]:
        async with httpx.AsyncClient(follow_redirects=True) as client:
            teams_resp = await client.send(self.__get_user_teams_request(access_token))
            return self.__complete_fetch_groups(teams_resp)

    def __get_user_teams_request(self, access_token):
        return httpx.Request(
            "GET",
            "https://api.github.com/user/teams",
            headers=self.__get_client_headers(access_token),
        )

    def __complete_fetch_groups(self, teams_resp):
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

    def _fetch_user(self, access_token: str) -> Optional[User]:
        user_req, emails_req = self.__get_user_details_requests(access_token)
        with httpx.Client(follow_redirects=True) as client:
            user_resp = client.send(user_req)
            emails_resp = client.send(emails_req)
            return self.__complete_fetch_user_details(user_resp, emails_resp)

    async def _fetch_user_async(self, access_token: str) -> Optional[User]:
        user_req, emails_req = self.__get_user_details_requests(access_token)
        async with httpx.AsyncClient(follow_redirects=True) as client:
            user_resp = await client.send(user_req)
            emails_resp = await client.send(emails_req)
            return self.__complete_fetch_user_details(user_resp, emails_resp)

    def __get_user_details_requests(self, access_token):
        return (
            httpx.Request(
                "GET",
                "https://api.github.com/user",
                headers=self.__get_client_headers(access_token),
            ),
            httpx.Request(
                "GET",
                "https://api.github.com/user/emails",
                headers=self.__get_client_headers(access_token),
            ),
        )

    def __complete_fetch_user_details(self, user_resp, emails_resp):
        user_resp.raise_for_status()
        emails_resp.raise_for_status()
        uj = json.loads(user_resp.text)
        ej = json.loads(emails_resp.text)
        for e in ej:
            if e["primary"]:
                uj["email"] = e["email"]
                break
        return User(uj, id=str(uj["id"]))

    def __get_client_headers(self, access_token):
        return {
            "Authorization": f"Bearer {access_token}",
            "User-Agent": f"Flet/{version}",
        }
