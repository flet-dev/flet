---
slug: flet-v-0-86-release-announcement
title: "Flet 0.86.0: Faster everywhere — new Android packaging, dart-bridge, and Python 3.14"
authors: feodor
tags: [releases]
---

<img src="/img/blog/flet-86/flet-86.png" className="screenshot screenshot-70" style={{borderRadius: '7px'}} alt="Flet 86" />

Flet 0.86.0 is our "anniversary" release — the last one before 1.0 — and the logo is a nod to [Expo 86](https://en.wikipedia.org/wiki/Expo_86), the World's Fair held in Vancouver in 1986. Expo 86's theme was *"Transportation and Communication"*, and by a happy coincidence that's exactly what this release is about: how Python and Dart **communicate** — a new in-process dart-bridge transport replacing sockets, plus dedicated data channels for bulk binary traffic — and how your app is **transported** to devices, with completely re-designed Android packaging and faster, leaner packaging on every other platform.

Under the retro logo, 0.86 pays down the last big pieces of technical debt on the road to 1.0: direct Python↔Dart communication without sockets, and a real integration-testing story for your apps.

Highlights in this release:

* **Multi-version Python** — bundle Python 3.12, 3.13, or 3.14 on all platforms, with the latest Pyodide 314.0.2 on the web and [70+ pre-built Android and iOS binary packages](https://pypi.flet.dev) for every supported version.
* **dart-bridge** — lightning-fast in-process communication between Python and Dart; no more sockets.
* **Data channels** — dedicated byte channels for bulk binary data, bypassing the control protocol.
* **New [`ft.RawImage`](/docs/controls/rawimage) control** — full-bandwidth pixel streaming from Pillow, NumPy, or camera frames straight to a GPU texture.
* **Faster Matplotlib** — raw RGBA frames over data channels: 2.5× higher FPS on interactive charts.
* **Re-designed Android packaging** — modern, extraction-free, memory-mapped; smaller and faster apps.
* **Faster startup everywhere** — unpacked app bundles, bytecode compilation by default, and lazy `import flet`.
* **Testing framework** — write pytest integration tests for your app and run them on real devices with `flet test`.
* **Flet MCP server** — accurate, version-specific Flet knowledge for your AI agent.
* **Multiprocessing support** in packaged desktop apps, custom boot screens, normalized app storage, and more.

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

## Multi-version Python

Until now, `flet build` shipped one hardcoded Python version. 0.86 lets you pick the runtime your app bundles — **3.12, 3.13, or 3.14** — on all platforms: Windows, macOS, Linux, Android, iOS, and web.

```bash
flet build apk --python-version 3.13
```

Or skip the flag and let Flet derive it from `requires-python` in your `pyproject.toml`; with neither, you get the latest supported stable — currently **Python 3.14.6**. Web builds get the matching Pyodide release automatically, up to the latest **Pyodide 314.0.2** for Python 3.14.

Behind the scenes there's now a **single source of truth for Python runtimes**: a manifest in the [python-build](https://github.com/flet-dev/python-build) repository defines the exact CPython build, Pyodide release, and dart-bridge version for every supported Python line, shared by the Flet CLI and `serious_python`. When a new CPython lands, supporting it is a manifest update — not a coordinated release train. And to make native dependencies just work on mobile, we publish [**70+ pre-built Android and iOS binary packages**](https://pypi.flet.dev) (numpy, pillow, cryptography, pydantic-core, and friends) for every supported Python version.

More info:

* PR: [#6577](https://github.com/flet-dev/flet/pull/6577)
* Docs: [Choosing a Python version](/docs/publish#choosing-a-python-version)
* Migration: [Default bundled Python is now 3.14](/docs/updates/breaking-changes/v0-86-0/default-bundled-python-3-14)

## dart-bridge: in-process Python ↔ Dart

Since its first release, a packaged Flet app has been two programs talking over a localhost socket: the Flutter client on one side, your Python app on the other. It worked, but it meant socket setup, message copies through the OS, and awkward lifecycle corners on mobile.

0.86 replaces that with [**dart-bridge**](https://github.com/flet-dev/dart-bridge): the Python interpreter is embedded **in the same process** as the Flutter app, and the two sides exchange messages over an FFI byte channel — no sockets, no network stack, no serialization detours. This is now how every app built with `flet build` runs on desktop and mobile.

Beyond raw speed, in-process embedding fixes real behaviors: on Android, when the OS keeps the process alive after a back-button quit and restarts only the Dart VM, the transport rebinds to the new VM — your Python process and its in-memory state survive, and the session is rebuilt seamlessly. It's also the foundation that made [multiprocessing support](#multiprocessing-in-desktop-apps) possible.

## Data channels

The Flet protocol is great for control updates, but it was never meant for moving megabytes of pixels or audio per frame — every byte went through MsgPack serialization on one side and deserialization on the other.

New in 0.86, [**data channels**](/docs/types/datachannel) are dedicated byte pipes between Dart and Python for exactly that: image frames, audio buffers, ML tensors. Frames bypass the control protocol entirely; in embedded (dart-bridge) mode each channel is backed by its own bridge, moving **4–7 GiB/s** on an M2 Pro. In dev and web modes, channels transparently mux over the active transport, and Pyodide gets zero-copy outbound sends via transferable ArrayBuffers.

Data channels are a building block for control authors — and the next two features are the first controls built on top of them.

More info:

* Docs: [DataChannel](/docs/types/datachannel)
* Migration: [Protocol framing upgrade](/docs/updates/breaking-changes/v0-86-0/data-channel-protocol-upgrade)

## New `RawImage` control

Use [`Image`](/docs/controls/image) for pictures that come from a file or URL. Use the new [**`ft.RawImage`**](/docs/controls/rawimage) when your Python code *produces* pixels — Pillow drawings, NumPy arrays, camera frames, procedural animations — and you want to push them to the screen repeatedly and fast.

Frames stream over a dedicated data channel: when the client runs on the same machine (desktop app, `flet run`, Pyodide), raw premultiplied RGBA goes straight to a GPU texture with no image encoding or decoding on either side; remote web sessions automatically fall back to compact PNG frames. The `render` methods are awaitable and resolve when the frame is actually displayed, so a plain loop self-paces to display speed:

```python
raw_image = ft.RawImage(expand=True)
page.add(raw_image)

while True:
    await raw_image.render(produce_pil_image())
```

[`render()`](/docs/controls/rawimage#flet.RawImage.render) accepts Pillow images and NumPy arrays, [`render_rgba()`](/docs/controls/rawimage#flet.RawImage.render_rgba) takes raw pixel bytes, and [`render_encoded()`](/docs/controls/rawimage#flet.RawImage.render_encoded) displays ready-made PNG/JPEG/WebP bytes. Pillow and NumPy are optional dependencies. The control ships with five gallery examples: a photo viewer, a plasma animation, a Pillow paint app, a Mandelbrot explorer, and Game of Life.

More info:

* PR: [#6674](https://github.com/flet-dev/flet/pull/6674)
* Docs: [RawImage](/docs/controls/rawimage)

## Faster Matplotlib

[`MatplotlibChart`](/docs/controls/charts/matplotlibchart) was the first control migrated to data channels, and interactive charts got dramatically faster in the process. On local transports, per-frame diffing and PNG encode/decode are skipped entirely: uncompressed RGBA frames stream straight from matplotlib's Agg buffer to the screen. A 1600×1000 figure at 2× DPR — 24 MB per frame — went from **7.4 to 18.7 fps**, to the point where matplotlib's own rendering is now the dominant per-frame cost. Remote web clients keep the bandwidth-friendly PNG full+diff pipeline.

Related: `flet build web` now defaults the renderer to `canvaskit`, because the `auto` renderer's JS↔Dart typed-data boundary made byte-streaming Pyodide apps 6–7× slower per frame. Pass `--renderer auto` to restore the old behavior.

More info:

* PR: [#6673](https://github.com/flet-dev/flet/pull/6673)

## Re-designed Android packaging

Packaging on Android has been **completely re-done** in 0.86 — this is the release's biggest single piece of engineering. What changed:

* **No more "legacy" packaging.** Android no longer unpacks native libraries from the `.apk` to disk — it serves them directly from the APK. The `useLegacyPackaging` / `keepDebugSymbols` workarounds are gone from the build template; all you need is `minSdk 23+`.
* **Real native libraries, loaded from memory.** Binary `.so` extension modules no longer hide inside a fake `libsitepackages.so` zip. They now live in proper `lib/{arch}` folders alongside other native libraries and are **memory-mapped directly from the APK** by a custom Python loader — no extraction, no disk copies.
* **Pure-Python-only zips.** `site-packages.zip` now contains only Python files; all platform-dependent binaries — historically the biggest size factor — are stripped out and moved to `lib/{arch}`.
* **Zero-compression, zero-extraction imports.** Both the stdlib and site-packages ship as *stored* (uncompressed) zips that Python imports from directly via `zipimport`, and the app zip ships in Android assets.
* **Compiled by default.** Compiling site-packages and app code on-device used to cost 2–3 seconds of startup on slow devices — now bytecode ships pre-compiled.

The result: smaller APKs, faster installs, and faster cold starts — with no packaging configuration on your side. For the rare "path-hungry" package that insists on reading its data files via `__file__` instead of `importlib.resources`, the new `--android-extract-packages` flag (or `[tool.flet.android].extract_packages`) ships it extracted to disk.

More info:

* PRs: [#6578](https://github.com/flet-dev/flet/pull/6578), [serious-python#223](https://github.com/flet-dev/serious-python/pull/223)
* Migration: [App files unpacked, storage dirs reworked](/docs/updates/breaking-changes/v0-86-0/app-files-unpacked-read-only-bundle), [Compile on by default](/docs/updates/breaking-changes/v0-86-0/compile-on-by-default)

## Faster startup on all platforms

Android wasn't the only platform to get a startup diet — three changes speed up every Flet app:

* **App ships unpacked inside the bundle.** On macOS, iOS, Windows, and Linux your Python sources now live unpacked in the app bundle next to the stdlib and site-packages — the first-launch `app.zip` extraction step is gone entirely.
* **Bytecode compilation is on by default.** `flet build` now compiles your app and its packages to `.pyc`, removing per-launch recompilation. As a bonus, shipping bytecode instead of `.py` sources hides your code from curious eyes. Use `--no-compile-app` / `--no-compile-packages` to opt out.
* **`import flet` is lazy.** The `flet` package used to eagerly execute its full ~270-module public API on import; it now resolves names on first access ([PEP 562](https://peps.python.org/pep-0562/)), so your app loads only what it uses. On a mid-range Android device this cut `import flet` from ~2.0 s to ~0.15 s — reducing total startup time 1.5–2× across all platforms. Type checkers and IDEs are unaffected.

More info:

* PRs: [#6597](https://github.com/flet-dev/flet/pull/6597), [#6598](https://github.com/flet-dev/flet/pull/6598)
* Migration: [Compile on by default](/docs/updates/breaking-changes/v0-86-0/compile-on-by-default)

## Testing framework and `flet test`

Flet apps can finally be tested the way they ship. The new testing framework lets you write **integration tests** that drive your app like a user would — find controls by key or text, tap buttons, enter text, assert the resulting UI, compare screenshots — while the app runs **on the target device** as a built monolithic app with embedded Python.

Tests are plain [pytest](https://docs.pytest.org), so fixtures, parametrization, and `-k` filtering all just work:

```python title="tests/test_main.py"
import flet.testing as ftt


async def test_increment(flet_app: ftt.FletTestApp):
    tester = flet_app.tester
    await tester.pump_and_settle()

    assert (await tester.find_by_text("0")).count == 1

    await tester.tap(await tester.find_by_key("increment"))
    await tester.pump_and_settle()

    assert (await tester.find_by_text("1")).count == 1
```

Run them on the platform of your choice:

```bash
flet test            # current desktop platform
flet test android    # attached Android device or emulator
```

New apps created with `flet create` include a `tests/` folder and pytest configuration out of the box.

More info:

* PR: [#6623](https://github.com/flet-dev/flet/pull/6623)
* Docs: [Integration testing](/docs/getting-started/integration-testing), [`flet test`](/docs/cli/flet-test)

## Flet MCP server

AI coding assistants are great at writing Flet apps — until they hallucinate a control property that doesn't exist. The new **`flet-mcp`** package is an [MCP](https://modelcontextprotocol.io) server that gives LLM agents accurate, version-specific knowledge about Flet: look up the real API, search enum members, find icons, search example projects, and inspect CLI options on demand.

```bash
pip install flet-mcp
```

Then point your AI client (Claude Desktop, Claude Code, Cursor, VS Code, ...) at it:

```json
{
  "mcpServers": {
    "flet": {
      "command": "flet",
      "args": ["mcp"]
    }
  }
}
```

More info:

* PRs: [#6624](https://github.com/flet-dev/flet/pull/6624), [#6654](https://github.com/flet-dev/flet/pull/6654)
* Docs: [Flet MCP server](/docs/cookbook/flet-mcp)

## Multiprocessing in desktop apps

Python `multiprocessing` now works in packaged desktop apps built with `flet build macos` / `windows` / `linux`: `Process`, `ProcessPoolExecutor`, the `spawn` and `forkserver` start methods, and the resource tracker all behave as expected. Previously, each worker process re-executed the app binary itself — launching another GUI instance and hanging.

Made possible by dart-bridge, worker command lines are now detected before Flutter starts and diverted to a headless embedded Python interpreter. Normal multiprocessing rules apply: guard `ft.run(...)` with `if __name__ == "__main__":`, define worker functions at module top level, and don't touch Flet UI objects from workers. Mobile platforms remain unsupported — iOS and Android don't allow apps to spawn child processes.

More info:

* Issue: [#4283](https://github.com/flet-dev/flet/issues/4283), PR: [#6662](https://github.com/flet-dev/flet/pull/6662)
* Docs: [Multiprocessing](/docs/cookbook/multiprocessing)

## Custom boot screen

There's a gap between the native splash screen and your app's first frame — the Flutter engine is up, but Python is still starting. In 0.86 that gap is always covered by a configurable **boot screen**. The built-in one is themable from `pyproject.toml` — background colors, spinner, and stage messages for light and dark modes:

```toml
[tool.flet.boot_screen.flet]
theme_mode = "auto"
spinner_size = 30
startup_message = "Starting up…"
```

If that's not enough, you can replace it entirely with your own Flutter widget shipped as an extension — animated logos, progress art, whatever fits your brand. Startup errors are rendered on the boot screen too, so a failed launch is a readable message instead of a black window.

More info:

* Docs: [Boot screen](/docs/publish#boot-screen), [Custom boot screen](/docs/publish#custom-boot-screen)

## Normalized app storage

App files now ship in a **read-only bundle**, and the writable storage directories were normalized across platforms: `FLET_APP_STORAGE_DATA` maps to the OS application-support directory and is the working directory of your app, `FLET_APP_STORAGE_TEMP` points to the OS temp directory, and the new `FLET_APP_STORAGE_CACHE` exposes the cache directory.

The best part is that development mode now mirrors on-device behavior: `flet run` sets the working directory to a hidden, git-ignored `.flet/storage/data` inside your project — so an app that writes files relative to the current directory behaves the same on your laptop as it will on a phone, and stray output files no longer litter your project root.

More info:

* Migration: [App files unpacked, storage dirs reworked](/docs/updates/breaking-changes/v0-86-0/app-files-unpacked-read-only-bundle)

## Other improvements

* **Swift Package Manager** for iOS and macOS builds, on by default with automatic CocoaPods fallback for non-SPM-ready packages (CocoaPods goes read-only in December 2026).
* New `flet clean` command deletes the app's `build` directory; the `--clear-cache` flag is deprecated ([#6233](https://github.com/flet-dev/flet/issues/6233)).
* Bundled **Flutter bumped to 3.44.2** — built-in Kotlin, Java 17, Gradle 8.14.
* `flet --version --json` emits machine-readable version info for CI ([#6577](https://github.com/flet-dev/flet/pull/6577)).
* Pyodide is no longer pre-baked into the build template — it's downloaded per version and cached under `~/.flet` ([#6577](https://github.com/flet-dev/flet/pull/6577)).
* `compression_quality` for [`FilePicker.pick_files()`](/docs/services/filepicker#flet.FilePicker.pick_files) ([#6573](https://github.com/flet-dev/flet/pull/6573)).
* [`ConsentManager`](/docs/controls/ads/consentmanager) in `flet-ads` for GDPR/EEA consent via Google UMP ([#6615](https://github.com/flet-dev/flet/pull/6615)).
* Stateful controls inside [`ResponsiveRow`](/docs/controls/responsiverow) no longer lose state when a resize crosses a breakpoint ([#6663](https://github.com/flet-dev/flet/pull/6663)).
* `Session.patch_control` mount/unmount scans improved from O(N²) to O(N) ([#6651](https://github.com/flet-dev/flet/pull/6651)).

## Breaking changes

0.86 is a foundational release, and a few changes need attention when upgrading:

* [Default bundled Python is now 3.14](/docs/updates/breaking-changes/v0-86-0/default-bundled-python-3-14) — pin `--python-version 3.12` if your native wheels aren't 3.14-ready yet.
* [App files ship unpacked in a read-only bundle; storage dirs reworked](/docs/updates/breaking-changes/v0-86-0/app-files-unpacked-read-only-bundle) — relative *writes* keep working (cwd is now the data dir); relative *reads* of bundled files should switch to `__file__` or `importlib.resources`.
* [App and packages are compiled to .pyc by default](/docs/updates/breaking-changes/v0-86-0/compile-on-by-default) — pass `--no-compile-app` / `--no-compile-packages` to opt out.
* [Protocol framing upgraded for DataChannel support](/docs/updates/breaking-changes/v0-86-0/data-channel-protocol-upgrade) — pre-0.86 clients and servers can't talk to 0.86 ones.
* [flet.version.pyodide_version removed](/docs/updates/breaking-changes/v0-86-0/removed-pyodide-version-export) and [flet build --clear-cache deprecated](/docs/updates/breaking-changes/v0-86-0/deprecated-clear-cache-flag).

See the full [CHANGELOG](https://github.com/flet-dev/flet/blob/main/CHANGELOG.md#0860) for the complete list of changes and fixes.

## Conclusion

Expo 86 celebrated moving people and messages; Flet 0.86 celebrates moving bytes and apps. With sockets replaced by an in-process bridge, packaging rebuilt around zero-extraction and pre-compiled bytecode, a real testing story, and any-version Python on every platform, this release closes out the foundational work we wanted done before 1.0. From here, the road to 1.0 is about polish — not plumbing.

Try it in your apps and share feedback in [GitHub Discussions](https://github.com/flet-dev/flet/discussions) or on [Discord](https://discord.gg/dzWXP8SHG8).

Happy Flet-ing!
