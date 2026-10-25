---
title: "Signing keys and store accounts"
---

# Signing keys and store accounts

Publishing needs two kinds of secrets, and Studio keeps both for you:

- **Signing keys** sign your app's builds, proving that updates come from you:
  Android signing keys, and Apple certificates (which Studio usually creates for you,
  see [Signing certificate](ios.md#signing-certificate)).
- **Store accounts** let Studio publish to a store on your behalf: Google Play
  service accounts and App Store Connect API keys.

Both are saved to your **Studio account** — personal or team — and can be used by
all its apps. Each app selects which ones it uses, per platform.

## Where to manage them

- **Settings › Signing keys** and **Settings › Store accounts** list what's saved to
  each of your Studio accounts, with how many apps use each one.
- **Publish › Settings › Android › Signing & accounts** selects the ones an app
  uses on Android. iOS actions select theirs on the action screen.
- An action's screen shows the ones it needs, with **Add signing key**, **Connect
  Google Play** or **Connect App Store Connect** when there are none yet. What you add there is saved to
  the Studio account and selected for the app.

{/* SCREENSHOT: /img/docs/studio/publishing/settings-signing-keys.png — Settings › Signing keys with a key and its ⋯ menu */}

Each one's **⋯** menu has:

- **Download backup** (signing keys): the keystore and its passwords, or an Apple
  certificate's `.p12` and its password, as a `.zip`.
  Only the Studio account's owner can download it, and each download is recorded.
  A key Studio created shows **No backup yet** until you've downloaded one — see
  [Back up your key](android.md#back-up-your-key).
- **Rename**: names are for telling them apart in lists, e.g. "Reflex Arcade upload
  key".
- **Delete** (signing keys) or **Disconnect** (store accounts). Apps that used it
  then show that it was deleted and ask you to select another one before their next
  run. Disconnecting a Google Play account only removes it from Studio: the service
  account and its permissions stay in Google Cloud and Play Console until you remove
  them there. Likewise, an App Store Connect key stays valid until you revoke it in
  App Store Connect, and deleting an Apple certificate doesn't revoke it at Apple.

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

### Should each app have its own signing key?

It's common either way. One key per app limits what a leaked key affects and lets
you hand an app over to someone else with its key. One key for all your apps is
simpler to look after. Studio suggests a name per app ("*app name* upload key") but
lets you select any key for any app — just don't change an app's key once it's on
Google Play.

### Can a team share keys and accounts?

Yes: keys and accounts saved to a team's Studio account can be used by all the
team's apps. Only the team's owner can download a key's backup.

### Is my Google Play account shared between apps?

A connected Google Play account can publish every app its service account has
permissions for in Play Console. Select it for each app that should use it.
