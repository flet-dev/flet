---
slug: packaging-desktop-apps-with-custom-icon
title: Packaging desktop apps with a custom icon
authors: feodor
tags: [releases]
---

Happy New Year! [Flet project](https://github.com/flet-dev/flet) has reached ⭐️ 3.3K stars ⭐️ on GitHub which is very exciting and encouraging! Thank you all for your support!

We are starting this year with the release of [Flet 0.3.2](https://pypi.org/project/flet/) bringing a long-awaited feature: creating standalone desktop bundles with a custom icon!

`flet` command has been used for running Flet program with [hot reload](https://docs.flet.dev/cli/flet-run/), but we recently re-worked Flet CLI to support multiple actions.

There is a new `flet pack` command that wraps [PyInstaller](https://github.com/pyinstaller/pyinstaller) API to package your Flet Python app into a standalone Windows executable or macOS app bundle which can be run by a user with no Python installed.

Command's `--icon` argument is now changing not only executable's icon, but Flet's app window icon and the icon shown in macOS dock, Windows taskbar, macOS "About" dialog, Task Manager and Activity Monitor:

<img src="/img/docs/getting-started/package-desktop/macos-dock.png" className="screenshot-20 screenshot-rounded" />

Bundle name, version and copyright can be changed too:

<img src="/img/docs/getting-started/package-desktop/flet-app-bundle-about-clean.png" className="screenshot-50" />

Find all available options for packaging desktop apps in the [updated guide](https://docs.flet.dev/publish/).

Upgrade Flet module to the latest version (`pip install flet --upgrade`), give `flet pack` command a try and [let us know](https://discord.gg/dzWXP8SHG8) what you think!