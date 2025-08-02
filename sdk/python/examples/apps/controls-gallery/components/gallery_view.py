import flet as ft
from components.controls_grid import ControlsGrid
from components.examples_view import ExamplesView
from components.left_navigation_menu import LeftNavigationMenu


class GalleryView(ft.Row):
    def __init__(self, gallery):
        super().__init__()
        self.gallery = gallery
        self.left_nav = LeftNavigationMenu(gallery)
        self.controls_grid = ControlsGrid(gallery)
        self.examples_view = ExamplesView(gallery)
        self.expand = True
        self.controls = [
            self.left_nav,
            ft.VerticalDivider(width=1),
            self.controls_grid,
            self.examples_view,
        ]

    def display_controls_grid(self, control_group_name):
        self.controls_grid.display(self.gallery.get_control_group(control_group_name))
        self.examples_view.examples.controls = []
        self.examples_view.visible = False
        self.page.update()

    def display_control_examples(self, control_group_name, control_name):
        self.examples_view.display(
            self.gallery.get_control(
                # self.gallery.selected_control_group.name, control_name
                control_group_name,
                control_name,
            )
        )
        self.controls_grid.visible = False
        self.page.update()
