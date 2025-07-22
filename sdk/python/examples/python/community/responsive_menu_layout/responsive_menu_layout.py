from copy import deepcopy

import flet
from flet import (
    AppBar,
    Card,
    Column,
    Container,
    ElevatedButton,
    IconButton,
    NavigationRail,
    NavigationRailDestination,
    Page,
    Row,
    Stack,
    Switch,
    Text,
    VerticalDivider,
    colors,
    icons,
)
from flet.utils import slugify


class ResponsiveMenuLayout(Row):
    def __init__(
        self,
        page,
        pages,
        *args,
        support_routes=True,
        menu_extended=True,
        minimize_to_icons=False,
        landscape_minimize_to_icons=False,
        portrait_minimize_to_icons=False,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)

        self.page = page
        self.pages = pages

        self._minimize_to_icons = minimize_to_icons
        self._landscape_minimize_to_icons = landscape_minimize_to_icons
        self._portrait_minimize_to_icons = portrait_minimize_to_icons
        self._support_routes = support_routes

        self.expand = True

        self.navigation_items = [navigation_item for navigation_item, _ in pages]
        self.routes = [
            f"/{item.pop('route', None) or slugify(item['label'])}"
            for item in self.navigation_items
        ]
        self.navigation_rail = self.build_navigation_rail()
        self.update_destinations()
        self._menu_extended = menu_extended
        self.navigation_rail.extended = menu_extended

        page_contents = [page_content for _, page_content in pages]

        self.menu_panel = Row(
            controls=[self.navigation_rail, VerticalDivider(width=1)],
            spacing=0,
            tight=True,
        )
        self.content_area = Column(page_contents, expand=True)

        self._was_portrait = self.is_portrait()
        self._panel_visible = self.is_landscape()

        self.set_navigation_content()

        if support_routes:
            self._route_change(page.route)
            self.page.on_route_change = self._on_route_change
        self._change_displayed_page()

        self.page.on_resize = self.handle_resize

    def select_page(self, page_number):
        self.navigation_rail.selected_index = page_number
        self._change_displayed_page()

    @property
    def minimize_to_icons(self) -> bool:
        return self._minimize_to_icons or (
            self._landscape_minimize_to_icons and self._portrait_minimize_to_icons
        )

    @minimize_to_icons.setter
    def minimize_to_icons(self, value: bool):
        self._minimize_to_icons = value
        self.set_navigation_content()

    @property
    def landscape_minimize_to_icons(self) -> bool:
        return self._landscape_minimize_to_icons or self._minimize_to_icons

    @landscape_minimize_to_icons.setter
    def landscape_minimize_to_icons(self, value: bool):
        self._landscape_minimize_to_icons = value
        self.set_navigation_content()

    @property
    def portrait_minimize_to_icons(self) -> bool:
        return self._portrait_minimize_to_icons or self._minimize_to_icons

    @portrait_minimize_to_icons.setter
    def portrait_minimize_to_icons(self, value: bool):
        self._portrait_minimize_to_icons = value
        self.set_navigation_content()

    @property
    def menu_extended(self) -> bool:
        return self._menu_extended

    @menu_extended.setter
    def menu_extended(self, value: bool):
        self._menu_extended = value

        dimension_minimized = (
            self.landscape_minimize_to_icons
            if self.is_landscape()
            else self.portrait_minimize_to_icons
        )
        if not dimension_minimized or self._panel_visible:
            self.navigation_rail.extended = value

    def _navigation_change(self, e):
        self._change_displayed_page()
        self.check_toggle_on_select()
        self.page.update()

    def _change_displayed_page(self):
        page_number = self.navigation_rail.selected_index
        if self._support_routes:
            self.page.route = self.routes[page_number]
        for i, content_page in enumerate(self.content_area.controls):
            content_page.visible = page_number == i

    def _route_change(self, route):
        try:
            page_number = self.routes.index(route)
        except ValueError:
            page_number = 0

        self.select_page(page_number)

    def _on_route_change(self, event):
        self._route_change(event.route)
        self.page.update()

    def build_navigation_rail(self):
        return NavigationRail(
            selected_index=0,
            label_type="none",
            on_change=self._navigation_change,
        )

    def update_destinations(self, icons_only=False):
        navigation_items = self.navigation_items
        if icons_only:
            navigation_items = deepcopy(navigation_items)
            for item in navigation_items:
                item.pop("label")

        self.navigation_rail.destinations = [
            NavigationRailDestination(**nav_specs) for nav_specs in navigation_items
        ]
        self.navigation_rail.label_type = "none" if icons_only else "all"

    def handle_resize(self, e):
        if self._was_portrait != self.is_portrait():
            self._was_portrait = self.is_portrait()
            self._panel_visible = self.is_landscape()
            self.set_navigation_content()
            self.page.update()

    def toggle_navigation(self, event=None):
        self._panel_visible = not self._panel_visible
        self.set_navigation_content()
        self.page.update()

    def check_toggle_on_select(self):
        if self.is_portrait() and self._panel_visible:
            self.toggle_navigation()

    def set_navigation_content(self):
        if self.is_landscape():
            self.add_landscape_content()
        else:
            self.add_portrait_content()

    def add_landscape_content(self):
        self.controls = [self.menu_panel, self.content_area]
        if self.landscape_minimize_to_icons:
            self.update_destinations(icons_only=not self._panel_visible)
            self.menu_panel.visible = True
            if not self._panel_visible:
                self.navigation_rail.extended = False
            else:
                self.navigation_rail.extended = self.menu_extended
        else:
            self.update_destinations()
            self.navigation_rail.extended = self._menu_extended
            self.menu_panel.visible = self._panel_visible

    def add_portrait_content(self):
        if self.portrait_minimize_to_icons and not self._panel_visible:
            self.controls = [self.menu_panel, self.content_area]
            self.update_destinations(icons_only=True)
            self.menu_panel.visible = True
            self.navigation_rail.extended = False
        else:
            if self._panel_visible:
                dismiss_shield = Container(
                    expand=True,
                    on_click=self.toggle_navigation,
                )
                self.controls = [
                    Stack(
                        controls=[self.content_area, dismiss_shield, self.menu_panel],
                        expand=True,
                    )
                ]
            else:
                self.controls = [
                    Stack(controls=[self.content_area, self.menu_panel], expand=True)
                ]
            self.update_destinations()
            self.navigation_rail.extended = self.menu_extended
            self.menu_panel.visible = self._panel_visible

    def is_portrait(self) -> bool:
        # Return true if window/display is narrow
        # return self.page.window_height >= self.page.window_width
        return self.page.height >= self.page.width

    def is_landscape(self) -> bool:
        # Return true if window/display is wide
        return self.page.width > self.page.height


