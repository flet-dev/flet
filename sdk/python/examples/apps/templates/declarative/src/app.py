"""The App component: provides contexts and declares the routes.

App-wide state goes here too: create it once with `ft.use_state` and provide it
with a context, so screens read it with `ft.use_context`.
"""

import theme
from components.screen import CompactContext
from views.home import HomeScreen

import flet as ft

# Each route's component returns a Screen (a View). Child routes stack on top of
# their parent, so back (button, gesture, system) returns to the parent.
ROUTES = [
    ft.Route(component=HomeScreen),  # "/"
]


def is_compact(width) -> bool:
    return not width or width < theme.COMPACT_BREAKPOINT


@ft.component
def App():
    page = ft.context.page
    compact, set_compact = ft.use_state(lambda: is_compact(page.width))

    def watch_width():
        def on_resize(e):
            set_compact(is_compact(e.width))

        page.on_resize = on_resize
        return lambda: setattr(page, "on_resize", None)

    ft.use_effect(watch_width, [])

    return CompactContext(compact, lambda: ft.Router(ROUTES, manage_views=True))
