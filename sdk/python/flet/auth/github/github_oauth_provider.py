import json
from datetime import datetime
from typing import Optional

import requests

from flet.auth.github.github_group import GitHubGroup
from flet.auth.github.github_user import GitHubUser
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

    def _get_user(self, access_token: str, fetch_groups: bool) -> Optional[User]:
        headers = {"Authorization": "Bearer {}".format(access_token)}
        user_resp = requests.get("https://api.github.com/user", headers=headers)
        uj = json.loads(user_resp.text)
        email_resp = requests.get("https://api.github.com/user/emails", headers=headers)
        ej = json.loads(email_resp.text)
        email = ""
        for e in ej:
            if e["primary"]:
                email = e["email"]
                break
        groups = []
        if fetch_groups:
            teams_resp = requests.get(
                "https://api.github.com/user/teams", headers=headers
            )
            tj = json.loads(teams_resp.text)
            for t in tj:
                groups.append(
                    GitHubGroup(
                        id=t["id"],
                        name=t["name"],
                        org_id=t["organization"]["id"],
                        org_login=t["organization"]["login"],
                        org_avatar_url=t["organization"]["avatar_url"],
                    )
                )
        return GitHubUser(
            id=str(uj["id"]),
            login=uj["login"],
            name=uj["name"],
            email=email,
            created_at=datetime.strptime(uj["created_at"], "%Y-%m-%dT%H:%M:%SZ"),
            groups=groups,
        )
