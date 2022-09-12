class Group:
    def __init__(self, name: str) -> None:
        self.name = name

    def __str__(self):
        return str(self.__dict__)
