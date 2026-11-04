---
title: "Privacy Policy"
---

# Flet Studio Privacy Policy

**Effective date:** November 5, 2026

This Privacy Policy explains how **Appveyor Systems Inc.** ("AppVeyor", "we", "us", or "our") collects, uses, shares, and protects personal information in connection with the Flet Studio service ("Flet Studio", "the Service"). Flet Studio is a hosted development environment for building, running, packaging, and publishing applications with the Flet framework.

This policy applies to information we collect from users of Flet Studio at https://studio.flet.dev and through the Flet Studio web application, from visitors to Flet Studio download pages at https://get.flet.app, and from subscribers to the Flet Studio status page at https://status.flet.dev.

---

## 1. Introduction

### 1.1 Who we are

Appveyor Systems Inc. is the operator of Flet Studio. Appveyor Systems Inc. also operates the AppVeyor CI/CD service, which is governed by a separate privacy policy at https://www.appveyor.com/privacy-policy/. This document applies only to Flet Studio.

### 1.2 Our role under GDPR

With respect to the personal information described in this policy (your account profile, sign-in metadata, usage data, the content you create or upload to Flet Studio, and information about visitors to download pages and the status page), **Appveyor Systems Inc. is the data controller**. We determine the purposes and means by which this information is processed.

Separately, when you build a Flet application using Flet Studio and that application collects or processes personal information about *your* own users, you are the controller for that personal information and Appveyor Systems Inc. may act as a processor on your behalf. The same applies to the testers you invite to register their iOS devices for your app (see Section 2.4): you are the controller of their device information, and we process it on your behalf. That relationship is governed by a Data Processing Agreement (DPA), not by this Privacy Policy. Contact us at privacy@flet.dev to discuss a DPA if you require one.

### 1.3 Scope

This policy covers personal information processed by Flet Studio as currently implemented, including paid plans and free trials, credit purchases, AI-assisted development, building, signing, and publishing apps, download pages, GitHub sync, the status page, and email communications. If we add features that materially change how personal information is processed, we will update this policy as described in Section 12.

---

## 2. Information We Collect

### 2.1 Information you provide

**Account profile.** When you create an account, we store the information needed to identify you and authenticate your sessions. This is provided through the identity provider you sign in with (GitHub, Google, or Microsoft) and includes:

- Your email address
- Your full name (if available from the provider)
- A unique user identifier issued by the provider
- Your username or handle (where the provider exposes one)
- Your profile avatar URL

**Account and team information.** For each account, we store the account name, a URL-safe slug, the account type (personal or team), the plan tier, and, for team accounts, the membership and role of each member.

**Content you create or upload.** When you use Flet Studio, we store the app source code, files, and versions that you create, edit, or upload to the Service, along with their metadata (file path, size, timestamps, app name, description, dependencies, tags). This content is stored in object storage hosted by our infrastructure provider, Railway.

**AI conversations.** When you use the AI agent, we store your prompts, the AI's responses (including generated code and a record of the actions the AI took in your project), and any ratings you give on responses. Conversations are stored in our database, per app and per account, until you delete the conversation or the associated app, until your account is deleted, or until the conversation hasn't been used for 30 days (90 days on paid plans), when it is deleted.

**Builds.** When you build an app, we store its build settings (such as its name, version, bundle identifier, icons, and the options you choose), the build's log, steps, and annotations, the files it produces (app packages and installers, "build files"), and when it ran, how long it took, and what it cost. Your app's files, build settings, and the signing material the build needs are sent to the build machine that runs it.

**Signing and publishing credentials.** To sign and publish your apps, you can store credentials in Flet Studio, such as Android keystores and their passwords, Apple App Store Connect API keys and signing certificates, Google Play service account keys, Microsoft Entra application secrets for the Microsoft Store and Azure Artifact Signing, and the names and identifiers that go with them. We store them encrypted (see Section 8) and use them only for the actions you start.

