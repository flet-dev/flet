import re
import urllib.parse
import weakref

__all__ = ["QueryString", "UrlComponents"]


class UrlComponents:
    """
    `UrlComponents` are meant to be used internally for decoding-encoding, it has no external use
    """

    def _encode_url_component(self, url: str) -> str:
        """
        Function encodes querystring part of URL\n
        Ex. q=dom & dogs -> q=dom+%26+dogs
        """
        return urllib.parse.quote(url)

    def _decode_url_component(self, url: str) -> str:
        """
        Function decodes querystring part of URL\n
        Ex. q=dom+%26+dogs -> q=dom & dogs
        """
        return urllib.parse.unquote(url)

    def _is_encoded(self) -> bool:
        """
        Function returns True if URL is already encoded
        """
        if "?" in self.url:
            q_result = self._querystring_part()
            return (
                self._decode_url_component(
                    self.url[q_result.start() + 1 : q_result.end()]
                )
                != self.url[q_result.start() + 1 : q_result.end()]
            )

    def _querystring_part(self, url_string: bool = False):
        """
        Function sliced url part and returns querystring part.\n
        Use case: checking querystring part for encode, assigning decoded value
        """
        pattern = re.compile(r"\?[\w\D]+")
        data = pattern.search(self.url)
        return data if url_string is False else self.url[data.start() + 1 : data.end()]


class QueryString(UrlComponents):
    """
    Note:
        `QueryString` class is meant to be for internal use inside of page. Hence, methods such as `get()` or `to_dict()` must be\n
        called from `page` object\n

    Constructor:
            `page` takes `Page` class an argument and extracts URL automatically\n

    Methods:
            Public:
                `get()` method takes `key` an argument and returns value according to key. (Ex: .../?name=Joe -> `get('name')` -> `Joe`)\n
                `to_dict` returns all the key-value pairs of querystring as a `dict`\n
                `path` returns url path (Ex: .../products?id=1 -> /products)

            Private(meant to be used only inside of page class):
                `post()` method takes key-value pair as an argument and returns proceeded querystring ready to be merged with URL

    """

    def __init__(self, page):
        self.__page = weakref.ref(page)
        self.url = None

    def get(self, key: str) -> str:
        self._data = self.to_dict
        return self._data[key]

    def post(self, kwargs: dict):
        return "?" + urllib.parse.urlencode(kwargs)

    @property
    def to_dict(self) -> dict:
        self._data = urllib.parse.urlparse(self.url).query
        return dict(urllib.parse.parse_qsl(self._data))

    # Path
    @property
    def path(self):
        self._updated_url = self.url.replace("#/", "") if "#" in self.url else self.url
        return urllib.parse.urlparse(self._updated_url).path

    def __call__(self):
        """
        Call dunder method updates url after updating `Page`
        """
        if page := self.__page():
            self.url = page.url + page.route

            # Checking if self.url is encoded and decoding it accordingly
            if self._is_encoded():
                self.url = (
                    page.url
                    + urllib.parse.urlparse(self.url).path
                    + "?"
                    + self._decode_url_component(
                        self._querystring_part(url_string=True)
                    )
                )
