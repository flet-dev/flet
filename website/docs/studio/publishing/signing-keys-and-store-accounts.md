---
title: "Signing keys and store accounts"
---

# Signing keys and store accounts

Publishing needs two kinds of secrets, and Studio keeps both for you:

- **Signing keys** sign your app's builds, proving that updates come from you: the
  app's Android key, and the Apple Distribution certificate.
- **Store accounts** let Studio publish to a store on your behalf: Google Play
  service accounts and App Store Connect API keys.

## Signing keys live with the app

**Each app has its own Android key.** Studio makes it on the app's first Android run
and uses it for every APK and app bundle after that. The **Apple Distribution
certificate** is your Apple team's: Studio makes it on the first iOS build and reuses
it for all your apps.

You find them where they're used: the **Signing** card on **Publish › Android ›
Settings** and **Publish › iOS › Settings**.

{/* SCREENSHOT: /img/docs/studio/publishing/signing-card.png — the Signing card on Publish › Android › Settings */}

- **What signs the builds**: **Made by Studio** (with **not backed up yet** until
  you've downloaded a backup), **Your key** for one you imported, or **Managed by
  Studio** for the Apple certificate.
- **Download backup** (Android) or **Download (.p12)** (Apple): the keystore and its
  passwords, or the certificate and its password, as a `.zip`. Only the Studio
  account's owner can download it, and each download is recorded. See
  [Back up your key](android.md#back-up-your-key).
- **Use your own key…** or **Use your own certificate…**: import one you already
  have. See [Use your own key](android.md#use-your-own-key) and
  [Signing certificate](ios.md#signing-certificate).
- **App registration details** (Android): the package name and fingerprints Google
  asks for when you register the app.

Action screens show the same card with **Manage**, which opens it there.

### When you delete an app

Deleting an app deletes its Android key too, unless another app uses it. The
confirmation offers **Download backup** first, and a key that was never backed up
needs you to confirm you don't need it.

### Unused signing keys

A key no app uses, for example one you replaced with **Use your own key…** or one
left from before Studio made a key per app, is listed under **Unused signing keys**
in **Settings › Store accounts**, with **Download backup**, **Rename** and **Delete**.
The list disappears once there are none.

## Store accounts are shared

Store accounts are saved to your **Studio account** (personal or team), so all its
apps can use them. Each app chooses which one it publishes with.

- Connect one from the store's card: **Connect Google Play** on Publish › Android,
  **Connect App Store Connect** on Publish › iOS. Choose an account you connected
  before, or connect another.
- **Connection details** on the card shows the account the app uses, with **Change
  connection…** and **Disconnect from this app**, which only unselects it for the app.
- **Settings › Store accounts** lists each Studio account's store accounts, with how
  many apps use each one. Each one's **⋯** menu has **Rename** and **Disconnect**.

Disconnecting a Google Play account only removes it from Studio: the service account
and its permissions stay in Google Cloud and Play Console until you remove them
there. Likewise, an App Store Connect key stays valid until you revoke it in App Store
Connect, and deleting an Apple certificate doesn't revoke it at Apple.

## How Studio keeps them safe

- **Never in your app.** Keys, passwords and store account keys are never written
  to your app's files, its version history or `pyproject.toml`, and never shown in
  a build's log. Don't put them in your app's files yourself either: anyone who can
  see the app's code could read them.
- **Encrypted.** Each one is encrypted on Studio's servers with its own key, which
  is itself encrypted with a master key kept outside the database.
- **Signing keys** are handed to the build machine of a run that needs one, once,
  for that build only, and deleted with the machine when it ends. Your app's own
  code runs on that machine too, as it does when you build on your own computer.
- **Store account keys** never leave Studio's servers: uploads to a store run
  there, not on the build machine. That includes the App Store Connect key, which
  Studio also uses there to create certificates and profiles.

## Questions

### Why one Android key per app?

A leaked or lost key then affects one app only, you can hand an app over to someone
else with its key, and registering an app with Google pairs its package name with its
own key. A keystore you already use for several apps can still be imported with **Use
your own key…** for each of them; keys shared from before stay shared and show which
other apps use them.

### Can a team share keys and accounts?

Yes: store accounts saved to a team's Studio account can be used by all the team's
apps, and each app's key belongs to the team's account too. Only the team's owner can
download a key's backup.

### Is my Google Play account shared between apps?

A connected Google Play account can publish every app its service account has
permissions for in Play Console. Choose it on each app's Google Play card.
