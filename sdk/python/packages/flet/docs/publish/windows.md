---
title: Packaging app for Windows
---

Flet CLI provides `flet build windows` command that allows packaging Flet app into a Windows application.

::note
The command can be run on Windows only.
::

## Prerequisites

### Visual Studio 2022

Building Flet app for Windows desktop requires [Visual Studio 2022](https://learn.microsoft.com/visualstudio/install/install-visual-studio?view=vs-2022) with **Desktop development with C++** workload installed.

[Follow this medium article](https://medium.com/@teamcode20233/a-guide-to-install-desktop-development-with-c-workload-542bb92cfe90) for the instructions on downloading & installing correct Visual Studio components for Flutter desktop development.

### Enable Developer Mode

While running `flet build` on Windows you may get the following error:

```
Building with plugins requires symlink support.

Please enable Developer Mode in your system settings. Run
  start ms-settings:developers
to open settings.
```

[Follow this SO answer](https://stackoverflow.com/a/70994092/1435891) for the instructions on how to enable developer mode in Windows 11.

## `flet build windows`

Creates a Windows application from your Flet app.