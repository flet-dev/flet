import flet as ft


def main(page: ft.Page):
    page.add(
        ft.Tabs(
            selected_index=1,
            animation_duration=300,
            expand=1,
            tabs=[
                ft.Tab(
                    label="Dining",
                    icon=ft.Icons.RESTAURANT,
                    content=ft.Tabs(
                        secondary=True,
                        tabs=[
                            ft.Tab(
                                label="Fast Food",
                                content=ft.Text("Grab something on the go!"),
                            ),
                            ft.Tab(
                                label="Fine Dining", content=ft.Text("Take your time!")
                            ),
                        ],
                    ),
                ),
                ft.Tab(
                    label="Entertainment",
                    icon=ft.Icons.LOCAL_ACTIVITY,
                    content=ft.Tabs(
                        secondary=True,
                        tabs=[
                            ft.Tab(label="Cinema", content=ft.Text("Find a Film!")),
                            ft.Tab(
                                label="Music", content=ft.Text("Listen to some Tunes!")
                            ),
                        ],
                    ),
                ),
                ft.Tab(
                    label="Lodging",
                    icon=ft.Icons.HOTEL,
                    content=ft.Tabs(
                        secondary=True,
                        tabs=[
                            ft.Tab(label="Hotel", content=ft.Text("Enjoy your Room!")),
                            ft.Tab(label="Hostel", content=ft.Text("Grab a Bunk!")),
                        ],
                    ),
                ),
            ],
        )
    )


ft.run(main)
