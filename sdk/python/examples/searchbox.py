import flet
from flet import SearchBox, Stack, Text


def searchboxes():
    return Stack(
        gap=20,
        controls=[
            Stack(
                horizontal=True,
                gap=25,
                controls=[
                    Stack(
                        controls=[
                            Text("Default searchbox", size="xLarge"),
                            SearchBox(),
                        ]
                    ),
                    Stack(
                        controls=[
                            Text("Underlined SearchBox", size="xLarge"),
                            SearchBox(
                                underlined=True, placeholder="Search files and folders"
                            ),
                        ]
                    ),
                ],
            ),
            Stack(
                horizontal=True,
                gap=25,
                controls=[
                    Stack(
                        controls=[
                            Text("Disabled SearchBox", size="xLarge"),
                            SearchBox(disabled=True, placeholder="Search something..."),
                            SearchBox(
                                underlined=True,
                                disabled=True,
                                placeholder="Search something...",
                            ),
                        ]
                    ),
                    Stack(
                        controls=[
                            Text("SearchBox with custom icon", size="xLarge"),
                            SearchBox(
                                placeholder="Filter something by",
                                icon="Filter",
                                icon_color="red",
                            ),
                        ]
                    ),
                ],
            ),
            Text("SearchBox with Search, Clear and Escape events", size="xLarge"),
            searchbox_with_search_clear_escape(),
            Text("SearchBox with Change event", size="xLarge"),
            searchbox_with_change(),
        ],
    )


def searchbox_with_search_clear_escape():
    def enter_clicked(e):
        messages.controls.append(Text(f"You have searched for {sb.value}."))
        sb.value = ""
        stack.update()

    def clear_or_esc_clicked(e):
        messages.controls.append(Text("You have cleared the box."))
        stack.update()

    sb = SearchBox(
        placeholder="Search something and click Enter, X or Esc",
        on_search=enter_clicked,
        on_clear=clear_or_esc_clicked,
    )
    messages = Stack()
    stack = Stack(controls=[sb, messages])
    return stack


def searchbox_with_change():
    def searchbox_changed(e):
        t.value = f"You have searched for {sb.value}."
        stack.update()

    sb = SearchBox(placeholder="Search something...", on_change=searchbox_changed)
    t = Text()
    stack = Stack(controls=[sb, t])
    return stack


def main(page):

    page.title = "Searchbox control samples"
    page.update()
    page.add(searchboxes())


flet.app("python-searchbox", target=main)
