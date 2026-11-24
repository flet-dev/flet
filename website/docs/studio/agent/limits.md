---
title: "Credits, limits and gotchas"
---

# Credits, limits and gotchas

What the agent costs, how far one request goes, what the agent can't do, and the
surprises to expect, with what to do about them.

## What a request costs

The agent uses [credits](../publishing/index.md#plans): your plan's monthly credits
first, then credit packs. A request is charged as it works, step by step, so its cost
depends on how much it does:

- While it runs, the status shows the credits so far (**≈ 6 credits…**). Past 250, it
  adds **a large request — Stop ends it with a summary**.
- When it's done, the reply shows what it cost (**13 credits**).
- The credits box under the message field shows what's left; click it for
  **Settings › Usage & billing**.

What makes a request cost more:

- **More work.** Reading many files, several runs of the app and long edits all add
  steps.
- **A long chat.** Every request sends the conversation to the agent, so the same
  request costs more late in a long chat. Start a [new chat](index.md#chats) with a
  summary when you move on to something new.
- **Expert.** The Expert agent uses credits faster than Pro.

Editing code yourself and running the preview cost nothing.

### A limit per request

The tier menu (**Pro ▾**) has **Credits per request**: **No limit** (the default), **Up
to 100**, **Up to 250** or **Up to 500**. With a limit, the menu reads like **Pro · 250
max**. When a request reaches it, the agent stops with **Stopped at your limit of 250
credits for one request** and sums up what it changed and what's left; send a message to
continue.

### Running out

If your account runs out of credits in the middle of a request, the request stops and
keeps what it changed: **AI credit limit reached — this run was stopped. Completed
changes were kept.** Buy a credit pack or move to Creator to continue.

### When you're not charged

- **The AI service failed** (it was overloaded, didn't respond, or dropped the
  connection): the request isn't charged, and its message says **You weren't charged
  for this request.**
- **It failed before the agent did anything**: nothing is charged.

A request that stops for another reason, such as **Stop**, your limit, or the agent
getting stuck, is charged for the work it did, and that work is kept.

## Limits of one request

- **One request at a time per app.** Sending another while the agent works says **The
  agent is already working on this app.**
- **About 14 minutes of work at a time.** A longer request continues by itself twice,
  then pauses; send a message to keep going. Nothing done so far is lost.
- **6 runs and 6 screenshots of the app per request.** The agent checks its work, but
  doesn't loop on it.

## What the agent can't do

- **Open links or search the web.** Paste the part of the docs or the API reference you
  want it to use.
- **See your screen or your phone.** It sees the app's files, this chat, and the preview
  when it runs or screenshots the app. Describe what you see, or attach a screenshot
  with a sentence.
- **See files you pick in the running app.** A file your app opens is in your browser,
  not in the project. Attach it to the chat instead.
- **Run commands.** There's no terminal: it adds packages to `pyproject.toml` rather than
  running `pip`, and it can't run test suites.
- **Start builds or releases by itself.** It suggests them; you start them. See
  [Publishing with the agent](index.md#publishing-with-the-agent).
- **Handle secrets.** It doesn't put API keys or passwords into your app's files, and
  signing keys never go through the chat. Don't paste live keys or passwords into the
  chat.
- **Work on other apps, or other topics.** It's scoped to the app you're in, and to Flet.

## Gotchas

### The preview runs in your browser

Your app's preview runs Python in the browser with
[Pyodide](https://pyodide.org/), not on a computer or a phone. Most apps run the same,
but some things only work in a built app (see
[What are the limitations?](../index.md#limitations)). The agent knows these rules and
says when a feature won't work in the preview. Expect these:

- **Packages.** Pure-Python packages and those Pyodide ships work. One with native code
  that Pyodide doesn't have fails to install, and the whole preview fails with it. Flet's
  own extensions (charts, maps, video, audio, camera, Lottie, Rive, data tables, code
  editor, color pickers, WebView, location, shadcn/ui and more) work.
- **No threads, subprocesses or `time.sleep`.** Long work blocks the app: the agent uses
  `async` code instead. Programs that drive other apps or a browser (Selenium,
  Playwright, pyautogui) don't run.
- **Web requests** go through the browser: the agent uses `httpx2` for them, and the API
  must allow requests from other sites (CORS). If it doesn't, the request fails in the
  preview but works in a built app.
- **Files and storage.** The app can't read your disk by path. Settings and small data
  are saved with `SharedPreferences`.
- **Device features.** Camera, microphone and location depend on what the browser
  allows. Phone-only features, such as locking the orientation or native Android and iOS
  libraries, work only in a built app.

### A change didn't take, or it keeps trying

- **Paste the error** (the **Script error** text or the red Console lines), or say exactly
  what you see and what you expected. See [Writing good requests](requests.md).
- **Name the device** for layout problems.
- **Undo and ask again**, more specifically, instead of steering a wrong change back
  ([Versions and undo](index.md#versions-and-undo)).
- **Start a new chat** with a summary when a chat is long and the agent repeats itself
  or loses track.
- **Try Expert** for a problem Pro can't crack.

### Messages you may see

| Message | What to do |
|---|---|
| The agent says the Studio tab is in the background, or that it couldn't run the app | Keep the Studio tab open and in front while the agent works, so it can run the app. |
| This task is taking longer than the time budget allows | Send a message, such as "continue". Everything done so far is kept. |
| Stopped before finishing. Send a message to continue. | The request ended early; what it changed is kept. Send a message to continue. |
| Lost the connection to the agent | It may still be working: reload the page. |
| The AI service is handling too many requests right now | Try again in a moment. You weren't charged. |
| The agent got stuck | What it changed is kept. Try again, more specifically, or in a new chat. |
