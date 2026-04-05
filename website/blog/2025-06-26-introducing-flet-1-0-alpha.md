---
slug: introducing-flet-1-0-alpha
title: Introducing Flet 1.0 Alpha
authors: feodor
tags: [news]
---

Flet has been in the making for over three years, steadily gaining traction and building a vibrant user community. As more developers adopt Flet for real-world projects, one thing has become clear: people are ready to commit — but they also want to see the same commitment from us.

Releasing **Flet 1.0** isn’t just about a version number. It’s about signaling stability, maturity, and long-term vision. A stable API, comprehensive documentation, better testing and clearly communicated roadmap — these are the foundational pieces developers need to confidently build serious apps on Flet.

But **Flet 1.0 isn’t just the next incremental release. It’s a complete re-architecture**.

The first versions of Flet inherited design decisions from Pglet — a web-based framework with a focus on multi-language support. While that served as a useful starting point, Flet has since evolved into a Python-centric framework for building cross-platform apps — web, desktop, and mobile.

With that evolution came technical debt, architectural misfits, and increasing complexity. Rather than patch over the cracks, we made a bold decision: to rewrite Flet from the ground up. It’s always risky to rewrite, but there’s no better time than now — before 1.0 — while the user base is still manageable and we can afford to break things in the name of long-term simplicity and maintainability.

After nearly five months of work, **today we’re releasing the Flet 1.0 Alpha — a technical preview of what’s coming.**

<!-- truncate -->

## What’s new

Flet 1.0 introduces major changes that simplify how you build, run, and scale apps. Some are improvements, some are breaking — all are focused on giving you a faster, more flexible developer experience.

* **Declarative approach to building Flet apps** - alongside the traditional imperative style.
* **Auto-update** - automatic page updates after event handler completion.
* **Services** - persistent, non-UI components that live across UI rebuilds and navigation. Existing controls such as `Audio`, `FilePicker`, `Clipboard` were re-written as services.
* **Complete WASM (WebAssembly) support for web apps** - faster download and performance on modern browsers.
* **Offline (no-CDN) mode for web apps** - Flutter resources and Pyodide are bundled with the app.
* **Embedding Flet apps into existing web page** - render Flet app into an HTML element on any web page.
* **Enhanced Extensions API** - to export services along with controls, with a room for future customizations like splash and loading screens.

### Declarative approach

Flet 1.0 introduces a **declarative/reactive approach** to building UIs in Flet. Developers can now mix **imperative** and **declarative** patterns in the same app, enabling more flexible and functional UI code.

#### Basic declarative Flet app example

```py
from dataclasses import dataclass

import flet as ft


@dataclass
class AppState:
    count: int

    def increment(self):
        self.count += 1


def main(page: ft.Page):
    state = AppState(count=0)

    page.floating_action_button = ft.FloatingActionButton(
        icon=ft.Icons.ADD, on_click=state.increment
    )
    page.add(
        ft.ControlBuilder(
            state,
            lambda state: ft.SafeArea(
                ft.Container(
                    ft.Text(value=f"{state.count}", size=50),
                    alignment=ft.Alignment.center(),
                ),
                expand=True,
            ),
            expand=True,
        )
    )


ft.run(main)
```

More declarative examples:

