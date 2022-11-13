from typing import Any, Optional

from beartype import beartype

from flet.control import Control, OptionalNumber
from flet.ref import Ref


class ShakeDetector(Control):
    def __init__(
        self,
        ref: Optional[Ref] = None,
        data: Any = None,
        # specific
        minimum_shake_count: Optional[int] = None,
        shake_slop_time_ms: Optional[int] = None,
        shake_count_reset_time_ms: Optional[int] = None,
        shake_threshold_gravity: OptionalNumber = None,
        on_shake=None,
    ):

        Control.__init__(
            self,
            ref=ref,
            data=data,
        )

        self.minimum_shake_count = minimum_shake_count
        self.shake_slop_time_ms = shake_slop_time_ms
        self.shake_count_reset_time_ms = shake_count_reset_time_ms
        self.shake_threshold_gravity = shake_threshold_gravity
        self.on_shake = on_shake

    def _get_control_name(self):
        return "shakedetector"

    # minimum_shake_count
    @property
    def minimum_shake_count(self) -> Optional[int]:
        return self._get_attr("minimumShakeCount")

    @minimum_shake_count.setter
    @beartype
    def minimum_shake_count(self, value: Optional[int]):
        self._set_attr("minimumShakeCount", value)

    # shake_slop_time_ms
    @property
    def shake_slop_time_ms(self) -> Optional[int]:
        return self._get_attr("shakeSlopTimeMS")

    @shake_slop_time_ms.setter
    @beartype
    def shake_slop_time_ms(self, value: Optional[int]):
        self._set_attr("shakeSlopTimeMS", value)

    # shake_count_reset_time_ms
    @property
    def shake_count_reset_time_ms(self) -> Optional[int]:
        return self._get_attr("shakeCountResetTimeMs")

    @shake_count_reset_time_ms.setter
    @beartype
    def shake_count_reset_time_ms(self, value: Optional[int]):
        self._set_attr("shakeCountResetTimeMs", value)

    # shake_threshold_gravity
    @property
    def shake_threshold_gravity(self) -> OptionalNumber:
        return self._get_attr("shakeThresholdGravity")

    @shake_threshold_gravity.setter
    @beartype
    def shake_threshold_gravity(self, value: OptionalNumber):
        self._set_attr("shakeThresholdGravity", value)

    # on_shake
    @property
    def on_shake(self):
        return self._get_event_handler("shake")

    @on_shake.setter
    def on_shake(self, handler):
        self._add_event_handler("shake", handler)
