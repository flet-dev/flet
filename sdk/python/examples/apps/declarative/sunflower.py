import logging
import math
import random
from dataclasses import dataclass, field
from typing import cast

import flet as ft

logging.basicConfig(level=logging.INFO)
logging.getLogger("flet_components").setLevel(logging.INFO)

MAX_SEEDS = 250

rnd = random.Random()


@dataclass
class Seed:
    key: int
    x: float
    y: float
    inner: bool = False


@dataclass
class AppModel(ft.Observable):
    seeds_count: float = MAX_SEEDS // 2
    seeds: list[Seed] = field(default_factory=list)

    def __post_init__(self):
        ft.context.page.title = "Sunflower"
        self.compute_seeds()

    def update_seeds_count(self, new_seeds_count: float):
        self.seeds_count = new_seeds_count
        self.compute_seeds()

    def compute_seeds(self):
        count = round(self.seeds_count)
        self.seeds.clear()
        tau = math.pi * 2
        scale_factor = 1 / 40
        phi = (math.sqrt(5) + 1) / 2

        # inner orange seeds
        for i in range(0, count):
            theta = i * tau / phi
            r = math.sqrt(i) * scale_factor
            self.seeds.append(
                Seed(
                    key=i, x=r * math.cos(theta), y=-1 * r * math.sin(theta), inner=True
                )
            )

        # outer gray seeds
        for j in range(count, MAX_SEEDS):
            x = math.cos(tau * j / (MAX_SEEDS - 1)) * 0.9
            y = math.sin(tau * j / (MAX_SEEDS - 1)) * 0.9
            self.seeds.append(Seed(key=j, x=x, y=y, inner=False))


@ft.component
def SeedView(seed: Seed, key=None) -> ft.Control:
    return ft.Container(
        width=5,
        height=5,
        bgcolor=ft.Colors.ORANGE if seed.inner else ft.Colors.GREY_700,
        align=ft.Alignment(seed.x, seed.y),
        animate_align=ft.Animation(round(rnd.random() * 500) + 250),
        border_radius=2.5,
    )


@ft.component
def Sunflower():
    app, _ = ft.use_state(lambda: AppModel())
    MemoSeedView = ft.memo(SeedView)
    return ft.View(
        appbar=ft.AppBar(title=ft.Text("Sunflower")),
        controls=[
            ft.Column(
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                expand=True,
                controls=[
                    ft.Container(
                        content=ft.Stack(
                            controls=[MemoSeedView(s, key=s.key) for s in app.seeds],
                            aspect_ratio=1.0,
                        ),
                        alignment=ft.Alignment.CENTER,
                        expand=True,
                    ),
                    ft.Row(
                        [
                            ft.Text(
                                f"Showing {round(app.seeds_count)} "
                                f"seed{'s' if app.seeds_count != 1 else ''}"
                            )
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                    ),
                    ft.Row(
                        [
                            ft.Slider(
                                min=1,
                                max=MAX_SEEDS,
                                value=app.seeds_count,
                                width=300,
                                on_change=lambda e: app.update_seeds_count(
                                    cast(float, e.control.value)
                                ),
                            )
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                    ),
                ],
            )
        ],
    )


ft.run(lambda page: page.render_views(Sunflower))
