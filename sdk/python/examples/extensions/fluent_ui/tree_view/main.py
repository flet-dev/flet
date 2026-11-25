import flet_fluent_ui as fluent

import flet as ft


def main(page: ft.Page):
    page.title = "Fluent TreeView"

    def count_selected(items: list[fluent.TreeViewItem]) -> int:
        # Files are the items without subitems.
        return sum(
            count_selected(item.items) if item.items else int(bool(item.selected))
            for item in items
        )

    def handle_selection_change(e: ft.Event[fluent.TreeView]):
        status.value = f"{count_selected(tree.items)} files to back up"

    tree = fluent.TreeView(
        selection_mode=fluent.TreeViewSelectionMode.MULTIPLE,
        on_selection_change=handle_selection_change,
        items=[
            fluent.TreeViewItem(
                "Documents",
                leading=fluent.FluentIcons.FOLDER_HORIZONTAL,
                expanded=True,
                items=[
                    fluent.TreeViewItem("Budget.xlsx"),
                    fluent.TreeViewItem("Report.docx"),
                ],
            ),
            fluent.TreeViewItem(
                "Pictures",
                leading=fluent.FluentIcons.FOLDER_HORIZONTAL,
                items=[
                    fluent.TreeViewItem("Beach.png"),
                    fluent.TreeViewItem("Mountains.png"),
                ],
            ),
        ],
    )
    status = ft.Text("0 files to back up")

    page.add(
        ft.SafeArea(content=ft.Column(controls=[ft.Container(tree, width=300), status]))
    )


if __name__ == "__main__":
    ft.run(main)
