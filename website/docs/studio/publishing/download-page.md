---
title: "Download page"
---

# Download page

Every app gets one public download page: a link like `get.flet.app/…` with the app's
icon, version and "What's new", a download for each platform, install steps, and a QR
code on computers. Each visitor sees their own system's download first (**Download
APK**, **Download for Windows**, **Download for Mac**…), with the others listed under
it and who signed each one.

The link stays the same across updates: share it once (on your website, in an email,
as a QR code on a flyer) and each new version replaces the app behind it. It exists
from the start, before anything is published, so you can share it early: until a build
is on the page, visitors see "Nothing to download yet".

Manage it under **Publish › Download page** in the app's sidebar. **All platforms**
shows its link and which platforms are live on it, and each platform's card has a
**Download page** line with **Manage**.

{/* SCREENSHOT: /img/docs/studio/publishing/download-page.png — the public download page on a phone */}

## Put a build on it

A platform's build form has a **Download page** box:

- **Android:** **Create APK** on the **Android app (APK)** card, with **Add this APK to
  the download page**, ticked by default. See [Android apps](android.md#download-page).
- **Windows, macOS, Linux:** **Create Windows app**, **Create Mac app** or **Create Linux
  app**, with **Add this installer** (or disk image, or app) **to the download page**.
  It's ticked once the page has a release, or when you start the build from **Publish ›
  Download page**. See [Desktop apps](desktop.md#download-page).

Once the page has that platform's build, the box reads **Replace the … download with
this …** and says which version is on the page now. Untick it for a build just to try
yourself: the page keeps what it has.

A build that's already made can go on without building again, and without credits:

- **Add to page…** on the platform's row in **Publish › Download page** (pick the
  version; the newest is selected), or **Add to page** on the card's **Download page**
  line.
- A platform with nothing to add yet has its next step on the row instead: **Create
  APK**, **Create Windows app**, …, or **Set up signing** (below).

## What can go on it

| Platform | What goes on the page |
|---|---|
| Android | The APK, signed with the app's [signing key](android.md#signing-key) |
| Windows | The installer, [signed with Azure Artifact Signing](desktop.md#sign-the-windows-app) |
| macOS | The disk image, [signed with Developer ID and notarized](desktop.md#sign-and-notarize-the-mac-app) |
| Linux | The `.tar.gz`, next to a signed Windows or Mac build ([why](#why-linux-needs-a-signed-windows-or-mac-build)) |

iOS and web apps don't go on the page: iOS builds install from their own
[install links](ios.md#install-links), and a web app is hosted.

An unsigned Windows or Mac build can't go on the page, including one made with **Skip
signing for this run**. The platform's row says **Needs a signed build** (Mac: **Needs a
signed, notarized build**) with **Set up signing**.

### Why Linux needs a signed Windows or Mac build

Your download page lives on Flet's domain (`get.flet.app`), so people trust that a file
there comes from a real, accountable developer. Windows and Mac builds prove it: they're
signed with a certificate Microsoft or Apple issued after checking who you are, and the
page shows the name they verified.

Linux apps have no signing like that, so a Linux file on its own says nothing about who
made it. Without a rule, the page would let anyone host an anonymous program on Flet's
domain, which is how malware spreads. So a Linux build goes on the page only next to a
signed Windows or Mac build of the same app: visitors see the verified publisher, and the
Linux download comes from the same developer.

If you take the last signed Windows or Mac build off the page, the Linux one comes off with
it. To share a Linux build without that, download it from its run (**Download .tar.gz**
on the **Linux app** card) and host it yourself.

## Update it

**Create new version** on a platform's card builds the app as it is now and replaces
that platform's download on the page. The other platforms stay as they are. Android
users install the new APK over the one they have and keep their data.

**Publish › Download page** lists each platform with the version on the page and until
when it stays up. On a platform's row:

- **Update to …** puts a newer build on the page that isn't there yet.
- **Change version…** lists the builds that can still go on the page, newest first, and
  puts the one you pick back on it as it was, with no new build. Use it to go back after
  a bad release.
- **Remove** takes that platform off the page; the others stay.

## Share the link

The link is at the top of **Publish › Download page**, with **Open**, **Copy**, **QR
code** and **Share**. Each platform's card shows it too while its build is on the page.

| | Explorer | Creator |
|---|---|---|
| Link | Unlisted: `get.flet.app/` and a random code | The unlisted link, plus a custom address: `get.flet.app/your-app` |
| How long a release stays up | 7 days after its build: publish a new version to keep the app up | 1 year after its build: a new version starts the year again |
| Run downloads in Studio | 7 days | 90 days |

Each release's own date is on its row.

## Page settings

**Page settings** at the bottom of **Publish › Download page**:

- **Custom address** (Creator): your own name in the link, `get.flet.app/your-app`.
  Click ✎, type lowercase letters, digits and hyphens (up to 40), then ✓. If you change
  it, the old name keeps redirecting for 30 days. The unlisted link keeps working too.
- **Unlisted link**: the link with the random code, with **Open**, **Copy**, **QR code**
  and **Share**. **Replace…** gives the page a new one; the old one stops working at
  once, and a custom address keeps working. Use it if the link reached people it
  shouldn't have.
- **Take page offline**: every platform's build comes off the page; your build files are
  kept. The link keeps working and shows "Nothing to download yet" until you put a build
  back.

## What your users see

The page offers the visitor's system first, with the others under it:

- **Android:** **Download APK** and the steps to install. Android asks them to allow
  their browser to install unknown apps the first time. Installing a newer version later
  keeps their data, because every update is signed with the same key.
- **Windows:** the installer, with the publisher Microsoft verified.
- **macOS:** the disk image, notarized by Apple: open it and drag the app to
  Applications.
- **Linux:** the `.tar.gz` to unpack and run.

Each page has a **Report this app** link. Flet reviews reports and can take a page
down; you'll see that in Studio.
