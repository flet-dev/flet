# From Imperative to Declarative in Flet: Migrating a Simple CRUD “User Manager”

**What we’re building:** this example is a tiny **CRUD “User Manager.”** You can **add** a user via a small form, **edit** a user inline (with Save/Cancel), **delete** a user, and the app always **shows the current list** of users. Both implementations below deliver the same behavior—the only difference is **how** the UI is updated and managed.

[Screenshot]

---

## Table of contents

1. [Example 1 — Imperative](#example-1--imperative)
2. [Example 2 — Declarative](#example-2--declarative)
3. [Mindset shift: UI = f(state)](#mindset-shift-ui--fstate)
4. [Rewrite recipes (imperative → declarative)](#rewrite-recipes-imperative--declarative)
5. [Local vs. global state](#local-vs-global-state)
6. [Identity & lists](#identity--lists)
7. [Practical tips & gotchas](#practical-tips--gotchas)
8. [Migration checklist](#migration-checklist)
9. [Closing](#closing)

---

## Example 1 — Imperative

In the imperative version, you think **UI-first**: decide exactly how the screen should look, and how it should change on each button click. Event handlers directly toggle control properties (like `visible`, `value`), insert/remove controls, and then call `page.update()` to push those visual changes. **Edit** hides the read-only label and action buttons, shows inputs and **Save/Cancel**; **Save** copies text field values back into the label and restores the original view; **Cancel** just restores the original view; **Delete** removes the whole row from the page. In short, behavior is implemented by **mutating controls** and **manually triggering re-renders**, not by evolving a separate state model.

```python
import flet as ft


class Item(ft.Row):
    def __init__(self, first_name, last_name):
        super().__init__()

        self.first_name_field = ft.TextField(first_name)
        self.last_name_field = ft.TextField(last_name)
        self.text = ft.Text(f"{first_name} {last_name}")
        self.edit_text = ft.Row(
            [
                self.first_name_field,
                self.last_name_field,
            ],
            visible=False,
        )
        self.edit_button = ft.Button("Edit", on_click=self.edit_item)
        self.delete_button = ft.Button("Delete", on_click=self.delete_item)
        self.save_button = ft.Button("Save", on_click=self.save_item, visible=False)
        self.cancel_button = ft.Button(
            "Cancel", on_click=self.cancel_item, visible=False
        )
        self.controls = [
            self.text,
            self.edit_text,
            self.edit_button,
            self.delete_button,
            self.save_button,
            self.cancel_button,
        ]

    def delete_item(self, e):
        self.page.controls.remove(self)
        self.page.update()

    def edit_item(self, e):
        print("edit_item")
        self.text.visible = False
        self.edit_button.visible = False
        self.delete_button.visible = False
        self.save_button.visible = True
        self.cancel_button.visible = True
        self.edit_text.visible = True
        self.page.update()

    def save_item(self, e):
        self.text.value = f"{self.first_name_field.value} {self.last_name_field.value}"
        self.text.visible = True
        self.edit_button.visible = True
        self.delete_button.visible = True
        self.save_button.visible = False
        self.cancel_button.visible = False
        self.edit_text.visible = False
        self.page.update()

    def cancel_item(self, e):
        self.text.visible = True
        self.edit_button.visible = True
        self.delete_button.visible = True
        self.save_button.visible = False
        self.cancel_button.visible = False
        self.edit_text.visible = False
        self.page.update()


def main(page: ft.Page):
    page.title = "CRUD Imperative Example"

    def add_item(e):
        item = Item(first_name.value, last_name=last_name.value)
        page.add(item)
        first_name.value = ""
        last_name.value = ""
        page.update()

    first_name = ft.TextField(label="First Name", width=200)
    last_name = ft.TextField(label="Last Name", width=200)

    page.add(
        ft.Row(
            [
                first_name,
                last_name,
                ft.Button("Add", on_click=add_item),
            ]
        )
    )


ft.run(main)
```
---

## Example 2 — Declarative

In the declarative version, you think **model-first**: the model is a set of **classes**, and the **data their objects hold is the single source of truth**. In our CRUD app, the model consists of `User` (persisted fields `first_name`, `last_name`) and a top-level `App` that owns `users: list[User]` plus actions like `add_user(first, last)` and `delete_user(user)`. Both classes are marked `@ft.observable`, so assigning to their attributes (e.g., `user.update(...)`, `app.users.remove(user)`) triggers re-rendering — no `page.update()`.

The UI is written as **components marked with `@ft.component`** that **return a view of the current state**: each row (`UserView`) keeps a bit of **local, transient state** (`is_editing`) and temporary input buffers to choose between read-only and edit representations, while the **durable data** lives on the model objects. Handlers **update state only**—not controls—and the framework updates whatever depends on that state. In short: **UI = f(state)**, with `User` and `App` providing the authoritative data.


```python
from dataclasses import dataclass, field

import flet as ft


@ft.observable
@dataclass
class User:
    first_name: str
    last_name: str

    def update(self, first_name: str, last_name: str):
        self.first_name = first_name
        self.last_name = last_name


@ft.observable
@dataclass
class App:
    users: list[User] = field(default_factory=list)

    def add_user(self, first_name: str, last_name: str):
        if first_name.strip() or last_name.strip():
            self.users.append(User(first_name, last_name))

    def delete_user(self, user: User):
        self.users.remove(user)


@ft.component
def UserView(user: User, delete_user) -> ft.Control:
    # Local (transient) editing state—NOT in User
    is_editing, set_is_editing = ft.use_state(False)
    new_first_name, set_new_first_name = ft.use_state(user.first_name)
    new_last_name, set_new_last_name = ft.use_state(user.last_name)

    def start_edit():
        set_new_first_name(user.first_name)
        set_new_last_name(user.last_name)
        set_is_editing(True)

    def save():
        user.update(new_first_name, new_last_name)
        set_is_editing(False)

    def cancel():
        set_is_editing(False)

    if not is_editing:
        return ft.Row(
            [
                ft.Text(f"{user.first_name} {user.last_name}"),
                ft.Button("Edit", on_click=start_edit),
                ft.Button("Delete", on_click=lambda: delete_user(user)),
            ]
        )

    return ft.Row(
        [
            ft.TextField(
                label="First Name",
                value=new_first_name,
                on_change=lambda e: set_new_first_name(e.control.value),
                width=180,
            ),
            ft.TextField(
                label="Last Name",
                value=new_last_name,
                on_change=lambda e: set_new_last_name(e.control.value),
                width=180,
            ),
            ft.Button("Save", on_click=save),
            ft.Button("Cancel", on_click=cancel),
        ]
    )


@ft.component
def AddUserForm(add_user) -> ft.Control:
    # Uses local buffers; calls parent action on Add
    new_first_name, set_new_first_name = ft.use_state("")
    new_last_name, set_new_last_name = ft.use_state("")

    def add_user_and_clear():
        add_user(new_first_name, new_last_name)
        set_new_first_name("")
        set_new_last_name("")

    return ft.Row(
        controls=[
            ft.TextField(
                label="First Name",
                width=200,
                value=new_first_name,
                on_change=lambda e: set_new_first_name(e.control.value),
            ),
            ft.TextField(
                label="Last Name",
                width=200,
                value=new_last_name,
                on_change=lambda e: set_new_last_name(e.control.value),
            ),
            ft.Button("Add", on_click=add_user_and_clear),
        ]
    )


@ft.component
def AppView() -> list[ft.Control]:
    app, _ = ft.use_state(
        App(
            users=[
                User("John", "Doe"),
                User("Jane", "Doe"),
                User("Foo", "Bar"),
            ]
        )
    )

    return [
        AddUserForm(app.add_user),
        *[UserView(user, app.delete_user) for user in app.users],
    ]


ft.run(lambda page: page.render(AppView))
```

---

## Mindset shift: UI = f(state)

The core idea is **determinism**: given the same state, your component should return the same UI. Think in two phases:

1. **Handle event → update state**
   Event handlers change *data only* (e.g., `set_is_editing(True)`, `user.update(...)`).
   They don’t hide/show controls or call `page.update()`.

2. **Render → derive UI from state**
   The component *returns* controls based on the current state snapshot.
   Because models are `@ft.observable` and locals come from `ft.use_state`, Flet re-runs the component when state changes and re-renders the right subtree.

## Imperative vs. Declarative (zoomed in)

### Example — Toggle “Edit mode”

* **Imperative:**
  “On **Edit** click, hide the label, show the inputs and Save/Cancel, copy values, then call `page.update()`.”

  ```python
  def on_edit(e):
      row.label.visible = False
      row.inputs.visible = True
      row.save.visible = True
      row.cancel.visible = True
      row.inputs.first.value = row.label_first.value
      row.inputs.last.value  = row.label_last.value
      e.page.update()
  ```

* **Declarative:**
  “On **Edit** click, set `is_editing = True`; the render function returns either the read-only row or the edit form based on that flag.”

  ```python
  import flet as ft

  is_editing, set_is_editing = ft.use_state(False)

  def on_edit(_):
      set_is_editing(True)

  def on_save(_):
      # e.g., user.update(first, last)
      set_is_editing(False)

  def RowView():
      return (
          ft.Row([
              ft.Text(f"{user.first_name} {user.last_name}"),
              ft.Button("Edit", on_click=on_edit),
          ])
          if not is_editing
          else ft.Row([
              ft.TextField(label="First Name"),
              ft.TextField(label="Last Name"),
              ft.Button("Save", on_click=on_save),
          ])
      )
  ```

---

## Declarative Building Blocks: Observables, Components, Hooks

Below are the key pieces of the Flet framework that make the declarative approach work:

### 1) Observables — your source of truth

`@ft.observable` marks a dataclass as **reactive**. When you assign to its fields (`user.first_name = "Ada"` or `app.users.append(user)`), Flet re-renders any components that read those fields—no `page.update()` calls. Use observables for **persisted/domain data** (things you actually save).

```python
from dataclasses import dataclass, field
import flet as ft

@ft.observable
@dataclass
class User:
    first_name: str
    last_name: str

@ft.observable
@dataclass
class AppState:
    users: list[User] = field(default_factory=list)
```

### 2) Components — functions that return UI

`@ft.component` turns a function into a **rendering unit**. It takes props (regular args), may use hooks, and **returns controls** that describe the UI for the current state. Components do **not** imperatively mutate the page tree; they just return what the UI *should* look like now.

```python
import flet as ft

@ft.component
def UserRow(user: User, on_delete) -> ft.Control:
    # returns a row for the current snapshot of `user`
    return ft.Row([
        ft.Text(f"{user.first_name} {user.last_name}"),
        ft.Button("Delete", on_click=lambda _: on_delete(user)),
    ])
```

### 3) Hooks — local, short-lived UI state

Hooks like `ft.use_state(...)` store **transient, per-component** values (e.g., `is_editing`, current input text). Calling the setter re-runs the component and reconciles the returned UI.

```python
import flet as ft

@ft.component
def EditableUserRow(user: User) -> ft.Control:
    is_editing, set_is_editing = ft.use_state(False)
    buf_first, set_buf_first = ft.use_state(user.first_name)
    buf_last,  set_buf_last  = ft.use_state(user.last_name)

    def save(_):
        user.first_name = buf_first
        user.last_name  = buf_last
        set_is_editing(False)

    return (
        ft.Row([
            ft.Text(f"{user.first_name} {user.last_name}"),
            ft.Button("Edit", on_click=lambda _: set_is_editing(True)),
        ]) if not is_editing else
        ft.Row([
            ft.TextField(value=buf_first, on_change=lambda e: set_buf_first(e.control.value)),
            ft.TextField(value=buf_last,  on_change=lambda e: set_buf_last(e.control.value)),
            ft.Button("Save", on_click=save),
            ft.Button("Cancel", on_click=lambda _: set_is_editing(False)),
        ])
    )
```

### How they fit together (event → state → render)

1. **Event handler runs** (e.g., click “Save”).
2. **Update state only** (observable fields or a hook setter).
3. **Framework re-renders** components that depend on that state.
4. **Component returns UI** for the new snapshot (no visibility toggles or `page.update()`).

### Rules of thumb

* Persisted/domain data → **observables**.
* Per-view, short-lived bits (toggles, input text) → **hooks**.
* **Components** never mutate controls; they *return* controls.
* Handlers **mutate state, not UI** — let Flet do the re-rendering.

---

## Rewrite recipes (imperative → declarative)

### 1) Visibility toggles → Conditional rendering

```python
# Imperative
self.text.visible = False
self.save_button.visible = True
self.page.update()

# Declarative
return (
    ft.Row([...read-only...])
    if not is_editing
    else ft.Row([...edit form...])
)
```

### 2) Direct control mutation → Model mutation

```python
# Imperative
self.text.value = f"{first} {last}"

# Declarative
user.update(new_first_name, new_last_name)
```

### 3) `page.update()` everywhere → Nowhere

* Imperative handlers end with `page.update()`.
* Declarative code updates **observable fields** or **`use_state` values** and lets Flet re-render.

### 4) Handlers manipulate **state**, not the view

```python
# Declarative example
set_is_editing(True)
set_new_first_name(user.first_name)
```

### 5) Extract UI into components

* `UserView` = one row (read-only/editing)
* `AddUserForm` = small, reusable add form

---

## Local vs. global state

* **Persisted data** (e.g., users) → `@ft.observable` dataclasses.
* **Transient UI state** (e.g., edit buffers) → local `use_state` in `UserView`.
  If multiple components must share the same editing buffers, lift them into the parent (`App`) instead.

---

## Identity & lists

When rendering lists, inserts/removals can shift positions. If you rely heavily on local `use_state` inside each row, consider giving each item a **stable identity** (e.g., `id`) so rows don’t accidentally reuse state after reordering. Keep list mutations simple (append/remove), or centralize editing state in the parent.

---

## Practical tips & gotchas

* **Event args:** prefer `lambda e:` or ignore explicitly with `lambda _:` for button handlers.
* **UX polish:**

  * `TextField(autofocus=True)` when entering edit mode
  * `on_submit=lambda e: save()` for Enter-to-save
  * Disable Save unless values actually changed
* **Composition:** pass **actions** (functions) like `add_user`, `delete_user` down to components—don’t pass controls.

---

## Migration checklist

* [ ] Move persistent data into `@ft.observable` dataclasses.
* [ ] Replace control mutation with **state mutation**.
* [ ] Replace `visible` toggles with **conditional return** of subtrees.
* [ ] Remove `page.update()` calls.
* [ ] Extract small components with `@ft.component`.
* [ ] Pass actions downward; keep components stateless where possible.
* [ ] Consider stable identity for list items if reordering.

---

## Closing

The declarative style makes your UI a straightforward function of your data. As your screen grows, you’ll add **state** and **components**, not scattered mutations. The result: simpler reasoning, easier testing, and faster iteration—without chasing `visible` flags or manual updates.
