import json
from typing import List, Optional

import requests

from flet.auth.group import Group
from flet.auth.oauth_provider import OAuthProvider
from flet.auth.user import User


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
        headers = {"Authorization": "Bearer {}".format(access_token)}
        groups = []
        teams_resp = requests.get("https://api.github.com/user/teams", headers=headers)
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
        headers = {"Authorization": "Bearer {}".format(access_token)}
        user_resp = requests.get("https://api.github.com/user", headers=headers)
        uj = json.loads(user_resp.text)
        email_resp = requests.get("https://api.github.com/user/emails", headers=headers)
        ej = json.loads(email_resp.text)
        for e in ej:
            if e["primary"]:
                uj["email"] = e["email"]
                break
        return User(uj, id=str(uj["id"]))
