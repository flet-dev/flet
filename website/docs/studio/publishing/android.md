---
title: "Android apps (APK and app bundle)"
---

# Android apps: APK and app bundle

The Android section of **Publish** has three actions:

| Action | What you get | For |
|---|---|---|
| **Create an APK** | An `.apk` file | Installing directly on a phone or tablet |
| **Create an app bundle (.aab)** | A signed `.aab` file | Uploading to Google Play yourself, e.g. an app's first release |
| **Publish to Google Play** | A release on a Google Play track | See [Publishing to Google Play](google-play/index.md) |

All three use the app's **Android signing key** when one is selected — the same key
for APKs and app bundles.

## Create an APK

Run **Create an APK** and **Download** the `.apk` when the run finishes.

To install it, open the file on the phone (download it there, or copy it over).
Android asks you to allow installing apps from that source — the browser or the
Files app — the first time: **Settings › Apps › Special app access › Install
unknown apps** if you need to change it later.

The APK is built for **Most phones** (`arm64-v8a`) unless you pick **All devices**
in the action screen's **Architectures** section — see
[Why is my APK so big?](#why-is-my-apk-so-big).

### Test-signed APKs

Without a signing key, the APK is signed with a **test key** and the run says so.
That's fine for trying the app, but Android only installs an update over an app
signed with the same key: a later APK signed with a different key (yours, or
another test key) won't install over it, and you have to uninstall the old one
first — which deletes the app's data on the phone.

Select a signing key as soon as you plan to keep the app installed: later APKs then
install over earlier ones as updates.

### Install over an earlier build

An APK installs over the copy on the phone when it's signed with the same key and
its **build number** isn't lower. Studio's build numbers always go up, so a newer run
installs over an older one.

### Share an APK outside Google Play

Android devices are starting to require that apps come from **registered
developers** — including apps installed from a website, an email or another
store. Google enforces it from September 30, 2026 in Brazil, Indonesia, Singapore
and Thailand, and on certified Android devices everywhere from 2027. An APK from a
developer who isn't registered can still be installed, but only through Android's
extra "advanced" install steps.

Apps you publish on Google Play are registered automatically. To share an APK
outside Google Play, register it with Google:

1. **Sign up and verify your identity** in the
   [Android Developer Console](https://android.google.com/developerconsole) — or,
   if the app is also on Google Play, in Play Console. Individuals need a photo ID
   and proof of address; organizations also a D-U-N-S number and a verified
   website.
2. **Register the app's package name and its signing key.** Studio shows both on
   **Create an APK**, with copy buttons: the package name as Android builds get it,
   and your signing key's SHA-256 fingerprint (also in **Settings › Signing keys ›
   ⋯ › Copy SHA-256 fingerprint**).
3. If the package name was already used by an app on devices, Google may ask you to
   **prove you hold the key**: an APK signed with it that contains a token Google
   gives you. Studio can't make that file yet — tell us if you need it.

Register an APK signed with **your own key**: a test-signed APK (made without a
key) can't be registered, and once registered, keep using the same key — Google
ties the app to it.

To share the app with a few testers only, **limited distribution** needs no
identity verification: up to 20 devices, through invitations.

See Google's [developer verification guides](https://developer.android.com/developer-verification/guides)
for the details.

To give people a link to download the app, use a [download page](#download-page).

## Download page

**Publish to a download page** builds a signed APK and puts it on a page your users
can open: a link like `get.flet.app/…`, with a **Download APK** button, the app's
icon, version and "What's new", install steps, and a QR code on computers.
The link stays the same across releases: share it once — on your website, in an
email, as a QR code on a flyer — and each publish replaces the app behind it.

{/* SCREENSHOT: /img/docs/studio/publishing/download-page.png — the public download page on a phone */}

The action needs your own [signing key](#signing-key), so updates install over
earlier versions. Register the app with Google too: see
[Share an APK outside Google Play](#share-an-apk-outside-google-play).

### Publish

1. Open **Publish › Android › Publish to a download page**.
2. Select a signing key, and optionally write **What's new**.
3. Click **Publish to a download page**. When the run finishes, the app is on the
   page.

Already made a signed APK with **Create an APK**? Open that run and click
**Publish to the download page** — no new build, no credits. The same button on
an earlier download page run puts that version back (a rollback).

### Share the link

The **Download page** section of the action screen, and the **Download page** row
in **Overview**, have the link with **Copy link**, **QR code** and **Open**.

| | Explorer | Creator |
|---|---|---|
| Link | Private: `get.flet.app/` and a random code | The private link, plus a readable one: `get.flet.app/your-app` |
| How long a release stays up | 7 days after its build: publish again to keep the app up | While it's the current release |
| Run downloads in Studio | 7 days | 90 days |

Set a readable link under **Readable link**: lowercase letters, digits and hyphens.
If you rename it, the old name keeps redirecting for 30 days.

### New link, take offline

In the **Download page** section's **⋯** menu:

- **Create a new link** — the current private link stops working at once. Use it
  if a link reached people it shouldn't have.
- **Take offline** — the page stops offering the app until you publish again.

### What your users see

The page shows the **Download APK** button and the steps to install: Android asks
them to allow their browser to install unknown apps the first time. Installing a
newer version later keeps their data — as long as you keep the same signing key.

Each page has a **Report this app** link. Flet reviews reports and can take a page
down; you'll see that in Studio.

## Create an app bundle (.aab)

An app bundle is what Google Play takes: Google builds the APKs for each device
from it. Studio always signs a bundle with the app's key, so the action needs one
selected.

Use **Create an app bundle (.aab)** to upload a release to Google Play yourself —
mainly an app's **first release**, which Google requires to be uploaded in Play
Console. After that, [Publish to Google Play](google-play/index.md) uploads for you.

A phone can't install an `.aab` directly.

## Signing key

A signing key proves your app's updates come from you. Select one in the
action screen's **Signing** section, in **Publish › Settings › Android › Signing &
accounts**, or manage your keys in **Settings › Signing keys**. Keys are saved to
your Studio account, so your other apps can use them too.

{/* SCREENSHOT: /img/docs/studio/publishing/signing-section.png — the action screen's Signing section with a key selected */}

### Create a key

**Add signing key › Create a new key** makes an upload key (RSA 2048, valid for
over 27 years, alias `upload`). The name is filled in as "*app name* upload key";
change it if you like.

### Back up your key

When Studio creates a key it offers **Download backup**: a `.zip` with the keystore
file and a text file with its alias and passwords. **Keep it somewhere safe**:

- Google Play only accepts updates signed with the key the app's first release was
  uploaded with.
- A key that's lost (or deleted from Studio without a backup) can only be replaced
  by asking Google to reset the app's upload key through Play Console support,
  which takes time.
- The backup is also what you'd use to build the app on your own computer with
  [`flet build`](../../publish/android.md#signing-an-android-bundle).

Keys you haven't backed up show **No backup yet** in **Settings › Signing keys**.
You can download a backup there at any time from the key's **⋯** menu. Only the
owner of the Studio account can.

### Import a key

**Add signing key › Import a keystore** takes a keystore made with `keytool` or
Android Studio: a `.jks`, `.keystore` or `.p12` file with its **key alias** (optional
if the keystore has one key), **keystore password**, and **key password** (only if
it's different).

Import the key you already sign the app with to keep updating an app that's on
Google Play.

Older Java keystore formats (JCEKS, BKS) aren't supported: Studio shows the
`keytool -importkeystore` command that converts one to PKCS12.

### APKs and Google Play installs

Google Play re-signs the copies it delivers with **Google's app signing key**
(Play App Signing). Your key is the app's **upload key**: it proves to Google that
an upload is yours. So on a phone:

- An APK from Studio won't update a copy installed from Google Play, and the other
  way round — uninstall one to install the other.
- To give testers the exact build Google Play delivers, use a Google Play testing
  track ([install your test build](google-play/index.md#install-your-test-build-on-a-phone)),
  or download a Google-signed universal APK from Play Console's **App bundle
  explorer**.

## Package name

The app's **package name** (e.g. `com.example.myapp`) identifies it on the phone
and on Google Play. Set it in **Publish › Settings › Android › Package name**
before you publish: it can't be changed after the app's first release on Google
Play — a different package name is a different app.

## Questions

### Why is my APK so big?

An APK holds Python, your app's packages, and native code for each phone
architecture it supports. Studio builds APKs for **Most phones** (`arm64-v8a`) by
default: practically every phone in use, at about a third of the size of all three.
Pick **All devices** in the action screen's **Architectures** section to also
support old 32-bit phones (`armeabi-v7a`) and x86 emulators and Chromebooks
(`x86_64`), or **Custom** to choose.

App bundles don't have this problem: they include all three, and Google Play
delivers each device only what it needs. Their architectures come from **Publish ›
Settings › Android › Advanced settings › Architectures**, which is also where an
APK's choice starts when you set it there.

### Can I use a different key for APKs?

Not yet: one key signs both the app's APKs and its app bundles.
