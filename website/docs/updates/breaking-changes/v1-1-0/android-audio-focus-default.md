---
title: "Android: every Audio now plays together by default"
---

# Android: every `Audio` now plays together by default

:::note
This guide is accurate as of Flet 1.1.0. Later releases might add new APIs or
additional migration paths.

The [breaking changes and deprecations index](../index.md) lists the guides created for each release.
:::

## Summary

Flet 1.1.0 changes how an [`Audio`][flet_audio.Audio] with no
[`context`][flet_audio.Audio.context] shares audio on Android.

- **Before**: an `Audio` that started playing paused anything else that was
  playing, whether that was another app's audio or another `Audio` of the same
  app. The paused audio didn't resume on its own.
- **Now**: the default is
  [`AudioFocus.DUCK_OTHERS`][flet_audio.AudioFocus.DUCK_OTHERS]. Every `Audio` of
  an app plays together, and other apps' audio usually gets quieter while the
  `Audio` plays, though some apps pause instead, especially for speech. It stays
  quieter while the `Audio` is paused, until the `Audio` is released or finishes
  after resuming.

The previous behavior is still available with
[`AudioFocus.GAIN`][flet_audio.AudioFocus.GAIN].

Only Android changes. On iOS, the default stays `GAIN`: an app's `Audio` never pause
each other there, so the problem this fixes doesn't exist. Other apps' audio is
therefore interrupted on iOS by default, and usually gets quieter on Android.
Windows, macOS, Linux and web ignore `context`.

## Symptoms

No error is raised - the change is audible. On Android, after the upgrade:

- A music player no longer stops the music of another app, which usually keeps
  playing at a lower volume.
- Starting a track while another one plays makes both audible, where starting the
  new track used to silence the previous one.

## Migration guide

### Music players

To keep pausing other apps' audio, set `focus` to `GAIN` on the player:

```python
import flet_audio as fta

player = fta.Audio(
    src="song.mp3",
    context=fta.AudioContext(focus=fta.AudioFocus.GAIN),
)
```

Leave short sound effects on the default. A `GAIN` player keeps playing while an
effect with no `context` plays. Set `focus` to
[`AudioFocus.MIX_WITH_OTHERS`][flet_audio.AudioFocus.MIX_WITH_OTHERS] on an effect
that shouldn't lower the volume of other apps either.

### Playing one track at a time

If your app relied on a new track silencing the previous one, pause the previous
track yourself:

```python
await current_track.pause()
await next_track.play()
```

Setting `GAIN` on every track also pauses the previous one, but
[`on_state_change`][flet_audio.Audio.on_state_change] doesn't fire for that pause, so
the paused track keeps reporting [`PLAYING`][flet_audio.AudioState.PLAYING]. It stays
paused, even after the other track stops, until
[`resume()`][flet_audio.Audio.resume] is called.

### Apps that declare `MODIFY_AUDIO_SETTINGS`

Setting `context` in an app that declares the
`android.permission.MODIFY_AUDIO_SETTINGS` permission resets the device's audio mode
and turns its speakerphone off, which can interrupt a call that the app has in
progress. See [`Audio.context`][flet_audio.Audio.context].

### No action needed for

- Apps that play sound effects over music, or several sounds at once. These now work
  with no `context`.
- Apps that play a single `Audio` and are fine with other apps' audio getting quieter
  while it plays.
- Apps that don't run on Android.

## Timeline

- Changed in: `1.1.0`

## References

- Issue: [#7034](https://github.com/flet-dev/flet/issues/7034)
- Pull request: [#7043](https://github.com/flet-dev/flet/pull/7043)
- Docs: [`AudioContext`][flet_audio.AudioContext], [`AudioFocus`][flet_audio.AudioFocus]
- Release notes: [Flet 1.1.0](../../release-notes.md)
