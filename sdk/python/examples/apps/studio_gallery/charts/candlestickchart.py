import flet as ft
import flet_charts as fch

CANDLE_DATA = [
    ("Mon", 24.8, 28.6, 23.9, 27.2),
    ("Tue", 27.2, 30.1, 25.8, 28.4),
    ("Wed", 28.4, 31.2, 26.5, 29.1),
    ("Thu", 29.1, 32.4, 27.9, 31.8),
    ("Fri", 31.8, 34.0, 29.7, 30.2),
    ("Sat", 30.2, 33.6, 28.3, 32.7),
    ("Sun", 32.7, 35.5, 30.1, 34.6),
]


@ft.component
def CandlestickChart():
    info_value, set_info_value = ft.use_state(
        "Interact with the chart to see event details."
    )

    def build_spots() -> list[fch.CandlestickChartSpot]:
        """Create candlestick spots from the static data."""
        spots: list[fch.CandlestickChartSpot] = []
        for index, (label, open_, high, low, close) in enumerate(CANDLE_DATA):
            spots.append(
                fch.CandlestickChartSpot(
                    x=float(index),
                    open=open_,
                    high=high,
                    low=low,
                    close=close,
                    selected=index == len(CANDLE_DATA) - 1,
                    tooltip=fch.CandlestickChartSpotTooltip(
                        text=(
                            f"{label}\n"
                            f"Open: {open_:0.1f}\n"
                            f"High: {high:0.1f}\n"
                            f"Low : {low:0.1f}\n"
                            f"Close: {close:0.1f}"
                        ),
                        bottom_margin=12,
                    ),
                )
            )
        return spots

    spots = build_spots()
    min_x = -0.5
    max_x = len(spots) - 0.5
    min_y = min(low for _, _, _, low, _ in CANDLE_DATA) - 1
    max_y = max(high for _, _, _, _, high in CANDLE_DATA) + 1

    def handle_event(e: fch.CandlestickChartEvent):
        if e.spot_index is not None and e.spot_index >= 0:
            label, open_, high, low, close = CANDLE_DATA[e.spot_index]
            set_info_value(
                f"{e.type.value} • {label}: "
                f"O {open_:0.1f}  H {high:0.1f}  L {low:0.1f}  C {close:0.1f}"
            )
        else:
            set_info_value(f"{e.type.value} • outside candlesticks")

    chart = fch.CandlestickChart(
        expand=True,
        min_x=min_x,
        max_x=max_x,
        min_y=min_y,
        max_y=max_y,
        baseline_x=0,
        baseline_y=min_y,
        bgcolor=ft.Colors.with_opacity(0.2, ft.Colors.BLUE_GREY_900),
        horizontal_grid_lines=fch.ChartGridLines(interval=2, dash_pattern=[2, 2]),
        vertical_grid_lines=fch.ChartGridLines(interval=1, dash_pattern=[2, 2]),
        left_axis=fch.ChartAxis(
            label_spacing=2,
            label_size=60,
            title=ft.Text("Price (k USD)", color=ft.Colors.GREY_300),
            show_min=False,
        ),
        bottom_axis=fch.ChartAxis(
            labels=[
                fch.ChartAxisLabel(
                    value=index,
                    label=ft.Text(name, color=ft.Colors.GREY_300),
                )
                for index, (name, *_rest) in enumerate(CANDLE_DATA)
            ],
            label_spacing=1,
            label_size=40,
            show_min=False,
            show_max=False,
        ),
        spots=spots,
        tooltip=fch.CandlestickChartTooltip(
            bgcolor=ft.Colors.BLUE_GREY_800,
            horizontal_alignment=fch.HorizontalAlignment.CENTER,
            fit_inside_horizontally=True,
        ),
        on_event=handle_event,
    )

    return ft.Container(
        expand=True,
        border_radius=16,
        padding=20,
        content=ft.Column(
            expand=True,
            spacing=20,
            controls=[
                ft.Text(
                    "Weekly OHLC snapshot (demo data)",
                    size=20,
                    weight=ft.FontWeight.BOLD,
                ),
                chart,
                ft.Text(info_value, size=14),
            ],
        ),
    )
