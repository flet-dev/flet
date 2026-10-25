---
title: "Publishing overview"
---

# Publishing your app

Flet Studio builds your app for Windows, macOS, Linux, Android, iOS and the web in
the cloud, and can deliver it to an app store — no Flutter, Xcode or Android SDK to
install. Open it with the **Publish** button in the app bar.

{/* SCREENSHOT: /img/docs/studio/publishing/overview.png — Publish › Overview with the Android section and its outputs */}

## Publish at a glance

**Publish** has three tabs:

- **Overview**: one section per platform with its actions, and under them what each
  action produced last — with **Download**, or where a store has it.
- **Activity**: every run of the app, newest first, with its status. Open one for
  its details.
- **Settings**: the app's build settings — shared ones, plus a scope per platform.

## Actions

Each action is one **run** for one platform:

| Platform | Actions |
|---|---|
| Windows | **Create Windows app (.zip)** |
| macOS | **Create macOS app (.app)** — not signed or notarized: for testing on your own Mac |
| Linux | **Create Linux app (.tar.gz)** |
| Android | **Create an APK**, **Publish to a download page**, **Create an app bundle (.aab)**, **Publish to Google Play**, **Update store listing** — see [Android apps](android.md), [the download page](android.md#download-page), [Google Play](google-play/index.md) and [the store listing](google-play/store-listing.md) |
| iOS | **Create an iOS Simulator app** (no Apple account needed), **Create an iOS app (.ipa)**, **Publish to TestFlight** — see [iOS apps](ios.md) |
| Web | **Create web app (.zip)** — the files to host yourself |

Microsoft Store, Mac App Store, App Store and publishing a website show **Coming soon**.

## Start a run

Click an action to open its screen:

- **The settings it needs**, such as the app's name and package name, open at the
  top; the rest of the platform's settings are further down. Changes are saved to
  the app as you make them.
- **Version and build** for this run.
- Anything to set up first, such as a [signing key](signing-keys-and-store-accounts.md),
  shown in red at the bottom until it's done.
- The **estimated credits** and your balance.

Then click the action's button. The run's details open and follow it live.

### Version and build number

- **Version** (e.g. `1.2.0`) is prefilled from your app's `pyproject.toml`. If you
  change it, the new version is saved to `pyproject.toml` when the run starts.
- **Build number** is one counter for the whole app, shared by all platforms, and
  Studio assigns the next one to each run. It's what stores use to tell builds
  apart (Google Play's *version code*, Apple's *build*). You can override it for
  one run with the pencil, but never below the next automatic number. Publishing to
  Google Play starts it above the highest one Google Play already has.

## Credits

Builds run on cloud machines and use **credits**, the same balance as the AI agent.
The action screen shows an estimate before you start, from how long your app's
earlier builds took. You're charged for the time the build actually takes, with a
per-run minimum. Uploading to a store afterwards is free.

Runs that fail because of Studio's build machines rather than your app — a machine
that didn't start or stopped answering — aren't charged. See **Settings › Plan &
usage** for your balance, plans and credit packs.

## Build settings

Your app's build settings live in its `pyproject.toml`, under `[project]` and
`[tool.flet]` — the same file `flet build` reads. **Publish › Settings** edits them:

- **Shared** settings apply to every platform: name, version, description, icon,
  splash screen, and more.
- **Each platform's** scope adds its own settings (Android's SDK versions and
  permissions, iOS's bundle ID, ...) and can **override** a shared one for that
  platform only.

Changes there are written to `pyproject.toml`, and edits you (or the agent) make to
the file show up there. See
[Publishing a Flet app](../../publish/index.md) for every setting.

Signing keys and store accounts are never stored in your app's files. See
[Signing keys and store accounts](signing-keys-and-store-accounts.md).

## Run details

Open a run from Overview or Activity:

- **Status**, cost, version and duration. A run can be canceled while it waits or
  builds.
- **Artifacts**: the files it produced, to download.
- **Errors and warnings**, each linked to the step it came from.
- **Steps**: what the build did, each with its own log. Times are shown in your
  local time. **Download log** saves the whole log as a text file, with the steps'
  titles as headers and times in UTC.

{/* SCREENSHOT: /img/docs/studio/publishing/run-details.png — run details with steps expanded */}

### Downloads expire

Studio keeps a run's files for **7 days** on the Explorer plan and **90 days** on
Creator, and at most the last three successful runs of each action. After that,
Overview says **Download expired** — start a new run to get the files again.
What's on a store stays there, and so does the app on its
[download page](android.md#download-page) while it's up.

### Queued runs

Runs wait in a queue when all build machines for a platform are busy, or when your
plan's limit of runs at a time is reached. A run that waits more than an hour is
canceled without charge.

## When a build fails

The run's **Errors and warnings** point at the step that failed: open it for its
log. Common causes are code that fails when the app is packaged (it runs before the
first screen), a dependency that has no build for the platform, or a setting the
platform rejects.

The **AI agent** can help: ask it why the build failed. It reads the run's steps,
errors and log, fixes what's in your app (code, dependencies, settings), and tells
you to start the run again.

## Questions

### Does a build work the same as the preview?

Not always. The preview runs your app in the browser with Pyodide, so it can only
use pure-Python packages and those built for Pyodide. A build packages your app with
real Python for the platform: packages with native code work there if they have a
build for it — see
[Python packages built in Flet](../../reference/binary-packages-android-ios.md) for
Android and iOS.

### Can I build on my own computer instead?

Yes. Download the app with **Download app as .zip file** in the app bar, then use
[`flet build`](../../publish/index.md). It reads the same `pyproject.toml`
settings.
