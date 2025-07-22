import flet as ft


def main(page: ft.Page):
    page.bgcolor = "#5946A7"

    def change(i):
        home.content.icon_color = "#060806"
        search.content.icon_color = "#060806"
        per.content.icon_color = "#060806"
        fav.content.icon_color = "#060806"
        home.width = 50
        search.width = 50
        per.width = 50
        fav.width = 50
        home.content.bgcolor = "#FBFFFD"
        search.content.bgcolor = "#FBFFFD"
        per.content.bgcolor = "#FBFFFD"
        fav.content.bgcolor = "#FBFFFD"
        home.content.text = "‎ "
        search.content.text = "‎ "
        per.content.text = "‎ "
        fav.content.text = "‎ "
        if i == "home":
            home.width = 117
            home.content.text = "Home"
            page.bgcolor = "#5946A7"
            home.content.icon_color = "#5946A7"
            home.content.bgcolor = "#DFD9F2"
        elif i == "fav":
            fav.width = 117
            fav.content.text = "Liked"
            page.bgcolor = "#B45386"
            fav.content.icon_color = "#B45386"
            fav.content.bgcolor = "#F8DAEB"
        elif i == "search":
            search.width = 117
            search.content.text = "Search"
            page.bgcolor = "#E1A01D"
            search.content.icon_color = "#E1A01D"
            search.content.bgcolor = "#FCEED2"
        elif i == "per":
            per.width = 117
            per.content.text = "Profile"
            page.bgcolor = "#1684A0"
            per.content.icon_color = "#1684A0"
            per.content.bgcolor = "#CEE8ED"
        page.update()

    home = ft.Container(
        animate=ft.animation.Animation(1000, "bounceOut"),
        width=117,
        height=100,
        content=ft.ElevatedButton(
            elevation=0,
            icon=ft.Icons.HOME,
            icon_color="#5946A7",
            color="#5946A7",
            text="Home",
            bgcolor="#DFD9F2",
            on_click=lambda i: [change("home")],
        ),
    )
    fav = ft.Container(
        animate=ft.animation.Animation(1000, "bounceOut"),
        width=50,
        height=100,
        content=ft.ElevatedButton(
            elevation=0,
            icon=ft.Icons.FAVORITE,
            icon_color="#060806",
            color="#B45386",
            text="Liked",
            bgcolor="#FBFFFD",
            on_click=lambda i: [change("fav")],
        ),
    )
    search = ft.Container(
        animate=ft.animation.Animation(1000, "bounceOut"),
        width=50,
        height=100,
        content=ft.ElevatedButton(
            elevation=0,
            icon=ft.Icons.SEARCH,
            icon_color="#060806",
            color="#E1A01D",
            text="Search",
            bgcolor="#FBFFFD",
            on_click=lambda i: [change("search")],
        ),
    )
    per = ft.Container(
        animate=ft.animation.Animation(1000, "bounceOut"),
        width=50,
        height=100,
        content=ft.ElevatedButton(
            elevation=0,
            icon=ft.Icons.PERSON_ROUNDED,
            icon_color="#060806",
            color="#1684A0",
            text="Profile",
            bgcolor="#FBFFFD",
            on_click=lambda i: [change("per")],
        ),
    )
    page.bottom_appbar = ft.BottomAppBar(
        bgcolor=ft.Colors.WHITE,
        shape=ft.NotchShape.CIRCULAR,
        content=ft.Row(
            controls=[
                ft.Row(
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=30,
                    controls=[home, fav, search, per],
                )
            ]
        ),
    )

    page.add(ft.Text(""))


ft.app(target=main)
