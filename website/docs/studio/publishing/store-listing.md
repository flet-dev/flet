---
title: "Google Play store listing"
---

# Google Play store listing

Your app's store listing — its name, descriptions, icon, feature graphic and
screenshots on Google Play — can be written and kept in Flet Studio, and sent to
Google Play without opening Play Console.

Open it with **Update store listing** in the Android section of **Publish**. The
screen is the listing itself: edit it there, then **Send to Google Play**. It
doesn't build the app and doesn't use credits.

{/* SCREENSHOT: /img/docs/studio/publishing/store-listing.png — the Update store listing screen: language, texts, graphics */}

:::note[Before you start]
Sending the listing needs a [connected Google Play account](google-play.md#step-2-connect-google-play)
and the app created in Play Console. If the app's listing is already on Google
Play, start with **Import from Google Play**.
:::

## Where the listing is kept

The listing is saved in your app's files, in a hidden `.store/google-play/` folder,
as you edit:

```
.store/google-play/
  details.toml                       default language, contact details
  en-US/title.txt                    the app's name
  en-US/short_description.txt
  en-US/full_description.txt
  en-US/video.txt                    a YouTube URL (optional)
  en-US/images/icon.png
  en-US/images/feature_graphic.png
  en-US/images/phone_screenshots/1.png, 2.png, ...
  en-US/images/tablet_screenshots/1.png, ...
  de-DE/...
```

- **It's never part of your app.** Builds and the preview leave the `.store`
  folder out; downloading the app as a `.zip` keeps it.
- **It's versioned with your app**: restoring an earlier version restores its
  listing too.
- **The AI agent can work on it.** **Write with AI** (and **Add and translate
  with AI** when adding a language) puts a ready request in the agent's message
  box; review it and send. Or just ask the agent to write, shorten or translate
  the texts — the listing updates as it edits these files.
- **Coming from fastlane?** Studio also reads fastlane `supply`'s folder names
  (`featureGraphic.png`, `phoneScreenshots/`, `tenInchScreenshots/`), so a
  `metadata/android` folder copied into `.store/google-play/` works; Studio moves
  a set to its own names when it next changes it.

## Languages

A listing has one or more languages, each with its own texts and graphics. The
**default language** is what Google Play shows people whose language isn't listed.

- **Add a language** (**+** next to the language) with its code, such as `de-DE`
  or `pt-BR`, optionally starting from another language's texts.
- A language without graphics uses the default language's, as on Google Play — so
  one set of screenshots usually covers them all.
- Removing a language removes it from the files. Google Play keeps its copy until
  you remove the language in Play Console: sending the listing only adds and
  updates languages.

## Texts

| Field | Limit |
|---|---|
| App name | 30 characters |
| Short description | 80 characters |
| Full description | 4000 characters |
| YouTube video | optional URL |

Google Play reviews listings: avoid claims like "best" or "#1", other apps' names,
and lists of keywords.

## Graphics

| Graphic | Requirements |
|---|---|
| **App icon** | 512 × 512 PNG, up to 1 MB |
| **Feature graphic** | 1024 × 500 PNG or JPEG, shown at the top of the listing |
| **Phone screenshots** | 2 to 8 |
| **Tablet screenshots** | optional, up to 8 |

Screenshots can be PNG or JPEG, 320 to 3840 pixels on each side, with the long
side at most twice the short one. Studio checks every image and shows what's
wrong under it. Transparent areas (such as a device frame's rounded corners)
become white when Studio uploads an image, since Google Play doesn't accept
transparency in screenshots.

Drag a screenshot by its handle to change its place: Google Play shows them in
that order.

### The app icon

**Use the app's icon** makes the listing icon from the icon your Android builds
use (Android's own icon if set, else the app's icon, else Flet's): 512 × 512,
centred, with transparent areas filled with the app's **Icon background** colour
(white if it has none). Use it again after changing the app's icon. An icon
smaller than 512 px is upscaled and may look blurry: a 1024 px icon works best.

### Take screenshots in the Preview

The Preview's **Android phone** and **Android tablet** devices are sized for
Google Play: 1080 × 1920 and 1600 × 2560 pixels.

1. In the Preview, choose the **Android phone** device (or **Android tablet**).
2. Open the screen of your app you want to show.
3. In the device options, under **Screenshot › Add to the Google Play store
   listing**, click **Screen** — or **Framed** to include the device frame.

The screenshot is added to the default language's phone (or tablet) screenshots.
Repeat for each screen. **Screen** and **Framed** above them still download the
image instead.

### Tablet screenshots

Google Play has separate slots for 7-inch and 10-inch tablets. One set of tablet
screenshots fills both. They're optional: without them, tablet users see the
phone screenshots. Add them if your app has a layout made for large screens.

## Contact details

An **email** address is required on the listing; a website and phone number are
optional. They're shown on the app's page on Google Play.

## Send the listing

- **Update store listing › Send to Google Play** sends only the listing.
- Or, on **Publish to Google Play**, tick **Also send the store listing** to send
  it in the same change as the release.

Either way, the run starts only when the listing has nothing wrong with it; the
screen lists what to fix. Studio uploads a graphic only when it changed, and the
run's details show what was sent.

Like a release, listing changes are reviewed by Google, and with managed
publishing they wait until you publish them in Play Console (**Not sent for
review**).

## Import from Google Play

**Import from Google Play** replaces the listing files with the app's current
listing on Google Play: every language's texts and graphics, and the contact
details. Use it to start from an app that's already published, or after editing
the listing in Play Console. What's in the files but not on Google Play is lost —
restore an earlier version of the app to get it back.

## What stays in Play Console

The listing in Studio covers the texts, graphics and contact details. These are
set in Play Console:

- the app's **category** and tags, and its **privacy policy** URL;
- **App content**: content rating, target audience, data safety, ads and other
  declarations;
- **pricing** and the countries the app is available in.
