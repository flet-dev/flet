---
title: "All deprecated APIs removed"
---

# All deprecated APIs removed

:::note
This guide is accurate as of Flet 1.0.0. Later releases might add new APIs or
additional migration paths.

The [breaking changes and deprecations index](../index.md) lists the guides created for each release.
:::

## Summary

Flet 1.0.0 removes every API that was deprecated in the previous Flet versions, so the
release ships deprecation-free. Each removal has a direct replacement.

### Controls and types

| Removed                                       | Replacement                                                      |
|-----------------------------------------------|------------------------------------------------------------------|
| `ElevatedButton`                              | [`Button`][flet.Button]                                          |
| `ConstrainedControl`                          | [`LayoutControl`][flet.LayoutControl]                            |
| `DragTargetEvent.x` / `.y`                    | `DragTargetEvent.local_position`                                 |
| `DragTargetEvent.offset`                      | `DragTargetEvent.global_position`                                |
| `Video.show_controls`                         | Set `Video.controls` to `None` to hide them                      |
| `Video.playlist_add()` / `.playlist_remove()` | Mutate `Video.playlist` directly, e.g. `append()` / `pop()`      |
| `Colors.BLACK12`, `Colors.WHITE70`, …         | The underscored names, e.g. `Colors.BLACK_12`, `Colors.WHITE_70` |

### Page and app APIs

| Removed                                          | Replacement                                        |
|--------------------------------------------------|----------------------------------------------------|
| `app()` / `app_async()`                          | `run()` / `run_async()`                            |
| `target` parameter of `run()` / `run_async()`    | `main`                                             |
| `Page.go()`                                      | `Page.push_route()`                                |
| `Page.launch_url()`                              | `UrlLauncher().launch_url()`                       |
| `Page.can_launch_url()`                          | `UrlLauncher().can_launch_url()`                   |
| `Page.close_in_app_web_view()`                   | `UrlLauncher().close_in_app_web_view()`            |
| `Page.url_launcher`                              | `UrlLauncher()`                                    |
| `Page.browser_context_menu`                      | `BrowserContextMenu()`                             |
| `Page.shared_preferences`                        | `SharedPreferences()`                              |
| `Page.clipboard`                                 | `Clipboard()`                                      |
| `Page.storage_paths`                             | `StoragePaths()`                                   |
| `FletApp.show_app_startup_screen`                | `FletApp.boot_screen_options`                      |
| `FletApp.app_startup_screen_message`             | `FletApp.boot_screen_options`                      |

### Tooling and configuration

| Removed                                                          | Replacement                                   |
|------------------------------------------------------------------|-----------------------------------------------|
| `--clear-cache` flag of `flet build` and `flet debug`            | The `flet clean` command                      |
| `[tool.flet.app.boot_screen]` / `[tool.flet.app.startup_screen]` | `[tool.flet.boot_screen]` with a named screen |
| Dart empty-string (`""`) widget-state key                        | `"default"`, or `ControlState.DEFAULT`        |

`DropdownM2` is **not** removed. Its deprecation in favour of `Dropdown` is
withdrawn, and it remains a supported control.

## Background

Flet's [compatibility policy](../../compatibility-policy.md) removes a
deprecated API after three minor releases. Rather than spread those removals
across several `0.8x` releases, they are taken together in 1.0.0 so that the
first stable release carries no deprecation debt and no compatibility shims.

Every API listed above emitted a runtime `DeprecationWarning` and carried a
deprecation label in the API docs before this release, so code that ran without
warnings on `0.86` needs no changes.

## Migration guide

Run your app on Flet `0.86` first and fix everything that emits a
`DeprecationWarning` — that is the complete list of what 1.0.0 removes. To
surface the warnings, run Python with them enabled:

```bash
python -W default::DeprecationWarning main.py
```

Then apply the replacements from the tables above.

Code before migration:

```python
import flet as ft

async def main(page: ft.Page):
    async def open_site(e):
        await page.launch_url("https://flet.dev")

    page.add(ft.ElevatedButton("Open", on_click=open_site))
    await page.go("/home")

ft.app(target=main)
```

Code after migration:

```python
import flet as ft

async def main(page: ft.Page):
    async def open_site(e):
        await ft.UrlLauncher().launch_url("https://flet.dev")

    page.add(ft.Button("Open", on_click=open_site))
    await page.push_route("/home")

ft.run(main)
```

Three of these removals have their own guides, written when the APIs were
deprecated:

- [`DragTargetEvent` coordinate fields](../v0-85-0/deprecated-drag-target-event-coordinates.md)
- [`Video` control APIs](../v0-85-0/deprecated-video-apis.md)
- [`flet build --clear-cache` flag](../v0-86-0/deprecated-clear-cache-flag.md)

## Timeline

- Removed in: `1.0.0`

## References

- API documentation: [`Button`][flet.Button], [`LayoutControl`][flet.LayoutControl], [`UrlLauncher`][flet.UrlLauncher], [`Colors`][flet.Colors]
- [Compatibility policy](../../compatibility-policy.md)
- Issues and PRs: [#6693](https://github.com/flet-dev/flet/pull/6693)
- Release notes: [Flet 1.0.0](../../release-notes.md#10x)
