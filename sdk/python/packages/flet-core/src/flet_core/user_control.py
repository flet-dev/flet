from typing import List

from flet_core.control import Control
from flet_core.stack import Stack


class UserControl(Stack):
    def build(self):
        pass

    def _build(self):
        content = self.build()
        if isinstance(content, Control):
            self.controls = [content]
        elif isinstance(content, List) and all(
            isinstance(control, Control) for control in content
        ):
            self.controls = content
        else:
            raise Exception(
                f"{self.__class__.__name__}.build() method must be implemented and returning either Control or List[Control]."
            )

    def _is_isolated(self):
        return True
