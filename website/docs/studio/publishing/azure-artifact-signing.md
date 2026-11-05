---
title: "Azure Artifact Signing"
---

# Azure Artifact Signing

Flet Studio signs your Windows app with your own
[Artifact Signing](https://learn.microsoft.com/azure/artifact-signing/) account, Microsoft's
code-signing service in Azure (formerly called Trusted Signing). Signed, Windows shows your
name as the app's publisher instead of "Unknown publisher", the app runs with Smart App
Control on, and SmartScreen builds up a reputation for it.

This page walks through setting it up in Azure, from an empty subscription to the first
signed build. You do it once: one connection can sign all your apps.

:::note[Creator plan]
Code signing is part of the Creator plan. On Explorer, Windows apps are built unsigned. See
[Plans](index.md#plans).
:::

:::tip[In short]
1. In the Azure portal, **create an Artifact Signing account**, **validate your identity**
   (Microsoft checks who you are: from a day to a few weeks) and **create a certificate
   profile** of type Public Trust.
2. In Microsoft Entra ID, **register an app** for Studio, add a **client secret**, and give
   the app the **Artifact Signing Certificate Profile Signer** role on your account.
3. In Studio, **Connect Azure Artifact Signing** on **Publish › Windows › Settings › Code
   signing**, and enter the names and IDs from steps 1 and 2.
:::

## Before you start

You need:

- **A paid Azure subscription.** Artifact Signing doesn't work with free, trial or
  sponsored subscriptions. If you don't have one, sign up at
  [azure.microsoft.com](https://azure.microsoft.com) and upgrade to pay-as-you-go.
- **To be eligible.** Public Trust certificates, the ones that sign apps for other people's
  PCs, are available to:
  - **organizations** in the United States, Canada, the European Union, the United Kingdom,
    Australia, New Zealand, Japan, South Korea, Singapore, Switzerland, Norway and Israel;
  - **individual developers** in the United States and Canada.
- **The Owner or Contributor role** on the subscription, to create the account and assign
  roles.

What it costs (Microsoft's prices, billed by Azure, not by Studio):

| Tier | Per month | Signatures included | Each extra signature | Certificate profiles |
|---|---|---|---|---|
| Basic | $9.99 | 5,000 | $0.005 | 1 of each type |
| Premium | $99.99 | 100,000 | $0.005 | 10 of each type |

Billing starts as soon as you create the account, and isn't pro-rated. **Basic is enough
for most developers**: every file Studio signs is one signature, and a typical Flet app
signs about 50 files per Windows build, so 5,000 signatures is about 100 signed builds a
month. You can change the tier later; the change applies from the next billing cycle.

:::tip
Start early. Identity validation takes from 1 to 20 business days, and can't be sped up.
You can set up everything else while you wait, but Studio can only connect once it's done.
:::

## Step 1. Register the resource provider

Azure only lets a subscription create Artifact Signing accounts after its resource provider
is registered:

1. In the [Azure portal](https://portal.azure.com), open **Subscriptions** and select your
   subscription.
2. Under **Settings**, open **Resource providers**.
3. Search for **Microsoft.CodeSigning**. Its status is **NotRegistered**: select it, then
   **Register**. After a minute the status is **Registered**.

With the Azure CLI: `az provider register --namespace "Microsoft.CodeSigning"`.

## Step 2. Create an Artifact Signing account

1. In the portal's search box, search for **Artifact Signing Accounts** and open it. Then
   **Create**.
2. Fill in the form:
   - **Subscription**: the one from step 1.
   - **Resource group**: an existing one, or **Create new** (e.g. `signing`).
   - **Account name**: 3 to 24 letters, digits and single hyphens, starting with a letter,
     unique across all of Azure (e.g. `acme-signing`). You can't rename it later. **Note
     it**: Studio asks for it.
   - **Region**: any region near you. **Note it**: Studio asks for it, and signing only
     works at the region's own endpoint.
   - **Pricing**: **Basic** (see above).
3. **Review + Create**, then **Create**. When the deployment finishes, **Go to resource**.

## Step 3. Validate your identity

Microsoft checks that you are who the certificate will say you are. The name it validates
is the one Windows shows as the app's publisher, so use your organization's legal name, or
your own legal name as an individual. It can't be changed afterwards: a mistake means a new
request.

### Give yourself the Identity Verifier role

Even the subscription's Owner can't request a validation without this role:

1. On the Artifact Signing account, open **Access control (IAM)** › **Add** › **Add role
   assignment**.
2. Search for **Artifact Signing Identity Verifier**, select it and **Next**.
3. **Select members**: yourself. Then **Review + assign**.

If **New identity** is greyed out in the next step, the role isn't there yet: wait a few
minutes and reload the page.

### Request the validation

On the account, open **Objects › Identity validations**.

**As an organization:** keep **Organization** selected, then **New identity › Public**, and
fill in:

- **Organization Name**: the legal name of the business, as registered. It goes on the
  certificate.
- **Website url**, **Business Identifier** (e.g. the company registration number) and the
  address.
- **Primary Email** and **Secondary Email**: two different addresses on a domain your
  organization owns (not Gmail or Outlook.com). Microsoft sends verification links to both;
  they expire after 7 days.
- **First Name** and **Last Name** of the person who represents the organization, exactly as
  on their government ID: they verify their identity too.

Microsoft may ask for documents: business registration or articles of incorporation, and
proof that you own the domain. Documents must be issued within the last 12 months.

**As an individual developer** (US and Canada): pick **Individual** in the dropdown, then
**New identity › Public**. The form is filled in from your Azure billing account, which
must be of type **Individual**, with your legal name and address as on your government ID.
You then verify your identity with your phone: a government photo ID, a selfie, and
Microsoft Authenticator to share the verified credential. Your city, state or province and
country appear on the certificate; your street address and email don't.

Check **Certificate subject preview**: this is what Windows will show. Then **Create**.

The request shows **In Progress**, then **Action Required** if Microsoft needs something
from you (you get an email), then **Completed** or **Failed**. If it fails, or a
verification link expired, create a new request.

The validation belongs to the subscription: every Artifact Signing account in it can use
it. It expires after a while: Azure emails you 60 days before, and you renew it on the same
page. If it expires, signing stops until it's renewed.

## Step 4. Create a certificate profile

A certificate profile is what you sign with: it ties your validated identity to the
certificates Microsoft issues.

1. On the account, open **Objects › Certificate profiles** › **Create** › **Public Trust**.
   Public Trust is the type for apps you give to other people. **Public Trust Test** isn't
   trusted by Windows, and **Private Trust** is for apps inside your organization only.
2. Fill in:
   - **Certificate Profile Name**: 5 to 100 letters, digits and single hyphens, starting
     with a letter (e.g. `acme-public`). **Note it**: Studio asks for it.
   - **Verified CN and O**: the identity validation from step 3. The list is empty until
     the validation is **Completed**.
   - **Include street address** and **Include postal code**: optional; they add those to
     the certificate.
3. Check the **Certificate Subject Preview**, then **Create**.

Microsoft issues certificates for the profile automatically. Each one is valid for three
days and renewed daily, so there is nothing to renew or upload. Studio timestamps every
signature, which keeps your signed files valid after the certificate expires.

## Step 5. Register an app for Studio

Studio signs in to Azure as an **app registration**: a separate identity you create for it,
with permission to sign and nothing else. You never give Studio your own Azure sign-in.

1. In the portal, open **Microsoft Entra ID › App registrations › New registration**.
2. **Name**: e.g. `Flet Studio signing`. Keep **Accounts in this organizational directory
   only**, and leave **Redirect URI** empty. **Register**.
3. On the app's **Overview**, copy two IDs. Studio asks for both:
   - **Application (client) ID**
   - **Directory (tenant) ID**

## Step 6. Add a client secret

1. On the app registration, open **Certificates & secrets › Client secrets › New client
   secret**.
2. **Description**: e.g. `Flet Studio`. **Expires**: choose a period (up to 24 months).
   **Add**.
3. Copy the secret's **Value** now: Azure shows it only once. Copy the **Value** column,
   not the **Secret ID**. Note the **Expires** date too.

Keep the value private: with it and the IDs, anyone can sign files with your name until
you delete the secret.

## Step 7. Let the app sign

Give the app registration the **Artifact Signing Certificate Profile Signer** role.
Without it, nothing can sign, not even the subscription's Owner.

1. On the Artifact Signing account, open **Access control (IAM)** › **Add** › **Add role
   assignment**.
2. Search for **Artifact Signing Certificate Profile Signer**, select it and **Next**.
3. **Select members**, and search for the app registration **by name** (e.g. `Flet Studio
   signing`): app registrations aren't listed until you search. Select it, then **Review +
   assign**.

Assigned on the account, the role lets the app sign with every certificate profile in it.
To limit it to one profile, assign it on the profile instead, with the Azure CLI:

```bash
az role assignment create \
  --assignee <Application (client) ID> \
  --role "Artifact Signing Certificate Profile Signer" \
  --scope "/subscriptions/<subscription ID>/resourceGroups/<resource group>/providers/Microsoft.CodeSigning/codeSigningAccounts/<account name>/certificateProfiles/<profile name>"
```

A new role can take up to 10 minutes to work. If Studio says the app can't sign right
after you assign it, wait a few minutes and try again.

## Step 8. Connect in Studio

Open your app's **Publish › Windows › Settings**, and on the **Code signing** card select
**Connect Azure Artifact Signing…**. (Or **Settings › Publishing accounts › Connect
account**, to connect it without an app.) Enter:

| Field in Studio | What to enter | Where it's from |
|---|---|---|
| **Region** | The account's region | Step 2 (the account's **Overview**) |
| **Artifact Signing account** | The account's name | Step 2 |
| **Certificate profile** | The profile's name | Step 4 |
| **Directory (tenant) ID** | A GUID | Step 5 (the app registration's **Overview**) |
| **Application (client) ID** | A GUID | Step 5 |
| **Client secret (Value)** | The secret's value | Step 6 |
| **Secret expires** (optional) | The secret's expiry date, as YYYY-MM-DD | Step 6 |

Then **Connect**. Studio checks the whole setup by signing a test digest once (one
signature on your bill), and shows who the certificate names: your validated organization
or name. The connection is selected for the app; your other apps can choose it on their
own **Code signing** card.

From the next run, Windows builds are signed. To build one unsigned test build, use **Skip
signing for this run** on the **Create Windows app** screen.

## What Studio signs

On every Windows run with signing, Studio signs every file of the app that isn't signed
yet (the `.exe`, and the `.dll` and `.pyd` files of Python and its packages), then the
installer and its uninstaller. Every signature is timestamped by Microsoft's timestamp
service. The run fails if any file isn't validly signed afterwards: Studio never hands you
a half-signed app.

Signing doesn't send your files to Microsoft: Artifact Signing signs a fingerprint (digest)
of each file, not the file itself. The client secret stays on Studio's servers; a build only gets an
access token that expires within the hour and can only sign.

## Keep it working

- **The client secret expires** (at most 24 months after you made it). Studio flags the
  connection 30 days before, on the **Code signing** card and in **Settings › Publishing
  accounts**, if you entered the expiry date. Make a new secret (step 6), then open the
  connection in **Settings › Publishing accounts** › **Update credentials…** and enter
  it. Your apps keep the connection. Then delete the old secret in Azure.
- **The identity validation expires** too. Renew it when Azure emails you, 60 days before
  (step 3).
- **SmartScreen** may still warn for a new app: it builds a reputation from downloads and
  installs, which can take a few weeks. Signing every release with the same profile keeps
  that reputation building.

## If connecting fails

Studio shows Azure's answer next to the field it's about:

| Studio says | What to do |
|---|---|
| Azure didn't accept the client secret: paste its Value, not its Secret ID. | Copy the **Value** of the secret (step 6). If you didn't copy it in time, make a new one. |
| This client secret has expired | Make a new secret (step 6). |
| No app registration with this client ID is in that tenant. | Check both IDs on the app registration's **Overview** (step 5). |
| No Azure tenant has this ID. | Copy the **Directory (tenant) ID** again (step 5). |
| This app registration can't sign with that profile | Assign the **Artifact Signing Certificate Profile Signer** role to the app registration (step 7), wait a few minutes, and try again. Also check that the identity validation is **Completed**. |
| Artifact Signing has no such account or certificate profile at this endpoint | Check the account and profile names, and that **Region** is the account's region. |

## Stop signing, or revoke

- **To stop an app's builds being signed**, use **Stop signing** on its **Code signing**
  card. The connection stays in your Studio account for other apps.
- **To stop Studio signing for good**, disconnect the account in **Settings › Publishing
  accounts**, then delete the client secret (or the app registration) in Azure. Without
  the secret, nobody can sign with it.
- **If someone signed something they shouldn't have** with your profile, delete the
  secret first, then revoke the certificates involved: on the certificate profile, search
  for the certificate's thumbprint › **Revoke**, and pick the date and time from which its
  signatures stop being valid. Revoking can't be undone and needs the Owner role on the
  subscription; see Microsoft's
  [revocation guide](https://learn.microsoft.com/azure/artifact-signing/how-to-cert-revocation).
  Deleting a profile or account stops new signatures, but doesn't revoke files already
  signed.

## Questions

### Can I use the account for other things too?

Yes. The account and profile are yours: you can also sign with them yourself, with
SignTool or in your own CI. Signatures from everywhere count towards the same monthly
allowance.

### Can I sign with my own certificate (.pfx)?

Not yet. Certificates for code signing now have to live in a hardware or cloud key store,
which Artifact Signing is.

### I'm outside the eligible countries. Can I still sign?

Not with Public Trust yet: Microsoft decides who it can validate. You can still build your
app unsigned (Windows shows "Unknown publisher" and SmartScreen warns before it runs), or
publish it on the [Microsoft Store](microsoft-store.md), where Microsoft signs it and no
code-signing certificate is needed.

### Do I need an EV certificate?

No. Artifact Signing doesn't issue EV certificates, and EV no longer skips SmartScreen's
reputation check anyway.
