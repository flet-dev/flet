import flet as ft


def main(page: ft.Page):
    def set_android(e: ft.Event[ft.Button]):
        page.platform = ft.PagePlatform.ANDROID
        page.update()
        print("New platform:", page.platform)

    def set_ios(e: ft.Event[ft.Button]):
        page.platform = ft.PagePlatform.IOS
        page.update()
        print("New platform:", page.platform)

    page.add(
        ft.Switch(label="Switch A", adaptive=True),
        ft.Button("Set Android", on_click=set_android),
        ft.Button("Set iOS", on_click=set_ios),
    )

    print("Default platform:", page.platform)


if __name__ == "__main__":
    ft.run(main)
