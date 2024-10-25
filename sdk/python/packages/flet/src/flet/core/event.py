class Event:
    def __init__(self, target: str, name: str, data: str):
        self.target: str = target
        self.name: str = name
        self.data: str = data

    def __repr__(self):
        attrs = ", ".join(f"{k}={v!r}" for k, v in self.__dict__.items())
        return f"{self.__class__.__name__}({attrs})"

    def __str__(self):
        attrs = ", ".join(
            f"{k}={v!r}"
            for k, v in self.__dict__.items()
            if k not in ["control", "page", "target", "data"]  # ignore these keys
        )
        return f"{self.__class__.__name__}({attrs}, data={self.data!r})"  # reinsert data as last arg
