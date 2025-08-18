import math
import random
from dataclasses import dataclass, field
from typing import cast

import flet as ft

MAX_SEEDS = 250

rnd = random.Random()


@dataclass
class Seed:
    key: int
    x: float
    y: float
    inner: bool = False


@dataclass
class State:
    seeds_count: int = MAX_SEEDS // 2
    seeds: list[Seed] = field(default_factory=list)

    def __post_init__(self):
        self.compute_seeds()

    def update_seeds_count(self, new_seeds_count: int):
        self.seeds_count = new_seeds_count
        self.compute_seeds()

    def compute_seeds(self):
        self.seeds.clear()
        tau = math.pi * 2
        scale_factor = 1 / 40
        phi = (math.sqrt(5) + 1) / 2

        # inner orange seeds
        for i in range(0, self.seeds_count):
            theta = i * tau / phi
            r = math.sqrt(i) * scale_factor
            self.seeds.append(
                Seed(
                    key=i, x=r * math.cos(theta), y=-1 * r * math.sin(theta), inner=True
                )
            )

        # outer gray seeds
        for j in range(self.seeds_count, MAX_SEEDS):
            x = math.cos(tau * j / (MAX_SEEDS - 1)) * 0.9
            y = math.sin(tau * j / (MAX_SEEDS - 1)) * 0.9
            self.seeds.append(Seed(key=j, x=x, y=y, inner=False))


@ft.cache
def seed_view(seed: Seed):
    return ft.Container(
        key=seed.key,
        width=5,
        height=5,
        bgcolor=ft.Colors.ORANGE if seed.inner else ft.Colors.GREY_700,
        align=ft.Alignment(seed.x, seed.y),
        animate_align=ft.Animation(round(rnd.random() * 500) + 250),
        border_radius=2.5,
    )


def main(page: ft.Page):
    state = State()
    page.theme_mode = ft.ThemeMode.DARK
    page.horizontal_alignment = ft.CrossAxisAlignment.STRETCH
    page.appbar = ft.AppBar(title=ft.Text("Sunflower"))
    page.dark_theme = ft.Theme(
        appbar_theme=ft.AppBarTheme(center_title=True, elevation=2)
    )
    page.add(
        ft.StateView(
            state,
            lambda state: ft.Column(
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    ft.Container(
                        content=ft.Stack(
                            controls=[seed_view(s) for s in state.seeds],
                            aspect_ratio=1.0,
                        ),
                        alignment=ft.Alignment.CENTER,
                        expand=True,
                    ),
                    ft.Row(
                        [
                            ft.Text(
                                f"Showing {state.seeds_count} "
                                f"seed{'s' if state.seeds_count != 1 else ''}"
                            )
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                    ),
                    ft.Row(
                        [
                            ft.Slider(
                                min=1,
                                max=MAX_SEEDS,
                                value=state.seeds_count,
                                width=300,
                                on_change=lambda e: state.update_seeds_count(
                                    round(cast(float, e.control.value))
                                ),
                            )
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                    ),
                ],
            ),
            expand=True,
        ),
    )


ft.run(main)
