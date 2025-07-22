import math
import threading
import time
from dataclasses import dataclass, field
from typing import Callable, Optional

import flet
from beartype.typing import List
from flet import (
    ButtonStyle,
    ClipBehavior,
    Container,
    ElevatedButton,
    FilledButton,
    Page,
    Stack,
    Vector,
    colors,
    icons,
)

try:
    from typing import Literal
except ImportError:
    from typing_extensions import Literal


Corner = Literal[
    "top left",
    "top right",
    "bottom left",
    "bottom right",
    "center",
]

Direction = Literal[
    "horizontal",
    "vertical",
    "curve down",
    "curve up",
]


@dataclass
class MenuItem:
    icon: str
    handler: Callable
    style: Optional[ButtonStyle] = field(default_factory=ButtonStyle)


class AnimatedMenuButton(Stack):
    DEFAULT_SIZE = 50
    DEFAULT_GAP = 5
    DEFAULT_OPEN_DURATION = 300  # milliseconds

    _corner_direction = {  # horizontal, vertical
        "top left": [1, 1],
        "top right": [-1, 1],
        "bottom left": [1, -1],
        "bottom right": [-1, -1],
    }
    _curve_parameters = {  # starting angle, angle delta, menu_rotation
        "top left down": [0, 1, 1],
        "top left up": [1, -1, -1],
        "top right down": [0, 1, -1],
        "top right up": [1, -1, 1],
        "bottom left down": [1, -1, 1],
        "bottom left up": [0, 1, -1],
        "bottom right down": [1, -1, -1],
        "bottom right up": [0, 1, 1],
    }

    def __init__(
        self,
        menu_items: List[MenuItem],
        *args,
        corner: Corner = "top left",
        direction: Direction = "vertical",
        margin: int = 8,
        menu_button_icon: str = icons.MENU,
        menu_button_style: ButtonStyle = None,
        menu_item_size: int = DEFAULT_SIZE,
        menu_item_gap: int = DEFAULT_GAP,
        menu_open_duration: int = DEFAULT_OPEN_DURATION,
        rotate_on_opening: bool = True,
        clip_behavior: ClipBehavior = "none",
        **kwargs,
    ):
        super().__init__(*args, clip_behavior=clip_behavior, **kwargs)
        self.menu_items = menu_items
        self.corner = corner
        self.direction = direction
        self.margin = margin
        self.menu_item_size = menu_item_size
        self.menu_item_gap = menu_item_gap
        self.menu_open_duration = menu_open_duration
        self.rotate_on_opening = rotate_on_opening

        self._open = False
        self._lock = threading.Lock()

        self.expand = True
        self.menu_button_container = Container(
            FilledButton(
                icon=menu_button_icon, style=menu_button_style, on_click=self.toggle
            ),
            width=self.menu_item_size,
            height=self.menu_item_size,
            border_radius=self.menu_item_size / 2,
            animate_rotation=self.menu_open_duration,
            animate_position=self.menu_open_duration,
        )

        self._angle_between_items = 0
        self._radius_to_fit_items = 0

        self._set_size_and_placement()

        self.controls = self._create_menu_buttons() + [self.menu_button_container]

    def _set_size_and_placement(self):
        """
        Make this Stack just large enough to contain the opened menu. Place everything in the right corner,
        with margin.
        """

        # Set size
        if self.direction.startswith("curve"):
            self._calculate_angle_and_radius()
            width = height = self._radius_to_fit_items + self.menu_item_size
        else:
            width = self.menu_item_size
            height = (len(self.menu_items) + 1) * self.menu_item_size + len(
                self.menu_items
            ) * self.menu_item_gap

            if self.direction == "horizontal":
                width, height = height, width

        self.width, self.height = width, height

        # Place this stack and the menu button in the right corner
        for attribute in self.corner.split():
            setattr(self, attribute, self.margin)
            setattr(self.menu_button_container, attribute, 0)

    def _create_menu_buttons(self):
        menu_buttons = [
            Container(
                ElevatedButton(
                    icon=menu_item.icon,
                    style=menu_item.style,
                    on_click=self._menu_click_handler,
                    data=menu_item.handler,
                    disabled=True,
                ),
                width=self.menu_item_size,
                height=self.menu_item_size,
                border_radius=self.menu_item_size / 2,
                opacity=0,
            )
            for menu_item in self.menu_items
        ]

        for attribute in self.corner.split():
            for button in menu_buttons:
                setattr(button, attribute, 0)

        return menu_buttons

    @property
    def open(self) -> bool:
        return self._open

    @open.setter
    def open(self, value: bool):
        was_open = self._open
        self._open = value

        with self._lock:
            if self._open != was_open:
                is_curved = self.direction.split()[0] == "curve"
                if self._open:
                    for button in self.controls[:-1]:
                        button.content.disabled = False
                    if is_curved:
                        self._open_animation_curve()
                    else:
                        self._open_animation_linear()
                else:
                    for button in self.controls[:-1]:
                        button.content.disabled = True
                    if is_curved:
                        self._close_animation_curve()
                    else:
                        self._close_animation_linear()

    def toggle(self, event):
        self.open = not self.open

    def _menu_click_handler(self, event):
        event.control.data(event)
        self.open = False

    def _open_animation_linear(self):
        distance_to_move = self._set_rolling_speed()
        distance_attribute = self._get_distance_attribute()
        if self.direction == "horizontal" and self.rotate_on_opening:
            self.menu_button_container.rotate = math.pi / 2
        setattr(self.menu_button_container, distance_attribute, distance_to_move)
        self.menu_button_container.update()
        for i, menu_item in enumerate(self.controls[:-1]):
            setattr(
                menu_item,
                distance_attribute,
                i * (self.menu_item_size + self.menu_item_gap),
            )
            menu_item.opacity = 1
            menu_item.update()
            time.sleep(self.menu_open_duration / 1000.0 / len(self.controls))

    def _close_animation_linear(self):
        distance_attribute = self._get_distance_attribute()
        self._set_rolling_speed()
        setattr(self.menu_button_container, distance_attribute, 0)
        if self.rotate_on_opening:
            self.menu_button_container.rotate = 0
        self.menu_button_container.update()
        for i, menu_item in enumerate(reversed(self.controls[:-1])):
            menu_item.opacity = 0
            menu_item.update()
            time.sleep(self.menu_open_duration / 1000.0 / len(self.controls))

    def _open_animation_curve(self):
        corner_and_direction_key = f"{self.corner} {self.direction.split()[1]}"
        (
            angle_multiplier,
            delta_multiplier,
            rotation_multiplier,
        ) = self._curve_parameters[corner_and_direction_key]

        if self.rotate_on_opening:
            self.menu_button_container.rotate = rotation_multiplier * math.pi / 2
            self.menu_button_container.animate_rotation = self.menu_open_duration
            self.menu_button_container.update()

        starting_angle = angle_multiplier * math.pi / 2

        vertical_attribute, horizontal_attribute = self.corner.split()
        for i, menu_item in enumerate(self.controls[:-1]):
            vector_to_menu_item = Vector.polar(
                starting_angle + delta_multiplier * i * self._angle_between_items,
                self._radius_to_fit_items,
            )
            setattr(menu_item, horizontal_attribute, vector_to_menu_item.x)
            setattr(menu_item, vertical_attribute, vector_to_menu_item.y)
            menu_item.animate_opacity = 100
            menu_item.opacity = 1
            menu_item.update()
            time.sleep(self.menu_open_duration / 1000.0 / (len(self.menu_items) - 1))

    def _close_animation_curve(self):
        if self.rotate_on_opening:
            self.menu_button_container.rotate = 0
            self.menu_button_container.animate_rotation = self.menu_open_duration
            self.menu_button_container.update()
        for menu_item in reversed(self.controls[:-1]):
            menu_item.animate_opacity = 100
            menu_item.opacity = 0
            menu_item.update()
            time.sleep(self.menu_open_duration / 1000.0 / (len(self.menu_items) - 1))

    def _get_distance_attribute(self):
        vertical, horizontal = self.corner.split()
        return horizontal if self.direction == "horizontal" else vertical

    def _set_rolling_speed(self):
        distance_to_move = (len(self.controls) - 1) * (self.menu_item_size + 5)
        radius = self.menu_item_size / 2
        distance_to_roll = 2 * math.pi * radius / 4
        time_to_roll = int(
            distance_to_roll / distance_to_move * self.menu_open_duration
        )
        self.menu_button_container.animate_rotation = time_to_roll

        return distance_to_move

    def _calculate_angle_and_radius(self):
        item_count = len(self.menu_items)
        available_angle = math.pi / 2
        self._angle_between_items = available_angle / (item_count - 1)
        half_angle = self._angle_between_items / 2
        distance_between_item_centers = self.menu_item_size + self.menu_item_gap
        half_distance = distance_between_item_centers / 2
        self._radius_to_fit_items = half_distance / math.sin(half_angle)


if __name__ == "__main__":

    def dummy_menu_handler(event):
        print("Clicked")

    def main(page: Page):
        menu_items = [
            MenuItem(icon=icons.ADD_OUTLINED, handler=dummy_menu_handler),
            MenuItem(icon=icons.EDIT_OUTLINED, handler=dummy_menu_handler),
            MenuItem(icon=icons.INFO_OUTLINED, handler=dummy_menu_handler),
            MenuItem(
                icon=icons.DELETE_OUTLINE,
                handler=dummy_menu_handler,
                style=ButtonStyle(bgcolor=colors.ERROR_CONTAINER),
            ),
        ]

        page.overlay.extend(
            [
                AnimatedMenuButton(menu_items),
                AnimatedMenuButton(
                    menu_items, corner="top right", direction="curve down"
                ),
                AnimatedMenuButton(
                    menu_items, corner="bottom left", direction="horizontal"
                ),
                AnimatedMenuButton(
                    menu_items, corner="bottom right", direction="curve up"
                ),
            ]
        )

        page.update()

    flet.app(target=main)