if __name__ == "__main__":

    def main(page: Page, title="Basic Responsive Menu"):
        page.title = title

        menu_button = IconButton(icons.MENU)

        page.appbar = AppBar(
            leading=menu_button,
            leading_width=40,
            bgcolor=colors.SURFACE_VARIANT,
        )

        pages = [
            (
                dict(
                    icon=icons.LANDSCAPE_OUTLINED,
                    selected_icon=icons.LANDSCAPE,
                    label="Menu in landscape",
                ),
                create_page(
                    "Menu in landscape",
                    "Menu in landscape is by default shown, side by side with the main content, but can be "
                    "hidden with the menu button.",
                ),
            ),
            (
                dict(
                    icon=icons.PORTRAIT_OUTLINED,
                    selected_icon=icons.PORTRAIT,
                    label="Menu in portrait",
                ),
                create_page(
                    "Menu in portrait",
                    "Menu in portrait is mainly expected to be used on a smaller mobile device."
                    "\n\n"
                    "The menu is by default hidden, and when shown with the menu button it is placed on top of the main "
                    "content."
                    "\n\n"
                    "In addition to the menu button, menu can be dismissed by a tap/click on the main content area.",
                ),
            ),
            (
                dict(
                    icon=icons.INSERT_EMOTICON_OUTLINED,
                    selected_icon=icons.INSERT_EMOTICON,
                    label="Minimize to icons",
                ),
                create_page(
                    "Minimize to icons",
                    "ResponsiveMenuLayout has a parameter minimize_to_icons. "
                    "Set it to True and the menu is shown as icons only, when normally it would be hidden.\n"
                    "\n\n"
                    "Try this with the 'Minimize to icons' toggle in the top bar."
                    "\n\n"
                    "There are also landscape_minimize_to_icons and portrait_minimize_to_icons properties that you can "
                    "use to set this property differently in each orientation.",
                ),
            ),
            (
                dict(
                    icon=icons.COMPARE_ARROWS_OUTLINED,
                    selected_icon=icons.COMPARE_ARROWS,
                    label="Menu width",
                ),
                create_page(
                    "Menu width",
                    "ResponsiveMenuLayout has a parameter manu_extended. "
                    "Set it to False to place menu labels under the icons instead of beside them."
                    "\n\n"
                    "Try this with the 'Menu width' toggle in the top bar.",
                ),
            ),
            (
                dict(
                    icon=icons.ROUTE_OUTLINED,
                    selected_icon=icons.ROUTE,
                    label="Route support",
                    route="custom-route",
                ),
                create_page(
                    "Route support",
                    "ResponsiveMenuLayout has a parameter support_routes, which is True by default. "
                    "\n\n"
                    "Routes are useful only in the web, where the currently selected page is shown in the url, "
                    "and you can open the app directly on a specific page with the right url."
                    "\n\n"
                    "You can specify a route explicitly with a 'route' item in the menu dict (see this page in code). "
                    "If you do not specify the route, a slugified version of the page label is used "
                    "('Menu width' becomes 'menu-width').",
                ),
            ),
            (
                dict(
                    icon=icons.PLUS_ONE_OUTLINED,
                    selected_icon=icons.PLUS_ONE,
                    label="Fine control",
                ),
                create_page(
                    "Adjust navigation rail",
                    "NavigationRail is accessible via the navigation_rail attribute of the ResponsiveMenuLayout. "
                    "In this demo it is used to add the leading button control."
                    "\n\n"
                    "These NavigationRail attributes are used by the ResponsiveMenuLayout, and changing them directly "
                    "will probably break it:\n"
                    "- destinations\n"
                    "- extended\n"
                    "- label_type\n"
                    "- on_change\n",
                ),
            ),
        ]

        menu_layout = ResponsiveMenuLayout(page, pages)

        page.appbar.actions = [
            Row(
                [
                    Text("Minimize\nto icons"),
                    Switch(on_change=lambda e: toggle_icons_only(menu_layout)),
                    Text("Menu\nwidth"),
                    Switch(
                        value=True, on_change=lambda e: toggle_menu_width(menu_layout)
                    ),
                ]
            )
        ]

        menu_layout.navigation_rail.leading = ElevatedButton(
            "Add", icon=icons.ADD, expand=True, on_click=lambda e: print("Add clicked")
        )

        page.add(menu_layout)

        menu_button.on_click = lambda e: menu_layout.toggle_navigation()

    def create_page(title: str, body: str):
        return Row(
            controls=[
                Column(
                    horizontal_alignment="stretch",
                    controls=[
                        Card(content=Container(Text(title, weight="bold"), padding=8)),
                        Text(body),
                    ],
                    expand=True,
                ),
            ],
            expand=True,
        )

    def toggle_icons_only(menu: ResponsiveMenuLayout):
        menu.minimize_to_icons = not menu.minimize_to_icons
        menu.page.update()

    def toggle_menu_width(menu: ResponsiveMenuLayout):
        menu.menu_extended = not menu.menu_extended
        menu.page.update()

    flet.app(target=main)
