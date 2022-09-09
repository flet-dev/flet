from typing import List


class User():
    def __init__(self, id: str, groups: List[str]) -> None:
        self.id = id
        self.groups = groups
