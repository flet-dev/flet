---
title: "Microsoft Store"
---

# Microsoft Store

Open **Publish › Windows**. The **Microsoft Store** card publishes your app on the
[Microsoft Store](https://apps.microsoft.com), where Windows users find, install and
update it. Studio packages the app as an MSIX (`.msix`) for the Store, and Microsoft
signs the package once it passes certification: you need no code-signing certificate.

You need a Microsoft Store developer account. Registration is free, for individuals
and companies: start it at [storedeveloper.microsoft.com](https://storedeveloper.microsoft.com).

## Connect Microsoft Store

Studio submits your app's updates with an application you add to your Partner Center
account:

1. In Partner Center, open **Account settings › User management › Microsoft Entra
   applications**. Your Partner Center account must be associated with a Microsoft
   Entra tenant (**Account settings › Tenants**), which needs someone with Global
   administrator rights in it.
2. Add an application, or create one there (**Create Microsoft Entra application**),
   with the **Manager** role. Studio doesn't use its **Reply URL**: enter
   `https://localhost/` (Partner Center refuses some addresses, such as one without
   the trailing slash).
3. Select **Add new key** and copy the key: Partner Center shows it once. Note when it
   expires.
4. Select the application's name in the list (or **Cancel** on the key screen) and copy
   its **Tenant ID** and **Client ID**.
5. On the card, select **Connect Microsoft Store** and enter them. Studio lists your
   apps with it to check it.

The key stays on Studio's servers; it never reaches a build.

## Choose the app

Reserve your app's name in [Partner Center](https://partner.microsoft.com/dashboard/apps-and-games)
first: **Apps and games › New product › MSIX or PWA app**, enter the name, then
**Reserve product name**. Then choose it on the card. Studio takes the package's
identity from Partner Center (`Package/Identity/Name` and `Package/Identity/Publisher`);
the API doesn't give the publisher display name, so copy it once from the app's
**Product identity** page (`Package/Properties/PublisherDisplayName`), exactly as shown.
It's the same for all apps in your account: Studio remembers it for the next one. The package is named as the app you
reserved (Partner Center accepts no other name), whatever the app's **Product name**.

## The first submission

Microsoft takes an app's first submission only in Partner Center, where it also asks
the age-ratings questionnaire. The card walks you through it:

1. **Create Store package (.msix)** and download it.
2. In Partner Center, on the app's overview page, select **Start submission**, then
   complete each section
   ([Microsoft's checklist](https://learn.microsoft.com/windows/apps/publish/publish-your-app/msix/create-app-submission)):
   - **Pricing and availability:** a base price (Free or a price). Markets, audience,
     discoverability and schedule have defaults.
   - **Properties:** a category, and a privacy policy URL if the app collects or
     transmits personal information.
   - **Age ratings:** the questionnaire.
   - **Packages:** upload the `.msix`.
   - **Store listings:** a description and at least one screenshot (1366 × 768 or
     larger), in at least one language. To take one, preview the app on **Windows 11**,
     open the preview options, turn on **Pin to 1280×720**, then **Screen**: it saves
     the app at 1920 × 1080.
   - **Submission options › Restricted capabilities:** explain why the app needs
     `runFullTrust`. The card has a ready-to-paste explanation.
3. Select **Submit for certification**.

Once Microsoft publishes it, the card shows the app on the Store and Studio sends the
updates.

## Updates

Select **Update** on the card. Studio builds the app, packages it, and submits it
to Partner Center: a new submission that keeps your listing, pricing and age rating
from the last one, with the new package. Tick **Also send the store listing** to send
your [store listing](#store-listing) in the same submission. Certification takes up to three business days;
the card shows where it is (**In certification**, **Published**) and why when it fails,
with a link to the certification report.

### Versions

The Store's versions have three numbers, like `1.2.0`. The first can't be `0`, and the
build number isn't part of them, so **every update needs a higher version**. The
Publish screen says which version the Store has and offers the next one.

## Store listing

The card's **Store listing** row opens the listing: its texts and screenshots, kept in
the app's `.store/microsoft-store/` folder (never packaged into the app). **Import from
Partner Center** fills it from the published listing.

| Field | Limit |
|---|---|
| Description | 10,000 characters (required) |
| Short description | 1,000; shown at the top of the listing, best under 270 |
| Product features | One per line: up to 20, 200 characters each |
| What's new in this version | 1,500 |
| Keywords | One per line: up to 7, 40 characters each, 21 words in all (not shown) |
| Screenshots | 1 to 10 PNG files, 1366 × 768 or larger |
| App tile icon | Optional, 300 × 300 PNG |

The app-wide **Details** are the copyright and trademark info, **Developed by**, and
additional license terms. The product name is always the name you reserved.

Take screenshots in the Preview: choose **Windows 11**, open the preview options, turn on
**Pin to 1280×720**, then **Add to the Microsoft Store listing › Screen** (1920 × 1080).

Every listing change is a submission that Microsoft certifies, like a new package. Send
it on its own with **Send to the Microsoft Store** on the listing screen (no build, no
credits), or with the next **Update**.

A few things to know:

- **Screenshots stay in Partner Center until you add your own.** The Store can't send
  images back, so an import brings the texts only, and a language without screenshots
  keeps the ones in Partner Center. Once you add screenshots, they replace those.
- A language without its own screenshots or tile icon uses the default language's.
- Languages that Partner Center has and Studio doesn't are left as they are.

## Questions

### Is the Store app signed with my Artifact Signing certificate?

No. Microsoft signs Store packages itself, so Studio doesn't sign the files inside
them either, even if you [sign your Windows app](desktop.md#sign-the-windows-app): Store
packages don't use up your Artifact Signing signatures.

### Can I publish an update while one is in certification?

No. Partner Center takes one submission at a time: wait until it's published, or delete
it in Partner Center.
