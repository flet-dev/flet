---
title: Trolli Tutorial
---

Let's make a clone of Trello in Python with the Flet framework and then deploy it to [fly.io](https://fly.io/)!

![app](https://raw.githubusercontent.com/flet-dev/flet/docs/fix-links/sdk/python/examples/tutorials/trolli/media/app.gif){width="100%"}
/// caption
///

The code for this tutorial can be found [here](https://github.com/flet-dev/examples/tree/main/python/apps/trolli) with self explanatory commits.
Be sure to run `pip install -r requirements.txt` after cloning.

You can see the live demo [here](https://gallery.flet.dev/trolli/).

## Why Flet?

Most developers are undoubtedly familiar with the situation of either having developed a console app that
turns out to have a wider audience than originally intended, or needing to develop an internal tool for
non-developers but which is destined to have a small user base and/or a relatively brief shelf life.
In situations like these it can often feel awkward to reach for an oversized tool such as electron,
a feature rich framework like flutter (irony acknowledged!), or try to quickly get a handle on some other
cross platform framework like .NET MAUI. What we would really like is to be able to throw a UI on our logic
that looks generically decent, has acceptable performance, and ideally, takes less time to write than did
the business logic, and preferably in the same language in which the rest of the logic was written - i.e.
a language with which we are already proficient (currently the only released library is in Python but C#,
Typescript, and Golang libraries are on the roadmap). This is exactly what the Flet platform aims to provide.

Flet takes a different approach to many new UI frameworks that is arguably more intuitive to the majority
of experienced programmers. Diverging from the currently ubiquitous declarative approach and opting instead
for an imperative model.

Having intimated that Flet is designed with simple GUIs in mind, lets nonetheless try to make something a
tad more complicated than, for example, a simple dashboard with some filters, and shoot for something like a
minimal version of Trello - and bestow upon it the totally-independently-arrived-at-name, _Trolli_.
For the purposes of this tutorial I'll assume the reader is familiar with the basic concept and setup of a
Flet project (read [the tutorials](https://flet.dev../tutorials) and the [docs](https://flet.dev/docs) if not), and instead focus more on aspects
that are not part of the existing tutorials.

## Defining Entities and Layout

With the proximate goal of creating the MVP of our clone, let's start by defining the main
entities (`boards`, `board_lists`, `items`), settle on an acceptable design and layout, and implement
a sort of pseudo-repository pattern so that in future development we can move from in-memory data storage
to persistent storage of some kind.

Here, in the `main.py` module we'll add this code and then continue to define the `TrelloApp` class.

```python title="main.py"
import flet as ft

if __name__ == "__main__":
    def main(page: ft.Page):
        page.title = "Flet Trello clone"
        page.padding = 0
        page.bgcolor = colors.BLUE_GREY_200
        app = TrelloApp(page)
        page.add(app)
        page.update()

    ft.run(main)
```

In terms of layout we can consider the app to consist of a header (`appbar`) and below that a
collapsible navigation panel, next to which is the active view consisting of either a board, settings,
members or whatever else we may choose. Something like this...

![mock-up](https://raw.githubusercontent.com/flet-dev/flet/docs/fix-links/sdk/python/examples/tutorials/trolli/media/mock-up.png){width="80%"}
/// caption
///

So the class for the app itself could look something like this...

```python
import flet as ft

class TrelloApp:
    def __init__(self, page: ft.Page):
        self.page = page
        self.appbar_items = [
            ft.PopupMenuItem(text="Login"),
            ft.PopupMenuItem(),  # divider
            ft.PopupMenuItem(text="Settings")
        ]
        self.appbar = ft.runBar(
            leading=ft.Icon(ft.Icons.GRID_GOLDENRATIO_ROUNDED),
            leading_width=100,
            title=ft.Text("Trolli",size=32, text_align="start"),
            center_title=False,
            toolbar_height=75,
            bgcolor=ft.Colors.LIGHT_BLUE_ACCENT_700,
            actions=[
                ft.Container(
                    content=ft.PopupMenuButton(
                        items=self.appbar_items
                    ),
                    margin=ft.margin.only(left=50, right=25)
                )
            ],
        )
        self.page.appbar = self.appbar
        self.page.update()
```

In a new file (`app_layout.py`) we can define a layout for our app in a class which will inherit from
the `Row` control and in which the navigation rail along with a toggle button to collapse and expand it,
and the main content area are laid out. But rather than define the navigation sidebar in that module, we'll
place that in its own `sidebar.py` module.

```python title="app_layout.py"
import flet as ft
from sidebar import Sidebar


class AppLayout(ft.Row):
    def __init__(self, app, page: ft.Page, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.app = app
        self.page = page
        self.toggle_nav_rail_button = ft.IconButton(
            icon=ft.Icons.ARROW_CIRCLE_LEFT,
            icon_color=ft.Colors.BLUE_GREY_400,
            selected=False,
            selected_icon=ft.Icons.ARROW_CIRCLE_RIGHT,
            on_click=self.toggle_nav_rail,
        )
        self.sidebar = Sidebar(self, page)
        self._active_view: Control = ft.Column(
            controls=[ft.Text("Active View")],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )
        self.controls = [self.sidebar, self.toggle_nav_rail_button, self.active_view]

    @property
    def active_view(self):
        return self._active_view

    @active_view.setter
    def active_view(self, view):
        self._active_view = view
        self.update()

    def toggle_nav_rail(self, e):
        self.sidebar.visible = not self.sidebar.visible
        self.toggle_nav_rail_button.selected = not self.toggle_nav_rail_button.selected
        self.page.update()
```

And here is the `Sidebar.py` file.

```python title="sidebar.py"
import flet as ft


class Sidebar(ft.Container):

    def __init__(self, app_layout, store: DataStore):
        self.store: DataStore = store
        self.app_layout = app_layout
        self.nav_rail_visible = True
        self.top_nav_items = [
            ft.NavigationRailDestination(
                label_content=ft.Text("Boards"),
                label="Boards",
                icon=ft.Icons.BOOK_OUTLINED,
                selected_icon=ft.Icons.BOOK_OUTLINED,
            ),
            ft.NavigationRailDestination(
                label_content=ft.Text("Members"),
                label="Members",
                icon=ft.Icons.PERSON,
                selected_icon=ft.Icons.PERSON,
            ),
        ]

        self.top_nav_rail = ft.NavigationRail(
            selected_index=None,
            label_type=ft.NavigationRailLabelType.ALL,
            on_change=self.top_nav_change,
            destinations=self.top_nav_items,
            bgcolor=ft.Colors.BLUE_GREY,
            extended=True,
            height=110,
        )

        self.toggle_nav_rail_button = ft.IconButton(ft.Icons.ARROW_BACK)

        super().__init__(
            content=ft.Column(
                [
                    ft.Row(
                        [
                            ft.Text("Workspace"),
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    ),
                    # divider
                    ft.Container(
                        bgcolor=ft.Colors.BLACK26,
                        border_radius=ft.border_radius.all(30),
                        height=1,
                        alignment=ft.alignment.center_right,
                        width=220,
                    ),
                    self.top_nav_rail,
                    # divider
                    ft.Container(
                        bgcolor=ft.Colors.BLACK26,
                        border_radius=ft.border_radius.all(30),
                        height=1,
                        alignment=ft.alignment.center_right,
                        width=220,
                    ),
                ],
                tight=True,
            ),
            padding=ft.padding.all(15),
            margin=ft.margin.all(0),
            width=250,
            bgcolor=ft.Colors.BLUE_GREY,
            visible=self.nav_rail_visible,
        )

    def top_nav_change(self, e):
        self.top_nav_rail.selected_index = e.control.selected_index
        self.update()
```

If we [run](../getting-started/running-app.md) the main app with
```
flet run
```

we can see the result and get hot reloading when we make any style changes.
For example, try adding `alignment=ft.MainAxisAlignment.CENTER` to the first row in the container like this…
```python
content = ft.Column(
    alignment=ft.MainAxisAlignment.CENTER),
    controls=[
        ft.Row([ft.Text("Workspace")]),
    ],
)
```

If you save the file you should be able to see the change in your app window.

![basic-nav-rail-toggle](https://raw.githubusercontent.com/flet-dev/flet/docs/fix-links/sdk/python/examples/tutorials/trolli/media/basic-nav-rail-toggle.gif){width="100%"}
/// caption
///

Before we move on let's define our basic entities. We'll need a `Board` class, which will keep a list of lists, each of which will be a `BoardList` object (apologies for the unfortunate lexical collisions here - the colloquial use of 'list' derives from the nature of the app, whereas the technical use of 'list' derives from python's particular term for an array-like data structure), and each of which, in turn, will contain a list of `Item` objects. If that's confusing, take some time to look over the source code to clear things up.

For each of the entities, we'll add an application wide unique id with an `id_counter = itertools.count()` statement at the top of each class and a call to `next(Board.id_counter)` at initialization. This way two lists or boards can have the same name but still represent distinct entities.

## Data Access Layer and Customization

Now that we have a basic layout and entities defined, let's add a few customization parameters to the app itself. Lets also take some time to create a basic data access interface. You can see the boiler plate for the interface and the in-memory implementation in the `data_store.py` and `memory_store.py` files respectively. This will make it easier for us to swap in some persistent storage solution in a future tutorial.

Here is the updated main function. We need to instantiate the `InMemoryStore` class within the main method so that each user session (i.e. each new tab using the app), has it's own version of the store. We'll then need to pass that store to each of the components that will need access to it.

We'll also add a new font in an *assets* directory, which is specified in the named argument to the app function.

```python

if __name__ == "__main__":

    def main(page: ft.Page):

        page.title = "Flet Trello clone"
        page.padding = 0
        page.theme = ft.Theme(font_family="Verdana")
        page.theme_mode = ft.ThemeMode.LIGHT
        page.theme.page_transitions.windows = "cupertino"
        page.fonts = {"Pacifico": "/Pacifico-Regular.ttf"}
        page.bgcolor = ft.Colors.BLUE_GREY_200
        page.update()
        app = TrelloApp(page)

    ft.run(main, assets_dir="https://raw.githubusercontent.com/flet-dev/flet/docs/fix-links/sdk/python/examples")

```

## Application Logic

You can run the app now but apart from a nicer font for the name, it still does not have any functionality.

Now it's time to fill out the application logic. Although this app might qualify as non-trivial, we won't
bother to separate the code into distinct application and business layers. The separation of the data access
and the rest of the logic will suffice for this non-architecturally focused tutorial, though further separation
may be a sensible thing to consider.

### Creating Views

First up, we will add views to correspond to the sidebar navigation destinations.

We need a view to display all boards and a view to display a Members pane which, for now, will simply be a
placeholder until a future tutorial. We'll add these views as controls to the `app_layout.py` module.

```python title="app_layout.py"
self.members_view = ft.Text("members view")

self.all_boards_view = ft.Column(
    [
        ft.Row(
            [
                ft.Container(
                    ft.Text(
                        value="Your Boards",
                        theme_style=ft.TextThemeStyle.HEADLINE_MEDIUM,
                    ),
                    expand=True,
                    padding=ft.padding.only(top=15),
                ),
                ft.Container(
                    ft.TextButton(
                        "Add new board",
                        icon=ft.Icons.ADD,
                        on_click=self.app.add_board,
                        style=ft.ButtonStyle(
                            bgcolor={
                                ft.ControlState.DEFAULT: ft.Colors.BLUE_200,
                                ft.ControlState.HOVERED: ft.Colors.BLUE_400,
                            },
                            shape={
                                ft.ControlState.DEFAULT: ft.RoundedRectangleBorder(
                                    radius=3
                                )
                            },
                        ),
                    ),
                    padding=ft.padding.only(right=50, top=15),
                ),
            ]
        ),
        ft.Row(
            [
                ft.TextField(
                    hint_text="Search all boards",
                    autofocus=False,
                    content_padding=ft.padding.only(left=10),
                    width=200,
                    height=40,
                    text_size=12,
                    border_color=ft.Colors.BLACK26,
                    focused_border_color=ft.Colors.BLUE_ACCENT,
                    suffix_icon=ft.Icons.SEARCH,
                )
            ]
        ),
        ft.Row([ft.Text("No Boards to Display")]),
    ],
    expand=True,
)
```

Since we are working in an imperative paradigm and have no explicit state management tool such as redux or the like,
we will need a method to 'rehydrate' the view that shows all the boards so that its current state reflects changes
made in other entities (namely the sideboard).

```python
def hydrate_all_boards_view(self):
    self.all_boards_view.controls[-1] = ft.Row(
        [
            ft.Container(
                content=ft.Row(
                    [
                        ft.Container(
                            content=ft.Text(value=b.name),
                            data=b,
                            expand=True,
                            on_click=self.board_click,
                        ),
                        ft.Container(
                            content=ft.PopupMenuButton(
                                items=[
                                    ft.PopupMenuItem(
                                        content=ft.Text(
                                            value="Delete",
                                            theme_style=ft.TextThemeStyle.LABEL_MEDIUM,
                                            text_align=ft.TextAlign.CENTER,
                                        ),
                                        on_click=self.app.delete_board,
                                        data=b,
                                    ),
                                    ft.PopupMenuItem(),
                                    ft.PopupMenuItem(
                                        content=ft.Text(
                                            value="Archive",
                                            theme_style=ft.TextThemeStyle.LABEL_MEDIUM,
                                            text_align=ft.TextAlign.CENTER,
                                        ),
                                    ),
                                ]
                            ),
                            padding=ft.padding.only(right=-10),
                            border_radius=ft.border_radius.all(3),
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                ),
                border=ft.border.all(1, ft.Colors.BLACK38),
                border_radius=ft.border_radius.all(5),
                bgcolor=ft.Colors.WHITE60,
                padding=ft.padding.all(10),
                width=250,
                data=b,
            )
            for b in self.store.get_boards()
        ],
        wrap=True,
    )
    self.sidebar.sync_board_destinations()
```

### Syncing Navigation Panel

Next up we need a visually distinct section of the navigation panel to display boards we've created.
We'll add a second, `bottom_nav_rail` to the sidebar to represent when a particular board is the active view.
This will necessitate a `sync_board_destinations` method in the sidebar component to be called whenever any change
has been made to the list of current boards.
We'll now have a change handler for each of the top and bottom nav rails.

```python
self.top_nav_rail = ft.NavigationRail(
    selected_index=None,
    label_type=ft.NavigationRailLabelType.ALL,
    on_change=self.top_nav_change,
    destinations=self.top_nav_items,
    bgcolor=ft.Colors.BLUE_GREY,
    extended=True,
    height=110,
)

self.bottom_nav_rail = ft.NavigationRail(
    selected_index=None,
    label_type=ft.NavigationRailLabelType.ALL,
    on_change=self.bottom_nav_change,
    extended=True,
    expand=True,
    bgcolor=ft.Colors.BLUE_GREY,
)

# ...

def sync_board_destinations(self):
    boards = self.store.get_boards()
    self.bottom_nav_rail.destinations = []
    for i in range(len(boards)):
        b = boards[i]
        self.bottom_nav_rail.destinations.append(
            ft.NavigationRailDestination(
                label_content=ft.TextField(
                    value=b.name,
                    hint_text=b.name,
                    text_size=12,
                    read_only=True,
                    on_focus=self.board_name_focus,
                    on_blur=self.board_name_blur,
                    border=ft.InputBorder.NONE,
                    height=50,
                    width=150,
                    text_align=ft.TextAlign.START,
                    data=i,
                ),
                label=b.name,
                selected_icon=ft.Icons.CHEVRON_RIGHT_ROUNDED,
                icon=ft.Icons.CHEVRON_RIGHT_OUTLINED,
            )
        )
```
Now we can add new boards and they appear in our navigation rail.
Unfortunately clicking on the navigation rail doesn't actually navigate to anything.

![add-board-capability](https://raw.githubusercontent.com/flet-dev/flet/docs/fix-links/sdk/python/examples/tutorials/trolli/media/add-board-capability.gif){width="100%"}
/// caption
///

There are several ways we could achieve this such as having every view present in the `app_layout.py`
module and then toggling visibility on/off of the relevant views depending on the navigation rail index.
But that wouldn't help much in a browser context, nor in a mobile context with a back button.
We'll need to consider routing. Flet provides a `TemplateRoute` utility class for url matching.

### Routing

In the `main.py` module let's wire up a handler to the `page.on_route_change` event.

```python title="main.py"
class TrelloApp(AppLayout):
    def __init__(self, page: ft.Page, user=None):
        ...
        self.page.on_route_change = self.route_change
        ...

    def initialize(self):
        self.page.views.append(
            ft.View(
                "/",
                [self.appbar, self],
                padding=ft.padding.all(0),
                bgcolor=ft.Colors.BLUE_GREY_200,
            )
        )
        self.page.update()
        # create an initial board for demonstration if no boards
        if len(self.boards) == 0:
            self.create_new_board("My First Board")
        self.page.go("/")

    def route_change(self, e):
        troute = ft.TemplateRoute(self.page.route)
        if troute.match("/"):
            self.page.go("/boards")
        elif troute.match("/board/:id"):
            if int(troute.id) > len(self.store.get_boards()):
                self.page.go("/")
                return
            self.set_board_view(int(troute.id))
        elif troute.match("/boards"):
            self.set_all_boards_view()
        elif troute.match("/members"):
            self.set_members_view()
        self.page.update()
```

While here, we'll also change our initialization method so that the app starts with a pre-made board
for demonstration purposes. Within that method note that we add a flet `View` object to the page.
The page maintains a list of Views as top level containers for other Controls in order to track navigation history.
We'll need to add the corresponding `set_***_view` methods to the `layout.py` module as well.
Here is the `set_board_view` method for example...

```python title="layout.py"
def set_board_view(self, i):
    self.active_view = self.store.get_boards()[i]
    self.sidebar.bottom_nav_rail.selected_index = i
    self.sidebar.top_nav_rail.selected_index = None
    self.page.update()
```

Now, if we fire up the project in a web browser with the
```
flet run -dw
```
command (_-d_ flag for hot reloading, and _-w_ flag for web) we can add some boards and reach them by
clicking or entering `board/{i}`, where *i* is the zero indexed board, as the url.

![navigation](https://raw.githubusercontent.com/flet-dev/flet/docs/fix-links/sdk/python/examples/tutorials/trolli/media/navigation.gif){width="100%"}
/// caption
///

### Changing Board Names

Next, we should include the ability to change the name of a board. In contrast to the more "*proper*"
title editing logic that was implemented in the `board_list.py` module I'm going to favor what some might
consider a more "*hacky*" approach because I personally dislike overly ceremonial editing flows,
particularly in such a low stakes, fluid sort of application. We'll make use of the `on_focus` and `on_blur`
events in the bottom navigation rail destinations in the `sidebar.py` module. Here are the handlers we'll add.

```python title="sidebar.py"
def board_name_focus(self, e):
    e.control.read_only = False
    e.control.border = ft.InputBorder.OUTLINE
    self.page.update()


def board_name_blur(self, e):
    self.store.update_board(
        self.store.get_boards()[e.control.data], {"name": e.control.value}
    )
    self.app_layout.hydrate_all_boards_view()
    e.control.read_only = True
    e.control.border = ft.InputBorder.NONE
    self.page.update()
```

This makes for a very intuitive way to change a board name without unnecessary dialogs or extraneous button presses.

Let's also quickly stub a login procedure which will be more fully realized in a future instalment.
For now, we'll simply add the following login method and wire it up to the login `PopupMenuItem` on_click event.

```python
def login(self, e):
    def close_dlg(e):
        if user_name.value == "" or password.value == "":
            user_name.error_text = "Please provide username"
            password.error_text = "Please provide password"
            self.page.update()
            return
        else:
            user = User(user_name.value, password.value)
            if user not in self.store.get_users():
                self.store.add_user(user)
            self.user = user_name.value
            self.page.client_storage.set("current_user", user_name.value)

        self.page.close(dialog)
        self.appbar_items[0] = ft.PopupMenuItem(
            text=f"{self.page.client_storage.get('current_user')}'s Profile"
        )
        self.page.update()

    user_name = ft.TextField(label="User name")
    password = ft.TextField(label="Password", password=True)
    dialog = ft.AlertDialog(
        title=ft.Text("Please enter your login credentials"),
        content=ft.Column(
            [
                user_name,
                password,
                ft.ElevatedButton(text="Login", on_click=close_dlg),
            ],
            tight=True,
        ),
        on_dismiss=lambda e: print("Modal dialog dismissed!"),
    )
    self.page.open(dialog)
```

## Drag and Drop

Next, we'll add crucial drag and drop functionality to lists themselves and items within lists.

We'll start with the simpler case of re-ordering lists within boards. In order to give some visual
indication of the target to which we're dragging a list, we'll modify the `board_list` containers `border` property,
darkening the color on the `list_will_drag_accept` event handler, and returning it to a lighter color in
the `list_drag_accept` and `list_drag_leave` handlers.

Next, we'll wrap the `board_list` view in a `DragTarget` object, all of which we will then wrap in a
`Draggable` object. Both of these will be passed a `group` parameter of "lists". This will be important since later
we will want to add the ability to drag and drop individual items between different lists so for that function
we'll specify a different group. If anything is unclear in the previous sentence. , have a look at the
relevant [documentation][flet.Draggable].

Now the composition of the view should look something like this.

```python
self.view = ft.DragTarget(
    group="items",
    content=ft.Draggable(
        group="lists",
        content=ft.DragTarget(
            group="lists",
            content=self.inner_list,
            data=self,
            on_accept=self.list_drag_accept,
            on_will_accept=self.list_will_drag_accept,
            on_leave=self.list_drag_leave,
        ),
    ),
    data=self,
    on_accept=self.item_drag_accept,
    on_will_accept=self.item_will_drag_accept,
    on_leave=self.item_drag_leave,
)
self.inner_list = ft.Container(
    content=ft.Column(
        [
            self.header,
            self.new_item_field,
            ft.TextButton(
                content=ft.Row(
                    [
                        ft.Icon(ft.Icons.ADD),
                        ft.Text("add card", color=ft.Colors.BLACK38),
                    ],
                    tight=True,
                ),
                on_click=self.add_item_handler,
            ),
            self.items,
            self.end_indicator,
        ],
        spacing=4,
        tight=True,
        data=self.title,
    ),
    width=250,
    border=ft.border.all(2, ft.Colors.BLACK12),
    border_radius=ft.border_radius.all(5),
    bgcolor=self.color if (self.color != "") else ft.Colors.BACKGROUND,
    padding=ft.padding.only(bottom=10, right=10, left=10, top=5),
)
```

with the event handlers defined thus.

```python
def list_drag_accept(self, e):
    src = self.page.get_control(e.src_id)
    l = self.board.content.controls
    to_index = l.index(e.control.data)
    from_index = l.index(src.content.data)
    l[to_index], l[from_index] = l[from_index], l[to_index]
    self.inner_list.border = ft.border.all(2, ft.Colors.BLACK12)
    self.page.update()

def list_will_drag_accept(self, e):
    if e.data == "true":
        self.inner_list.border = ft.border.all(2, ft.Colors.BLACK)
    self.update()

def list_drag_leave(self, e):
    self.inner_list.border = ft.border.all(2, ft.Colors.BLACK12)
    self.update()
```


Note the manipulation of the opacity field acting as a visual indication that the dragged item will be accepted
on the target.

![drag-drop-list](https://raw.githubusercontent.com/flet-dev/flet/docs/fix-links/sdk/python/examples/tutorials/trolli/media/drag-drop-list.gif){width="100%"}
/// caption
///

Now for the slightly more complex case of dragging items within a list (including potentially to another list on
the same board). Now that we want a `board_list` to not only be a drag target for other lists, but also for items
being dragged to it from a different list, we'll need to add another `DragTarget` wrapper to the list, but this time
we'll assign the group name "items" so that it only responds to the dragging of items.

Since we'll have the ability to drag the list to a location above or below an existing list we'll employ a
different visual indicator strategy to what we've implemented for list dragging.
We'll make sure that every time a new `item` is added to the `board_list` it will be interspersed with a visual
indicator (implemented as a simple Container object).

The `item.py` module will now need its view wrapped by `Draggable` and `DragTarget` and assigned to the "items"
group as seen below together with event handlers.

```python
self.view = ft.Draggable(
    group="items",
    content=ft.DragTarget(
        group="items",
        content=self.card_item,
        on_accept=self.drag_accept,
        on_leave=self.drag_leave,
        on_will_accept=self.drag_will_accept,
    ),
    data=self,
)
self.card_item = ft.Card(
    content=ft.Row(
        [
            ft.Container(
                content=ft.Checkbox(label=f"{self.item_text}", width=200),
                border_radius=ft.border_radius.all(5),
            )
        ],
        width=200,
        wrap=True,
    ),
    elevation=1,
    data=self.list,
)


def drag_accept(self, e):
    src = self.page.get_control(e.src_id)

    # skip if item is dropped on itself
    if src.content.content == e.control.content:
        self.card_item.elevation = 1
        self.list.set_indicator_opacity(self, 0.0)
        e.control.update()
        return

    # item dropped within same list but not on self
    if src.data.list == self.list:
        self.list.add_item(chosen_control=src.data, swap_control=self)
        self.card_item.elevation = 1
        e.control.update()
        return

    # item added to different list
    self.list.add_item(src.data.item_text, swap_control=self)
    # remove from the list to which draggable belongs
    src.data.list.remove_item(src.data)
    self.list.set_indicator_opacity(self, 0.0)
    self.card_item.elevation = 1
    self.page.update()


def drag_will_accept(self, e):
    if e.data == "true":
        self.list.set_indicator_opacity(self, 1.0)
    self.card_item.elevation = 20 if e.data == "true" else 1
    self.page.update()


def drag_leave(self, e):
    self.list.set_indicator_opacity(self, 0.0)
    self.card_item.elevation = 1
    self.page.update()
```

We need somewhere to house the logic that will decide on how and when to modify the items owned by a `board_list`
object based on a drag event. There are surely design pattern militants out there that will find several dozen
unholy violations of the sacred order of clean software design in the following approach but for this
size of application, simply overloading the `add_item` method to take optional keyword args when called from
different places, as seen below, seems to me like a perfectly workable approach.

```python
def add_item(
    self,
    item: str | None = None,
    chosen_control: ft.Draggable | None = None,
    swap_control: ft.Draggable | None = None,
):

    controls_list = [x.controls[1] for x in self.items.controls]
    to_index = (
        controls_list.index(swap_control) if swap_control in controls_list else None
    )
    from_index = (
        controls_list.index(chosen_control) if chosen_control in controls_list else None
    )
    control_to_add = ft.Column(
        [
            ft.Container(
                bgcolor=ft.Colors.BLACK26,
                border_radius=ft.border_radius.all(30),
                height=3,
                alignment=ft.alignment.center_right,
                width=200,
                opacity=0.0,
            )
        ]
    )

    # rearrange (i.e. drag drop from same list)
    if (from_index is not None) and (to_index is not None):
        self.items.controls.insert(to_index, self.items.controls.pop(from_index))
        self.set_indicator_opacity(swap_control, 0.0)

    # insert (drag from other list to middle of this list)
    elif to_index is not None:
        new_item = Item(self, self.store, item)
        control_to_add.controls.append(new_item)
        self.items.controls.insert(to_index, control_to_add)

    # add new (drag from other list to end of this list, or use add item button)
    else:
        new_item = (
            Item(self, self.store, item)
            if item
            else Item(self, self.store, self.new_item_field.value)
        )
        control_to_add.controls.append(new_item)
        self.items.controls.append(control_to_add)
        self.store.add_item(self.board_list_id, new_item)
        self.new_item_field.value = ""

    self.page.update()
```

And with these changes, we should be able to drag lists around within the board and also drag items between different lists.

![drag-lists-and-items](https://raw.githubusercontent.com/flet-dev/flet/docs/fix-links/sdk/python/examples/tutorials/trolli/media/drag-lists-and-items.gif){width="100%"}
/// caption
///

## Handling Page Resizing

The only final bit of logic we need to add is some page resizing to ensure that if more lists exist than can be displayed, there is a scroll bar to reach them. This logic will also have to take into account the state of the sidebar - extended or not.

We'll add a resize method to `board.py` module:
```python title="board.py"
def resize(self, nav_rail_extended, width, height):
    self.board_lists.width = (width - 310) if nav_rail_extended else (width - 50)
    self.height = height
    self.update()
```

and wire up this `page.on_resize` handler in the `app_layout.py` module:
```python title="app_layout.py"
def page_resize(self, e=None):
    if type(self.active_view) is Board:
        self.active_view.resize(self.sidebar.visible, self.page.width, self.page.height)
    self.page.update()
```

## Deploying
TBA

## Summary

Hopefully this walkthrough gives the reader some idea of how actual usable apps can be developed and
deployed using the Flet framework. The flexibility, speed of development and developer experience make
it a really compelling tool to reach for in many different use cases and there is an ever growing number
of devs doing just that.
