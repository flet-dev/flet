class EventHandler:
    def __init__(self) -> None:
        self.__handlers = {}

    def handler(self, e):
        for h in self.__handlers.keys():
            h(e)

    def subscribe(self, handler):
        self.__handlers[handler] = True

    def unsubscribe(self, handler):
        if handler in self.__handlers:
            self.__handlers.pop(handler)
