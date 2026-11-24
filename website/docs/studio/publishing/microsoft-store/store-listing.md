---
title: "Microsoft Store listing"
---

# Microsoft Store listing

Your app's Microsoft Store listing (its descriptions, product features, keywords,
screenshots and details) can be written and kept in Flet Studio, and sent to Partner
Center without opening it.

Open it with **Create listing** or **Update listing** on the **Store listing** row of the
**Microsoft Store** card in **Publish › Windows**. The screen is the listing itself: edit
it there, then send it. Sending the listing on its own doesn't build the app and doesn't
use credits.

The **Store listing** row says where the listing stands: **Not created yet**, **No
update sent**, **Sent** with the date, or **Changed, not sent** when it was edited
since. When something on it needs fixing, the row says what.

:::note[Before you start]
Sending the listing needs a [connected Microsoft Store account](index.md#connect-microsoft-store),
the app [chosen on the card](index.md#choose-the-app), and its
[first submission](index.md#the-first-submission) made in Partner Center. If the app's
listing is already on the Store, start with
[Import from Partner Center](#import-from-partner-center).
:::

## Where the listing is kept

The listing is saved in your app's files, in a hidden `.store/microsoft-store/` folder,
as you edit:

```
.store/microsoft-store/
  details.toml                       default language, copyright, Developed by,
                                     additional license terms
  en-us/description.txt
  en-us/short_description.txt
  en-us/features.txt                 one feature per line
  en-us/release_notes.txt            "What's new in this version"
  en-us/keywords.txt                 one keyword per line
  en-us/images/screenshots/1.png, 2.png, ...
  en-us/images/app_tile_icon.png     optional
  de-de/...
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
**default language** is the one the Store shows people whose language isn't listed.

- **Add a language** (**+** next to the language): choose it from the Microsoft Store's
  languages, and start from empty texts or from another language's.
- A language without its own screenshots or tile icon uses the default language's, so
  one set usually covers them all.
- Removing a language removes it from the files. Partner Center keeps its own copy until
  you remove the language there: sending the listing only adds and updates languages.
  Languages that Partner Center has and Studio doesn't are left as they are.

## Texts

| Field | Limit |
|---|---|
| Description | 10,000 characters, required: what the app does, in plain text |
| Short description | 1,000 characters, optional: shown at the top of the listing; keep it under 270. Without it, the description's first paragraph is used |
| Product features | One per line: up to 20, 200 characters each, shown as a bulleted list |
| What's new in this version | 1,500 characters, optional: for an update, what changed. Leave it empty for the first release |
| Keywords | One per line: up to 7, 40 characters each, 21 words in all. They help people find the app; not shown |

The listing has no app name: the product name is always the name you
[reserved in Partner Center](index.md#choose-the-app).

## Screenshots

| Image | Requirements |
|---|---|
| **Screenshots** | 1 to 10 PNG files, 1366 × 768 or larger (up to 3840 on the long side) |
| **App tile icon** | Optional: a 300 × 300 PNG the Store shows instead of the icon in the package |

Studio checks every image and shows what's wrong under it. Transparent areas in
screenshots become white when Studio uploads them; the tile icon keeps its transparency.
Without a tile icon, the Store uses the app's icon from its package.

Drag a screenshot by its handle to change its place: the Store shows them in that order.

**Screenshots stay in Partner Center until you add your own.** The Store can't send
images back, so a language without screenshots in Studio keeps the ones in Partner
Center. Once you add screenshots, they replace those.

### Take screenshots in the Preview

The Preview's **Windows 11** device captures the app's window. Pinned, it captures at
1920 × 1080, a size the Store takes:

1. In the Preview, choose the **Windows 11** device.
2. In the device options, turn on **Pin to 1280×720**.
3. Open the screen of your app you want to show.
4. Under **Screenshot › Add to the Microsoft Store listing**, click **Screen**.

The screenshot is added to the default language's screenshots. Repeat for each screen.
An unpinned window captures at its own size: the Preview says when it's too small for
the Store.

## Details

These are app-wide, the same in every language:

- **Copyright and trademark info**, e.g. `© 2026 Acme Inc.`
- **Developed by**: shown as "Developed by" beside your publisher name.
- **Additional license terms** (optional): plain-text terms, or a link to them.

## Send the listing

Every listing change is a submission that Microsoft certifies, like a new package:

- **Send to the Microsoft Store** on the listing screen sends only the listing: no
  build, no credits.
- Or, on **Update**, tick **Also send the store listing** to send it in the same
  submission as the new package.

Either way, the run starts only when the listing has nothing wrong with it; the screen
lists what to fix. Certification takes up to three business days; the card shows where
it is. Partner Center takes one submission at a time, so wait until one is published
before sending the next.

## Import from Partner Center

**Import from Partner Center** replaces the listing files with the app's published
listing: every language's texts, and the app's details. The Store can't send images
back, so its screenshots stay in Partner Center until you add some in Studio. What's in
the files but not in Partner Center is lost: restore an earlier version of the app to
get it back.

## What stays in Partner Center

The listing in Studio covers the texts, screenshots, tile icon and details. These are
set in Partner Center:

- **pricing and availability**: the markets and the price;
- **properties**: the category, privacy policy URL, support info and system
  requirements;
- **age ratings**: the questionnaire, answered in the first submission.
