import json

import flet as ft

NOTES = "notes.json"


async def main(page: ft.Page):
    page.title = "Notes"
    storage = ft.FileStorage()
    notes: list[str] = []

    def show():
        note_list.controls = [ft.Text(n) for n in notes]
        status.value = f"{len(notes)} notes saved"
        page.update()

    async def save():
        await storage.write(NOTES, json.dumps(notes).encode())

    async def add_note():
        if not new_note.value:
            return
        notes.append(new_note.value)
        new_note.value = ""
        await save()
        show()

    async def clear_notes():
        notes.clear()
        await storage.delete(NOTES)
        show()

    page.add(
        ft.SafeArea(
            content=ft.Column(
                controls=[
                    ft.Row(
                        [
                            new_note := ft.TextField(
                                label="New note", on_submit=add_note
                            ),
                            ft.Button("Add", on_click=add_note),
                            ft.OutlinedButton("Clear", on_click=clear_notes),
                        ]
                    ),
                    status := ft.Text(),
                    note_list := ft.Column(),
                ]
            )
        )
    )

    # The notes outlive the app: load what an earlier run saved.
    saved = await storage.read(NOTES)
    if saved is not None:
        notes.extend(json.loads(saved))
    show()


if __name__ == "__main__":
    ft.run(main)
