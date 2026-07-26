---
title: "Declarative vs Imperative"
examples: "cookbook/declarative_vs_imperative_crud_app"
---

import {CodeExample} from '@site/src/components/crocodocs';

By default, a Flet app is **imperative**: you directly change control properties like `visible` and `value`, add or remove controls, and Flet pushes the change to the page for you. That's fine for small apps, but it doesn't scale well — as a screen grows, the logic for keeping related controls in sync gets duplicated across event handlers, and it's easy to miss one and end up with an inconsistent UI.

Flet also supports a **declarative** approach: the state of your app is the single source of truth, and the UI is derived from it. You don't change controls or their properties directly; instead, only change application state, by assigning to an observable field or calling a hook's setter (which will be discussed later in the article). Flet detects the change and re-renders UI that depends on it.

This article shows the same simple "User Manager" app built both ways — imperative and declarative — so you can compare the two approaches directly. It's a classic CRUD app: list users, add a new one, edit inline, and delete:

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

State lives in two `@ft.observable` classes: `User` (`first_name`, `last_name`) and `App` (`users: list[User]`, with `add_user`/`delete_user`). `@ft.component` functions read that state and return controls — `UserView` renders one row, read-only or editing; `AddUserForm` renders the add form. Each row's "editing" flag and input buffers are local `ft.use_state` hooks: they're view-only and don't belong on `User`.

Handlers only touch state — `set_is_editing(True)`, `user.update(...)`, `app.users.remove(user)` — and Flet re-renders whatever reads it.

<figure className="doc-screenshot-figure"><img alt="declarative data flow diagram" className="doc-screenshot" src="/docs/assets/cookbook/declarative-vs-imperative-crud-app/crud-declarative.drawio.png" style={{width: "55%"}} /></figure>

<CodeExample path={frontMatter.examples + '/declarative/main.py'} language="python" displayTitle={false} />

## Observables, components, and hooks

* **Observables** (`@ft.observable`) hold durable, worth-saving data — like `User` and `App` above. Assigning to a field, or changing a list/dict field (`app.users.append(...)`), triggers a re-render.
* **Components** (`@ft.component`) are functions that take props, optionally call hooks, and return controls describing the UI right now. They never change the control tree directly.
* **Hooks** (`ft.use_state`) hold local state scoped to one component instance — like the "editing" flag above. A plain local variable won't do the job: it resets on every render, and changing it doesn't trigger one.

```python
# Broken: a plain local resets on every render, and changing it doesn't trigger one
@ft.component
def CounterBroken():
    count = 0
    return ft.Row([
        ft.Text(str(count)),
        ft.Button("+", on_click=lambda _: (count := count + 1)),
    ])

# Correct: hook state survives across renders and triggers one when set
@ft.component
def Counter():
    count, set_count = ft.use_state(0)
    return ft.Row([
        ft.Text(str(count)),
        ft.Button("+", on_click=lambda _: set_count(count + 1)),
    ])
```

## Imperative → declarative cheat sheet

| Imperative | Declarative |
| --- | --- |
| `control.visible = False` | Return a different control tree based on state |
| `control.value = new_value` | Change the model: `user.update(first, last)` |
| `page.update()` — automatic in handlers, explicit outside them | Not needed anywhere — setting state re-renders automatically |
| One handler changing several controls at once | Small, focused components — one per piece of UI |