**Store listings.** When you publish to a store, we store the listing details you enter (such as the app's name, description, screenshots, category, support and privacy policy URLs, and contact details) and send them to the store you choose.

**Download pages.** When you publish a build on a download page, we store the page's settings (its name, link, and which builds it offers) and the releases published on it.

**GitHub connection.** When you connect GitHub, we store your GitHub user access and refresh tokens (encrypted), the identifiers of the GitHub App installations you can use, and, for each connected app, the repository, branch, and folder, and a record of the sync (commit identifiers and messages). Commits that Flet Studio makes on your behalf name you as their author, with your GitHub name and GitHub's no-reply email address for your account.

**Billing information.** When you purchase a paid plan or credits, Stripe collects your payment card details and billing address at checkout. We store your Stripe customer and subscription identifiers, your plan status and trial dates, and records of your purchases, credit grants, and credit charges, and we retain billing addresses and purchase records for bookkeeping in QuickBooks Online. When you start a free trial, we also store the card fingerprint Stripe provides for your card (an identifier of the card, not its number), so that each card can be used for only one trial.

**Newsletter subscription.** When you create an account, your email address and name are added to the Flet Studio newsletter mailing list, operated by Mailgun. Your subscription and unsubscribe status is maintained by Mailgun, not in our database. You can unsubscribe at any time using the toggle in account settings, the unsubscribe link in every newsletter email, or your mail client's unsubscribe function.

### 2.2 Information collected automatically

**Sign-in and security data.** When you sign in, we record the timestamp of your most recent successful sign-in and the IP address from which it occurred. We also keep a record of each signed-in session, with the browser's user agent and the IP address it signed in from, so that sessions can be renewed and revoked; and an internal token version counter that is used to invalidate active sessions when you sign out or change credentials. We use this information to maintain account security, detect suspicious activity, and provide an audit trail.

**Usage data.** To enforce per-account quotas and prevent abuse, we maintain daily counters of certain actions (for example, how many gallery clones or archive uploads you have performed in the last 24 hours) and a running total of the storage your account is consuming. These counters are tied to your account, not to individual sign-in sessions.

**Credit usage metering.** For each AI agent run, we record the model used, its token counts, and the resulting credit cost; for each build, we record the minutes charged and their credit cost. These records are kept in a usage ledger tied to your account. We use them to charge usage against your credits and to enforce quotas.

**Server-side telemetry.** When telemetry is enabled, our server software emits operational traces and logs to a server-side observability tool (Pydantic Logfire) to help us diagnose errors, investigate incidents, and monitor performance. These traces may incidentally include account or request identifiers; we apply a PII-scrubbing rule to redact sensitive fields. Telemetry is configurable and is not enabled in all environments.

We do **not** use client-side analytics services. We do not load Google Analytics, Mixpanel, Segment, advertising pixels, or any similar product into the Flet Studio web application or its download pages.

### 2.3 Information from third parties

When you authenticate via GitHub, Google, or Microsoft, we receive the profile fields listed in Section 2.1 from the provider you choose. We do not receive your password for that provider.

When you connect GitHub, you choose which repositories the Flet Studio GitHub App can access. We read and write only those repositories, and only the files of the apps you connect to them. GitHub notifies us when those repositories change (for example, a push, a rename, or a change of visibility).

When you make a purchase, we receive payment and subscription status events from Stripe (for example, that a payment succeeded, a subscription renewed, a trial is about to end, or a subscription was cancelled). These events reference Stripe identifiers.

When you publish an app, we receive information from the store or service you publish to through your account, such as app records, build and review status, and, for Apple, the list of registered devices.

### 2.4 People who are not Flet Studio users

**Download page visitors.** When someone opens a download page or downloads a build from it, we use their IP address briefly to limit the rate of requests, and we count how many times install and registration links are used. Download pages are served through Cloudflare (see Section 5.1).

**Reports about download pages.** Anyone can report a download page. A report contains the reason, any details the reporter writes, the reporter's email address if they choose to give it, and a one-way hash of their IP address, which we use to recognize repeated reports from the same visitor without storing the address itself.

**iOS testers.** When a tester registers an iPhone or iPad through a device registration link, the device sends its identifier (UDID), model, and name to Flet Studio, and we register the device with the app owner's Apple Developer account. We do not keep our own copy of this information; it is kept by Apple in the app owner's account.

**Status page subscribers.** When someone subscribes to updates on the status page, we send a confirmation email, and once they confirm, their email address is added to a mailing list kept by Mailgun. Every email includes a link to unsubscribe.

---

## 3. How We Use Information

We use personal information to:

- Provide the Service: authenticate you, render your accounts and projects, store and serve your content
- Operate AI-assisted development features: your prompts, conversation history, and the project context needed to generate a response are sent to our AI model providers (see Section 5.1)
- Build, sign, and publish your apps as you request, including sending them to the stores you choose and hosting your download pages
- Sync your apps with the GitHub repositories you connect
- Improve the Service: we may review AI conversations to diagnose problems with the AI features and improve their quality (for example, refining prompts, tooling, and agent behavior)
- Process payments, charge AI and build usage against your credits, maintain billing and credit-usage records, and calculate applicable taxes
- Check eligibility for free trials, and prevent repeat trials
- Send the Flet Studio newsletter with product news and updates; you can opt out at any time (see Section 2.1)
- Send status page updates to people who subscribed
- Enforce per-account limits, handle reports about download pages, and prevent abuse of the Service
- Maintain the security and integrity of the Service, including investigating fraud, abuse, or unauthorized access
- Diagnose, debug, and improve the Service through server-side telemetry
- Communicate with you about your account or service-related matters when you contact us
- Comply with legal obligations

We do **not** use your personal information or User Content for advertising, for profiling, or for automated decision-making that produces legal or similarly significant effects (for example, suspending an account by algorithm with no human review), and we do **not** use them to train machine-learning models, nor do we permit our AI model providers to do so (see Section 5.1).

---

## 4. Legal Bases for Processing (GDPR)

If you are located in the European Economic Area, the United Kingdom, or Switzerland, we rely on the following legal bases under the GDPR (or its UK equivalent) when we process your personal information:

- **Performance of a contract**: to provide the Service you have signed up for. This covers account creation, authentication, storage of your content, quota enforcement, paid subscriptions, free trials, and credit purchases, the AI features you invoke, and the builds, signing, publishing, download pages, and GitHub sync you request.
- **Legitimate interests**: to keep the Service secure, prevent abuse (including repeat free trials and abuse of download pages), handle reports, debug and improve the Service, maintain operational telemetry, and send the Flet Studio newsletter to existing account holders with product news and updates (with an easy opt-out at any time and the right to object described in Section 10).
- **Compliance with a legal obligation**: when we are required to retain, disclose, or process personal information to comply with applicable law (for example, retaining billing records for tax purposes).
- **Consent**: for status page subscriptions, which you confirm by email and can withdraw at any time with the unsubscribe link. If we introduce other features that require consent, we will request it separately and you will be able to withdraw it at any time.

---

## 5. How We Share Information

We do not sell your personal information. We do not share your personal information with third parties for advertising or for cross-context behavioral advertising of any kind.

We share personal information only with the following categories of recipients:

### 5.1 Service providers (subprocessors)

We rely on a small number of third-party service providers to operate Flet Studio. Each acts as a processor on our behalf and is bound by appropriate contractual obligations:

| Service provider | Purpose | Data shared |
|---|---|---|
| **GitHub, Google, Microsoft** | OAuth identity providers used to authenticate accounts | Authentication exchange; we receive the profile fields listed in Section 2.1 from the provider you choose |
| **Railway** | Hosting for our application servers, our managed PostgreSQL database, and the object storage that holds user-uploaded content, build files, and download page releases | All personal information stored by the Service is hosted on Railway infrastructure |
| **Google Cloud (Compute Engine)** | Single-use build machines for Linux, Android, web, and Windows builds, in the United States | Your app's files, build settings, and the signing material the build needs, for the duration of the build |
| **Dedicated Mac (dedicatedmac.io)** | Hosting for the Mac computers that run our macOS and iOS build machines, in a data center in Phoenix, Arizona, United States | Your app's files, build settings, and the signing material the build needs, for the duration of the build |
| **Cloudflare** | DNS and network proxy for download pages (get.flet.app); hosting for the status page (status.flet.dev) | Visitors' IP addresses and request details; status page subscribers' email addresses while a subscription is confirmed |
| **xAI** | AI model provider for the AI agent | Your prompts, conversation history, app source code and files (including images), and your name, email address, and username. Sent only when you use AI features; **not used to train models** |
| **OpenAI** | AI model provider for the AI agent | Same as xAI; **not used to train models** |
| **Stripe** | Payment processing, subscription and trial management, and tax calculation | Email address, account identifier, plan, and, collected by Stripe directly at checkout, your billing address and payment card details; your purchase history; the card fingerprint used for free trials |
| **Mailgun** | Newsletter and email delivery, including free trial reminders; the status page mailing list | Email address, full name, and newsletter subscription/suppression status; status page subscribers' email addresses |
| **Pydantic Logfire** | Server-side observability and tracing | Request traces, query traces, and error spans; PII-scrubbed before transmission |
| **Intuit QuickBooks Online** | Accounting and bookkeeping | Billing address, purchase and invoice records |

Our agreements with our AI model providers do not permit them to use your data to train their models.

### 5.2 Services you connect

When you direct us to, we send your information to services you use with your own account:

- **Apple** (App Store Connect, TestFlight, and the Apple notary service): your app, its build files, store listing, and the iOS devices your testers register
- **Google** (Google Play Console): your app, its build files, and store listing
- **Microsoft** (Partner Center and Azure Artifact Signing): your app, its build files, and store listing, and the files to be signed
- **GitHub**: your app's files and the commits that sync them, in the repositories you connect

These services act as independent controllers under their own privacy policies, not as our processors.

### 5.3 Public content

Content you make public can be seen by anyone: public apps (their source code and description) and download pages (their builds and the details shown on them, to anyone with the link).

### 5.4 Legal and safety disclosures

We may disclose personal information when we believe in good faith that disclosure is required by law or by a valid legal process (such as a subpoena or court order).

### 5.5 Business transfers

If Appveyor Systems Inc. is involved in a merger, acquisition, reorganization, or sale of assets, personal information may be transferred as part of that transaction. We will notify you of any change in ownership or material change in the use of your personal information.

---

## 6. Cookies and Similar Technologies

Flet Studio uses only what is strictly necessary to keep you signed in. Specifically:

- A single authentication cookie named `flet_studio_auth`, transmitted only over HTTPS in production environments
- A JSON Web Token stored in your browser's `localStorage` (via the Flet framework's shared-preferences mechanism), used to maintain your session

