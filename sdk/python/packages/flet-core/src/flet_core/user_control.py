from flet_core.stack import Stack
from flet_core.utils import deprecated


class UserControl(Stack):
    @deprecated(
        reason="UserControl is deprecated. See https://flet.dev/docs/getting-started/custom-controls.",
        version="0.21.0",
        delete_version="1.0",
    )
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def build(self):
        pass

    def is_isolated(self):
        return True
