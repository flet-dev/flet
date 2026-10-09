import urllib.parse
import weakref

__all__ = ["QueryString", "UrlComponents"]


class UrlComponents:
    """
    `UrlComponents` are meant to be used internally for decoding-encoding, it has no \
    external use
    """

    def _encode_url_component(self, url: str) -> str:
        """
        Function encodes querystring part of URL\n Ex. q=dom & dogs -> q=dom+%26+dogs
        """
        return urllib.parse.quote(url)

    def _decode_url_component(self, url: str) -> str:
        """
        Function decodes querystring part of URL\n Ex. q=dom+%26+dogs -> q=dom & dogs
        """
        return urllib.parse.unquote(url)


class QueryString(UrlComponents):
    """
    Note: `QueryString` class is meant to be for internal use inside of page. Hence, \
    methods such as `get()` or `to_dict()` must be\n called from `page` object\n

    Constructor:
            `page` takes `Page` class an argument and extracts URL automatically\n

    Methods:
            Public:
                `get()` method takes `key` an argument and returns value according to
                key. (Ex: .../?name=Joe -> `get('name')` -> `Joe`)\n
                `to_dict` returns all the key-value pairs of querystring as a `dict`\n
                `path` returns url path (Ex: .../products?id=1 -> /products)

            Private(meant to be used only inside of page class):
                `post()` method takes key-value pair as an argument and returns
                proceeded querystring ready to be merged with URL

    """

    def __init__(self, page):
        self.__page = weakref.ref(page)

    def get(self, key: str) -> str:
        """
        Return the query parameter value for `key` from the current page route.

        Raises:
            KeyError: If `key` does not exist in the parsed query parameters.
        """
        self._data = self.to_dict
        return self._data[key]

    def post(self, kwargs: dict):
        """
        Build an encoded querystring from key-value pairs.

        Returns:
            A querystring that starts with `?` and is ready to append to a URL.
        """
        return "?" + urllib.parse.urlencode(kwargs)

    @property
    def to_dict(self) -> dict:
        """
        Parse the query component of the current page route into a dictionary.

        The route is read on every access, so the result always matches
        :attr:`flet.Page.route`. Keys and values are percent-decoded, with `+`
        decoded as a space. When a key appears more than once, its last value is
        returned.
        """
        return dict(urllib.parse.parse_qsl(self._split_route().query))

    # Path
    @property
    def path(self):
        """
        Return the path component of the current page route.
        """
        return self._split_route().path

    def _split_route(self) -> urllib.parse.SplitResult:
        """
        Split the current page route into its URL components.
        """
        page = self.__page()
        return urllib.parse.urlsplit((page.route if page else None) or "")
