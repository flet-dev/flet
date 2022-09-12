from datetime import datetime
from typing import List

from flet.auth.group import Group


class GitHubGroup(Group):
    def __init__(
        self, name: str, id: int, org_id: int, org_login: str, org_avatar_url: str
    ) -> None:
        super().__init__(f"{org_login}/{name}")
        self.id = id
        self.org_id = org_id
        self.org_login = org_login
        self.org_avatar_url = org_avatar_url
