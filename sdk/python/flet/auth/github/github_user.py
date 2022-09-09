from typing import List

from flet.auth.user import User


class GitHubUser(User):
    def __init__(self, id: str, groups: List[str], full_name: str, email: str) -> None:
        super().__init__(id, groups)
        self.full_name = full_name
        self.email = email
