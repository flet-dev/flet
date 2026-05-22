"""Recursive routes — unbounded URL depth, one View per segment.

A route marked ``recursive=True`` can match itself as its own
descendant. The Router emits one ``_RouteMatch`` per consumed URL
segment, which (in ``manage_views=True`` mode) turns into one View per
segment in the navigation stack — so the back gesture walks one level
at a time.

Sibling-wins-over-recursion: non-recursive children of a recursive
route are tried BEFORE self-recursion at every depth. Here that means
``/folder/<anything>/search`` matches the ``Search`` page (not a
folder named "search"), without needing to declare ``search`` at every
depth manually.

Try this in the browser bar:

* ``/folder`` → folder root
* ``/folder/a`` → 1 level deep
* ``/folder/a/b`` → 2 levels deep
* ``/folder/a/b/c/d/e`` → 5 levels deep (no fixed limit)
* ``/folder/a/b/search`` → search page below ``a/b``
"""

import flet as ft


@ft.component
def Home():
    page = ft.context.page
    return ft.View(
        route="/",
        appbar=ft.AppBar(title=ft.Text("Folder Browser")),
        controls=[
            ft.Text("A toy file browser.", size=18),
            ft.Button("Open /folder", on_click=lambda: page.navigate("/folder")),
        ],
    )


@ft.component
def Folders():
    """Root of the folder tree (``/folder``)."""
    page = ft.context.page
    return ft.View(
        route="/folder",
        appbar=ft.AppBar(title=ft.Text("Folders")),
        controls=[
            ft.Text("Top-level folders:", weight=ft.FontWeight.BOLD),
            *[
                ft.Button(
                    f"Open {name}",
                    on_click=lambda _e, n=name: page.navigate(f"/folder/{n}"),
                )
                for name in ("docs", "projects", "scratch")
            ],
            ft.Button(
                "Search at root",
                on_click=lambda: page.navigate("/folder/search"),
            ),
        ],
    )


@ft.component
def Folder():
    """A folder at any depth. Re-used by the recursive route at every level.

    ``use_route_params()`` returns just the current segment (e.g.
    ``{"name": "b"}`` at depth 2). ``use_view_path()`` returns the
    accumulated URL up to this view, useful for showing the full path
    and for building child URLs.
    """
    page = ft.context.page
    params = ft.use_route_params()
    view_path = ft.use_view_path()
    segments = [s for s in view_path[len("/folder") :].split("/") if s]
    return ft.View(
        route=view_path,
        appbar=ft.AppBar(title=ft.Text(" / ".join(segments) or "Folders")),
        controls=[
            ft.Text(f"Current segment: {params['name']}"),
            ft.Text(f"Full path: {view_path}"),
            ft.Text("Open a sub-folder:", weight=ft.FontWeight.BOLD),
            *[
                ft.Button(
                    f"Into {child}",
                    on_click=lambda _e, c=child: page.navigate(f"{view_path}/{c}"),
                )
                for child in ("alpha", "beta", "gamma")
            ],
            ft.Button(
                "Search here",
                on_click=lambda: page.navigate(f"{view_path}/search"),
            ),
        ],
    )


@ft.component
def Search():
    """Non-recursive child of the recursive Folder route. Wins over
    self-recursion at every depth, so ``/folder/<any-segments>/search``
    always lands here instead of being eaten as another folder named
    "search"."""
    page = ft.context.page
    view_path = ft.use_view_path()
    # Strip trailing "/search" to learn the folder we're searching in.
    folder = view_path[: -len("/search")] or "/folder"
    return ft.View(
        route=view_path,
        appbar=ft.AppBar(title=ft.Text("Search")),
        controls=[
            ft.Text(f"Searching in: {folder}"),
            ft.TextField(label="Query", autofocus=True),
            ft.Button("Back to folder", on_click=lambda: page.navigate(folder)),
        ],
    )


@ft.component
def App():
    return ft.Router(
        [
            ft.Route(
                component=Home,
                children=[
                    ft.Route(
                        path="folder",
                        component=Folders,
                        children=[
                            # Declared ONCE — the `search` sibling check
                            # happens at every recursion depth.
                            ft.Route(
                                path=":name",
                                component=Folder,
                                recursive=True,
                                children=[
                                    ft.Route(path="search", component=Search),
                                ],
                            ),
                        ],
                    ),
                ],
            ),
        ],
        manage_views=True,
    )


if __name__ == "__main__":
    ft.run(lambda page: page.render_views(App))