Download pages do not set cookies. We do **not** set any advertising cookies, analytics cookies, social-media cookies, or other tracking technologies. Because we use only strictly-necessary technologies, we do not display a cookie consent banner.

---

## 7. Data Retention

- **Account data** (profile fields, account/team records) is retained for as long as your account is active.
- **User content** (apps, files, versions) is retained for as long as your account is active or until you delete it.
- **Sign-in metadata** (last sign-in timestamp, last sign-in IP) is overwritten on each new sign-in; older values are not kept. **Session records** are kept while the session can still be used (up to 7 days without activity) and are deleted after it is signed out or expires.
- **Usage counters** are kept per day and are not retained beyond what is needed for quota enforcement and operational analysis.
- **AI conversations** are deleted 30 days after the conversation was last used (90 days on paid plans), or earlier when you delete the conversation or the associated app, or your account is deleted. A conversation in active use keeps its earlier messages.
- **Build logs** (a build's log, steps, and annotations) are deleted 30 days after the build (1 year on paid plans); a short record of each build (what was built, when, its status and cost) is kept with the app. **Build files** are deleted after 7 days (90 days on paid plans), and sooner when newer builds of the same kind replace them. **Download page releases** expire after 7 days (1 year on paid plans).
- **Signing and publishing credentials** and **GitHub tokens** are kept until you delete them or disconnect, or until your account is deleted.
- **Free trial card fingerprints** are kept for as long as we offer free trials, including after the account that used the trial is deleted (without a link to that account), so that each card can be used for only one trial.
- **Reports about download pages** are kept for 2 years.
- **iOS device information** registered by testers is not kept by Flet Studio; it is kept by Apple in the app owner's account.
- **Status page subscriptions** are kept by Mailgun until the subscriber unsubscribes.
- **Billing records** (purchase and credit-usage ledgers, invoices) are retained for as long as required by applicable tax and accounting law, generally seven years in Canada, even after account deletion.
- **Newsletter list membership** is maintained by Mailgun until you unsubscribe; when we process an account-deletion request, we also remove your address from the mailing list.
- **Server-side telemetry** (Logfire traces and logs) is retained for a limited period configured with our observability provider.
- We may adopt shorter retention periods for specific data categories in the future; if we do, we will update this policy.
- **Account deletion**: when you request deletion of your account, we delete or anonymize your account profile, content, credentials, GitHub connections, download pages, and associated records within 30 days, except where we are required to retain certain information to comply with legal obligations or to resolve disputes.

To request deletion, email privacy@flet.dev from the email address associated with your account.

---

## 8. Data Security

We protect personal information using a combination of technical and organizational measures:

- All traffic between your browser and Flet Studio is encrypted in transit using TLS.
- Personal information is stored on infrastructure operated by Railway, which provides encryption at rest for managed databases and object storage.
- Signing and publishing credentials and GitHub tokens are additionally encrypted with their own keys (AES-GCM envelope encryption), under master keys that are kept outside the database. They are decrypted only to perform an action you started.
- Build machines are used for a single build and deleted afterwards. Each build can reach only its own files, using a token that works only for that build, and macOS build machines are isolated from each other on the network.
- Access to production systems is limited to personnel who require it for their role, authenticated using strong credentials.
- Authentication tokens carry a version claim that allows us to revoke all of your active sessions immediately when needed.

No method of transmission or storage is perfectly secure, but we work to maintain protections appropriate to the sensitivity of the information we handle.

---

## 9. International Data Transfers

Appveyor Systems Inc. and our infrastructure providers may store and process personal information in jurisdictions other than the one in which you reside. In particular, builds run on machines in the United States (Google Cloud, and Mac computers hosted in Phoenix, Arizona). Where personal information of users located in the European Economic Area, the United Kingdom, or Switzerland is transferred to a country that has not been recognized as providing an adequate level of data protection, we rely on appropriate safeguards, including the European Commission's Standard Contractual Clauses or equivalent mechanisms.

---

## 10. Your Rights (EEA, UK, and Swiss Residents)

If you are located in the European Economic Area, the United Kingdom, or Switzerland, you have the following rights with respect to your personal information under applicable data-protection law:

- **Right of access**: to obtain confirmation as to whether we process personal information about you, and to receive a copy of that information
- **Right to rectification**: to have inaccurate personal information corrected and incomplete information completed
- **Right to erasure ("right to be forgotten")**: to have your personal information deleted in the circumstances described in the GDPR
- **Right to restriction of processing**: to have processing limited in certain circumstances
- **Right to data portability**: to receive your personal information in a structured, commonly-used, machine-readable format and to transmit it to another controller
- **Right to object**: to object to processing carried out on the basis of our legitimate interests
- **Right to lodge a complaint**: with the data-protection supervisory authority in the country where you live or work, or where the alleged infringement took place

To exercise any of these rights, email **privacy@flet.dev** from the email address associated with your account. If you are an iOS tester, please contact the owner of the app you registered your device for, since your device information is kept in their Apple Developer account. We will respond to your request within the time limits prescribed by applicable law (generally one month). We will not discriminate against you for exercising any of your rights.

---

## 11. Children's Privacy

Flet Studio is not directed to children under the age of 16, and we do not knowingly collect personal information from children under 16. If we become aware that we have collected personal information from a child under 16 without verified parental consent, we will take steps to delete that information. If you believe a child has provided us with personal information, please contact us at privacy@flet.dev.

---

## 12. Changes to This Policy

We may update this Privacy Policy from time to time to reflect changes to the Service or to our legal obligations. When we make material changes, we will update the "Effective date" at the top of this policy and, where appropriate, notify you through the Service or by email before the changes take effect. Your continued use of Flet Studio after a change takes effect constitutes acceptance of the revised policy.

---

## 13. Contact Us

If you have questions about this Privacy Policy or about how Flet Studio handles your personal information, please contact us:

**Appveyor Systems Inc.**
Email: privacy@flet.dev
