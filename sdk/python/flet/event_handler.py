class EventHandler:
    def __init__(self, result_converter=None) -> None:
        self.__handlers = {}
        self.__result_converter = result_converter

    def handler(self, e):
        for h in self.__handlers.keys():
            if self.__result_converter is not None:
                r = self.__result_converter(e)
                if r is not None:
                    r.target = e.target
                    r.name = e.name
                    r.data = e.data
                    r.control = e.control
                    r.page = e.page
                    h(r)
            else:
                h(e)

    def subscribe(self, handler):
        if handler is not None:
            self.__handlers[handler] = True

    def unsubscribe(self, handler):
        if handler in self.__handlers:
            self.__handlers.pop(handler)

    def count(self):
        return len(self.__handlers)
