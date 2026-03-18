"""Dynamic segments — :param paths with use_route_params()."""

import flet as ft


@ft.component
def UserProfile():
    params = ft.use_route_params()
    return ft.Column(
        [
            ft.Text(f"User: {params['userId']}", size=24),
            ft.Text(f"All params: {params}"),
            ft.Button(
                "View post #10",
                on_click=lambda: ft.context.page.navigate(
                    f"/users/{params['userId']}/posts/10"
                ),
            ),
            ft.Button(
                "Back to users",
                on_click=lambda: ft.context.page.navigate("/"),
            ),
        ]
    )


@ft.component
def UserPost():
    params = ft.use_route_params()
    return ft.Column(
        [
            ft.Text(f"User: {params['userId']}, Post: {params['postId']}", size=24),
            ft.Text(f"All params: {params}"),
            ft.Button(
                "Back to user",
                on_click=lambda: ft.context.page.navigate(f"/users/{params['userId']}"),
            ),
        ]
    )


@ft.component
def UserList():
    return ft.Column(
        [
            ft.Text("Users", size=24),
            ft.Button(
                "User alice",
                on_click=lambda: ft.context.page.navigate("/users/alice"),
            ),
            ft.Button(
                "User bob",
                on_click=lambda: ft.context.page.navigate("/users/bob"),
            ),
        ]
    )


@ft.component
def App():
    return ft.Router(
        [
            ft.Route(index=True, component=UserList),
            ft.Route(
                path="users/:userId",
                children=[
                    ft.Route(index=True, component=UserProfile),
                    ft.Route(path="posts/:postId", component=UserPost),
                ],
            ),
        ]
    )


ft.run(lambda page: page.render(App))
