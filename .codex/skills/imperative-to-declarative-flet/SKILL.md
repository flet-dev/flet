---
name: imperative-to-declarative-flet
description: Convert an imperative Flet Python app in which controls are mutated and then page.update is called to declarative style using flet.component, flet.observable and state hooks.
metadata:
  short-description: Port Flet app to declarative
---

# Imperative → Declarative (Flet Python)

Port an existing imperative Flet app to “components mode” with `@ft.component`, hooks, and (optionally) `@ft.observable` models.

## Outcomes

- Original folder unchanged; new sibling folder created.
- Entry point uses `page.render(App)` (components mode).
- UI is derived from state; minimal/zero manual `page.update()` for normal UI updates.

## Choose a state strategy

- **Use `@ft.observable`** for nested app data you mutate in place (boards/lists/cards, drag+drop reorder).
- **Use `ft.use_state`** for local ephemeral UI state (hover flags, input text, dialog selection).
- Avoid storing live `Control`/component objects in state; store ids/enums and create controls during render.

## Workflow

### 1) Create a new declarative copy

- Copy the existing app folder to a new one (e.g. `trolli` → `trolli-declarative-*`).
- Keep `assets/` with the new folder.

### 2) Switch to components mode entrypoint

- Create a root component `@ft.component def App(): ...`.
- Run with:
  - `ft.run(lambda page: page.render(App), assets_dir=...)`
- Set page globals either:
  - in a `main(page)` function before `page.render(App)`, or
  - in `ft.on_mounted(...)` (works, but ordering can be less obvious).

### 3) Centralize routing in `App`

- Keep `app.route: str` as source of truth.
- In one place, define:
  - `route_change(e)` to normalize/redirect/validate routes and set `app.route`
  - a render-time `match app.route` (or a derived `active_screen`) to pick `content`
- Prefer: `route_change` mutates route state; `App()` render chooses UI based on that state.

### 4) Componentize UI

- Move UI chunks into `src/components/*.py`.
- Each component:
  - takes only the model(s) it needs
  - uses hooks for local UI state
  - mutates observable models for app data changes

### 5) Dialogs: reduce `page.update()` usage

If a dialog mutates existing controls and calls `page.update()`, convert it to:

- `@ft.component` dialog content with `ft.use_state` for `error`, `selected_color`, etc.
- event handlers call setters (no explicit updates)
- show it via `page.show_dialog(ft.AlertDialog(content=DialogContent(...)))`

### 6) Assets/fonts checklist

- Prefer an absolute `assets_dir` derived from `__file__`.
- If running via `flet run`, be aware it can set `FLET_ASSETS_DIR` and override `assets_dir=`.
- Font registration uses the dict key as the font family name:
  - `page.fonts = {"Pacifico": "Pacifico-Regular.ttf"}`
  - use `font_family="Pacifico"`.

## Common pitfalls (and fixes)

- **Event handler typing is invariant** (`Event[Sub]` ≠ `Event[Base]`):
  - If `on_click` is declared on `Button`, annotate `e` as `ft.Event[ft.Button]` (or use `def handler(): ...`).
- **`TemplateRoute` params are dynamic**:
  - `raw = getattr(troute, "id", None)` then `isinstance(raw, str)` before `int(raw)`.
- **`controls=[*[...], ...]` can confuse type checkers** with components:
  - build lists in two steps and annotate/cast, or return raw controls from non-component factories.

