import re
import repath


class TemplateRoute:
    """
    A route helper class that allows you to match a route template against a route string.

    Example:

    ```python
    troute = TemplateRoute(page.route)

    if troute.match("/books/:id"):
        print("Book view ID:", troute.id)
    elif troute.match("/account/:account_id/orders/:order_id"):
        print("Account:", troute.account_id, "Order:", troute.order_id)
    else:
        print("Unknown route")
    ```

    When the `:id` part is optional, you can use the `?` suffix the , e.g.,

    ```python
    troute = TemplateRoute(page.route, defaults={"id": get_random_id()})
    if troute.match("/books/:id?"):
        # if the route is "/books", the `id` property will be set to the random ID
        print("Book view ID:", troute.id)
    else:
        print("Unknown route")
    ```

    ---

    This can be useful when you want to do complicated routing logic in your app as introduced in
    the [navigation and routing](https://flet.dev/docs/guides/python/navigation-and-routing) guide.
    """

    def __init__(self, route: str, *, defaults={}) -> None:
        self.__last_params = {}
        self.__defaults = defaults
        self.route = route
        self.__set_props(defaults, skip_none=False)

    def match(self, route_template: str) -> bool:
        # remove old properties
        for k in self.__last_params:
            setattr(self, k, None)

        # perform new match
        pattern = repath.pattern(route_template)
        match = re.match(pattern, self.route)

        if match:
            self.__last_params = match.groupdict()
            # optional pattern such as `:id?` will be matched and set as None
            # if there are defaults provided, we skip overwriting the properties with None
            skip_none = True if self.__defaults else False
            self.__set_props(self.__last_params, skip_none=skip_none)
            return True
        return False

    def __set_props(self, kwargs, *, skip_none=False):
        for k, v in kwargs.items():
            if skip_none and v is None:
                continue
            setattr(self, k, v)
