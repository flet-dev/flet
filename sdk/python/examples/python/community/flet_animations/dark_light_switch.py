import flet as ft


def main(page: ft.Page):
    global dic
    dic = {}
    page.bgcolor = "white"
    page.padding = 0
    angel_ = 0
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.MainAxisAlignment.CENTER
    global def_
    def_ = 0

    def change(i):
        global def_
        if def_ == 0:
            init = -1
            page.bgcolor = "#2C2B2C"
            while True:
                init += 0.1
                dark_ligt_switch.controls[0].alignment = ft.alignment.Alignment(init, 0)
                dark_ligt_switch.controls[0].content.rotate = ft.Rotate(
                    angle=init, alignment=ft.alignment.center
                )
                if init >= 1:
                    break
                if init >= 0:
                    dark_ligt_switch.controls[
                        0
                    ].content.content.name = ft.Icons.DARK_MODE
                    dark_ligt_switch.controls[0].content.content.color = "white"
                    dark_ligt_switch.controls[0].content.bgcolor = "#2C2B2C"
                page.update()
            def_ = 1
        else:
            init = 1
            page.bgcolor = "white"
            while True:
                init -= 0.1
                dark_ligt_switch.controls[0].alignment = ft.alignment.Alignment(init, 0)
                dark_ligt_switch.controls[0].content.rotate = ft.Rotate(
                    angle=init, alignment=ft.alignment.center
                )
                if init <= -1:
                    break
                if init <= 0:
                    dark_ligt_switch.controls[
                        0
                    ].content.content.name = ft.Icons.LIGHT_MODE
                    dark_ligt_switch.controls[0].content.content.color = "yellow"
                    dark_ligt_switch.controls[0].content.bgcolor = "white"
                page.update()
            def_ = 0

    shadow_ = ft.BoxShadow(
        spread_radius=1,
        blur_radius=15,
        color=ft.Colors.BLUE_GREY_300,
        offset=ft.Offset(0, 0),
        blur_style=ft.ShadowBlurStyle.OUTER,
    )
    dark_ligt_switch = ft.Row(
        alignment="center",
        controls=[
            ft.Container(
                shadow=shadow_,
                animate=ft.animation.Animation(600, "easeInOut"),
                alignment=ft.alignment.Alignment(-1, 0),
                padding=ft.Padding.only(left=5, right=5),
                content=ft.Container(
                    animate_rotation=ft.animation.Animation(600, "easeInOut"),
                    content=ft.Icon(name=ft.Icons.LIGHT_MODE, color="#FFDC5D", size=27),
                    height=40,
                    width=40,
                    border_radius=100,
                    bgcolor="white",
                    shadow=shadow_,
                ),
                height=50,
                width=100,
                border_radius=100,
                bgcolor="#FEFDFE",
                on_click=change,
            )
        ],
    )
    page.add(dark_ligt_switch)


ft.app(target=main)
