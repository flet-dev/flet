---
title: "Publishing to Google Play"
---

# Publishing to Google Play

Flet Studio can build your Android app, sign it with your key and release it on a
Google Play track — Internal testing, Closed testing, Open testing or Production —
in one run. This page covers the one-time setup, publishing, and getting a test
build onto your phone.

:::tip[In short]
1. Create the app in Play Console and **upload its first release yourself**
   (Google requires it) — Studio's **Create an app bundle (.aab)** makes the file.
2. **Connect Google Play**: a Google Cloud service account with release
   permissions in Play Console.
3. Run **Publish to Google Play**: Studio builds, signs and uploads every later
   release.
:::

## Before you start

You need:

- A **Google Play developer account** ([Play Console](https://play.google.com/console)).
- An **Android signing key** selected for the app in Studio — see
  [Android apps](../android.md#signing-key). Google Play only accepts updates signed
  with the key the app's first release was uploaded with, so keep using the same
  one.
- The app's **package name** set in Studio (**Publish › Settings › Android ›
  Package name**, e.g. `com.example.myapp`). It must be the app's package name in
  Play Console, and it can't be changed after the first release.

## Step 1. Create the app and upload its first release

Google doesn't let tools create an app or upload its very first release: that has
to happen in Play Console. Do it once per app:

1. In Play Console, **Create app**: enter its name, language and type, and accept
   the declarations.
2. In Studio, open **Publish** and run **Create an app bundle (.aab)** for the app.
   When the run finishes, **Download** the `.aab`.
3. In Play Console, go to **Test and release › Testing › Internal testing** and
   **Create new release**. Upload the `.aab` and roll the release out.

Google Play now knows the app and remembers the key it was signed with as the
app's **upload key**. Google re-signs the copies it delivers with its own key
(Play App Signing), which is why your key must never change — see
[Android apps](../android.md#apks-and-google-play-installs).

{/* SCREENSHOT: /img/docs/studio/publishing/play-console-first-release.png — Play Console › Internal testing › Create new release, with the .aab uploaded */}

## Step 2. Connect Google Play

Studio uploads your releases with a **service account**: a Google Cloud robot user
you give release permissions to in Play Console. You set it up once and can use it
for all your apps.

### In Google Cloud

1. Open a project in the [Google Cloud console](https://console.cloud.google.com/).
   **Any project works** — an existing one, or a new one just for publishing (the
   project picker at the top › **New project**). It doesn't have to be linked to
   your Play Console account, and it costs nothing: the Google Play Android
   Developer API is free, and no billing account is needed.
2. Enable the **Google Play Android Developer API** for it
   (**APIs & Services › Library**, search for "Google Play Android Developer").
3. Go to **IAM & Admin › Service accounts** and **Create service account**. Give
   it a name, e.g. `my-app-google-play`.
   - **No role is needed**: skip the optional "Grant this service account access
     to project" step. Permissions come from Play Console, not Google Cloud.
4. Open the service account, then **Keys › Add key › Create new key › JSON**. A
   `.json` key file downloads. Keep it private: anyone with it can publish as the
   service account.

### In Play Console

1. Open **Users and permissions**: it's an account-level page, not an app's. From
   the [Play Console](https://play.google.com/console) home, click the developer
   account icon at the top right (next to **Notifications**) › **Manage developer
   account** › **Users and permissions**. Then **Invite new users**.
2. Enter the service account's email (`…@….iam.gserviceaccount.com`, also in the
   JSON key as `client_email`).
3. On the **App permissions** tab, **Add app** and choose your app. In
   **Permissions for *your app***, tick:
   - under **App access**: **View app information (read-only)**. Play Console ticks
     the permissions that come with it (such as *View app quality information*)
     for you;
   - under **Releases**: **Release apps to testing tracks**;
   - under **Releases**, only if you'll submit to Production from Studio:
     **Release to production, exclude devices, and use Play App Signing**;
   - under **Store presence**, only if you'll send the
     [store listing](store-listing.md) from Studio: **Manage store presence** —
     and, while the app is still a draft in Play Console (its name shows
     "(unreviewed)"), **Draft apps › Edit and delete draft apps** too. Releases
     don't need it.

   Leave the rest unticked: Studio doesn't need **Admin**, financial data or tester
   lists.
4. **Invite user**. A service account doesn't have to accept anything.

Permission changes can take a few minutes to apply.

### In Studio

In the **Google Play** panel of **Publish › Overview** (or at the bottom of the
**Publish to Google Play** screen, or in **Settings › Store accounts**), click
**Connect Google Play**, choose the JSON key file and **Connect**. The name is filled
in from the service account's email; change it if you like.

The account is saved to your Studio account, so your other apps can use it too, and
selected for this app. Studio checks access straight away: the panel's **App** line
shows the app's package name with a **Play Console** link, or what's wrong and how
to fix it. **Change** switches the app to another account.

{/* SCREENSHOT: /img/docs/studio/publishing/connect-google-play.png — the Connect Google Play dialog with a key chosen */}

## Step 3. Publish

Open **Publish**, then **Publish to Google Play** in the Android section.

{/* SCREENSHOT: /img/docs/studio/publishing/google-play-action.png — the Publish to Google Play screen: Release section, Signing & accounts with the Connected line, and the footer button */}

- **Track**: where the build goes.

  | Track | Who gets it | Button |
  |---|---|---|
  | Internal testing | Up to 100 testers you list in Play Console; available within minutes | Upload to Internal testing |
  | Closed testing | Testers you invite (lists or Google Groups) | Upload to Closed testing |
  | Open testing | Anyone who joins from your store listing | Upload to Open testing |
  | Production | Everyone, after Google's review | Submit for review |

- **What's new**: optional release notes (up to 500 characters) shown on Google
  Play, in the **Language** you enter (default `en-US`). They belong to this
  release only and aren't remembered for the next one.
- **Store listing**: tick **Also send the store listing** to send the app's name,
  descriptions and screenshots in the same change — see
  [Google Play store listing](store-listing.md).
- **Version and build number**: the build number becomes the release's version
  code. Studio starts it above the highest one Google Play already has, so it never
  clashes.

Then click the track's button.

### What happens during a run

1. **The build.** Studio builds a signed `.aab` in the cloud, as for any action.
   This part costs credits, for the time it takes.
2. **The upload.** When the build is done, the run shows **Uploading to Google
   Play** while Studio's servers upload the bundle, release it on the track and
   send the change to Google Play. This part doesn't cost credits.

Your service account's key is only used by Studio's servers for the upload: it's
never sent to the machine that builds your app.

### Where your build is

Once the run succeeds, the Google Play row on **Overview** says where the build is:

| Status | Meaning | What to do |
|---|---|---|
| **On Internal testing** (or another testing track) | Released on the track | Testers get it through the Play Store — on Closed and Open testing once Google's review passes |
| **In review** | Submitted to Production | Wait for Google's review; Play Console shows its progress |
| **Draft in Play Console** | The app's setup in Play Console isn't finished, so Google only accepts draft releases | Finish the app's setup, then roll the draft out in Play Console |
| **Not sent for review** | The app uses managed publishing | Send the changes for review in Play Console |

**Play Console** on the row and in the run's details opens Play Console.

## When an upload fails

If the build succeeded but the upload didn't, the run fails with what Google Play
said and how to fix it. Many of these are fixed in Play Console and then
**Retry upload** (on Overview and in the run's details): it uploads the same build
again, without building it again or charging credits. Studio first checks whether
Google Play already has the build, so a retry never submits it twice.

| Error | Fix |
|---|---|
| Google Play has no app *package* yet | Create the app and upload its first release yourself ([step 1](#step-1-create-the-app-and-upload-its-first-release)), then **Retry upload** |
| Google Play needs a contact email for the app | Add an email under **Contact details** in the [store listing](store-listing.md), then send it again |
| *Service account* can't change this app's store listing | Give it **Store presence › Manage store presence** for the app in Play Console › Users and permissions — and **Draft apps › Edit and delete draft apps** while the app is a draft — wait a few minutes, then **Retry upload** |
| *Service account* can't release this app | Give it the app's permissions in Play Console › Users and permissions ([step 2](#in-play-console)), wait a few minutes, then **Retry upload** |
| Enable the Google Play Android Developer API | Enable it in the service account's Google Cloud project, then **Retry upload** |
| Google rejected the service account key | The key was deleted or the account disabled: create a new JSON key and connect it |
| This build number is already on Google Play | Start a new run; leave the build number automatic, or set a higher one |
| Google Play expects a different upload key | Select the key the app's first release was uploaded with. Play Console › Test and release › **App integrity** shows its SHA-1; **Settings › Signing keys** shows yours |
| Google Play rejected a debug build | Select a signing key for the app and start a new run |
| Google Play rejected the target SDK | Raise **Target SDK version** in Publish › Settings › Android (SDK), then start a new run |
| Google Play is busy right now | **Retry upload** in a few minutes |

If **Retry upload** isn't offered, the run's details say why — usually that a new
run is needed.

## Install your test build on a phone

An app on a testing track doesn't show up in Play Store search. Testers get to it
through links.

### Add testers

In Play Console, go to **Test and release › Testing › Internal testing ›
Testers**. Create an email list, add the **Google accounts** of your testers
(including your own), tick the list and save.

Google doesn't notify the people on the list: send them the **Join on the web**
link yourself (next step).

### Join the test

Each tester does this once:

1. Open the track's **Join on the web** link — **Copy link** on the Testers tab
   (`https://play.google.com/apps/internaltest/…`). Send it to your testers, or
   open it yourself.
2. Sign in with the Google account that's on the list and **Accept invite**. The
   page then says "You're a tester for …".
3. **Download test app** opens the app's Play Store page: **Install** on the phone,
   or on a computer choose **Install** and pick the phone — Google Play installs it
   remotely.

New releases on the track arrive as normal Play Store updates (**Play Store ›
your profile icon › Manage apps & device › Updates available** to get one now).

{/* SCREENSHOT: /img/docs/studio/publishing/play-join-test.png — the "You're a tester" page with Download test app */}

### "Item not found"

The Play Store says **Item not found** until the account has joined the test:

- **Join first** with the Join on the web link — being on the email list isn't
  enough.
- Use the link behind **Download test app**: for an internal test it carries an
  `ah=…` token, and the plain `…/details?id=<package>` link without it can show
  Item not found.
- Check the account the **Play Store app** uses (its profile icon). It can differ
  from the phone's or the browser's account.
- Testers' addresses must be **Google accounts**. An address on your own domain
  only works if it's the address you sign in to Google with.
- A newly published app can take a few minutes, occasionally longer, to become
  available. If it still doesn't show, clear the Play Store's cache (**Settings ›
  Apps › Google Play Store › Storage › Clear cache**) and try again.

### "(unreviewed)" in the app's name

Until the app's store listing is set up and reviewed, testers see a temporary name
such as `com.example.myapp (unreviewed)` on Google Play. Send a
[store listing](store-listing.md) from Studio (or fill in **Grow users › Store
presence › Main store listing** in Play Console) to fix it. The app's name on the phone, under its icon, is already the
right one: it comes from the app itself.

## Production

- **Google reviews** releases on Production, and on Closed and Open testing too
  (Internal testing isn't reviewed). Reviews usually take from hours to a few days;
  Play Console shows their progress.
- **New personal developer accounts** have to run a closed test with at least 12
  testers for 14 days before they can apply for production access. Until then,
  Production releases fail with Google's message saying so. Publish to Closed
  testing from Studio in the meantime.
- **Managed publishing** (Play Console › Publishing overview) holds approved changes
  until you publish them. Studio's uploads then show **Not sent for review**: send
  them for review in Play Console.

## Questions

### Do I have to use Studio for the first release too?

No — any `.aab` signed with your key works. Studio's **Create an app bundle (.aab)**
is the easy way to get one signed with the key Studio will keep using.

### Can I use an app that's already on Google Play?

Yes. [Import its upload key](../android.md#import-a-key) (the keystore you've been
signing with), set the same package name, connect Google Play, and publish. The
build number must be higher than Google Play's latest; Studio starts above it
automatically.

### Can I install the APK Studio builds instead?

Yes, but not over a copy installed from Google Play, and the other way round:
Google Play re-signs its copies with Google's key, and Android only updates an app
with one signed by the same key. See
[Android apps](../android.md#apks-and-google-play-installs).

### What can't Studio do on Google Play yet?

Staged rollouts, custom tracks, release notes in several languages, in-app
products, and the parts of the app's setup outside its store listing (category,
App content declarations, pricing and countries). Use Play Console for those.
