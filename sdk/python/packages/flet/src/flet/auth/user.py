from flet.auth.group import Group


class User(dict):
    def __init__(self, kwargs, id: str) -> None:
        super().__init__(kwargs)
        self.id = id
        self.groups = []
