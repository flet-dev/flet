import re

import repath

__all__ = ["TemplateRoute"]


class TemplateRoute:
    """
    Matches a concrete route string against parameterized route templates.

    Instances keep the original route in `route` and expose matched template
    parameters as dynamic attributes after a successful call to `match()`.
    Parameter attributes captured by a previous match are reset to `None` before
    each new matching attempt, preventing stale values from leaking between
    checks.
    """

    def __init__(self, route: str) -> None:
        self.__last_params = {}
        self.route = route

    def match(self, route_template: str) -> bool:
        """
        Tries to match this instance route against a route template.

        The template is compiled with `repath.pattern()`. If matching succeeds,
        named parameters are stored and also assigned as attributes on this
        object (for example, `self.user_id`). If matching fails, previously
        captured attributes remain cleared.

        Args:
            route_template: Route template in a format supported by
                `repath.pattern()`.

        Returns:
            `True` if the route matches the template; otherwise `False`.
        """
        # remove old properties
        for k in self.__last_params:
            setattr(self, k, None)

        # perform new match
        pattern = repath.pattern(route_template)
        match = re.match(pattern, self.route)

        if match:
            self.__last_params = match.groupdict()
            for k, v in self.__last_params.items():
                setattr(self, k, v)
            return True
        return False
