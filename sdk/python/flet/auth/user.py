from typing import List, Optional

from flet.auth.group import Group


class User(dict):
    def __init__(self, id: str, groups: Optional[List[Group]] = None) -> None:
        self.id = id
        self.groups = groups or []

    def __str__(self):
        return str(self.__dict__)
