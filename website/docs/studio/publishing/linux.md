---
title: "Linux"
---

# Linux

Open **Publish › Linux**. The **Linux app** card's **Create Linux app** builds a
`.tar.gz` with the app's folder and its executable.

When the run finishes, the card shows the build with **Download**. **Create new
version** builds the app as it is now. Downloads are kept for a while (see
[Downloads expire](index.md#downloads-expire)); after that the card says **Download
expired** and **Create new version** builds it again.

The app's settings (its name, icon, version, …) are on the **Settings** tab, with the
defaults in **All platforms › Settings**.

## Open the app

1. Extract the download: `tar -xzf <app>.tar.gz`.
2. Run the executable in the extracted folder, e.g. `./<app>/<app>`. Keep the folder
   together: the executable needs the `lib` and `data` folders next to it.

The app needs GTK 3, which desktop Linux distributions include. On a minimal system,
install it first (`sudo apt install libgtk-3-0` on Debian and Ubuntu).

Linux apps aren't code-signed: Linux has no system-wide signing for apps like Windows
and macOS do.

## Download page

Your Linux build can go on the app's [download page](download-page.md), the same page
and link as its Android APK and Windows and Mac builds.

- **Add this app to the download page** on **Create Linux app** publishes the build when
  it's done (**Replace the Linux download with this app** once the page has one). It's
  ticked by default once the page has a release, or when you start the build from
  **Publish › Download page**.
- A Linux build goes on next to a signed [Windows](windows.md#sign-the-windows-app) or
  [Mac](macos.md#sign-and-notarize-the-mac-app) one
  ([why](download-page.md#why-linux-needs-a-signed-windows-or-mac-build)).

Adding an existing build, changing the version, the link and the page's settings are on
[Download page](download-page.md).
