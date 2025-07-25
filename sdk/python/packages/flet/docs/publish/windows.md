---
title: Packaging app for Windows
---

Instructions for packaging a Flet app into a Windows application.

**See complementary information [here](index.md).**

## Prerequisites

### Visual Studio 2022

[Visual Studio 2022](https://learn.microsoft.com/visualstudio/install/install-visual-studio?view=vs-2022) is required 
with **Desktop development with C++** workload installed.

Follow this [guide](https://medium.com/@teamcode20233/a-guide-to-install-desktop-development-with-c-workload-542bb92cfe90) 
for instructions on downloading & installing correct Visual Studio components for Flutter desktop development.

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

you need to enable Developer Mode as it indicates.
Follow this [guide](https://stackoverflow.com/a/70994092/1435891) on how to do that.
