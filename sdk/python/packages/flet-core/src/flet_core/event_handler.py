from flet_core.utils import is_asyncio


class EventHandler:
    def __init__(self, result_converter=None) -> None:
        self.__handlers = {}
        self.__result_converter = result_converter

    def get_handler(self):
        if is_asyncio():
            return self.__async_handler
        else:
            return self.__sync_handler

    def __sync_handler(self, e):
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

    async def __async_handler(self, e):
        for h in self.__handlers.keys():
            if self.__result_converter is not None:
                r = self.__result_converter(e)
                if r is not None:
                    r.target = e.target
                    r.name = e.name
                    r.data = e.data
                    r.control = e.control
                    r.page = e.page
                    await h(r)
            else:
                await h(e)

    def subscribe(self, handler):
        if handler is not None:
            self.__handlers[handler] = True

    def unsubscribe(self, handler):
        if handler in self.__handlers:
            self.__handlers.pop(handler)

    def count(self):
        return len(self.__handlers)
