import flet as ft


def main(page: ft.Page):
    def set_android(e: ft.Event[ft.ElevatedButton]):
        page.platform = ft.PagePlatform.ANDROID
        page.update()
        print("New platform:", page.platform)

    def set_ios(e: ft.Event[ft.ElevatedButton]):
        page.platform = ft.PagePlatform.IOS
        page.update()
        print("New platform:", page.platform)

    page.add(
        ft.Switch(label="Switch A", adaptive=True),
        ft.ElevatedButton("Set Android", on_click=set_android),
        ft.ElevatedButton("Set iOS", on_click=set_ios),
    )

    print("Default platform:", page.platform)


ft.run(main)
