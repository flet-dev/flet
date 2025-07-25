import flet as ft


def main(page: ft.Page):
    page.theme_mode = ft.ThemeMode.LIGHT
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    lp_counter = 0
    cl_counter = 0
    td_counter = 0

    def on_click(e):
        nonlocal cl_counter
        cl_counter += 1
        t1.spans[-1] = ft.TextSpan(
            text=f"  {cl_counter}  ",
            style=ft.TextStyle(size=16, bgcolor=ft.Colors.TEAL_300),
        )
        page.update()

    def on_long_press(e):
        nonlocal lp_counter
        lp_counter += 1
        t3.spans[-1] = ft.TextSpan(
            text=f"  {lp_counter}  ",
            style=ft.TextStyle(size=16, bgcolor=ft.Colors.TEAL_300),
        )
        page.update()

    def on_tap_down(e):
        nonlocal td_counter
        td_counter += 1
        t2.spans[-1] = ft.TextSpan(
            text=f"  {td_counter}  ",
            style=ft.TextStyle(size=16, bgcolor=ft.Colors.TEAL_300),
        )
        page.update()

    c = ft.Container(
        bgcolor=ft.Colors.PINK_900,
        alignment=ft.Alignment.CENTER,
        padding=ft.Padding.all(10),
        height=150,
        width=150,
        on_click=on_click,
        on_long_press=on_long_press,
        on_tap_down=on_tap_down,
        content=ft.Text(
            "Press Me!",
            text_align=ft.TextAlign.CENTER,
            style=ft.TextStyle(
                size=30,
                # weight=ft.FontWeight.BOLD,
                foreground=ft.Paint(
                    color=ft.Colors.BLUE_700,
                    stroke_cap=ft.StrokeCap.BUTT,
                    stroke_width=2,
                    stroke_join=ft.StrokeJoin.BEVEL,
                    style=ft.PaintingStyle.STROKE,
                ),
            ),
            theme_style=ft.TextThemeStyle.DISPLAY_MEDIUM,
        ),
    )
    t1 = ft.Text(
        spans=[
            ft.TextSpan(
                text="On Click", style=ft.TextStyle(size=16, weight=ft.FontWeight.BOLD)
            ),
            ft.TextSpan(text=" counter:  ", style=ft.TextStyle(size=16, italic=True)),
            ft.TextSpan(
                text=f"  {cl_counter}  ",
                style=ft.TextStyle(size=16, bgcolor=ft.Colors.TEAL_300),
            ),
        ]
    )
    t2 = ft.Text(
        spans=[
            ft.TextSpan(
                text="Tap Down", style=ft.TextStyle(size=16, weight=ft.FontWeight.BOLD)
            ),
            ft.TextSpan(text=" counter:  ", style=ft.TextStyle(size=16, italic=True)),
            ft.TextSpan(
                text=f"  {td_counter}  ",
                style=ft.TextStyle(size=16, bgcolor=ft.Colors.TEAL_300),
            ),
        ]
    )
    t3 = ft.Text(
        spans=[
            ft.TextSpan(
                text="Long Press",
                style=ft.TextStyle(size=16, weight=ft.FontWeight.BOLD),
            ),
            ft.TextSpan(text=" counter:  ", style=ft.TextStyle(size=16, italic=True)),
            ft.TextSpan(
                text=f"  {lp_counter}  ",
                style=ft.TextStyle(size=16, bgcolor=ft.Colors.TEAL_300),
            ),
        ]
    )

    page.add(c, t1, t3, t2)


ft.run(main)
