import pytest
import pytest_asyncio

import flet as ft
import flet.testing as ftt


# Create a new flet_app instance for each test method
@pytest_asyncio.fixture(scope="function", autouse=True)
def flet_app(flet_app_function):
    return flet_app_function


@pytest.mark.asyncio(loop_scope="function")
async def test_basic(flet_app: ftt.FletTestApp, request):
    await flet_app.assert_control_screenshot(
        name=request.node.name,
        expand_screenshot=True,
        control=ft.Tabs(
            length=2,
            content=ft.Column(
                controls=[
                    ft.TabBar(
                        tabs=[
                            ft.Tab(label="Tab 1"),
                            ft.Tab(label="Tab 2", icon=ft.Icons.SETTINGS),
                        ]
                    ),
                    ft.TabBarView(
                        expand=True,
                        controls=[
                            ft.Container(
                                content=ft.Text("This is Tab 1"),
                                alignment=ft.Alignment.CENTER,
                            ),
                            ft.Container(
                                content=ft.Text("This is Tab 3"),
                                alignment=ft.Alignment.CENTER,
                            ),
                        ],
                    ),
                ],
            ),
        ),
    )


@pytest.mark.asyncio(loop_scope="function")
async def test_nesting(flet_app: ftt.FletTestApp, request):
    await flet_app.assert_control_screenshot(
        name=request.node.name,
        expand_screenshot=True,
        control=ft.Tabs(
            length=2,
            expand=True,
            selected_index=1,
            content=ft.Column(
                expand=True,
                controls=[
                    ft.TabBar(
                        tabs=[
                            ft.Tab(label=ft.Text("Main Tab 1")),
                            ft.Tab(label=ft.Text("Main Tab 2")),
                        ],
                    ),
                    ft.TabBarView(
                        expand=True,
                        controls=[
                            ft.Text("Main Tab 1 content"),
                            ft.Tabs(
                                length=2,
                                expand=True,
                                content=ft.Column(
                                    expand=True,
                                    controls=[
                                        ft.TabBar(
                                            secondary=True,
                                            tabs=[
                                                ft.Tab(label=ft.Text("SubTab 1")),
                                                ft.Tab(label=ft.Text("SubTab 2")),
                                            ],
                                        ),
                                        ft.TabBarView(
                                            expand=True,
                                            controls=[
                                                ft.Text("Nested Tab 1 content"),
                                                ft.Text("Nested Tab 2 content"),
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


@pytest.mark.asyncio(loop_scope="function")
async def test_disabled_tab(flet_app: ftt.FletTestApp):
    clicked_indexes = []
    flet_app.page.padding = 0
    flet_app.resize_page(300, 300)
    flet_app.page.add(
        tabs := ft.Tabs(
            selected_index=0,
            length=3,
            expand=True,
            content=ft.Column(
                expand=True,
                controls=[
                    ft.TabBar(
                        scrollable=False,
                        on_click=lambda e: clicked_indexes.append(int(e.data)),
                        tabs=[
                            ft.Tab(label="Tab 1"),
                            tab_2 := ft.Tab(label="Tab 2"),
                            ft.Tab(label="Tab 3"),
                        ],
                    ),
                    ft.TabBarView(
                        expand=True,
                        controls=[
                            ft.Text("View 1"),
                            ft.Text("View 2"),
                            ft.Text("View 3"),
                        ],
                    ),
                ],
            ),
        )
    )
    await flet_app.tester.pump_and_settle()

    # click tab2
    await flet_app.tester.tap((await flet_app.tester.find_by_text("Tab 2")).first)
    await flet_app.tester.pump_and_settle()
    assert tabs.selected_index == 1
    assert clicked_indexes == [1]

    # disable tab2
    tabs.selected_index = 0
    tab_2.disabled = True
    flet_app.page.update()
    await flet_app.tester.pump_and_settle()

    # click tab2 (disabled)
    await flet_app.tester.tap((await flet_app.tester.find_by_text("Tab 2")).first)
    await flet_app.tester.pump_and_settle()
    assert tabs.selected_index == 0
    assert clicked_indexes == [1]

    # re-enable tab2
    tab_2.disabled = False
    flet_app.page.update()
    await flet_app.tester.pump_and_settle()

    # click tab2
    await flet_app.tester.tap((await flet_app.tester.find_by_text("Tab 2")).first)
    await flet_app.tester.pump_and_settle()
    assert tabs.selected_index == 1
    assert clicked_indexes == [1, 1]


@pytest.mark.asyncio(loop_scope="function")
async def test_disabled_tabbar(flet_app: ftt.FletTestApp):
    clicked_indexes = []
    flet_app.page.padding = 0
    flet_app.resize_page(300, 300)
    flet_app.page.add(
        tabs := ft.Tabs(
            selected_index=0,
            length=3,
            expand=True,
            content=ft.Column(
                expand=True,
                controls=[
                    tab_bar := ft.TabBar(
                        disabled=True,
                        scrollable=False,
                        on_click=lambda e: clicked_indexes.append(int(e.data)),
                        tabs=[
                            ft.Tab(label="Tab 1"),
                            ft.Tab(label="Tab 2"),
                            ft.Tab(label="Tab 3"),
                        ],
                    ),
                    ft.TabBarView(
                        expand=True,
                        controls=[
                            ft.Text("View 1"),
                            ft.Text("View 2"),
                            ft.Text("View 3"),
                        ],
                    ),
                ],
            ),
        )
    )
    await flet_app.tester.pump_and_settle()

    # click tab2 (disabled TabBar)
    await flet_app.tester.tap((await flet_app.tester.find_by_text("Tab 2")).first)
    await flet_app.tester.pump_and_settle()
    assert tabs.selected_index == 0
    assert clicked_indexes == []

    # re-enable tabbar
    tab_bar.disabled = False
    flet_app.page.update()
    await flet_app.tester.pump_and_settle()

    await flet_app.tester.tap((await flet_app.tester.find_by_text("Tab 2")).first)
    await flet_app.tester.pump_and_settle()
    assert tabs.selected_index == 1
    assert clicked_indexes == [1]


@pytest.mark.asyncio(loop_scope="function")
async def test_disabled_tabs(flet_app: ftt.FletTestApp):
    clicked_indexes = []
    flet_app.page.padding = 0
    flet_app.resize_page(300, 300)
    flet_app.page.add(
        tabs := ft.Tabs(
            disabled=True,
            selected_index=0,
            length=3,
            expand=True,
            content=ft.Column(
                expand=True,
                controls=[
                    ft.TabBar(
                        scrollable=False,
                        on_click=lambda e: clicked_indexes.append(int(e.data)),
                        tabs=[
                            ft.Tab(label="Tab 1"),
                            ft.Tab(label="Tab 2"),
                            ft.Tab(label="Tab 3"),
                        ],
                    ),
                    ft.TabBarView(
                        expand=True,
                        controls=[
                            ft.Text("View 1"),
                            ft.Text("View 2"),
                            ft.Text("View 3"),
                        ],
                    ),
                ],
            ),
        )
    )
    await flet_app.tester.pump_and_settle()

    # click tab2 (disabled Tabs)
    await flet_app.tester.tap((await flet_app.tester.find_by_text("Tab 2")).first)
    await flet_app.tester.pump_and_settle()
    assert tabs.selected_index == 0
    assert clicked_indexes == []

    # re-enable Tabs
    tabs.disabled = False
    flet_app.page.update()
    await flet_app.tester.pump_and_settle()

    # click tab2
    await flet_app.tester.tap((await flet_app.tester.find_by_text("Tab 2")).first)
    await flet_app.tester.pump_and_settle()
    assert tabs.selected_index == 1
    assert clicked_indexes == [1]


@pytest.mark.asyncio(loop_scope="function")
async def test_unbounded_tabbarview_height(flet_app: ftt.FletTestApp, request):
    flet_app.page.theme_mode = ft.ThemeMode.LIGHT
    await flet_app.assert_control_screenshot(
        name=request.node.name,
        control=ft.Column(
            controls=[
                ft.Tabs(
                    length=1,
                    content=ft.Column(
                        controls=[
                            ft.TabBar(
                                tabs=[
                                    ft.Tab(label="Tab 1"),
                                ]
                            ),
                            ft.TabBarView(
                                controls=[
                                    ft.Container(
                                        content=ft.Text("Tab 1 content"),
                                        alignment=ft.Alignment.CENTER,
                                    )
                                ],
                            ),
                        ],
                    ),
                )
            ]
        ),
    )