* [Edit form](https://github.com/flet-dev/examples/blob/v1/python/apps/declarative/edit-form.py)
* [Progress bar with yield](https://github.com/flet-dev/examples/blob/v1/python/apps/declarative/progress-with-yield.py)
* 🚀 [Reactive ToDo app](https://github.com/flet-dev/examples/blob/v1/python/apps/todo/todo-reactive.py)

🚧 Documentation is in progress 🚧

### Auto-update

`Control.update()` is now automatically called once its event handler method is finished.
Most of Flet apps will now work without explicit `update()` calls.

Use `yield` inside long-running event handlers to refresh UI, for example:

```py
async def button_click():
  progress.value = "Something started"
  yield
  await asyncio.sleep(3)
  progress.value = "Something finished"
```

🚧 Documentation is in progress 🚧

### Services

"Service" is a persistent, non-visual control that can "survive" page updates and navigation transitions.

Some of the existing controls were re-implemented as services (breaking change):

* `Audio` ([extension](https://pypi.org/project/flet-audio/))
* `AudioRecorder` ([extension](https://pypi.org/project/flet-audio-recorder/))
* `FilePicker`
* `Flashlight` ([extension](https://pypi.org/project/flet-flashlight/))
* `Geolocator` ([extension](https://pypi.org/project/flet-geolocator/))
* `HapticFeedback`
* `InterstitialAd` ([extension](https://pypi.org/project/flet-ads/))
* `PermissionHandler` ([extension](https://pypi.org/project/flet-permission-handler/))
* `SemanticsService`
* `ShakeDetector`

Service instances must be added to `page.services` list to work.

### WebAssembly support

Flet 1.0 web apps use WebAssembly (WASM) by default on [selected browsers](https://docs.flutter.dev/platform-integration/web/wasm#learn-more-about-browser-compatibility). 

Built-in Flet web client and Flet apps built with `flet build web` are now include both Dart2JS (with CanvasKit as a renderer) and WebAssembly (with SKWASM renderer) targets.

🚧 Documentation is in progress 🚧

### Offline mode for web apps

Flet 1.0 has "no-CDN" mode which allows bundling the following resources along with your app instead of loading them from external CDNs:

* CanvasKit
* SkWASM
* Pyodide
* Fonts

To enable no-CDN during runtime either add `no_cdn=True` to `ft.run()` (it's a new `ft.run()`) call:

```py
ft.run(main, no_cdn=True)
```

or set `FLET_WEB_NO_CDN` environment variable to `1`, `true` or `yes`.

To enable no-CDN for `flet build` add `--no-cdn` argument.

🚧 Documentation is in progress 🚧

### Embedding Flet web apps

You can now embed a Flet web app into any HTML element within an existing web page.

It's also possible to render multiple views of the same app in different HTML elements.

🚧 Documentation is in progress 🚧

### Enhanced Extensions API

The new extensions API allows exporting from your Flutter package of both control and service widgets. Technically, an extension is a class now rather than a method which will allow us to add more hooks into it like custom spash and loading screens.

For example, `flet-ads` extension before has just one `createControl` method:

```dart title="create_control.dart"
import 'package:flet/flet.dart';
import 'package:google_mobile_ads/google_mobile_ads.dart';

import 'banner.dart';
import 'interstitial.dart';

CreateControlFactory createControl = (CreateControlArgs args) {
  switch (args.control.type) {
    case "banner_ad":
      return BannerAdControl(
          parent: args.parent, control: args.control, backend: args.backend);
    case "interstitial_ad":
      return InterstitialAdControl(
          parent: args.parent, control: args.control, backend: args.backend);
    default:
      return null;
  }
};

void ensureInitialized() {
  if (isMobilePlatform()) {
    MobileAds.instance.initialize();
  }
}
```

and for Flet v1 it has two methods `createWidget` and `createService`:

```dart title="extension.dart"
import 'package:flet/flet.dart';
import 'package:flutter/cupertino.dart';
import 'package:google_mobile_ads/google_mobile_ads.dart';

import 'banner.dart';
import 'interstitial.dart';

class Extension extends FletExtension {
  @override
  void ensureInitialized() {
    if (isMobilePlatform()) {
      MobileAds.instance.initialize();
    }
  }

  @override
  FletService? createService(Control control) {
    switch (control.type) {
      case "InterstitialAd":
        return InterstitialAdService(control: control);
      default:
        return null;
    }
  }

  @override
  Widget? createWidget(Key? key, Control control) {
    switch (control.type) {
      case "BannerAd":
        return BannerAdControl(control: control);
      default:
        return null;
    }
  }
}
```

This change is breaking.

🚧 Documentation is in progress 🚧

### Other changes and improvements

### `ft.run` with `before_main`

A new `before_main` arg added to `ft.run()` (replaces `ft.run()`). `before_main` is a hook that allows to reliable configure page-level event handlers before Flutter client starts sending events. `before_main` is a function that accepts one parameter: `page: ft.Page`

Example usage:

```py
def config(page: ft.Page):
  page.on_resize = lambda e: print("Page resized!")

def main(page: ft.Page):
  page.add(ft.Text("Hello!"))

ft.run(main, before_main=config)
```

#### Storage paths

There is a new `page.storage_paths` multi-platform API based on [path_provider](https://pub.dev/packages/path_provider) for finding commonly used locations on the filesystem:

```py
get_application_cache_directory_async(self) -> str
get_application_documents_directory_async(self) -> str
get_application_support_directory_async(self) -> str
get_downloads_directory_async(self) -> Optional[str]
get_external_cache_directories_async(self) -> Optional[List[str]]
get_external_storage_directories_async(self) -> Optional[List[str]]
get_library_directory_async(self) -> str
get_external_cache_directory_async(self) -> Optional[str]
get_temporary_directory_async(self) -> str
get_console_log_filename_async(self) -> str
```

🚧 Documentation is in progress 🚧

#### Event handlers without `e`

Event handlers can now omit `e` parameter, for example both of these work:

```py
button_1.on_click = lambda: print("Clicked!")
button_2.on_click = lambda e: print("Clicked!", e)
```

or

```py
def increment():
   print("Increment clicked")

inc_btn.on_click = increment
```

#### `Control.before_event(e)` hook

The method is called before calling any event handler.

It receives an instance of `ControlEvent` as parameter and should return either `True` or `False`. Returning `False` cancels event handler. Example implementation in `Page` class:

```py
    def before_event(self, e: ControlEvent):
        if isinstance(e, RouteChangeEvent):
            if self.route == e.route:
                return False
            self.query()
        return super().before_event(e)
``` 

#### `ft.context.page` works everywhere

It's now possible to get a reference to a current `Page` instance in any part of Flet program.

## The new Architecture

Flet 1.0 is not just a feature release — it's a ground-up rewrite designed to address technical debt, improve maintainability, and unlock long-term performance and flexibility. Here are some of the most impactful architectural changes:

### Simplified Python control implementation

- Controls are now implemented as Python **dataclasses**, bringing:
  - Automatic constructor generation
  - Native support for default values, type annotations, and field validation
  - No more manual conversions to/from `str` or `JSON`
  - Seamless support for **complex property types** (nested dataclasses, enums, etc.)

- This significantly reduces boilerplate and makes adding new controls trivial — often zero-maintenance.

### Strong typing and IDE support

- Event handlers are now **strongly typed**, improving both runtime safety and developer ergonomics.
- All controls include **docstrings**, enabling rich auto-generated API documentation with **Docusaurus**.

### Smarter UI diffing

- A new **diffing algorithm** powers efficient updates to the UI tree.
- It’s optimized for both **imperative** and **declarative** Flet programming styles.
- This results in faster rebuilds and fewer unnecessary redraws.

### Dart runtime modernization

- Replaced the old Redux-based state management with **InheritedWidget** + **Provider**.
- The internal control hierarchy on the Dart side now mirrors the Python control tree, enabling **more efficient traversal and updates**.

### Binary protocol for performance

- A new **binary serialization protocol** (MessagePack) replaces the JSON-based message format:
  - Significantly reduces traffic size
  - No more base64 encoding for transferring binary data (e.g., images, files)

- Control property names in Dart now **exactly match their Python counterparts**, making it easier to debug and extend across both runtimes.

## Breaking changes

Flet 1.0 is a major release and includes breaking changes — for good reason!

The Flet team maintains a list of known breaking changes in [this issue](https://github.com/flet-dev/flet/issues/5238).

If you discover something else that’s broken or incorrect, please submit a new issue or discussion. Once confirmed, we’ll update the list.

Below is a summary of the most significant and impactful breaking changes:

### Single-threaded async UI model

Flet 1.0 adopts a single-threaded async UI model, similar to JavaScript or Flutter. This design makes concurrency more predictable and better suited for the browser and mobile platforms.

* Blocking calls like `time.sleep()` will freeze the UI. Instead of `time.sleep()` use `async def` event handlers and using `await asyncio.sleep()` for delays.
* Switch to async APIs whenever possible.
* For CPU-bound tasks, offload them to threads using `asyncio.to_thread(...)`.

🚧 Example with CPU-bound method updating progress bar 🚧

### Async control methods

All controls' get- and set- methods are async now.

Methods that do not return any results have fire-and-forget sync wrappers.

🚧 Documentation is in progress 🚧

### `ft.run()` replaces `ft.run()`

`target` argument renamed to `main` and the rest of method arguments stays the same. A new `before_main` argument added (see above).

### `Page` split

`Page` split into `Page` and `PageView`.

To support Flet embedding with multi-views.

It's not a breaking-change per-se if you just continue to use `page` instance methods or properties.

🚧 Documentation is in progress 🚧

### Dialogs

To display a dialog, banner, snack bar, drawer, or any similar popup control, use `page.show_dialog(dialog_control)` instead of `page.open()`.

To close the topmost popup, use `page.pop_dialog()`.

### Drawers

`page.drawer` and `page.end_drawer` were removed.

:::note
We might re-introduce this in the future, to fix displaying of the top menu icon button as in this [example](https://api.flutter.dev/flutter/material/Scaffold/endDrawer.html).
:::

Use `NavigationDrawer.position` property and then `page.show_dialog()` to display drawer instead of `page.drawer` and `page.end_drawer`.

### FilePicker

FilePicker is now a service and must be added to `page.services` list to work.

API re-worked to provide async methods immediatly returning dialog results without using "result" event handlers.

```py
files: list[FilePickerFile] = await file_picker.pick_files_async(allow_multiple=True)
file_name: str = await file_picker.save_file_async()
dir_name: str = await file_picker.get_directory_path_async()
```

Full examples:

* [All dialogs](https://github.com/flet-dev/examples/blob/v1/python/controls/utility/file-picker/file-picker-all-modes.py)
* [Upload](https://github.com/flet-dev/examples/blob/v1/python/controls/utility/file-picker/file-picker-upload-progress.py)

### Clipboard

Instead of `page.set_clipboard()` use `page.clipboard.set_async()`.

Instead of `page.get_clipboard()` use `page.clipboard.get_async()`.

### Client storage

"Client storage" is now "Shared Preferences".

`page.client_storage` property renamed to `page.shared_preferences`.

### Scrollables

In scrollable controls `on_scroll_interval` property renamed to `scroll_interval`.

### Buttons

All buttons: no `text` property, use `content` instead.

### Charts

Chart controls have been moved to a separate package [flet-charts](https://pypi.org/project/flet-charts/).

### Control ID is integer

`e.target` is a number now, not a string.

## Trying Flet 1.0 Alpha

We are releasing Flet 1.0 Alpha as [0.70.0.devXXXX](https://pypi.org/project/flet/#history).

:::info
Going forward Flet 1.0 will be called `v1` and Flet 0.x will be called `v0`.

`main` branch of Flet repository will have Flet 1.0 and `v0` branch will have Flet 0.x.
:::

:::caution
Make sure you are installing Flet pre-release to a new virtual environment.
:::

To install Flet v1 Alpha with pip:

```
pip install --pre 'flet[all]>=0.70.0.dev0'
```

or install with uv:

```
uv add 'flet[all]>=0.70.0.dev0' --prerelease=allow
```

or add `flet >=0.70.0.dev0` to dependencies of your Python project.

### `flet build`

To make `flet build` work with Flet 1.0 Alpha specify exact version of `flet` and all extension packages in `dependencies` section of your `pyproject.toml`:

```
dependencies=[
  "flet >=0.70.0.dev0",
  "flet-audio >=0.2.0.dev0",
  "flet-video >=0.2.0.dev0",
  ...
]
```

Extensions for Flet v1 will have version `0.2.x` and above and Flet v0 extensions will have version `0.1.x`.

## Roadmap to Flet 1.0

* Flet 0.70 aka "**Flet 1.0 Alpha**" - this release. Generated docs are not yet included. We may release a few Flet 0.71, 0.72, 0.73, etc. to fix things.
* Flet 0.80 aka "**Flet 1.0 Beta**" - docs generated from sources are ready. All extensions are working and documented. Integration tests are available.
* Flet 0.90 aka "**Flet 1.0 RC**" - website landing page is updated, API complete and frozen.
* Flet 1.0 aka "**Flet 1.0 RTM**" - final release! :tada:

## Conclusion

Flet 1.0 Alpha marks the beginning of a new chapter for the framework — one focused on performance, maintainability, and developer experience. It introduces a streamlined architecture, a powerful declarative programming model, and a reimagined extension system — all while laying the groundwork for a stable and scalable 1.0 release.

This is a technical preview, and while it's not production-ready yet, we invite you to try it out, share your feedback, and help us shape the future of Flet.

We’re incredibly excited about what’s coming next — and we’re just getting started.