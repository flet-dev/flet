import flet as ft


def main(page: ft.Page):
    
    print(page.width)
    print(page.height)

    page.add(
        ft.ListView(
            expand=True,
            controls=[
                ft.FletMap(expand=True, latitude=40.766666,
                           longtitude=29.916668,zoom=12,screenView = [6,4],)
            ]
        ))

    # page.add(ft.FletMap(expand=True))


if __name__ == '__main__':
    # FletMap()
    ft.app(target=main)
