import flet as ft


class PopupColorItem(ft.PopupMenuItem):
    def __init__(self, color, name):
        super().__init__()
        self.content = ft.Row(
            controls=[
                ft.Icon(name=ft.Icons.COLOR_LENS_OUTLINED, color=color),
                ft.Text(name),
            ],
        )
        self.on_click = self.seed_color_changed
        self.data = color

    def seed_color_changed(self, e):
        self.page.theme = self.page.dark_theme = ft.Theme(color_scheme_seed=self.data)
        self.page.update()


class NavigationItem(ft.Container):
    def __init__(self, destination, item_clicked):
        super().__init__()
        self.ink = True
        self.padding = 10
        self.border_radius = 5
        self.destination = destination
        self.icon = destination.icon
        self.text = destination.label
        self.content = ft.Row([ft.Icon(self.icon), ft.Text(self.text)])
        self.on_click = item_clicked


class NavigationColumn(ft.Column):
    def __init__(self, gallery):
        super().__init__()
        self.expand = 4
        self.spacing = 0
        self.scroll = ft.ScrollMode.ALWAYS
        self.width = 200
        self.gallery = gallery
        self.selected_index = 0
        self.controls = self.get_navigation_items()

    def before_update(self):
        super().before_update()
        self.update_selected_item()

    def get_navigation_items(self):
        navigation_items = []
        for destination in self.gallery.control_groups:
            navigation_items.append(
                NavigationItem(destination, item_clicked=self.item_clicked)
            )
        return navigation_items

    def item_clicked(self, e):
        self.selected_index = e.control.destination.index
        self.update_selected_item()
        self.page.go(f"/{e.control.destination.name}")

    def update_selected_item(self):
        # self.selected_index = self.gallery.control_groups.index(
        #     self.gallery.selected_control_group
        # )
        for item in self.controls:
            item.bgcolor = None
            item.content.controls[0].name = item.destination.icon
        self.controls[self.selected_index].bgcolor = ft.Colors.SECONDARY_CONTAINER
        self.controls[self.selected_index].content.controls[0].name = self.controls[
            self.selected_index
        ].destination.selected_icon


class LeftNavigationMenu(ft.Column):
    def __init__(self, gallery):
        super().__init__()
        self.gallery = gallery

        self.rail = NavigationColumn(gallery=gallery)

        self.dark_light_text = ft.Text("Light theme")
        self.dark_light_icon = ft.IconButton(
            icon=ft.Icons.BRIGHTNESS_2_OUTLINED,
            tooltip="Toggle brightness",
            on_click=self.theme_changed,
        )

        self.controls = [
            self.rail,
            ft.Column(
                expand=1,
                controls=[
                    ft.Row(
                        controls=[
                            self.dark_light_icon,
                            self.dark_light_text,
                        ]
                    ),
                    ft.Row(
                        controls=[
                            ft.PopupMenuButton(
                                icon=ft.Icons.COLOR_LENS_OUTLINED,
                                items=[
                                    PopupColorItem(
                                        color="deeppurple", name="Deep purple"
                                    ),
                                    PopupColorItem(color="indigo", name="Indigo"),
                                    PopupColorItem(color="blue", name="Blue (default)"),
                                    PopupColorItem(color="teal", name="Teal"),
                                    PopupColorItem(color="green", name="Green"),
                                    PopupColorItem(color="yellow", name="Yellow"),
                                    PopupColorItem(color="orange", name="Orange"),
                                    PopupColorItem(
                                        color="deeporange", name="Deep orange"
                                    ),
                                    PopupColorItem(color="pink", name="Pink"),
                                ],
                            ),
                            ft.Text("Seed color"),
                        ]
                    ),
                ],
            ),
        ]

    def theme_changed(self, e):
        if self.page.theme_mode == ft.ThemeMode.LIGHT:
            self.page.theme_mode = ft.ThemeMode.DARK
            self.dark_light_text.value = "Dark theme"
            self.dark_light_icon.icon = ft.Icons.BRIGHTNESS_HIGH
        else:
            self.page.theme_mode = ft.ThemeMode.LIGHT
            self.dark_light_text.value = "Light theme"
            self.dark_light_icon.icon = ft.Icons.BRIGHTNESS_2
        self.page.update()
