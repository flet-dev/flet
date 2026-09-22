---
title: "Client actions"
---

import {CodeExample} from '@site/src/components/crocodocs';

Some things a browser can do are only allowed while it is handling a click or a
key press: opening a file picker, writing to the clipboard, showing a share
sheet, opening a new tab. The permission lasts for that one gesture and no
longer.

That is a problem for the usual Flet pattern. When you call
[`FilePicker.pick_files()`](../services/filepicker.md#flet.FilePicker.pick_files)
from an `on_click` handler, the click travels to your Python code, your code
runs, and the instruction to open the dialog travels back - by which point the
browser no longer considers a gesture to be in progress and quietly refuses.

Safari enforces this strictly, Chrome and Firefox are lenient about it, so the
symptom is confusing: the same app works on Android and on the desktop, and
silently does nothing on an iPhone or iPad. Nothing is logged, because from the
browser's point of view nothing went wrong.

**Client actions** close that gap. An action is attached to a control instead of
being called from a handler, so the client already knows what to do when the tap
arrives and can do it immediately, inside the gesture:

```python
ft.Button("Upload", action=ft.PickFiles(file_picker, allow_multiple=True))
```

## Opening a URL

[`OpenUrl`](../types/openurl.md) opens a link. Opening a *new tab* is the part
that browsers guard, since that is what a popup blocker exists to stop.

<CodeExample path="services/url_launcher/open_url_action/main.py" language="python" />

The [`url`](../controls/button.md#flet.Button.url) property that controls have
always had works the same way and is unchanged - `OpenUrl` is for when you want
to combine it with other actions, or keep every gesture-gated operation written
the same way.

## Copying to the clipboard

<CodeExample path="services/clipboard/copy_action/main.py" language="python" />

## Sharing

<CodeExample path="services/share/share_text_action/main.py" language="python" />

## Picking files

[`PickFiles`](../types/pickfiles.md) is the action that fixes file picking in a
web app on iOS.

Because the dialog opens before your code sees the click, the selection cannot
be returned to a caller the way `pick_files()` returns it. It arrives at
[`FilePicker.on_result`](../services/filepicker.md#flet.FilePicker.on_result)
instead. The picked files stay associated with the `FilePicker`, so
[`upload()`](../services/filepicker.md#flet.FilePicker.upload) works exactly as
before.

<CodeExample path="services/file_picker/pick_files_action/main.py" language="python" />

## What each action maps to

| Action | Equivalent method |
|---|---|
| [`OpenUrl`](../types/openurl.md) | [`UrlLauncher.launch_url()`](../services/urllauncher.md#flet.UrlLauncher.launch_url) |
| [`CopyToClipboard`](../types/copytoclipboard.md) | [`Clipboard.set()`](../services/clipboard.md#flet.Clipboard.set) |
| [`ShareText`](../types/sharetext.md) | [`Share.share_text()`](../services/share.md#flet.Share.share_text) |
| [`PickFiles`](../types/pickfiles.md) | [`FilePicker.pick_files()`](../services/filepicker.md#flet.FilePicker.pick_files) |

An action runs first, then your `on_click` handler is called as usual - so you
can still react to the click in Python.

A control accepts a list as well as a single action, if you need more than one:

```python
ft.Button(
    "Copy and open",
    action=[ft.CopyToClipboard(link), ft.OpenUrl(link, target=ft.UrlTarget.BLANK)],
)
```

## Limits

**An action's arguments are fixed before the click.** This follows from what an
action is - the client has to know the whole operation in advance, because there
is no time to ask. To copy or share a value that changes, update the action when
the value changes, as the clipboard example above does. There is no way around
this; it is the browser's rule, not Flet's.

**Reading the clipboard still prompts.** Safari shows a paste-confirmation UI
for [`Clipboard.get()`](../services/clipboard.md#flet.Clipboard.get) whatever you
do. An action makes the read possible, not invisible.

**Outside the browser this does not apply.** On desktop, Android and iOS apps
there is no such restriction, and the ordinary method calls work fine. Actions
work everywhere, so you can use them unconditionally if your app also runs on
the web - but there is nothing to fix if it does not.
