---
title: "Desktop apps (Windows, macOS, Linux)"
---

# Desktop apps: Windows, macOS and Linux

Open **Publish › Windows**, **macOS** or **Linux**. Each has one card with the app,
packaged for that system:

| Platform | Card | What you get |
|---|---|---|
| Windows | **Create Windows app** | An installer (`setup.exe`), and a portable `.zip` with the app's folder and its `.exe` |
| macOS | **Create macOS app** | The `.app`, zipped |
| Linux | **Create Linux app** | A `.tar.gz` with the app's folder and its executable |

When the run finishes, the card shows the build with **Download** (on Windows,
**Download › Installer** or **Portable**). **Update** builds
the app as it is now. Downloads are kept for a while (see
[Downloads expire](index.md#downloads-expire)); after that the card says **Download
expired** and **Update** builds it again.

The settings for each platform (the app's name, icon, version, …) are on its
**Settings** tab, with the defaults in **All platforms › Settings**.

{/* SCREENSHOT: /img/docs/studio/publishing/windows-card.png — Publish › Windows with the built app */}

## Open the app

Studio's desktop apps aren't signed with a code-signing certificate yet, so the system
asks before opening them the first time.

### Windows

**Download › Installer (setup.exe)** is what to give your users:

1. Run the `setup.exe`.
2. If **Windows protected your PC** (SmartScreen) appears, click **More info ›
   Run anyway**.

That's it: Setup asks nothing, installs the app for the current user in a few seconds
(no administrator rights needed) and opens it. The app is then in the Start menu, and
in **Settings › Apps** to uninstall it. To install it for every user of the PC instead,
run `setup.exe /ALLUSERS` from an administrator's command prompt. Running
the `setup.exe` of a newer build upgrades it in place, keeping the app's data, as
long as the app's [bundle ID](../../publish/index.md#bundle-id) stays the same: Setup
finds the installed app by it. Running the `setup.exe` of the build that's installed,
or of an older one, just opens the installed app: to go back to an older build,
uninstall the app first.

**Download › Portable (.zip)** runs without installing, e.g. from a USB stick or on a
PC where you can't install apps:

1. Unzip the download (**right-click › Extract All…**). Keep the folder together: the
   `.exe` needs the files next to it.
2. Run the app's `.exe`, and confirm SmartScreen as above.

Keep the app's **company name** and **product name** the same between releases, too:
the app keeps its data in a folder named after them.

### macOS

1. Unzip the download (double-click it) and move the `.app` to **Applications** if you
   like.
2. Open it. macOS says it can't verify the app, because it isn't notarized by Apple.
   Click **Done** (not **Move to Trash**).
3. Open **System Settings › Privacy & Security**, scroll to the message about the app,
   and click **Open Anyway**, then confirm with your password. macOS remembers it for
   that app.

On macOS 14 and earlier, **right-click the app › Open** and confirm instead.

### Linux

1. Extract the download: `tar -xzf <app>.tar.gz`.
2. Run the executable in the extracted folder, e.g. `./<app>/<app>`. Keep the folder
   together: the executable needs the `lib` and `data` folders next to it.

The app needs GTK 3, which desktop Linux distributions include. On a minimal system,
install it first (`sudo apt install libgtk-3-0` on Debian and Ubuntu).

## Questions

### Can I put the app on the Microsoft Store or the Mac App Store?

Not from Studio yet. Download the app as a `.zip` from the app bar and build it on your
own computer with [`flet build`](../../publish/index.md), which can make store-ready,
signed packages.

### Can the Windows installer be signed?

Not yet. Until it is, SmartScreen asks before running it, as above.
