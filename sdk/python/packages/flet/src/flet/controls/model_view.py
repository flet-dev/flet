from typing import Optional

from flet.controls.base_control import control
from flet.controls.control import Control

__all__ = ["ModelView"]


@control("ModelView", kw_only=True)
class ModelView(Control):
    _content: Optional[Control] = None

    # def init(self):
    #     super().init()
    #     print(f"ModelView.init(), key={self.key}, id={self._i}")

    def build(self):
        super().build()
        print(f"ModelView.build(), key={self.key}, id={self._i}")

    def render(self):
        return None

    def before_update(self):
        print(f"ModelView({self._i}).before_update()")
        frozen = getattr(self, "_frozen", None)
        if frozen:
            del self._frozen

        self._content = self.render()

        if self._content:
            object.__setattr__(self._content, "_frozen", True)
        if frozen:
            self._frozen = frozen
