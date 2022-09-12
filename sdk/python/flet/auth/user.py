import json
from typing import List

from flet.auth.group import Group


class User:
    def __init__(self, id: str, groups: List[Group]) -> None:
        self.id = id
        self.groups = groups

    def __str__(self):
        return str(self.__dict__)
