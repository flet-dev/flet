---
title: "App Store listing"
---

# App Store listing

Your app's App Store listing (its name, subtitle, description, keywords, screenshots,
categories and App Review details) can be written and kept in Flet Studio, and sent to
App Store Connect without opening it. One listing serves both iOS and the Mac App Store:
the same texts, with Mac screenshots for the Mac.

Open it with **Create listing** or **Update listing** on the **Store listing** row of the
**App Store & TestFlight** card in **Publish › iOS** (or **Publish › macOS**). The screen
is the listing itself: edit it there, then send it. It doesn't build the app and doesn't
use credits.

The **Store listing** row says where the listing stands: **Not created yet**, **No
update sent**, **Sent** with the date, or **Changed, not sent** when it was edited
since. When something on it needs fixing, the row says what.

:::note[Before you start]
Sending the listing needs a [connected App Store Connect account](../ios.md#connect-app-store-connect)
and the app [created in App Store Connect](index.md#create-the-app-in-app-store-connect).
If the app's listing is already on the App Store, start with
[Import from App Store](#import-from-app-store).
:::

## Where the listing is kept

The listing is saved in your app's files, in a hidden `.store/app-store/` folder, as you
edit:

```
.store/app-store/
  details.toml                       default language, categories, copyright,
                                     App Review and TestFlight details
  en-US/name.txt
  en-US/subtitle.txt
  en-US/description.txt
  en-US/keywords.txt
  en-US/promotional_text.txt
  en-US/support_url.txt, marketing_url.txt, privacy_policy_url.txt
  en-US/images/iphone_screenshots/1.png, 2.png, ...
  en-US/images/ipad_screenshots/1.png, ...
  en-US/images/mac_screenshots/1.png, ...
  de-DE/...
```

- **It's never part of your app.** Builds and the preview leave the `.store` folder
  out; downloading the app as a `.zip` keeps it.
- **It's versioned with your app**: restoring an earlier version restores its listing
  too.
- **The AI agent can work on it.** **Write with AI** (and **Add and translate with AI**
  when adding a language) puts a ready request in the agent's message box; review it and
  send. Or just ask the agent to write, shorten or translate the texts: the listing
  updates as it edits these files.

## Languages

A listing has one or more languages, each with its own texts and screenshots. The
**default language** is the app's primary language in App Store Connect.

- **Add a language** (**+** next to the language): choose it from the App Store's
  languages, and start from empty texts or from another language's.
- A language without screenshots uses the default language's, so one set usually covers
  them all.
- Removing a language removes it from the files. App Store Connect keeps its own copy
  until you remove the localization there: sending the listing only adds and updates
  languages.

## Texts

| Field | Limit |
|---|---|
| App name | 30 characters |
| Subtitle | 30 characters, optional: a short summary under the name |
| Description | 4,000 characters |
| Keywords | 100 characters, comma-separated: words people might search for (not shown) |
| Promotional text | 170 characters, optional: shown above the description |
| Support URL | Required: a page where users can get help |
| Marketing URL | Optional |
| Privacy policy URL | Required for every app |

The app name, subtitle and privacy policy URL belong to the app in App Store Connect; the
others belong to the version you're preparing, so each new version can have its own.
Promotional text is the one Apple lets you change without a new version.

## Screenshots

| Screenshots | Size | Needed for |
|---|---|---|
| **iPhone (6.9")** | 1 to 10, 1320 × 2868 (or 1290 × 2796, 1260 × 2736) | iOS |
| **iPad (13")** | 1 to 10, 2064 × 2752 (or 2048 × 2732) | iOS: Flet apps run on iPad too, so Apple asks for both |
| **Mac** | 1 to 10, 2880 × 1800 (or 2560 × 1600, 1440 × 900, 1280 × 800) | The [Mac App Store](../mac-app-store.md) |

Screenshots can be PNG or JPEG, up to 10 MB, in portrait or landscape. Studio checks
every image and shows what's wrong under it. Transparent areas become white when Studio
uploads them. The app's icon comes from its build: the listing has no icon of its own.

Drag a screenshot by its handle to change its place: the App Store shows them in that
order. A set is only uploaded again when it changed.

### Take screenshots in the Preview

The Preview's **iPhone 6.9"**, **iPad 13"** and **macOS** devices capture at Apple's
sizes: 1320 × 2868, 2064 × 2752 and 2880 × 1800 pixels.

1. In the Preview, choose the **iPhone 6.9"** device (or **iPad 13"**, or **macOS**).
2. Open the screen of your app you want to show.
3. In the device options, under **Screenshot › Add to the App Store listing**, click
   **Screen**.

The screenshot is added to the default language's iPhone (or iPad, or Mac) screenshots.
Repeat for each screen. **Screen** and **Framed** above them still download the image
instead.

## App details

- **Primary category** (required) and **secondary category** (optional). For the Mac App
  Store, the primary category is the **App category** chosen on the macOS card.
- **Copyright** (required), e.g. `2026 Acme Inc.`

## App Review and TestFlight

**App Review contact**: the name, email and phone (with the country code) App Review can
reach. All are required.

- **Sign-in**: whether App Review needs an account to try the app. If it does, enter the
  demo user name and password in App Store Connect › the version › **App Review
  Information**: Studio doesn't keep them.
- **Notes for App Review** (optional): anything the reviewer needs, e.g. how to try a
  feature. Don't put passwords here.

**TestFlight**: the **beta app description** and **feedback email**. Apple's beta review
reads them before external testers get an app's first build; internal testers don't
need them. See [Test Information for external testers](index.md#test-information-for-external-testers).

## Send the listing

- **Send to the App Store** on the listing screen sends only the listing.
- Or, on **Publish to the App Store**, tick **Also send the App Store listing** to send
  it with the version you submit.

Either way, the run starts only when the listing has nothing wrong with it; the screen
lists what to fix. The run's details show what was sent.

The listing goes to the app's version that's still being prepared: the one with the
app's current version number (**Publish › iOS › Settings › Version**), which Studio
creates if needed. On **Publish › macOS**, the card's **Update listing** sends the texts
with the Mac screenshots to the macOS version.

App Store Connect doesn't let you change a version that's waiting for or in review:
remove it from review there first, or wait for Apple's decision.

## Import from App Store

**Import from App Store** replaces the listing files with the app's current listing in
App Store Connect: every language's texts and screenshots, and the app's details. Use it
to start from an app that's already published, or after editing the listing in App
Store Connect. What's in the files but not in App Store Connect is lost: restore an
earlier version of the app to get it back.

## What stays in App Store Connect

The listing in Studio covers the texts, screenshots, categories, copyright and App
Review details. These are set in App Store Connect:

- **App Privacy**: what data the app collects;
- **pricing and availability**;
- the **age rating** questionnaire;
- the demo account App Review signs in with, if the app needs one.
