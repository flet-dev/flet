---
slug: flet-v-0-85-release-announcement
title: "Flet 0.85.0: Declarative apps grow up — Router, dialogs, and more"
authors: feodor
tags: [releases]
---

Flet 0.85.0 brings first-class declarative navigation and dialog management, richer media controls, and a long list of bug fixes.

Highlights in this release:

* Declarative `ft.Router` for `@ft.component` apps — nested routes, layouts with outlets, dynamic segments, data loaders, and `manage_views=True` for native view-stack navigation.
* New `ft.use_dialog()` hook — dialogs are now reactive state in declarative apps, not imperative `page.show_dialog()` calls.
* `flet-video`: configurable controls, `Video.take_screenshot()`, and `on_position_change` / `on_duration_change` events.
* `AudioRecorder` PCM16 streaming via `on_stream` chunks and direct upload through `AudioRecorderUploadSettings`.
* Tons of bug fixes — charts, web assets, packaging, mobile orientation, and more.

{/* truncate */}

## How to upgrade

If you use pip:

```bash
pip install 'flet[all]' --upgrade
```

If you use uv with `pyproject.toml` and want to upgrade everything:

```bash
uv sync --upgrade
```

If you want to upgrade only Flet packages:

```bash
uv sync --upgrade-package flet \
  --upgrade-package flet-cli \
  --upgrade-package flet-desktop \
  --upgrade-package flet-web
```

## Declarative Router

Imperative Flet apps have always had `Page.route` and `Page.views` for navigation. But declarative apps — the ones built around `@ft.component` — had to roll their own: subscribe to route changes, parse the path, render the right component. It worked, but it was boilerplate that every app reinvented.

0.85.0 adds `ft.Router`: a declarative, React Router-style component that matches the current page route against a tree of `ft.Route` definitions and renders the matched component chain. Here's the simplest possible example:

```python
import flet as ft

@ft.component
def Home():
    return ft.Text("Home page", size=24)

@ft.component
def About():
    return ft.Text("About page", size=24)

@ft.component
def App():
    return ft.SafeArea(
        content=ft.Column([
            ft.Row([
                ft.Button("Home", on_click=lambda: ft.context.page.navigate("/")),
                ft.Button("About", on_click=lambda: ft.context.page.navigate("/about")),
            ]),
            ft.Router([
                ft.Route(index=True, component=Home),
                ft.Route(path="about", component=About),
            ]),
        ])
    )

ft.run(lambda page: page.render(App))
```

Routes can nest, and a parent route can render a shared layout that wraps its children using `ft.use_route_outlet()`:

```python
@ft.component
def AppLayout():
    outlet = ft.use_route_outlet()
    return ft.Column([
        ft.Container(
            content=ft.Row([
                ft.Text("My App", size=20, weight=ft.FontWeight.BOLD),
                ft.Button("Home", on_click=lambda: ft.context.page.navigate("/")),
                ft.Button("About", on_click=lambda: ft.context.page.navigate("/about")),
            ]),
            bgcolor=ft.Colors.SURFACE_BRIGHT,
            padding=10,
        ),
        ft.Container(content=outlet, padding=20),
    ])

@ft.component
def App():
    return ft.Router([
        ft.Route(component=AppLayout, children=[
            ft.Route(index=True, component=Home),
            ft.Route(path="about", component=About),
        ]),
    ])
```

What `Router` supports:

* **Nested routes** with shared layouts via `outlet=True` and `ft.use_route_outlet()`.
* **Dynamic segments** like `/users/:id` and **optional segments** like `/posts/:id?`.
* **Splats** for catch-all paths (`/files/*`).
* **Custom regex constraints** on segment values.
* **Data loaders** that run before a route renders.
* **Active link detection** so navigation UI can highlight the current route.
* **Authentication patterns** for guarded routes.
* **`manage_views=True`** — switches the router into view-stack mode where each route returns a full `View` with its own `AppBar`. Navigating deeper pushes views onto the stack, and the user can swipe back or tap the AppBar back button on mobile.

More info:

