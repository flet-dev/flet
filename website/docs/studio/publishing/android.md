---
title: "Android apps (APK and app bundle)"
---

# Android apps: APK and app bundle

The Android section of **Publish** has three actions:

| Action | What you get | For |
|---|---|---|
| **Create an APK** | An `.apk` file | Installing directly on a phone or tablet |
| **Create an app bundle (.aab)** | A signed `.aab` file | Uploading to Google Play yourself, e.g. an app's first release |
| **Publish to Google Play** | A release on a Google Play track | See [Publishing to Google Play](google-play.md) |

All three use the app's **Android signing key** when one is selected — the same key
for APKs and app bundles.

## Create an APK

Run **Create an APK** and **Download** the `.apk` when the run finishes.

To install it, open the file on the phone (download it there, or copy it over).
Android asks you to allow installing apps from that source — the browser or the
Files app — the first time: **Settings › Apps › Special app access › Install
unknown apps** if you need to change it later.

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

## Create an app bundle (.aab)

An app bundle is what Google Play takes: Google builds the APKs for each device
from it. Studio always signs a bundle with the app's key, so the action needs one
selected.

Use **Create an app bundle (.aab)** to upload a release to Google Play yourself —
mainly an app's **first release**, which Google requires to be uploaded in Play
Console. After that, [Publish to Google Play](google-play.md) uploads for you.

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
  track ([install your test build](google-play.md#install-your-test-build-on-a-phone)),
  or download a Google-signed universal APK from Play Console's **App bundle
  explorer**.

## Package name

The app's **package name** (e.g. `com.example.myapp`) identifies it on the phone
and on Google Play. Set it in **Publish › Settings › Android › Package name**
before you publish: it can't be changed after the app's first release on Google
Play — a different package name is a different app.

## Questions

### Why is my APK so big?

An APK holds Python, your app's packages, and native code for every phone
architecture it supports — by default all three (`arm64-v8a`, `armeabi-v7a`,
`x86_64`), so one file runs on any device. To make it smaller, choose fewer in
**Publish › Settings › Android**, under **Advanced settings › Architectures ›
Target architectures**: most phones today only need `arm64-v8a`, but the APK then
only installs on those. The setting applies to app bundles too.

App bundles don't have this problem: Google Play delivers each device only what it
needs.

### Can I use a different key for APKs?

Not yet: one key signs both the app's APKs and its app bundles.
