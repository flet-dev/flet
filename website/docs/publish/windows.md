---
title: "Packaging app for Windows"
---

Instructions for packaging a Flet app into a Windows application.

:::tip[Info]
This guide provides detailed Windows-specific information.
Complementary and more general information is available [here](index.md).
:::

:::info[Alternative: flet pack]
For a PyInstaller-based way to package desktop apps — no Visual
Studio or Flutter toolchain required — see [`flet pack`](using-pyinstaller.md).
:::

## Prerequisites

### Visual Studio

Visual Studio ([2022](https://learn.microsoft.com/en-us/visualstudio/install/install-visual-studio?view=vs-2022)
or [2026](https://learn.microsoft.com/en-us/visualstudio/install/install-visual-studio?view=visualstudio))
is required with the **Desktop development with C++** workload installed.

Follow this [guide](https://medium.com/@teamcode20233/a-guide-to-install-desktop-development-with-c-workload-542bb92cfe90)
for instructions on downloading and installing correct Visual Studio
components for Flutter desktop development.

## `flet build windows`

:::note[Note]
This command can be run on **Windows only**.
:::

Builds a Windows application.

## Troubleshooting

| Symptom                                           | Cause and fix                                                                                                                                                    |
|---------------------------------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `Building with plugins requires symlink support`  | Windows **Developer Mode** is off — run `start ms-settings:developers`, enable it (see [this guide](https://stackoverflow.com/a/70994092/1435891)), and rebuild. |
| `Unable to find suitable Visual Studio toolchain` | The **Desktop development with C++** workload is missing — install it with the Visual Studio Installer (see [Prerequisites](#visual-studio)).                    |
