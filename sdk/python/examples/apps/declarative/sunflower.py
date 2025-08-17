import math
from dataclasses import dataclass, field

import flet as ft

MAX_SEEDS = 250


@dataclass
class Seed:
    x: float
    y: float
    inner: bool = False


@dataclass
class State:
    seeds_count: int = MAX_SEEDS // 2
    seeds: list[Seed] = field(default_factory=list)

    def change_seeds(self, new_seeds: int):
        self.seeds_count = new_seeds
        self.compute_seeds()

    def compute_seeds(self):
        tau = math.pi * 2
        scale_factor = 1 / 40
        phi = (math.sqrt(5) + 1) / 2

        for i in range(0, self.seeds_count):
            theta = i * tau / phi
            r = math.sqrt(i) * scale_factor
            self.seeds.append(
                Seed(x=r * math.cos(theta), y=-1 * r * math.sin(theta), inner=True)
            )

        for j in range(self.seeds_count, MAX_SEEDS):
            x = math.cos(tau * j / (MAX_SEEDS - 1)) * 0.9
            y = math.sin(tau * j / (MAX_SEEDS - 1)) * 0.9
            self.seeds.append(Seed(x=x, y=y, inner=False))


def main(page: ft.Page):
    page.theme_mode = ft.ThemeMode.DARK
    page.horizontal_alignment = ft.CrossAxisAlignment.STRETCH
    page.add(
        ft.ControlBuilder(
            State(),
            lambda state: ft.Column(
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    ft.Text(
                        "Sunflower",
                        theme_style=ft.TextThemeStyle.HEADLINE_MEDIUM,
                        text_align=ft.TextAlign.CENTER,
                    ),
                    ft.Container(
                        content=ft.Stack(
                            controls=[ft.Text("Hello")],
                            aspect_ratio=1.0,
                        ),
                        bgcolor=ft.Colors.AMBER,
                        alignment=ft.Alignment.CENTER,
                        expand=True,
                    ),
                    ft.Row(
                        [ft.Text(f"Showing {state.seeds_count} seeds")],
                        alignment=ft.MainAxisAlignment.CENTER,
                    ),
                    ft.Row(
                        [
                            ft.Slider(
                                min=1,
                                max=MAX_SEEDS,
                                value=state.seeds_count,
                                width=300,
                                on_change=lambda e: state.change_seeds(
                                    round(e.control.value)
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
