---
title: "Android apps"
---

# Android apps

Open **Publish › Android**. Its **Overview** has a card for each place an Android app
goes:

| Card | What it does |
|---|---|
| **Google Play** | Publishes the app to Google Play's testing tracks and to Production. See [Publishing to Google Play](google-play/index.md). |
| **Direct download** | Builds an APK and puts it on your app's own [download page](#download-page): a link anyone can open on their phone. |

Each card shows its next step while it isn't set up yet, then what's live, with
**Update** to publish a new version. **Activity** lists the platform's runs, and
**Settings** has its [signing key](#signing-key) and settings.

{/* SCREENSHOT: /img/docs/studio/publishing/android-overview.png — Publish › Android with the Google Play and Direct download cards */}

## Download page

**Create APK** builds a signed APK and puts it on a page your users can open: a link
like `get.flet.app/…`, with a **Download APK** button, the app's icon, version and
"What's new", install steps, and a QR code on computers. The link stays the same
across updates: share it once (on your website, in an email, as a QR code on a
flyer) and each update replaces the app behind it.

{/* SCREENSHOT: /img/docs/studio/publishing/download-page.png — the public download page on a phone */}

### Create the APK

1. On **Publish › Android**, click **Create APK** on the **Direct download** card.
2. Optionally write **What's new**, and pick the [architectures](#why-is-my-apk-so-big).
3. Click **Create APK**. When the run finishes, the app is on the page.

The first Android run makes the app's [signing key](#signing-key). Back it up when
the card asks: every update has to be signed with it.

### Update it

**Update APK** on the card builds the app as it is now and replaces the one on the
page. Your users install it over the version they have and keep their data.

### Share the link

The card has the page's link with **Open**, **Copy**, **QR code** and **Share**.
**Download APK** gives you the file without sharing the link.

| | Explorer | Creator |
|---|---|---|
| Link | Private: `get.flet.app/` and a random code | The private link, plus a readable one: `get.flet.app/your-app` |
| How long a release stays up | 7 days after its build: update the APK to keep the app up | While it's the current release |
| Run downloads in Studio | 7 days | 90 days |

Set a readable link under **Readable link** on Create APK: lowercase letters, digits
and hyphens. If you rename it, the old name keeps redirecting for 30 days.

### New link, take offline

In the **Download page** section's **⋯** menu on Create APK:

- **Create a new link**: the current private link stops working at once. Use it if
  a link reached people it shouldn't have.
- **Take offline**: the page stops offering the app until you update it again.

### What your users see

The page shows the **Download APK** button and the steps to install: Android asks
them to allow their browser to install unknown apps the first time. Installing a
newer version later keeps their data, because every update is signed with the same
key.

Each page has a **Report this app** link. Flet reviews reports and can take a page
down; you'll see that in Studio.

## Share an APK outside Google Play

Android devices are starting to require that apps come from **registered
developers**, including apps installed from a website, an email or another store.
Google enforces it from September 30, 2026 in Brazil, Indonesia, Singapore and
Thailand, and on certified Android devices everywhere from 2027. An APK from a
developer who isn't registered can still be installed, but only through Android's
extra "advanced" install steps.

Apps you publish on Google Play are registered automatically. To share an APK
outside Google Play, register it with Google:

1. **Sign up and verify your identity** in the
   [Android Developer Console](https://android.google.com/developerconsole) or, if
   the app is also on Google Play, in Play Console. Individuals need a photo ID and
   proof of address; organizations also a D-U-N-S number and a verified website.
2. **Register the app's package name and its signing key.** Open **Publish ›
   Android › Settings**, and on the **Signing** card click **App registration
   details**: the package name and the key's SHA-256 fingerprint, each with a copy
   button. Create APK's Signing card has the same details.
3. If the package name was already used by an app on devices, Google may ask you to
   **prove you hold the key**: an APK signed with it that contains a token Google
   gives you. Studio can't make that file yet; tell us if you need it.

Once registered, keep using the same key: Google ties the app to it.

To share the app with a few testers only, **limited distribution** needs no
identity verification: up to 20 devices, through invitations.

See Google's [developer verification guides](https://developer.android.com/developer-verification/guides)
for the details.

## Signing key

A signing key proves your app's updates come from you. **Each app has its own**:
Studio makes it on the app's first Android run, and uses it for every APK and app
bundle after that.

Find it on **Publish › Android › Settings**, in the **Signing** card:

- what the key is: **Made by Studio** (with **not backed up yet** until you've
  downloaded a backup), or **Your key** for one you imported;
- **Download backup** and **Use your own key…**;
- **App registration details**: the package name and fingerprints Google asks for.

Action screens show the same card with **Manage**, which opens it.

{/* SCREENSHOT: /img/docs/studio/publishing/signing-card.png — the Signing card on Publish › Android › Settings, registration details open */}

### Back up your key

**Download backup** saves a `.zip` with the keystore file and a text file with its
alias and passwords. **Keep it somewhere safe**:

- Google Play only accepts updates signed with the key the app's first release was
  uploaded with.
- Phones only install an update over an app signed with the same key, so a
  download page update signed with another key won't install over your users' copy.
- A lost key can only be replaced on Google Play by asking Google to reset the
  app's upload key through Play Console support, which takes time.
- The backup is also what you'd use to build the app on your own computer with
  [`flet build`](../../publish/android.md#signing-an-android-bundle).

Until you download it, the **Direct download** card and the Signing card remind
you. Only the owner of the Studio account can download a backup.

### Use your own key

**Use your own key…** imports a keystore made with `keytool` or Android Studio: a
`.jks`, `.keystore` or `.p12` file with its **key alias** (optional if the keystore
has one key), **keystore password**, and **key password** (only if it's different).
Use it to keep updating an app that's already on Google Play with the key you sign
it with.

If the app's current key has already signed builds, Studio warns you first: Google
Play won't accept updates signed with another key unless you reset the upload key
in Play Console, and phones won't update a download page APK over one signed with
another key.

The key you replace isn't deleted. Once no app uses it, it's listed under **Unused
signing keys** in **Settings › Store accounts**, where you can back it up and delete
it.

Older Java keystore formats (JCEKS, BKS) aren't supported: Studio shows the
`keytool -importkeystore` command that converts one to PKCS12.

### When you delete the app

Deleting an app deletes its signing key too, unless another app uses it. The
confirmation offers **Download backup** first, and if the key was never backed up
you have to confirm you don't need it.

### APKs and Google Play installs

Google Play re-signs the copies it delivers with **Google's app signing key**
(Play App Signing). Your key is the app's **upload key**: it proves to Google that
an upload is yours. So on a phone:

- An APK from Studio won't update a copy installed from Google Play, and the other
  way round: uninstall one to install the other.
- To give testers the exact build Google Play delivers, use a Google Play testing
  track ([install your test build](google-play/index.md#install-your-test-build-on-a-phone)),
  or download a Google-signed universal APK from Play Console's **App bundle
  explorer**.

## App bundle (.aab)

An app bundle is what Google Play takes: Google builds the APKs for each device from
it. Studio signs it with the app's key.

You need one for an app's **first release** on Google Play, which Google requires to
be uploaded in Play Console: the Google Play card's setup has **Create app bundle**
and then **Download .aab**. After that,
[Google Play's tracks](google-play/index.md) upload for you.

A phone can't install an `.aab` directly.

## Package name

The app's **package name** (e.g. `com.example.myapp`) identifies it on the phone and
on Google Play. Set it in **Publish › Android › Settings › Package name** before you
publish: it can't be changed after the app's first release on Google Play (a
different package name is a different app).

## Questions

### Why is my APK so big?

An APK holds Python, your app's packages, and native code for each phone
architecture it supports. Create APK builds for **Most phones** (`arm64-v8a`) by
default: practically every phone in use, at about a third of the size of all three.
Pick **All devices** in its **Architectures** section to also support old 32-bit
phones (`armeabi-v7a`) and x86 emulators and Chromebooks (`x86_64`), or **Custom**
to choose.

App bundles don't have this problem: they include all three, and Google Play
delivers each device only what it needs. Their architectures come from **Publish ›
Android › Settings › Advanced settings › Architectures**, which is also where an
APK's choice starts when you set it there.

### Can I use a different key for APKs and app bundles?

No: one key per app signs both, so the app on the download page and the one on
Google Play are signed by the same upload key.
