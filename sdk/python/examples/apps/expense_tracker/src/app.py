"""The App component: provides contexts and declares the routes.

App-wide state goes here too: create it once with `ft.use_state` and provide it
with a context, so screens read it with `ft.use_context`.
"""

import theme
from components.screen import CompactContext
from services.receipts import ReceiptPhotos
from state import AppState, StateContext
from storage import Storage
from views.category_form import CategoryFormScreen
from views.expense_details import ExpenseDetailsScreen
from views.expense_form import ExpenseFormScreen
from views.home import HomeScreen
from views.insights import InsightsScreen
from views.settings import SettingsScreen

import flet as ft

# Each route's component returns a Screen (a View). Child routes stack on top of
# their parent, so back (button, gesture, system) returns to the parent.
ROUTES = [
    ft.Route(
        component=HomeScreen,
        children=[
            ft.Route(path="expenses/new", component=ExpenseFormScreen, modal=True),
            ft.Route(
                path="expenses/:id",
                component=ExpenseDetailsScreen,
                children=[
                    ft.Route(path="edit", component=ExpenseFormScreen, modal=True),
                ],
            ),
        ],
    ),
    ft.Route(path="insights", component=InsightsScreen),
    ft.Route(
        path="settings",
        component=SettingsScreen,
        children=[
            ft.Route(path="categories/new", component=CategoryFormScreen, modal=True),
            ft.Route(path="categories/:id", component=CategoryFormScreen, modal=True),
        ],
    ),
]


def is_compact(width) -> bool:
    return not width or width < theme.COMPACT_BREAKPOINT


@ft.component
def App():
    page = ft.context.page
    compact, set_compact = ft.use_state(lambda: is_compact(page.width))
    state, _ = ft.use_state(lambda: AppState(Storage(), ReceiptPhotos()))
    ft.use_effect(state.load, [])

    def watch_width():
        def on_resize(e):
            set_compact(is_compact(e.width))

        page.on_resize = on_resize
        return lambda: setattr(page, "on_resize", None)

    ft.use_effect(watch_width, [])

    return StateContext(
        state,
        lambda: CompactContext(compact, lambda: ft.Router(ROUTES, manage_views=True)),
    )
