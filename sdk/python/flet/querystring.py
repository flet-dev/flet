import re
from flet import Page


class QueryString:
    """
    Note:
            `QueryString must be inside of url on change function`\n

    Constructor:
            If `page` argument is passed, `QueryString` takes url out automatically of `page` object\n
            If `url` (customly specified url) is specified, then `QueryString` will work on `url` argument\n

    Methods:
            `get()` method takes `key` an an argument and returns value according to key. (Ex: .../?name=Joe) -> `get('name')` -> `Joe`\n
            `to_dict()` returns all the key-value pairs of querystring as a `dict`\n

    """

    def __init__(self, page: Page = None, url: str = None):
        self.url = page.url + page.route if url is None else url

    def get(self, key: str) -> str:
        self._pattern = re.compile(f"{key}=[\w\+?]+")
        self._res = self._pattern.search(self.url)
        self._res = self.url[self._res.start() + len(key) + 1 : self._res.end()]
        return self._res if "+" not in self._res else self._res.replace("+", " ")

    def to_dict(self) -> dict:
        self._key_pattern = re.compile(r"[\w]+=")
        self._keys = [i[:-1] for i in self._key_pattern.findall(self.url)]

        self._value_pattern = re.compile(r"=[\w\+?]+")
        self._values = [
            i[1:].replace("+", " ") for i in self._value_pattern.findall(self.url)
        ]

        return {i: j for i, j in zip(self._keys, self._values)}
