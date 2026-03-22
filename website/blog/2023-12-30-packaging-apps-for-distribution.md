---
slug: packaging-apps-for-distribution
title: Packaging apps for distribution
authors: feodor
tags: [releases]
---

Dear friends! In the final post of this year I would like to thank you all for your contributions
to Flet project whether it's spreading a word, submitting pull request, joining Discord discussion or a even sending an annoying bug report!

<!-- truncate -->

With your fantastic support we achieved a lot in year 2023:

* 70+ controls (special thanks to [@ndonkoHenri](https://github.com/ndonkoHenri) for his tremendous contribution).
* 7,700 stars on GitHub.
* 2,150 users with community moderators (thank you guys!) on Discord.
* Flet integration with Pyodide for pure client-side Python apps - no other frameworks provide a better UI for Pyodide!
* Flet app in AppStore and Google Play - great way to test on mobile devices and real proof of Flet apps being accepted in stores.
* ...and finally... drum roll...🥁🥁🥁 `flet build` command is here! 🎉🎉🎉

🎄 "New Year" 🎄 edition of Flet 0.18.0 has been just released which allows packaging
your Flet apps for distribution on all platforms: iOS, Android, Web, macOS, Windows and Linux!

**The one command to rule them all!**

The full circle is now closed: you can create (`flet create`), run (`flet run`) and build (`flet build`) your Flet apps with Flet CLI.

Flet CLI provides `flet build` command that allows packaging Flet app into a standalone executable or install package for distribution.

`flet build` command supersedes both [`flet pack`](https://docs.flet.dev/cookbook/packaging-desktop-app/) (packaging into desktop app) and [`flet publish`](https://docs.flet.dev/publish/web/static-website/) (packaging into a static website) commands and allows converting your Flet app into Android or iOS bundle, desktop app and a static website.

For building desktop apps `flet build` does not longer rely on PyInstaller like `flet pack` does, but uses Flutter SDK to produce a fast, offline, fully customizable (your own icons, about dialog and metadata) executable for Windows, Linux and macOS with Python runtime embedded into executable and running in-process.

Static websites built with `flet build`, compared to `flet publish`, have faster load time as all Python dependencies are now packaged into a single archive instead of being pulled in runtime with `micropip`. `flet build web` also detects native Python [packages built into Pyodide](https://pyodide.org/en/stable/usage/packages-in-pyodide.html), such as `bcrypt`, `html5lib`, `numpy` and many others, and installs them from Pyodide package registry.

Check [Packaging app for distribution](https://docs.flet.dev/publish/) guide for complete information about `flet build` command.

Let us know what you think by joining [Flet Discord server](https://discord.gg/dzWXP8SHG8) or creating a new thread on [Flet GitHub discussions](https://github.com/flet-dev/flet/discussions).

We wish you Happy New Year! Enjoy your holidays!