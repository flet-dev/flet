import flet
from flet import Message, Nav, Stack, Text, nav


def navs(page):

    nav1 = None

    def menu_item_expanded(e):
        page.controls.insert(
            0, Message(value=f'Menu item "{e.data}" was expanded', dismiss=True)
        )
        page.update()

    def menu_item_collapsed(e):
        page.controls.insert(
            0, Message(value=f'Menu item "{e.data}" was collapsed', dismiss=True)
        )
        page.update()

    def menu_item_changed(e):
        page.controls.insert(
            0, Message(value=f'Menu item was changed to "{nav1.value}"', dismiss=True)
        )
        page.update()

    nav1 = Nav(
        on_collapse=menu_item_collapsed,
        on_expand=menu_item_expanded,
        on_change=menu_item_changed,
        items=[
            nav.Item(
                expanded=False,
                text="Actions",
                items=[
                    nav.Item(
                        expanded=True,
                        text="New",
                        items=[
                            nav.Item(key="email", text="Email message", icon="Mail"),
                            nav.Item(
                                key="calendar",
                                text="Calendar event",
                                icon="Calendar",
                                icon_color="salmon",
                            ),
                        ],
                    ),
                    nav.Item(
                        text="Share",
                        items=[
                            nav.Item(
                                disabled=True,
                                key="share",
                                text="Share to Facebook",
                                icon="Share",
                            ),
                            nav.Item(key="twitter", text="Share to Twitter"),
                        ],
                    ),
                    nav.Item(
                        text="Links",
                        items=[
                            nav.Item(
                                text="Flet website",
                                icon="NavigateExternalInline",
                                url="https://flet.dev",
                                new_window=True,
                            ),
                            nav.Item(
                                text="Google website",
                                icon="NavigateExternalInline",
                                url="https://google.com",
                                new_window=True,
                            ),
                        ],
                    ),
                ],
            ),
            nav.Item(
                expanded=True,
                text="Settings",
                items=[
                    nav.Item(
                        expanded=True,
                        text="New",
                        items=[
                            nav.Item(key="email", text="Email message", icon="Mail"),
                            nav.Item(
                                key="calendar",
                                text="Calendar event",
                                icon="Calendar",
                                icon_color="salmon",
                            ),
                        ],
                    ),
                    nav.Item(
                        text="Share",
                        items=[
                            nav.Item(
                                disabled=True,
                                key="share",
                                text="Share to Facebook",
                                icon="Share",
                            ),
                            nav.Item(key="twitter", text="Share to Twitter"),
                        ],
                    ),
                    nav.Item(
                        text="Links",
                        items=[
                            nav.Item(
                                text="Flet website",
                                icon="NavigateExternalInline",
                                url="https://flet.dev",
                                new_window=True,
                            ),
                            nav.Item(
                                text="Google website",
                                icon="NavigateExternalInline",
                                url="https://google.com",
                                new_window=True,
                            ),
                        ],
                    ),
                ],
            ),
        ],
    )

    nav2 = Nav(
        items=[
            nav.Item(
                items=[
                    nav.Item(
                        expanded=True,
                        text="New",
                        items=[
                            nav.Item(key="email", text="Email message", icon="Mail"),
                            nav.Item(
                                key="calendar", text="Calendar event", icon="Calendar"
                            ),
                            nav.Item(
                                text="More options",
                                items=[
                                    nav.Item(
                                        key="option",
                                        text="Web component",
                                        icon="WebComponents",
                                    )
                                ],
                            ),
                        ],
                    ),
                    nav.Item(
                        expanded=True,
                        text="Share",
                        items=[
                            nav.Item(
                                key="facebook", text="Share on Facebook", icon="Share"
                            ),
                            nav.Item(
                                key="twitter", text="Share to Twitter", icon="Share"
                            ),
                        ],
                    ),
                ]
            )
        ]
    )

    return Stack(
        gap=30,
        controls=[
            Stack(
                controls=[
                    Text(
                        "Nav with groups and Expand, Collapse and Change events",
                        size="xLarge",
                    ),
                    nav1,
                ]
            ),
            Stack(controls=[Text("Nav without groups", size="xLarge"), nav2]),
        ],
    )


def main(page):

    page.title = "Nav control samples"
    page.update()
    page.add(navs(page))


flet.app("python-nav", target=main)
