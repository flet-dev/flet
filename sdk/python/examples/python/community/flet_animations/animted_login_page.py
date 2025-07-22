import flet as ft


def main(page: ft.Page):
    global dic
    dic = {}
    page.vertical_alignment = ft.MainAxisAlignment.END
    page.horizontal_alignment = ft.MainAxisAlignment.END
    page.padding = 0
    global def_, animated_container
    def_ = 0

    def change(i):
        global def_, animated_container
        if def_ == 0:
            animated_container.content = side_bar_right
            animated_container.update()
            init = -1
            a = 20
            b = 300
            c = 20
            d = 300
            step = 0
            page.update()
            while True:
                init += 0.1
                login_register_page.alignment = ft.alignment.Alignment(init, 0)
                a += 14
                b -= 14
                c += 14
                d -= 14
                login_register_page.content.content.border_radius = (
                    ft.border_radius.only(a, b, c, d)
                )
                if init >= 1:
                    break
                if init >= 0:
                    pass
                page.update()
            def_ = 1
        else:
            init = 1

            a = 300
            b = 20
            c = 300
            d = 20
            side_bar_left.border_radius = ft.border_radius.only(300, 20, 300, 20)
            page.update()
            animated_container.content = side_bar_left
            animated_container.update()
            while True:
                init -= 0.1
                login_register_page.alignment = ft.alignment.Alignment(init, 0)
                a -= 14
                b += 14
                c -= 14
                d += 14
                login_register_page.content.content.border_radius = (
                    ft.border_radius.only(a, b, c, d)
                )
                if init <= -1:
                    break
                if init <= 0:
                    pass
                page.update()

            def_ = 0

    img = ft.Image(
        src="D:/download_d_temp/colorful-abstract-wave-background-colorful-paper-cut/paper_cut_background_2.jpg",
        fit=ft.BoxFit.CONTAIN,
    )
    shadow_ = ft.BoxShadow(
        spread_radius=10,
        blur_radius=20,
        color=ft.Colors.BLACK,
        offset=ft.Offset(0, 0),
        blur_style=ft.ShadowBlurStyle.OUTER,
    )
    text_login = ft.Row(
        alignment="center",
        controls=[ft.Text("Welcome Back.", size=45, weight=ft.FontWeight.W_700)],
    )
    text_login_2 = ft.Row(
        alignment="center",
        controls=[
            ft.Text("Login to your account.", size=20, weight=ft.FontWeight.W_400)
        ],
    )
    login_button = ft.Row(
        alignment="center",
        controls=[
            ft.ElevatedButton(
                height=40,
                width=100,
                text="Login",
                bgcolor="black",
                color="white",
                on_click=change,
            )
        ],
    )
    text_register = ft.Row(
        alignment="center",
        controls=[ft.Text("Hi, welcome to", size=45, weight=ft.FontWeight.W_700)],
    )
    text_register_2 = ft.Row(
        alignment="center",
        controls=[ft.Text("our website.", size=45, weight=ft.FontWeight.W_700)],
    )
    text_register_3 = ft.Row(
        alignment="center",
        controls=[
            ft.Text("Register to use our website.", size=20, weight=ft.FontWeight.W_400)
        ],
    )
    register_button = ft.Row(
        alignment="center",
        controls=[
            ft.ElevatedButton(
                height=40,
                width=110,
                text="Register",
                bgcolor="black",
                color="white",
                on_click=change,
            )
        ],
    )
    side_bar_right = ft.Container(
        animate=ft.animation.Animation(600, "easein"),
        expand=True,
        width=430,
        border_radius=ft.border_radius.only(20, 300, 20, 300),
        bgcolor="white",
        content=ft.Column(
            spacing=20,
            alignment="center",
            controls=[
                ft.Column(spacing=0, controls=[text_register, text_register_2]),
                text_register_3,
                register_button,
            ],
        ),
    )
    side_bar_left = ft.Container(
        animate=ft.animation.Animation(600, "easein"),
        expand=True,
        width=430,
        border_radius=ft.border_radius.only(20, 300, 20, 300),
        bgcolor="white",
        content=ft.Column(
            spacing=20,
            alignment="center",
            controls=[text_login, text_login_2, login_button],
        ),
    )
    register_form = ft.Container(bgcolor="black", height=500, expand=True)
    login_form = ft.Container(bgcolor="black", height=500, expand=True)
    animated_container = ft.AnimatedSwitcher(
        content=side_bar_left,
        transition="scale",
        duration=400,
        reverse_duration=300,
        switch_in_curve="easein",
        switch_out_curve="easeout",
    )
    login_register_page = ft.Container(
        animate=ft.animation.Animation(600, "easein"),
        border=ft.border.all(0.2, "white"),
        alignment=ft.alignment.Alignment(-1, 0),
        height=500,
        width=800,
        blur=30,
        border_radius=20,
        shadow=shadow_,
        content=animated_container,
    )
    page.overlay.append(
        ft.Row(
            alignment="center",
            controls=[
                ft.Column(
                    alignment="center", controls=[ft.Stack([login_register_page])]
                )
            ],
        )
    )
    page.update()
    page.add(img)


ft.app(target=main)
