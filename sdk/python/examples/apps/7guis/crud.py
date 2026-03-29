from dataclasses import dataclass

import flet as ft


@dataclass
class Person:
    id: int
    first_name: str
    last_name: str


def main(page: ft.Page):
    page.title = "7GUIs - CRUD"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    people = [
        Person(id=1, first_name="Ada", last_name="Lovelace"),
        Person(id=2, first_name="Grace", last_name="Hopper"),
        Person(id=3, first_name="Katherine", last_name="Johnson"),
        Person(id=4, first_name="Alan", last_name="Turing"),
    ]
    next_id = max(person.id for person in people) + 1
    selected_id: int | None = people[0].id

    def get_selected_person() -> Person | None:
        for person in people:
            if person.id == selected_id:
                return person
        return None

    def filtered_people() -> list[Person]:
        prefix = filter_field.value.strip().lower()
        if not prefix:
            return people
        return [
            person for person in people if person.last_name.lower().startswith(prefix)
        ]

    def set_selection(person_id: int | None):
        nonlocal selected_id
        selected_id = person_id
        refresh_ui()

    def person_label(person: Person) -> str:
        return f"{person.last_name}, {person.first_name}"

    def build_person_item(person: Person) -> ft.Container:
        is_selected = person.id == selected_id
        return ft.Container(
            padding=14,
            border_radius=16,
            bgcolor=ft.Colors.BLUE_100 if is_selected else ft.Colors.WHITE,
            border=ft.Border.all(
                2 if is_selected else 1,
                ft.Colors.BLUE_400 if is_selected else ft.Colors.BLACK_12,
            ),
            on_click=lambda e, person_id=person.id: set_selection(person_id),
            content=ft.Row(
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                controls=[
                    ft.Text(
                        person_label(person),
                        weight=ft.FontWeight.W_600,
                        overflow=ft.TextOverflow.ELLIPSIS,
                        expand=True,
                    ),
                    ft.Icon(ft.Icons.CHEVRON_RIGHT, color=ft.Colors.BLUE_GREY_400),
                ],
            ),
        )

    def refresh_ui():
        selected_person = get_selected_person()
        if selected_person:
            first_name.value = selected_person.first_name
            last_name.value = selected_person.last_name
            update_button.disabled = False
            delete_button.disabled = False
        else:
            first_name.value = ""
            last_name.value = ""
            update_button.disabled = True
            delete_button.disabled = True

        people_list.controls = [
            build_person_item(person) for person in filtered_people()
        ]
        page.update()

    def validate_form() -> bool:
        first_name.error = None
        last_name.error = None
        ok = True
        if not first_name.value.strip():
            first_name.error = "Required"
            ok = False
        if not last_name.value.strip():
            last_name.error = "Required"
            ok = False
        if not ok:
            page.update()
        return ok

    def create_person(e: ft.Event[ft.IconButton]):
        nonlocal next_id, selected_id
        if not validate_form():
            return
        people.append(
            Person(
                id=next_id,
                first_name=first_name.value.strip(),
                last_name=last_name.value.strip(),
            )
        )
        selected_id = next_id
        next_id += 1
        refresh_ui()

    def update_person(e: ft.Event[ft.IconButton]):
        person = get_selected_person()
        if person is None or not validate_form():
            return
        person.first_name = first_name.value.strip()
        person.last_name = last_name.value.strip()
        refresh_ui()

    def delete_person(e: ft.Event[ft.IconButton]):
        nonlocal selected_id
        if selected_id is None:
            return
        visible = filtered_people()
        remaining = [person for person in people if person.id != selected_id]
        people[:] = remaining
        selected_id = remaining[0].id if remaining else None
        if visible and visible[0].id == selected_id:
            selected_id = visible[0].id
        refresh_ui()

    page.add(
        ft.SafeArea(
            content=ft.Container(
                padding=28,
                border_radius=24,
                bgcolor=ft.Colors.INDIGO_50,
                content=ft.Column(
                    tight=True,
                    spacing=20,
                    scroll=ft.ScrollMode.AUTO,
                    controls=[
                        ft.Text("CRUD", size=28, weight=ft.FontWeight.W_700),
                        ft.Text(
                            "Filter by surname, select a person, then create, update, or remove records.",
                            color=ft.Colors.BLUE_GREY_700,
                        ),
                        ft.Row(
                            wrap=True,
                            vertical_alignment=ft.CrossAxisAlignment.START,
                            controls=[
                                ft.Container(
                                    width=250,
                                    height=360,
                                    padding=16,
                                    border_radius=20,
                                    bgcolor=ft.Colors.WHITE,
                                    content=ft.Column(
                                        spacing=14,
                                        controls=[
                                            filter_field := ft.TextField(
                                                label="Filter by last name",
                                                width=220,
                                                on_change=lambda e: refresh_ui(),
                                            ),
                                            ft.Divider(height=1),
                                            people_list := ft.ListView(
                                                expand=True, spacing=10
                                            ),
                                        ],
                                    ),
                                ),
                                ft.Container(
                                    width=250,
                                    padding=16,
                                    border_radius=20,
                                    bgcolor=ft.Colors.WHITE,
                                    content=ft.Column(
                                        spacing=14,
                                        controls=[
                                            first_name := ft.TextField(
                                                label="First name",
                                                width=220,
                                            ),
                                            last_name := ft.TextField(
                                                label="Last name",
                                                width=220,
                                            ),
                                            ft.Row(
                                                alignment=ft.MainAxisAlignment.CENTER,
                                                controls=[
                                                    ft.IconButton(
                                                        ft.Icons.PERSON_ADD,
                                                        icon_color=ft.Colors.BLUE,
                                                        tooltip="Create",
                                                        on_click=create_person,
                                                    ),
                                                    update_button := ft.IconButton(
                                                        ft.Icons.EDIT_SQUARE,
                                                        tooltip="Update",
                                                        on_click=update_person,
                                                    ),
                                                    delete_button := ft.IconButton(
                                                        ft.Icons.DELETE_OUTLINE,
                                                        tooltip="Delete",
                                                        style=ft.ButtonStyle(
                                                            color=ft.Colors.RED,
                                                        ),
                                                        on_click=delete_person,
                                                    ),
                                                ],
                                            ),
                                        ],
                                    ),
                                ),
                            ],
                        ),
                    ],
                ),
            ),
        )
    )
    refresh_ui()


if __name__ == "__main__":
    ft.run(main)
