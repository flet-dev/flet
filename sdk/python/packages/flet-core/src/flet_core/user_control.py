from flet_core.stack import Stack
from flet_core.utils.deprecated import deprecated_class


@deprecated_class(
    reason="UserControl is deprecated. See https://flet.dev/docs/getting-started/custom-controls.",
    version="0.21.0",
    delete_version="0.26.0",
)
class UserControl(Stack):
    def build(self):
        pass

    def is_isolated(self):
        return True
