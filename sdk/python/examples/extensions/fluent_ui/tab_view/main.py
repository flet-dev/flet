import flet_fluent_ui as fluent

import flet as ft


def main(page: ft.Page):
    page.title = "Fluent TabView"

    count = 0

    def new_tab() -> fluent.Tab:
        nonlocal count
        count += 1
        return fluent.Tab(
            f"Document {count}",
            icon=fluent.FluentIcons.DOCUMENT,
            content=ft.Container(
                padding=12,
                content=ft.Text(f"Contents of document {count}"),
            ),
            on_close=close_tab,
        )

    def add_tab(e: ft.Event[fluent.TabView]):
        tabs.tabs.append(new_tab())
        tabs.selected_index = len(tabs.tabs) - 1

    def close_tab(e: ft.Event[fluent.Tab]):
        index = tabs.tabs.index(e.control)
        tabs.tabs.remove(e.control)
        if tabs.selected_index >= index:
            tabs.selected_index = max(0, tabs.selected_index - 1)

    def reorder_tab(e: ft.OnReorderEvent):
        tabs.tabs.insert(e.new_index, tabs.tabs.pop(e.old_index))
        tabs.selected_index = e.new_index

    tabs = fluent.TabView(
        height=200,
        tabs=[new_tab(), new_tab()],
        on_add=add_tab,
        on_reorder=reorder_tab,
    )

    page.add(ft.SafeArea(content=tabs))


if __name__ == "__main__":
    ft.run(main)
