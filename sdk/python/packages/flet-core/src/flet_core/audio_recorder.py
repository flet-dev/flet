from typing import Any, Optional

from flet_core.control import Control
from flet_core.ref import Ref


class AudioRecorder(Control):
    """


    -----

    Online docs: https://flet.dev/docs/controls/audiorecorder
    """

    def __init__(
        self,
        ref: Optional[Ref] = None,
        data: Any = None,
        # specific
    ):
        Control.__init__(
            self,
            ref=ref,
            data=data,
        )

    def _get_control_name(self):
        return "audiorecorder"
