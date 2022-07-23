class EventHandler:
    def __init__(self, result_converter=None) -> None:
        self.__handlers = {}
        self.__result_converter = result_converter

    def handler(self, e):
        for h in self.__handlers.keys():
            if self.__result_converter != None:
                h(self.__result_converter(e))
            else:
                h(e)

    def subscribe(self, handler):
        self.__handlers[handler] = True

    def unsubscribe(self, handler):
        if handler in self.__handlers:
            self.__handlers.pop(handler)