* PR: [#6406](https://github.com/flet-dev/flet/pull/6406)
* Guide: [Router](/docs/cookbook/router)
* Docs: [Router](https://flet.dev/docs/controls/router)

## `use_dialog()` hook

Dialogs in imperative Flet are imperative: you call `page.show_dialog(...)` to open, `page.close_dialog()` to close. That model doesn't fit declarative apps, where the UI is supposed to be a function of state. Until now, the workaround was to keep a reference to the dialog and toggle `open` manually — fiddly and easy to get wrong.

The new `ft.use_dialog()` hook closes that gap. Pass a `DialogControl` to show it, pass `None` to dismiss it. The dialog is portaled into the page's dialog overlay automatically, and removed when the component unmounts:

```python
import asyncio
import flet as ft

@ft.component
def App():
    show, set_show = ft.use_state(False)
    deleting, set_deleting = ft.use_state(False)

    async def handle_delete():
        set_deleting(True)
        await asyncio.sleep(2)
        set_deleting(False)
        set_show(False)

    ft.use_dialog(
        ft.AlertDialog(
            modal=True,
            title=ft.Text("Delete report.pdf?"),
            content=ft.Text(
                "Deleting, please wait..." if deleting else "This cannot be undone."
            ),
            actions=[
                ft.Button(
                    "Deleting..." if deleting else "Delete",
                    disabled=deleting,
                    on_click=handle_delete,
                ),
                ft.TextButton(
                    "Cancel",
                    on_click=lambda: set_show(False),
                    disabled=deleting,
                ),
            ],
            on_dismiss=lambda: set_show(False),
        )
        if show
        else None
    )

    return ft.Button("Delete File", icon=ft.Icons.DELETE, on_click=lambda: set_show(True))
```

A subtle but important detail: the hook uses **frozen-diff reactive updates**. When the component re-renders and you pass back a *new* dialog instance with different field values, the hook diffs it field-by-field against the previous instance and emits only the actual deltas — instead of replacing the dialog wholesale. That means a `TextField` inside an `AlertDialog` keeps its cursor, focus, and selection across re-renders, even though Python is handing the framework a brand-new control object on every build.

You can also call `use_dialog()` multiple times in the same component to manage independent dialogs (e.g. a rename dialog and a delete dialog on the same screen), and each one is tracked separately.

More info:

* PR: [#6335](https://github.com/flet-dev/flet/pull/6335)

## Better video controls

`flet-video` got a substantial upgrade. The control bar is now fully configurable: you can use the built-in controls, replace them with your own widgets, hide them entirely, or specify different controls for normal and fullscreen modes. There's also a new `Video.take_screenshot()` method for capturing the currently displayed frame, and two new events for keeping your UI in sync with playback:

* `on_position_change` — fires as playback progresses, useful for driving a custom progress bar.
* `on_duration_change` — fires when the video's duration becomes known (or changes between playlist entries).

```python
async def handle_screenshot(e):
    image_bytes = await video.take_screenshot()
    # save, upload, display in an Image, etc.

video = ft.Video(
    playlist=[ft.VideoMedia("https://example.com/clip.mp4")],
    on_position_change=lambda e: print(f"At {e.position}s"),
    on_duration_change=lambda e: print(f"Duration: {e.duration}s"),
)
```

More info:

* PR: [#6463](https://github.com/flet-dev/flet/pull/6463)

## AudioRecorder streaming

Until 0.85.0, `AudioRecorder` recorded to a file and you read the file back when you were done. That's fine for "record then transcribe" flows, but it doesn't work for real-time use cases — voice activity detection, live transcription, streaming an LLM voice assistant.

Now `AudioRecorder` can stream raw PCM16 chunks via the new `on_stream` event as audio is captured. Here's the core of the streaming example — receive chunks, buffer them, and write a WAV when recording stops:

```python
import flet as ft
import flet_audio_recorder as far

def main(page: ft.Page):
    buffer = bytearray()

    def handle_stream(e: far.AudioRecorderStreamEvent):
        buffer.extend(e.chunk)
        status.value = f"Streaming chunk {e.sequence}; {e.bytes_streamed} bytes."

    async def start(e):
        buffer.clear()
        await recorder.start_recording(
            configuration=far.AudioRecorderConfiguration(
                encoder=far.AudioEncoder.PCM16BITS,
                sample_rate=44100,
                channels=1,
            ),
        )

    recorder = far.AudioRecorder(on_stream=handle_stream)
    page.add(ft.Button("Start", on_click=start), status := ft.Text())
```

For server-side capture without buffering through Python, point the recorder at an upload URL and the audio uploads as it streams:

```python
upload_url = page.get_upload_url(file_name="rec.pcm", expires=600)
await recorder.start_recording(
    upload=far.AudioRecorderUploadSettings(upload_url=upload_url, file_name="rec.pcm"),
    configuration=far.AudioRecorderConfiguration(encoder=far.AudioEncoder.PCM16BITS),
)
```

More info:

* PR: [#6423](https://github.com/flet-dev/flet/pull/6423)
* Issue: [#5858](https://github.com/flet-dev/flet/issues/5858)

## Other improvements

* Scrollable `NavigationRail` with optional `pin_leading_to_top` and `pin_trailing_to_bottom` ([#6356](https://github.com/flet-dev/flet/pull/6356)).
* Scroll support on `ResponsiveRow` for layouts whose content exceeds available height ([#6417](https://github.com/flet-dev/flet/pull/6417)).
* `CodeEditor.issues` for displaying analysis error markers in the gutter, with analysis performed in Python ([#6407](https://github.com/flet-dev/flet/pull/6407)).
* `Page.pop_views_until()` to pop multiple views and return a result to the destination ([#6347](https://github.com/flet-dev/flet/pull/6347)).
* `NavigationDrawerDestination.label` now accepts custom controls; new `NavigationDrawerTheme.icon_theme` ([#6395](https://github.com/flet-dev/flet/pull/6395)).
* `DragTargetEvent.local_position` and `global_position` (deprecating `x`, `y`, `offset`) ([#6401](https://github.com/flet-dev/flet/pull/6401)).
* `Page.theme_animation_style` for customizing the theme cross-fade between `theme` and `dark_theme` ([#6476](https://github.com/flet-dev/flet/pull/6476)).

## Bug fixes worth calling out

* Unbounded browser memory growth in `MatplotlibChart` on Flutter web during animations ([#6473](https://github.com/flet-dev/flet/pull/6473)).
* 3- and 4-digit hex color shorthand (`#c00`, `#fc00`) rendering as invisible ([#6421](https://github.com/flet-dev/flet/pull/6421)).
* `auto_scroll` silently doing nothing unless `scroll` was also explicitly set ([#6404](https://github.com/flet-dev/flet/pull/6404)).
* Flet web returning `index.html` with `200 OK` for missing asset files instead of a proper `404` ([#6425](https://github.com/flet-dev/flet/pull/6425)).
* `Lottie` failing to load local asset files on Windows desktop ([#6426](https://github.com/flet-dev/flet/pull/6426)).
* `Page.on_resize` and `Page.on_media_change` not firing after mobile orientation changes ([#6423](https://github.com/flet-dev/flet/pull/6423)).
* `flet pack` desktop bundles missing the client archive on Windows and Linux ([#6403](https://github.com/flet-dev/flet/pull/6403)).
* `Duration` fields silently decoding to `0` when given a Python `float` (e.g. `Duration(seconds=2.0)`) ([#6480](https://github.com/flet-dev/flet/pull/6480)).
* `page.window.destroy()` taking several seconds to close Windows desktop apps when `prevent_close` is enabled ([#6428](https://github.com/flet-dev/flet/pull/6428)).
* `Page` and `View` vertical centering when scrolling is enabled ([#6450](https://github.com/flet-dev/flet/pull/6450)).
* `LineChart` silently dropping custom axis labels whose value matched a tick after floating-point rounding ([#6459](https://github.com/flet-dev/flet/pull/6459)).
* Linux memory retention when repeatedly removing `flet_video.Video` controls ([#6416](https://github.com/flet-dev/flet/pull/6416)).

See the full [CHANGELOG](https://github.com/flet-dev/flet/blob/main/CHANGELOG.md#0850) for the complete list.

## Conclusion

Flet 0.85.0 fills in two pieces that declarative apps were really missing: routing and dialogs. Combined with smoother video, real-time audio, and a healthy round of bug fixes, this release moves the `@ft.component` programming model from "promising" to "production-ready for real apps".

Try it in your apps and share feedback in [GitHub Discussions](https://github.com/flet-dev/flet/discussions) or on [Discord](https://discord.gg/dzWXP8SHG8).

Happy Flet-ing!
