from datetime import datetime
from typing import List

from flet.auth.group import Group
from flet.auth.user import User


class GitHubUser(User):
    def __init__(
        self,
        id: str,
        login: str,
        groups: List[Group],
        name: str,
        email: str,
        created_at: datetime,
    ) -> None:
        super().__init__(id, groups)
        self.login = login
        self.name = name
        self.email = email
        self.created_at = created_at
