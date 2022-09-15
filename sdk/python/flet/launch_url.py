import dataclasses
import time
from typing import Any, Optional

from beartype import beartype

from flet.control import Control
from flet.ref import Ref


@dataclasses.dataclass
class LaunchUrlData:
    ts: str
    url: str
    web_window_name: Optional[str] = dataclasses.field(default=None)
    web_popup_window: Optional[bool] = dataclasses.field(default=False)


class LaunchUrl(Control):
    def __init__(self, ref: Optional[Ref] = None, data: Any = None):

        Control.__init__(
            self,
            ref=ref,
            data=data,
        )

    def _get_control_name(self):
        return "launchurl"

    def _is_isolated(self):
        return True

    def launch_url(
        self,
        url: str,
        web_window_name: Optional[str] = None,
        web_popup_window: bool = False,
    ):
        d = LaunchUrlData(
            str(time.time()),
            url=url,
            web_window_name=web_window_name,
            web_popup_window=web_popup_window,
        )
        self._set_attr_json("launchUrl", d)
        self.update()
