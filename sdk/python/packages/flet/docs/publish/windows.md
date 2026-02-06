---
title: Packaging app for Windows
---

Instructions for packaging a Flet app into a Windows application.

/// admonition | Info
    type: tip
This guide provides detailed Windows-specific information.
Complementary and more general information is available [here](index.md).
///

## Prerequisites

### Visual Studio

Visual Studio ([2022](https://learn.microsoft.com/en-us/visualstudio/install/install-visual-studio?view=vs-2022)
or [2026](https://learn.microsoft.com/en-us/visualstudio/install/install-visual-studio?view=visualstudio))
is required with the **Desktop development with C++** workload installed.

Follow this [guide](https://medium.com/@teamcode20233/a-guide-to-install-desktop-development-with-c-workload-542bb92cfe90)
for instructions on downloading and installing correct Visual Studio
components for Flutter desktop development.

## `flet build windows`

/// admonition | Note
This command can be run on **Windows only**.
///

Builds a Windows application.

## Troubleshooting

### Developer mode

If you get the below error:

```
Building with plugins requires symlink support.

Please enable Developer Mode in your system settings. Run
  start ms-settings:developers
to open settings.
```

Then, you need to enable Developer Mode as it indicates.
Follow this [guide](https://stackoverflow.com/a/70994092/1435891) on how to do that.
