---
title: "Writing good requests"
---

# Writing good requests

The agent sees your app's files and this chat. It doesn't see your screen, which device
your preview shows, or what you have in mind. The more of that you put in words, the
fewer requests a change takes, and the fewer credits it costs.

## Start a new app

Say what the app is for, who uses it, its main screens and what it keeps:

> A habit tracker for my phone. A list of habits with a checkbox for today, a screen to
> add a habit with a name and an icon, and a weekly streak chart. Save everything on the
> device. Calm green colors.

The agent asks about anything open, once. Answer in full words ("store it on the device,
no account"), or reply "use your defaults". A short "ok" means its defaults.

Start from a working core, then add to it. A whole product spec in one message is built
in parts, and whatever doesn't fit is left for later.

## One change at a time

A request with one clear change is done well. Several changes in one message work too,
and the agent shows them as a plan, but keep them related and few: in a long list, an
item can get less attention than you meant. For a large feature, ask for it in steps and
check each one in the preview.

## Say what you see and what you want

Name the screen and the control, and describe what's wrong and what you expect:

| Instead of | Try |
|---|---|
| It doesn't work | Tapping **Save** on the Add habit screen does nothing. It should save the habit and go back to the list. |
| Make it look better | On the list, put each habit on a card with 12 px padding and a rounded border, and make the checkbox bigger. |
| Change the color | Use `#2E7D32` for the app bar and buttons. |
| Fix the layout | On the iPhone, in portrait, the chart overflows the screen on the right. It should fit the width. |

Give colors as hex codes and sizes in pixels when they matter. Words like "luxury",
"modern" or "animated" leave a lot to guess: say what you'd see.

## Say which device

Your preview can show a phone, a tablet or a desktop window (the device menu above the
preview), and a layout that's fine on one can break on another. The agent doesn't know
which one you're looking at, so name it ("on the Android phone, in landscape"), or ask it
to check: "take a screenshot on the iPhone and fix what's cut off". Mention dark mode if
your device uses it.

## Errors: paste the text

When the app shows **Script error** or the Console has red lines, paste that text into
your message. With the traceback, a fix usually takes one request; without it, the agent
has to guess. You can also ask it to run the app and read the Console itself: "run it and
fix the error".

`print()` and logging output appear in the **Console** too. Ask the agent to add logging
when a bug is hard to pin down.

## Screenshots need a sentence

The agent sees an attached screenshot, but not what bothers you about it. Add one line:
"the Save button is hidden under the keyboard" is enough.

## Pasted code

Say what to do with it: replace the app, add it as a new file, or keep it exactly as it
is. Paste only the part that matters, not a whole minified library.

## Ask before it changes anything

To explore first, say so: "explain how saving works, don't change anything", or "plan
how you'd add login, then wait". You get an answer, and nothing in the app changes until
you say go.

## A new topic, a new chat

When you move to a different feature, or to a different app idea, start a
[new chat](index.md#chats) with a summary. The agent stays focused, and requests stay
fast and cheap. Starting another app in the same project's chat can replace screens you
meant to keep: for a new idea, create a new app.

## Small edits: do them yourself

Changing a label, a color or a number in the editor is instant and free. Leave the agent
the changes that span files or need thinking.

## Keep the preview visible

The agent runs your app in your preview to check its work. Keep the Studio tab open and
in front while it works: in a background tab, it can't run the app or take screenshots.

## Undo instead of explaining

If a change went the wrong way, restore the version from before it (**Versions**), or
ask "undo that", then ask again, more specifically. It's quicker and cheaper than steering
a wrong change back. See [Versions and undo](index.md#versions-and-undo).
