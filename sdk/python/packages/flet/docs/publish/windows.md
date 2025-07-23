---
title: Packaging app for Windows
---

Flet CLI provides `flet build windows` command that allows packaging Flet app into a Windows application.

/// admonition | Note
The command can be run on Windows only.
///

/// admonition | Important
    type: danger
## Prerequisites

### Visual Studio 2022

Building Flet app for Windows desktop requires [Visual Studio 2022](https://learn.microsoft.com/visualstudio/install/install-visual-studio?view=vs-2022) with
**Desktop development with C++** workload installed.

Follow this [guide](https://medium.com/@teamcode20233/a-guide-to-install-desktop-development-with-c-workload-542bb92cfe90) for the instructions on downloading & installing correct
Visual Studio components for Flutter desktop development.
///

## `flet build windows`

Creates a Windows application from your Flet app.

## Troubleshooting

### Developer mode

If you get the below error:

```
Building with plugins requires symlink support.

Please enable Developer Mode in your system settings. Run
  start ms-settings:developers
to open settings.
```

you need to enable Developer Mode as indicated.
Follow this [guide](https://stackoverflow.com/a/70994092/1435891) on how to do that.
