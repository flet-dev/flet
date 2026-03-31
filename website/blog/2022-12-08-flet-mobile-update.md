---
slug: flet-mobile-update
title: Flet mobile update
authors: feodor
tags: [news]
---

This post is a continuation of [Flet mobile strategy](/blog/flet-mobile-strategy) published a few months ago.

Our original approach to Flet running on a mobile device was Server-Driven UI. Though SDUI has its own benefits (like bypassing App Store for app updates) it doesn't work in all cases, requires web server to host Python part of the app and, as a result, adds latency which is not great for user actions requiring nearly instance UI response, like drawing apps.

I've been thinking on how to make Python runtime embedded into Flutter iOS or Android app to run user Python program. No doubt, it's technically possible as Kivy and BeeWare projects do that already.

<!-- truncate -->

## Current Flet architecture

The current architecture of Flet desktop app is shown on the diagram below:

<img src="/img/blog/mobile-update/flet-desktop-architecture.svg" className="screenshot-100" />

Running Flet program on a desktop involves three applications (processes) working together:

* **Python runtime** (`python3`) - Python interpreter running your Python script. This is what you are starting from a command line. Python starts Fletd server and connects to it via WebSockets.
* **Fletd server** (`fletd`)- Flet web server written in Go, listening on a TCP port. Fletd holds the state of all user sessions (for desktop app there is only one session) and dispatches page updates and user generated events between Python program and Flet client.
* **Flet client** (`flet`) - desktop app written in Flutter and displaying UI in a native OS window. Flet client connects to Fletd server via WebSockets.

The architecture above works well for Flet web apps where web server is essential part, but for desktop it seems redundant:

* If all three processes run on the same computer WebSockets could be replaced with sockets or named pipes with less overhead.
* Fletd server has no much sense as there is only one user session and UI state is persistently stored in Flet desktop client which is never "reloaded".

## Flet new desktop architecture

Flet desktop app architecture can be simplified by replacing Fletd with a "stub" written in Python and communicating with Flet desktop client via sockets (Windows) and named pipes (macOS and Linux):

<img src="/img/blog/mobile-update/flet-desktop-architecture-v2.svg" className="screenshot-70" />

## Flet mobile architecture

Mobile applications are running in a very strict context with a number of limitations. For example, on iOS the app cannot spawn a new processes. Other words, Flet Flutter app cannot just start "python.exe" and pass your script as an argument.

Luckily for us, [Python can be embedded](https://docs.python.org/3/extending/embedding.html) into another app as a C library and Dart (the language in which Flutter apps are written) allows calling C libraries via [FFI](https://dart.dev/guides/libraries/c-interop) (Foreign Function Interface).

Additionally, while Android allows loading of dynamically linked libraries iOS requires all libraries statically linked into app executable. [This article](https://blog.logrocket.com/dart-ffi-native-libraries-flutter/) covers Dart FFI in more details, if you are curious.

Flet mobile architecture could look like this:

<img src="/img/blog/mobile-update/flet-mobile-architecture-v2.svg" className="screenshot-40" />

Python runtime will be statically or dynamically linked with Flutter client app and called via FFI and/or named pipes.

Running Python on mobile will have some limitations though. Most notable one is the requirement to use "pure" Python modules or modules with native code compiled specifically for mobile ARM64 architecture.

## Asyncio support

[Asyncio](https://docs.python.org/3/library/asyncio.html) is part of Python 3 and we start seeing more and more libraries catching up with async/await programming model which is more effective for I/O-bound and UI logic.

Currently, Flet is spawning all UI event handlers in new threads and it's also a pain to see `threading.sleep()` calls hogging threads here and there just to do some UI animation. All that looks expensive.

Using of async libraries from a sync code is [possible](https://github.com/flet-dev/flet/issues/128), but looks hacky and inefficient as it keeps CPU busy just to wait async method to finish. So, we want a first-class support of async code in Flet app.

Async/await model is a state machine switching between tasks in a single thread. By going async Flet will able to utilize [streams](https://docs.python.org/3/library/asyncio-stream.html) for socket server and use async [WebSockets library](https://pypi.org/project/websockets/) library. It will be possible to use both sync and async event handlers in a single Flet app without any compromises or hacks.

Even more exciting, async Flet will be able to run entirely in the browser within [Pyodide](https://pyodide.org/) - Python distribution based on WebAssembly (WASM). WebAssembly doesn't have multi-threading support yet, so running in a single thread is a must. Just imagine, Flet web app with a truly offline Flet PWA that does not require a web server to run a Python code!

## Development plan

We are going to crunch the scope above in a few iterations:

1. Async API support with async WebSockets library. Works with the same Fletd in Go.
2. Fletd server ("stub") in Python to use with a desktop.
3. Embedding Python with Fletd "stub" and user program into iOS.
4. Embedding Python into Android.
5. Packaging mobile apps for iOS and Android.

:::caution HELP WANTED
🙏 I'm looking for a help from the community with developing C/C++/native code integration part between Flutter and Python on iOS and Android. It could be either free help or a paid job - let me know if you are interested!
:::

Hop to [Discord](https://discord.gg/dzWXP8SHG8) to discuss the plan, offer help, ask questions!