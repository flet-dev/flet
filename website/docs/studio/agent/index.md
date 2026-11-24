---
title: "AI agent"
---

# AI agent

Describe what you want, and the agent builds it: a new app from an idea, a new screen or
feature, a fix for a bug, or an explanation of how the code works. It edits your
project's files, runs the app in your preview, checks the result, and tells you what it
did.

The agent is the **Agent** panel next to the preview (the **Agent** tab on a phone).
Sign in to use it. On someone else's public app or a gallery example, the same box reads
**Remix**: the app is copied to your account, and your message is the copy's first request.

See [Writing good requests](requests.md) for how to get good results, and
[Credits, limits and gotchas](limits.md) for what it costs and what it can't do.

## What it can do

- **Write and change code.** Create, edit, rename and delete files, across as many
  files as the change needs. Each edit is shown as a diff.
- **Run and check your app.** Restart your preview, read the **Console** (errors and
  `print()` output), and take screenshots of it. A screenshot can be on any preview
  device, such as a phone in landscape. That switches your preview to the device.
- **Use the Flet of your Studio.** The agent looks up the Flet API instead of guessing
  it, for the Flet version Studio runs (**Settings › About › Flet SDK version**), and
  reads built-in guides on layout, colors, animations, input and app structure.
- **Add packages.** It adds them to `pyproject.toml`, and the preview installs them. Your
  preview runs in the browser, so not every package works there: see
  [Gotchas](limits.md#gotchas).
- **Name and describe the app, and draw its icon.** It sets the app's title and
  description and makes `assets/icon.svg`.
- **Save and restore versions** of the app (see [Versions and undo](#versions-and-undo)).
- **Use what you attach**: a screenshot of a bug, a mockup, a PDF spec, a data file or
  an image for the app (see [Attachments](#attachments)).
- **Help publish.** Change build settings, suggest a build or a release for you to
  start, and read a failed build's log to fix the cause (see
  [Publishing with the agent](#publishing-with-the-agent)).

It works on one app: the one you're in. It answers questions about Flet and your app,
not other topics.

## A request, step by step

Type in the box and press **Enter** (**Shift+Enter** for a new line). While the agent
works:

- **The status line** shows what it's doing and for how long, such as
  **Editing src/main.py · 0:32 · step 5**, and the credits used so far
  (**≈ 6 credits…**).
- **Activity rows** list its steps. Reading and searching are grouped (**Explored the
  app · 8 tools**); open a row to see each step. Each change has its own row, such as
  **Edited src/main.py +9 −7**: open it for the diff, or click the file name to open the
  file.
- **A plan** appears for a request with several parts: a checklist the agent ticks off
  as it goes (**Plan · 2 of 4 done**).

When it's done, it says what it changed and how to check it, with the request's credits
under the reply. Your files and preview reload; the preview restarts unless the agent
already ran it after its last change. Rate a reply with 👍 or 👎: it helps us improve the
agent.

The request keeps running if you reload the page or close the tab, and the panel picks it
up again when you come back. To run the app and take screenshots, though, the agent needs
the Studio tab open and visible: in a background tab it carries on without checking its
work.

### A new app

For a new app, the agent first sketches a plan and asks about the choices that matter,
such as what's saved and which screens the app has. It asks once: answer the questions,
or reply "use your defaults". Then it builds the app, names it and draws its icon.

### Stopping

While it works, **Send** becomes **Stop**. The agent finishes its current step and writes
what it changed and what's left; press **Stop** again to end at once. Changes already made
are kept, and the work done is charged. Send a message to continue.

### Editing while it works

You can keep using the editor. **Run** is off until the agent is done. If you have unsaved
changes in a file the agent also edits, yours win when the request ends, and Studio tells
you which file.

## Chats

Each app has one chat with the agent, and the agent remembers it: a follow-up such as
"make it bigger" is about what you just discussed.

**New chat** (at the top of the panel) clears the chat and starts over. It can **Carry
over a summary of this chat**: the agent sums up what was built and decided, and keeps it
in mind in the new chat (shown as **Continued from a previous chat**). The summary costs a
few credits. Clearing a chat also removes the files attached in it; your app's files stay.

Start a new chat for a new feature once a chat gets long. Every request sends the
conversation to the agent, so a long chat makes requests slower and dearer, and the agent
can lose track of early details. After 30 requests, or once a chat is very large, Studio
suggests it: **Long chat: a new one with a summary keeps requests fast and cheaper.**

A chat you don't use for 30 days (90 days on Creator) is removed. Your app isn't.

## Versions and undo

A version is a snapshot of the app's files. **Versions** (the clock at the top of the
panel) lists them: **Create version** saves one, and **Restore this version** puts the
app's files back as they were. Restoring replaces all current files, so create a version
first if you want to keep the current state.

The agent saves a version before a large or risky change. To undo its last change, say
so ("undo that" or "restore the version from before the settings page"), or restore the
version yourself, which costs nothing.

An app keeps up to 20 versions on Explorer and 200 on Creator. An app connected to GitHub
uses its commits instead: each request that changes files is one commit, and **Versions**
lists the branch's commits. See [GitHub sync](../github.md).

## Attachments

Attach files with the paperclip, or paste them (a screenshot from the clipboard works
too):

| What | Up to | The agent… |
|---|---|---|
| Images (PNG, JPEG, GIF, WebP) | 10 MB | sees them |
| PDFs | 10 MB | reads them |
| Text and code (`.py`, `.json`, `.csv`, `.md`, `.toml`, `.yaml`, `.log`, …) | 200 KB | reads them |

Up to 8 files a message. Attachments belong to the chat, not the app: to use one in the
app, such as a logo or a data file, ask the agent to add it to the project.

## Publishing with the agent

The agent knows Studio's [publishing](../publishing/index.md):

- **Build settings.** Ask it to change the app's version, permissions, splash colors or
  other build settings, and it updates `pyproject.toml`. Signing settings are yours to
  set.
- **Builds and releases.** Ask it to build or release, and it suggests the run as a card:
  what will be built, where it goes, and its credits. Nothing starts until you click the
  card's button, such as **Start** or **Send to Google Play**; **Edit on the action
  screen** opens the full form instead. A card expires after a day.
- **Failed runs.** **Ask AI to fix** on a failed run puts a request in the agent's box for
  you to send. The agent reads the run's log, fixes what it can in the app, and suggests a
  new run, or a retry when only the upload failed.
- **Store listings.** **Write with AI** in a store listing does the same for the listing's
  texts.

## Pro and Expert

The tier menu in the box picks the agent:

- **Pro** (default) handles most apps and changes.
- **Expert** is a more capable model for large or tricky work, and uses credits faster.
  It's part of the Creator plan.

The same menu sets a **Credits per request** limit. See
[Credits, limits and gotchas](limits.md).
