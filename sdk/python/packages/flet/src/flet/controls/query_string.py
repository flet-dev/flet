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
    The query string of the current page route, available as :attr:`flet.Page.query`.

    It is parsed from :attr:`flet.Page.route` on every access, so it can be read
    in `main()` as well as in a :attr:`flet.Page.on_route_change` handler. For
    example, with the route `/products?id=1&sort=price`:

    - `page.query.get("id")` returns `"1"`;
    - `page.query.to_dict` returns `{"id": "1", "sort": "price"}`;
    - `page.query.path` returns `"/products"`.

    Values are always strings. To navigate to a route with a query string, pass
    the parameters as keyword arguments to :meth:`flet.Page.navigate` or
    :meth:`flet.Page.push_route`.
    """

    def __init__(self, page):
        self.__page = weakref.ref(page)

    def get(self, key: str) -> str:
        """
        Return the value of the query parameter `key` in the current page route.

        Args:
            key: The name of the query parameter.

        Returns:
            The decoded value. When `key` appears more than once, its last
                non-empty value.

        Raises:
            KeyError: If the route has no query parameter `key` with a non-empty
                value.
        """
        return self.to_dict[key]

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
        decoded as a space. Parameters without a value, such as `debug` in
        `?debug` or `?debug=`, are left out. When a key appears more than once,
        its last non-empty value is returned.
        """
        return dict(urllib.parse.parse_qsl(self._split_route()[1]))

    # Path
    @property
    def path(self) -> str:
        """
        Return the path component of the current page route, without the query
        string and fragment.
        """
        return self._split_route()[0]

    def _split_route(self) -> tuple[str, str]:
        """
        Split the current page route into its path and query string, dropping a
        `#` fragment.
        """
        page = self.__page()
        route = (page.route if page else None) or ""
        path, _, query = route.partition("#")[0].partition("?")
        return path, query
