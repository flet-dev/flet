class User(dict):
    def __init__(self, id: str, **kwargs) -> None:
        super().__init__(**kwargs)
        self.id = id
        self.groups = []
        for key, value in kwargs.items():
            self.__setattr__(key, value)
