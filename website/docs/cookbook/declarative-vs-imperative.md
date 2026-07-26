---
title: "Declarative vs Imperative"
examples: "cookbook/declarative_vs_imperative_crud_app"
---

import {CodeExample} from '@site/src/components/crocodocs';

By default, a Flet app follows an **imperative** approach: you directly change control properties like `visible` and `value`, add or remove controls, and Flet pushes the change to the page for you. That's fine for small apps, but it doesn't scale well — as a screen grows, the logic for keeping related controls in sync gets duplicated across event handlers, and it's easy to miss one and end up with an inconsistent UI.

Flet also supports a **declarative** approach: the state of your app is the single source of truth, and the UI is derived from it. You don't change controls or their properties directly; instead, only change application state, by assigning to [an observable field](#observables) or calling [a hook's setter](#hooks). Flet [components](#components) detect the change and re-render UI that depends on it.

This article shows the same simple "User Manager" app built both ways — imperative and declarative — so you can compare the two approaches directly. It's a classic CRUD app: list users, add a new user, edit inline, and delete:

<figure className="doc-screenshot-figure"><img alt="view" className="doc-screenshot" src="/docs/assets/cookbook/declarative-vs-imperative-crud-app/crud1.png" style={{width: "45%"}} /></figure>

<figure className="doc-screenshot-figure"><img alt="inline edit" className="doc-screenshot" src="/docs/assets/cookbook/declarative-vs-imperative-crud-app/crud2.png" style={{width: "55%"}} /></figure>

## Imperative

In this example, clicking a button changes control properties directly (`visible`, `value`) and adds or removes controls from the page's control list — that's what makes it imperative. Flet pushes each change to the page automatically.

* **Add** creates a new `Item` row from the `first_name`/`last_name` `TextField` values, appends it to `page.controls`, and clears both fields.
* **Edit** resets the `TextField`s to the row's `first_name`/`last_name`, sets `visible=False` on `text`, `edit_button`, and `delete_button`, and `visible=True` on `edit_text`, `save_button`, and `cancel_button` — switching the row into edit mode.
* **Save** copies the two `TextField` values into `first_name`/`last_name` and `text.value`, then sets `visible=True` on `text`, `edit_button`, and `delete_button`, and `visible=False` on `edit_text`, `save_button`, and `cancel_button` — returning to read-only mode with the new values.
* **Cancel** sets `visible=True` on `text`, `edit_button`, and `delete_button`, and `visible=False` on `edit_text`, `save_button`, and `cancel_button` — returning to read-only mode without saving.
* **Delete** removes the row's `Item` instance from `page.controls`.

<CodeExample path={frontMatter.examples + '/imperative/main.py'} language="python" displayTitle={false} />

## Declarative

In [this example](#example), clicking a button doesn't change controls directly. Instead, it changes application state that exists separately from UI. As soon as the state changes, Flet detects it and re-renders UI.

To understand how Flet stores state and detects when it changes, you need to understand the concepts that lay in the declarative approach: [Observables](#observables), [Components](#components), and [Hooks](#hooks).

### Observables

Observables (`@ft.observable`) are classes whose instances hold your application's state. In this "User Manager" app, each `User` instance holds one person's name, and a single `App` instance holds the list of users. The `@ft.observable` decorator makes their attribute and collection changes trackable: assigning to a field like `user.first_name`, or changing a list field like `app.users.append(...)`, notifies the components subscribed to it, triggering them to re-render.

```python
@ft.observable
@dataclass
class User:
    first_name: str
    last_name: str

    def update(self, first_name: str, last_name: str):
        self.first_name = first_name  # notifies subscribed components
        self.last_name = last_name
```

### Components

Components (`@ft.component`) are functions that take arguments — like `user` and `delete_user` in `UserView(user, delete_user)` — and return the controls describing the UI for its current state. Only the arguments that are themselves `@ft.observable` instances, like `user`, get subscribed to; a plain callback like `delete_user` is just passed through.

```python
@ft.component
def UserView(user: User, delete_user) -> ft.Control:
    return ft.Row([
        ft.Text(f"{user.first_name} {user.last_name}"),
        ft.Button("Delete", on_click=lambda: delete_user(user)),
    ])
```

Unlike the imperative example, a component doesn't change an existing control's properties or modify `page.controls`. It just returns a new set of controls each render, and Flet reconciles that against what's already on screen, patching only what changed.

A component renders once when it's first created, and again whenever an observable it's subscribed to — received as an argument, or held via a hook — is changed, or a hook's setter replaces its value; only that component re-renders, not the whole app. On each render, it subscribes again to every such observable. The subscription is to the whole object, not individual fields — which is why, in the example below, editing one user only re-renders its `UserView` (it is subscribed to that one `user`), while adding or deleting re-renders all of `AppView` (it is subscribed to `app`, and a user list change is a change to `app`).

### Hooks

Hooks (`ft.use_state`) hold local state scoped to one component instance — like a row's "editing" flag. A plain local variable won't do the job: it resets on every render, and changing it doesn't trigger one. Calling a hook's setter re-renders that component, using the same mechanism as observables — just scoped to one component.

```python
# Broken: a plain local resets on every render, and changing it doesn't trigger one
@ft.component
def UserView(user: User, delete_user) -> ft.Control:
    is_editing = False
    if not is_editing:
        return ft.Row([
            ft.Text(f"{user.first_name} {user.last_name}"),
            ft.Button("Edit", on_click=lambda: (is_editing := True)),  # no re-render
        ])
    ...

# Correct: hook state survives across renders and triggers one when set
@ft.component
def UserView(user: User, delete_user) -> ft.Control:
    is_editing, set_is_editing = ft.use_state(False)
    if not is_editing:
        return ft.Row([
            ft.Text(f"{user.first_name} {user.last_name}"),
            ft.Button("Edit", on_click=lambda: set_is_editing(True)),
        ])
    ...
```

### Example

The state lives in two `@ft.observable` classes, `User` (`first_name`, `last_name`) and `App` (`users: list[User]`, with `add_user`/`delete_user`). `@ft.component` functions read that state and return controls — `UserView` renders one row, read-only or editing; `AddUserForm` renders the add form. Each row's "editing" flag and input buffers are local `ft.use_state` hooks: they're view-only and don't belong on `User`.

* **Add** (in `AddUserForm`) calls `add_user_and_clear()`, which calls `app.add_user(...)` — appending a `User` to `app.users` — then clears its own local `use_state` buffers. `AppView` holds `app` via `use_state`, so this re-renders `AppView`, regenerating the whole user list.
* **Edit** calls `start_edit()`, which resets the local buffer hooks to the user's current values and calls `set_is_editing(True)` — re-rendering just that row's `UserView` into its editing form.
* **Save** calls `save()`, which calls `user.update(...)` and `set_is_editing(False)`. `user` was passed directly into this `UserView`, so only this one row re-renders with the new values.
* **Cancel** calls `cancel()`, which calls `set_is_editing(False)` — re-rendering that row back to read-only without touching `user`.
* **Delete** calls `app.delete_user(user)`, removing it from `app.users` — like Add, this re-renders all of `AppView`, not just the one row.

<figure className="doc-screenshot-figure"><img alt="declarative data flow diagram" className="doc-screenshot" src="/docs/assets/cookbook/declarative-vs-imperative-crud-app/crud-declarative.drawio.png" style={{width: "55%"}} /></figure>

<CodeExample path={frontMatter.examples + '/declarative/main.py'} language="python" displayTitle={false} />

## Imperative → declarative cheat sheet

| Imperative | Declarative |
| --- | --- |
| `control.visible = False` | Return a different control tree based on state |
| `control.value = new_value` | Change the model: `user.update(first, last)` |
| `page.update()` — automatic in handlers, explicit outside them | Not needed anywhere — setting state re-renders automatically |
| One handler changing several controls at once | Small, focused components — one per piece of UI |
