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
copy the **Publisher display name** from the app's **Product identity** page, exactly
as shown.

## The first submission

Microsoft takes an app's first submission only in Partner Center, where it also asks
the age-ratings questionnaire. The card walks you through it:

1. **Create Store package (.msix)** and download it.
2. In Partner Center, on the app's overview page, select **Start submission**, then
   complete:
   - **Properties:** a privacy policy URL, required for desktop apps.
   - **Age ratings:** the questionnaire.
   - **Store listings:** a description and at least one screenshot (1366 × 768 or
     larger).
   - **Packages:** upload the `.msix`.
   - **Submission options › Restricted capabilities:** explain why the app needs
     `runFullTrust`. The card has a ready-to-paste explanation.
3. Submit it for certification.

Once Microsoft publishes it, the card shows the app on the Store and Studio sends the
updates.

## Updates

Select **Update** on the card. Studio builds the app, packages it, and submits it
to Partner Center: a new submission that keeps your listing, pricing and age rating
from the last one, with the new package. Certification takes up to three business days;
the card shows where it is (**In certification**, **Published**) and why when it fails,
with a link to the certification report.

### Versions

The Store's versions have three numbers, like `1.2.0`. The first can't be `0`, and the
build number isn't part of them, so **every update needs a higher version**. The
Publish screen says which version the Store has and offers the next one.

## Questions

### Is the Store app signed with my Artifact Signing certificate?

No. Microsoft signs Store packages itself. If you
[sign your Windows app](desktop.md#sign-the-windows-app), the files inside the package
are signed with your certificate too.

### Can I publish an update while one is in certification?

No. Partner Center takes one submission at a time: wait until it's published, or delete
it in Partner Center.
