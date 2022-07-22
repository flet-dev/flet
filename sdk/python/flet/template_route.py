import re
import repath


class TemplateRoute:
    def __init__(self, route: str) -> None:
        self.__last_params = {}
        self.route = route

    def match(self, route_template: str) -> bool:
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
