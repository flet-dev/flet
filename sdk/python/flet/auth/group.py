class Group(dict):
    def __init__(self, kwargs, name: str) -> None:
        super().__init__(kwargs)
        self.name = name
