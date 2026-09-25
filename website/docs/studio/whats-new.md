---
title: "What's new"
---

# What's new in Flet Studio

New features, improvements, and bug fixes in Flet Studio, listed in
reverse-chronological order. Flet Studio ships independently of the Flet SDK — see
[Flet release notes](../updates/release-notes.md) for SDK changes.

## September 25, 2026

* **Get more done with your AI credits.** Recent model releases and lower model
  pricing let you do roughly **5–10 times more AI work with the same credits**
  than before, depending on the task and agent tier.
* Choose between **Pro** and **Expert** AI agents in the message composer. Pro is
  available to everyone; Expert is available with a paid plan or an existing
  wallet credit balance. Studio remembers your selection.
* Creator now offers **annual billing at $300/year** — equivalent to $25/month,
  with two months free compared with monthly billing at $30/month. Plan AI credits
  still reset monthly when you pay annually.
* Manage your billing interval in the billing portal. Switching from monthly to
  annual billing is prorated; switching from annual to monthly billing takes
  effect at the end of your paid year.
* Creating private apps and making public apps private now requires the
  **Creator plan**. Existing private apps on Explorer keep working.
* On-demand AI credit top-ups are now available only on paid plans. Explorer
  users can continue spending wallet credits they already hold.
* Newly added wallet AI credits expire **12 months after they are added**.
  Existing wallet credits remain non-expiring. Credits with the earliest expiry
  are spent first, and account settings show how many credits expire next and
  when.
* Credit-pack purchases now appear in the billing portal's invoice history.

## September 15, 2026

* Flet Studio now uses **Flet 1.0.0**, including the updated API reference available
  to its AI agent. See the [Flet 1.0 announcement](/blog/flet-1-0) for what's new
  in the SDK.
* Refreshed Flet and Flet Studio logos for light and dark themes.
* The agent creates app icons at **1024 × 1024** or larger and has updated guidance
  for Flet 1.0's icon generation: one source image for all platforms, transparent
  backgrounds, and platform-appropriate framing and background colors.
* Fixed an extra blank app being created when the app-creation action replayed
  after signing in. Also fixed a race that could lose that action when the
  sign-in dialog closed.

## August 26, 2026

* The agent's activity list is much quieter. Lookups — API references, icon searches,
  file reads — now fold into a single expandable row, so what the agent *changed* stands
  out from what it merely read along the way. Expand any row to see every call it made.
* File edits show an inline diff with added and removed line counts, so you can see
  exactly what changed without opening the file.
* File names in the activity list are links — click one to open it in the editor.
* Clearer wording and a distinct icon for every tool the agent uses.
* Fixed an error that could stop a run when you sent a follow-up message in a long
  conversation.
* Your unsaved edits are no longer overwritten when the agent changes the same file
  you're typing in.

<img src="/img/docs/studio/agent-tool-activity.png" className="screenshot-60" style={{borderRadius: '7px'}} alt="Agent activity list with a grouped lookup row, an inline diff, and clickable file links" />

## July 14, 2026

* New AI agent that helps you build and modify Flet apps with natural-language instructions.
* Paid Creator plan and AI credit packs, with billing powered by Stripe.
* Flet Studio newsletter — manage your subscription in account settings.
* Updated [Terms of Service](terms-of-service.md) and [Privacy Policy](privacy-policy.md) to cover AI features, paid plans, and the newsletter.

## May 29, 2026

* New sign in options: Google and Microsoft.

## May 26, 2026

* The initial public release of Flet Studio.
