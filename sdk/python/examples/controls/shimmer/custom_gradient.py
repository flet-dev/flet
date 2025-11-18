import flet as ft


def _stat_block(
    title: str,
    subtitle: str,
    *,
    width: int = 240,
    height: int = 350,
) -> ft.Control:
    def metric(width: int, height: int = 14) -> ft.Control:
        return ft.Container(
            width=width,
            height=height,
            bgcolor=ft.Colors.WHITE,
            opacity=0.6,
            border_radius=ft.BorderRadius.all(height),
        )

    return ft.Container(
        width=width,
        height=height,
        padding=ft.Padding.all(20),
        bgcolor=ft.Colors.with_opacity(0.1, ft.Colors.BLACK),
        border_radius=ft.BorderRadius.all(24),
        content=ft.Column(
            spacing=16,
            controls=[
                metric(140),
                ft.Row(spacing=10, controls=[metric(60, 10), metric(90, 10)]),
                ft.Container(
                    width=width - 40,
                    height=56,
                    border_radius=ft.BorderRadius.all(16),
                    bgcolor=ft.Colors.WHITE,
                    opacity=0.35,
                ),
                ft.Column(spacing=8, controls=[metric(120, 12), metric(160, 12)]),
                ft.Text(title, weight=ft.FontWeight.W_600),
                ft.Text(subtitle, size=12),
            ],
        ),
    )


def main(page: ft.Page):
    page.title = "Shimmer - custom gradients"
    page.padding = 30
    page.bgcolor = "#0e0e18"
    accent = ft.LinearGradient(
        begin=ft.Alignment(-1.0, -0.5),
        end=ft.Alignment(1.0, 0.5),
        colors=[
            ft.Colors.PURPLE,
            ft.Colors.PINK_300,
            ft.Colors.AMBER_200,
            ft.Colors.PURPLE,
        ],
        stops=[0.1, 0.55, 0.9, 1.0],
    )

    cards = ft.Row(
        wrap=True,
        spacing=24,
        run_spacing=24,
        controls=[
            ft.Shimmer(
                gradient=accent,
                direction=ft.ShimmerDirection.TTB,
                period=2200,
                content=_stat_block("Recent activity", "Smooth top-to-bottom sweep"),
            ),
        ],
    )

    page.add(cards)


if __name__ == "__main__":
    ft.run(main)
