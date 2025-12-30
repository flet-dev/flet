import asyncio
from itertools import islice

import flet as ft

# logging.basicConfig(level=logging.INFO)
ft.context.disable_auto_update()


class IconBrowser(ft.Container):
    def __init__(self, expand=False, height=500):
        super().__init__()
        if expand:
            self.expand = expand
        else:
            self.height = height

    def build(self):
        def batches(iterable, batch_size):
            iterator = iter(iterable)
            while batch := list(islice(iterator, batch_size)):
                yield batch

        # fetch all icon constants from icons.py module
        icons_list = list(ft.Icons)

        async def search_click():
            await display_icons(search_txt.value)

        search_txt = ft.TextField(
            expand=1,
            hint_text="Enter keyword and press search button. "
            "To view all icons enter *",
            autofocus=True,
            on_submit=search_click,
        )

        search_query = ft.Row(
            [search_txt, ft.IconButton(icon=ft.Icons.SEARCH, on_click=search_click)]
        )

        search_results = ft.GridView(
            expand=1,
            runs_count=10,
            max_extent=150,
            spacing=5,
            run_spacing=5,
            child_aspect_ratio=1,
        )
        status_bar = ft.Text()

        async def copy_to_clipboard(e):
            icon_key = e.control.data
            print("Copy to clipboard:", icon_key)
            await ft.Clipboard().set(icon_key)
            self.page.show_dialog(ft.SnackBar(ft.Text(f"Copied {icon_key}")))

        def search_icons(search_term: str):
            # switch variable to allow empty search, which shows all icons
            all_icons = 0
            for icon in icons_list:
                icon_name = icon.name
                if all_icons == 1 or search_term != "":
                    # match search to query
                    if search_term != "" and search_term in icon_name:
                        all_icons = 0
                        yield icon
                    # turn on switch, empty search, and yield to not skip 1st icon
                    elif search_term == "*":
                        all_icons = 1
                        search_term = ""
                        yield icon
                    # all_icons is 1, which allows for empty search, which shows all
                    elif search_term == "" and all_icons == 1:
                        yield icon
                    else:
                        all_icons = 0

        async def display_icons(search_term: str):
            # clean search results
            search_query.disabled = True
            self.update()

            search_results.controls.clear()
            search_results.update()

            print("Searching for icons with term:", search_term)

            for batch in batches(search_icons(search_term.upper()), 500):
                for icon in batch:
                    icon_name = icon.name
                    icon_key = f"ft.Icons.{icon_name}"
                    # print("Found icon:", icon_key)
                    search_results.controls.append(
                        ft.TextButton(
                            content=ft.Container(
                                content=ft.Column(
                                    [
                                        ft.Icon(icon=icon, size=30),
                                        ft.Text(
                                            value=f"{icon_name}",
                                            size=12,
                                            width=100,
                                            no_wrap=True,
                                            text_align=ft.TextAlign.CENTER,
                                            color=ft.Colors.ON_SURFACE_VARIANT,
                                        ),
                                    ],
                                    spacing=5,
                                    alignment=ft.MainAxisAlignment.CENTER,
                                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                ),
                                alignment=ft.Alignment.CENTER,
                            ),
                            tooltip=f"{icon_key}\nClick to copy to a clipboard",
                            on_click=copy_to_clipboard,
                            data=icon_key,
                        )
                    )
                status_bar.value = f"Icons found: {len(search_results.controls)}"
                self.update()
                print(f"Displayed {len(search_results.controls)} icons so far...")
                await asyncio.sleep(0.1)  # allow UI to update

            if len(search_results.controls) == 0:
                self.page.show_dialog(ft.SnackBar(ft.Text("No icons found")))
            search_query.disabled = False
            self.update()

        self.content = ft.Column(
            [
                search_query,
                search_results,
                status_bar,
            ],
            expand=True,
        )


def main(page: ft.Page):
    page.title = "Flet icons browser"
    page.add(IconBrowser(expand=True))


ft.run(main)
