import asyncio
import copy
import json
from pathlib import Path

import flet as ft

APP_NAME = "Mind Queue"
DATA_FILE = Path(__file__).resolve().parent / "data.json"


def load_data():
    if not DATA_FILE.exists():
        raise FileNotFoundError(f"{DATA_FILE} not found")
    with DATA_FILE.open("r", encoding="utf-8") as f:
        return json.load(f)


def save_data(data):
    with DATA_FILE.open("w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)


def main(page: ft.Page):
    page.title = APP_NAME
    page.theme_mode = ft.ThemeMode.DARK
    page.bgcolor = "#111111"
    page.padding = ft.padding.symmetric(horizontal=24, vertical=24)
    page.horizontal_alignment = ft.CrossAxisAlignment.START
    page.vertical_alignment = ft.MainAxisAlignment.START
    page.scroll = ft.ScrollMode.HIDDEN

    data = load_data()
    current_system: str | None = None

    def handle_keyboard_event(e: ft.KeyboardEvent):
        if e.key == "Escape" and current_system is not None:
            show_dashboard()

    page.on_keyboard_event = handle_keyboard_event

    # ---------- Dialog helpers ----------
    def confirm_delete_system(system_name: str):
        def do_delete(ev):
            close_current_dialog()
            delete_system(system_name)

        def do_cancel(ev):
            close_current_dialog()

        dlg = ft.AlertDialog(
            modal=True,
            title=ft.Text("Confirm delete"),
            content=ft.Text(
                f"Delete '{system_name}' permanently?\n\nThis action cannot be undone."
            ),
            actions=[
                ft.TextButton("Cancel", on_click=do_cancel),
                ft.TextButton(
                    "Delete",
                    icon=ft.Icons.DELETE_FOREVER,
                    icon_color="red",
                    on_click=do_delete,
                ),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )
        open_dialog(dlg)

    def close_current_dialog():
        for ctl in page.overlay:
            if isinstance(ctl, ft.AlertDialog):
                ctl.open = False
        page.update()

    def open_dialog(dialog: ft.AlertDialog):
        if dialog not in page.overlay:
            page.overlay.append(dialog)
        dialog.open = True
        page.update()

    # ---------- System ----------
    def clone_system(system_name: str):
        if system_name not in data:
            return

        base_name = f"Copy of {system_name}"
        new_name = base_name
        counter = 2

        while new_name in data:
            new_name = f"{base_name} ({counter})"
            counter += 1

        # deep copy to avoid shared references
        data[new_name] = copy.deepcopy(data[system_name])
        save_data(data)

    def delete_system(system_name: str):
        nonlocal current_system
        if len(data.keys()) == 1:
            return
        data.pop(system_name, None)
        save_data(data)
        current_system = None
        show_dashboard()

    # ---------- Dashboard ----------

    def show_dashboard(e=None):
        nonlocal current_system
        current_system = None

        page.appbar = None
        page.clean()

        title = ft.Row(
            [ft.Text(APP_NAME, size=32, weight=ft.FontWeight.BOLD)],
            alignment=ft.MainAxisAlignment.CENTER,
        )

        systems_list: list[ft.Control] = []

        def open_system(system_name: str):
            show_system(system_name)

        def open_system_actions(system_name: str):
            def do_open(e):
                close_current_dialog()
                show_system(system_name)

            async def do_clone(e):
                close_current_dialog()
                clone_system(system_name)
                await asyncio.sleep(0)
                show_dashboard()

            dlg = ft.AlertDialog(
                modal=True,
                title=ft.Text(system_name),
                actions=[
                    # ft.TextButton("Open", on_click=do_open),
                    ft.TextButton(
                        "Clone",
                        icon=ft.Icons.CONTENT_COPY,
                        on_click=do_clone,
                    ),
                    ft.TextButton(
                        "Delete",
                        icon=ft.Icons.DELETE_OUTLINE,
                        icon_color=ft.Colors.RED,
                        disabled=len(data) == 1,
                        on_click=lambda e: confirm_delete_system(system_name),
                    ),
                    ft.TextButton("Cancel", on_click=lambda e: close_current_dialog()),
                ],
                actions_alignment=ft.MainAxisAlignment.END,
            )
            open_dialog(dlg)

        for system_name in data:
            gesture = ft.GestureDetector(
                content=ft.Container(
                    ft.Row(
                        [ft.Text(system_name, size=18, weight=ft.FontWeight.W_600)],
                    ),
                    padding=10,
                    margin=ft.margin.only(bottom=8),
                    border_radius=8,
                    bgcolor="#1c1c1c",
                ),
                on_tap=lambda e, n=system_name: open_system(n),
                on_long_press_start=lambda e, n=system_name: open_system_actions(n),
                mouse_cursor=ft.MouseCursor.CLICK,
            )
            systems_list.append(gesture)

        def open_add_system_dialog(e):
            name_field = ft.TextField(label="System name")

            def on_add(ev):
                try:
                    name = name_field.value.strip()

                    # simple validation instead of silently doing nothing
                    if not name:
                        name_field.error_text = "Name is required"
                        page.update()
                        return

                    if name in data:
                        name_field.error_text = "System already exists"
                        page.update()
                        return

                    # create system and persist
                    data[name] = {}
                    save_data(data)

                    # close dialog and redraw dashboard
                    close_current_dialog()
                    show_dashboard()

                except Exception as ex:
                    # if *anything* goes wrong, don't freeze – log it
                    print("add_system error:", ex)

            dlg = ft.AlertDialog(
                modal=True,
                title=ft.Text("Add system"),
                content=name_field,
                actions=[
                    ft.TextButton("Cancel", on_click=close_current_dialog),
                    ft.TextButton("Add", on_click=on_add),
                ],
            )
            open_dialog(dlg)

        add_system_btn = ft.FilledButton(
            "Add system", icon=ft.Icons.ADD, on_click=open_add_system_dialog
        )

        page.add(
            ft.Column(
                [
                    title,
                    ft.Column(systems_list, spacing=4),
                    ft.Container(height=14),
                    add_system_btn,
                ],
                spacing=12,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            )
        )
        page.update()

    # ---------- System View ----------

    def show_system(system_name: str):
        nonlocal current_system
        current_system = system_name
        system_data: dict[str, list[list]] = data.get(system_name, {})

        def edit_system_name():
            name_field = ft.TextField(label="System name", value=system_name)

            def on_save(ev):
                new_name = name_field.value.strip()
                if not new_name or new_name == system_name or new_name in data:
                    close_current_dialog()
                    return

                data[new_name] = data.pop(system_name)
                save_data(data)
                close_current_dialog()
                show_system(new_name)

            dlg = ft.AlertDialog(
                modal=True,
                title=ft.Text("Rename system"),
                content=name_field,
                actions=[
                    ft.TextButton("Cancel", on_click=close_current_dialog),
                    ft.TextButton("Save", on_click=on_save),
                ],
            )
            open_dialog(dlg)

        page.appbar = ft.AppBar(
            leading=ft.IconButton(icon=ft.Icons.ARROW_BACK, on_click=show_dashboard),
            title=ft.Text(system_name, size=32, weight=ft.FontWeight.BOLD),
            bgcolor=page.bgcolor,
            center_title=True,
            actions=[
                ft.IconButton(
                    icon=ft.Icons.EDIT,
                    tooltip="Rename",
                    on_click=lambda e: edit_system_name(),
                )
            ],
        )

        page.clean()
        content_controls: list[ft.Control] = []

        # ---------- Task helpers ----------

        def clone_task(header: str, index: int):
            if header not in system_data:
                return
            tasks = system_data[header]
            if index < 0 or index >= len(tasks):
                return

            title, label, done = tasks[index]

            # Clone task (reset done)
            cloned = [f"{title} (copy)", label, False]

            tasks.insert(index + 1, cloned)
            save_data(data)

        def toggle_task(header: str, index: int, value: bool):
            if header not in system_data:
                return
            if index < 0 or index >= len(system_data[header]):
                return
            try:
                system_data[header][index][2] = value
                save_data(data)
                close_current_dialog()
                show_system(system_name)
            except Exception as ex:
                print("toggle_task error:", ex)

        def delete_task(header: str, index: int):
            if header not in system_data:
                return
            if index < 0 or index >= len(system_data[header]):
                return
            try:
                system_data[header].pop(index)
                save_data(data)
                close_current_dialog()
                show_system(system_name)
            except Exception as ex:
                print("delete_task error:", ex)

        def edit_task(header: str, index: int):
            if header not in system_data:
                return
            if index < 0 or index >= len(system_data[header]):
                return

            try:
                title_val, label_val, done_val = system_data[header][index]
            except Exception as ex:
                print("edit_task load error:", ex)
                return

            title_field = ft.TextField(label="Title", value=title_val)
            label_field = ft.TextField(label="Task", value=label_val)

            def on_save(ev):
                tl = title_field.value.strip()
                lb = label_field.value.strip()
                if not tl or not lb:
                    return

                if header not in system_data:
                    return
                if index < 0 or index >= len(system_data[header]):
                    return

                try:
                    system_data[header][index][0] = tl
                    system_data[header][index][1] = lb
                    save_data(data)
                    close_current_dialog()
                    show_system(system_name)
                except Exception as ex:
                    print("edit_task save error:", ex)

            dlg = ft.AlertDialog(
                modal=True,
                title=ft.Text("Edit task"),
                content=ft.Column([title_field, label_field], tight=True),
                actions=[
                    ft.TextButton("Cancel", on_click=close_current_dialog),
                    ft.TextButton("Save", on_click=on_save),
                ],
            )
            open_dialog(dlg)

        def move_task(header: str, index: int, direction: int):
            """Move a task up or down within its header (no UI calls here)."""
            if header not in system_data:
                return
            tasks = system_data[header]
            new_index = index + direction
            if new_index < 0 or new_index >= len(tasks):
                return
            try:
                tasks[index], tasks[new_index] = tasks[new_index], tasks[index]
                save_data(data)
            except Exception as ex:
                print("move_task error:", ex)

        def open_task_actions(header: str, index: int):
            """Long-press menu: Move up / Move down / Edit / Delete."""
            total = len(system_data.get(header, []))
            is_first = index == 0
            is_last = index == total - 1

            def do_clone(ev):
                close_current_dialog()
                clone_task(header, index)
                show_system(system_name)

            def do_move_up(ev):
                close_current_dialog()
                move_task(header, index, -1)
                show_system(system_name)

            def do_move_down(ev):
                close_current_dialog()
                move_task(header, index, +1)
                show_system(system_name)

            def do_edit(ev):
                close_current_dialog()
                edit_task(header, index)

            def do_delete(ev):
                close_current_dialog()
                delete_task(header, index)

            def do_cancel(ev):
                close_current_dialog()

            dlg = ft.AlertDialog(
                modal=True,
                title=ft.Text("Task actions"),
                actions=[
                    ft.TextButton(
                        "Move up",
                        icon=ft.Icons.ARROW_UPWARD,
                        on_click=do_move_up,
                        disabled=is_first,
                    ),
                    ft.TextButton(
                        "Move down",
                        icon=ft.Icons.ARROW_DOWNWARD,
                        on_click=do_move_down,
                        disabled=is_last,
                    ),
                    ft.TextButton("Edit", on_click=do_edit),
                    ft.TextButton(
                        "Clone",
                        icon=ft.Icons.CONTENT_COPY,
                        on_click=do_clone,
                    ),
                    ft.TextButton(
                        "Delete",
                        icon=ft.Icons.DELETE_OUTLINE,
                        on_click=do_delete,
                    ),
                    ft.TextButton("Cancel", on_click=do_cancel),
                ],
                actions_alignment=ft.MainAxisAlignment.END,
            )
            open_dialog(dlg)

        def add_task(header: str):
            title_field = ft.TextField(label="Title")
            label_field = ft.TextField(label="Task")

            def on_add(ev):
                tl = title_field.value.strip()
                lb = label_field.value.strip()
                if not tl or not lb:
                    return
                system_data.setdefault(header, []).append([tl, lb, False])
                save_data(data)
                close_current_dialog()
                show_system(system_name)

            dlg = ft.AlertDialog(
                modal=True,
                title=ft.Text(f"Add task to {header}"),
                content=ft.Column([title_field, label_field], tight=True),
                actions=[
                    ft.TextButton("Cancel", on_click=close_current_dialog),
                    ft.TextButton("Add", on_click=on_add),
                ],
            )
            open_dialog(dlg)

        # ---------- Header helpers ----------

        def delete_header(header: str):
            system_data.pop(header, None)
            save_data(data)
            show_system(system_name)

        def edit_header(header: str):
            name_field = ft.TextField(label="Header name", value=header)

            def on_save(ev):
                new_name = name_field.value.strip()
                if not new_name or new_name == header or new_name in system_data:
                    close_current_dialog()
                    return

                system_data[new_name] = system_data.pop(header)
                save_data(data)
                close_current_dialog()
                show_system(system_name)

            dlg = ft.AlertDialog(
                modal=True,
                title=ft.Text("Rename header"),
                content=name_field,
                actions=[
                    ft.TextButton("Cancel", on_click=close_current_dialog),
                    ft.TextButton("Save", on_click=on_save),
                ],
            )
            open_dialog(dlg)

        def add_header():
            name_field = ft.TextField(label="Header name")

            def on_add(ev):
                name = name_field.value.strip()
                if not name:
                    return
                system_data[name] = []
                save_data(data)
                close_current_dialog()
                show_system(system_name)

            dlg = ft.AlertDialog(
                modal=True,
                title=ft.Text("Add header"),
                content=name_field,
                actions=[
                    ft.TextButton("Cancel", on_click=close_current_dialog),
                    ft.TextButton("Add", on_click=on_add),
                ],
            )
            open_dialog(dlg)

        # ---------- Draw headers + tasks ----------

        def confirm_delete_header(header_name: str):
            txt = ft.Text(
                f"Delete '{header_name}' permanently?\nThis cannot be undone."
            )

            def do_delete(ev):
                close_current_dialog()
                delete_header(header_name)

            def do_cancel(ev):
                close_current_dialog()

            dlg = ft.AlertDialog(
                modal=True,
                title=ft.Text("Confirm delete"),
                content=txt,
                actions=[
                    ft.TextButton("Cancel", on_click=do_cancel),
                    ft.TextButton(
                        "Delete", icon=ft.Icons.DELETE_FOREVER, on_click=do_delete
                    ),
                ],
                actions_alignment=ft.MainAxisAlignment.END,
            )
            open_dialog(dlg)

        for header_name, tasks in system_data.items():
            content_controls.append(ft.Container(height=10))

            # header row
            content_controls.append(
                ft.Row(
                    [
                        ft.Text(header_name, size=20, weight=ft.FontWeight.BOLD),
                        ft.Row(
                            [
                                ft.IconButton(
                                    icon=ft.Icons.EDIT,
                                    tooltip="Rename",
                                    on_click=lambda e, h=header_name: edit_header(h),
                                ),
                                ft.IconButton(
                                    icon=ft.Icons.DELETE_OUTLINE,
                                    icon_color="red",
                                    tooltip="Delete",
                                    on_click=lambda e, h=header_name: (
                                        confirm_delete_header(h)
                                    ),
                                ),
                            ]
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                )
            )

            # tasks
            for idx, (title_str, label, done) in enumerate(tasks):
                current_index = idx  # capture for lambdas

                color = ft.Colors.WHITE70 if done else ft.Colors.WHITE
                deco = (
                    ft.TextDecoration.LINE_THROUGH if done else ft.TextDecoration.NONE
                )

                row = ft.Row(
                    [
                        ft.Checkbox(
                            value=done,
                            width=24,
                            height=24,
                            on_change=lambda e, s=header_name, i=current_index: (
                                toggle_task(s, i, e.control.value)
                            ),
                        ),
                        ft.Text(
                            title_str,
                            size=16,
                            weight=ft.FontWeight.BOLD,
                            color=color,
                            style=ft.TextStyle(decoration=deco),
                        ),
                        ft.Container(width=8),
                        ft.Text(
                            label,
                            size=16,
                            color=color,
                            style=ft.TextStyle(decoration=deco),
                        ),
                        ft.Container(expand=True),
                    ],
                    alignment=ft.MainAxisAlignment.START,
                    spacing=6,
                )

                gesture = ft.GestureDetector(
                    content=row,
                    on_tap=lambda e, s=header_name, i=current_index: edit_task(s, i),
                    on_long_press_start=lambda e, s=header_name, i=current_index: (
                        open_task_actions(s, i)
                    ),
                    mouse_cursor=ft.MouseCursor.CLICK,
                )
                content_controls.append(gesture)

            # add task button under this header
            content_controls.append(
                ft.FilledButton(
                    "Add task",
                    icon=ft.Icons.ADD,
                    on_click=lambda e, s=header_name: add_task(s),
                )
            )

        # bottom: add header + delete system
        content_controls.append(ft.Container(height=16))

        def confirm_delete_system():
            txt = ft.Text(
                f"Delete '{system_name}' permanently?\nThis cannot be undone."
            )

            def do_delete(ev):
                close_current_dialog()
                delete_system(system_name)

            def do_cancel(ev):
                close_current_dialog()

            dlg = ft.AlertDialog(
                modal=True,
                title=ft.Text("Confirm delete"),
                content=txt,
                actions=[
                    ft.TextButton("Cancel", on_click=do_cancel),
                    ft.TextButton(
                        "Delete", icon=ft.Icons.DELETE_FOREVER, on_click=do_delete
                    ),
                ],
                actions_alignment=ft.MainAxisAlignment.END,
            )
            open_dialog(dlg)

        content_controls.append(
            ft.Row(
                [
                    ft.FilledButton(
                        "Add Header",
                        icon=ft.Icons.ADD,
                        on_click=lambda e: add_header(),
                    ),
                    ft.FilledButton(
                        "Delete System",
                        icon=ft.Icons.DELETE_FOREVER,
                        bgcolor="red",
                        color="white",
                        on_click=lambda e: confirm_delete_system(),
                    ),
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            )
        )

        page.add(ft.Column(content_controls, spacing=6, expand=True))
        page.update()

    # start at dashboard
    show_dashboard()


if __name__ == "__main__":
    ft.app(target=main)
