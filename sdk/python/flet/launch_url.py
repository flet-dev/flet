import dataclasses
import time
from typing import Optional

from beartype import beartype

from flet.control import Control
from flet.ref import Ref


@dataclasses.dataclass
class LaunchUrlData:
    ts: str
    url: Optional[str]


class LaunchUrl(Control):
    def __init__(
        self,
        ref: Ref = None,
        data: any = None,
        #
        # Specific
        #
        url: str = None,
    ):

        Control.__init__(
            self,
            ref=ref,
            data=data,
        )

        self.url = url

    def _get_control_name(self):
        return "launchurl"

    def _is_isolated(self):
        return True

    # url
    @property
    def url(self):
        return self.__url

    @url.setter
    @beartype
    def url(self, value: Optional[str]):
        self.__url = value
        d = LaunchUrlData(str(time.time()), value)
        self._set_attr_json("value", d)
