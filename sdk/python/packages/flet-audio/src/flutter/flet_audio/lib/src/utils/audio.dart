import 'package:audioplayers/audioplayers.dart';
import 'package:flet/flet.dart';
import 'package:flutter/foundation.dart';

ReleaseMode? parseReleaseMode(String? value, [ReleaseMode? defaultValue]) {
  return parseEnum(ReleaseMode.values, value, defaultValue);
}

AudioContextConfigFocus? parseAudioFocus(String? value,
    [AudioContextConfigFocus? defaultValue]) {
  return parseEnum(AudioContextConfigFocus.values, value, defaultValue);
}

/// Parses an `AudioContext`, or its defaults when [value] isn't set.
///
/// The Android focus defaults to `duckOthers` rather than audioplayers' `gain`,
/// under which each player that starts pauses the others for good, unlike on
/// other platforms.
AudioContext parseAudioContext(dynamic value) {
  final Map context = value is Map ? value : const {};
  return AudioContextConfig(
    focus: parseAudioFocus(
        context["focus"]?.toString(),
        isAndroidMobile()
            ? AudioContextConfigFocus.duckOthers
            : AudioContextConfigFocus.gain)!,
    respectSilence: parseBool(context["respect_silence"], false)!,
  ).build();
}

/// Keeps other apps' audio lowered on iOS only while an `Audio` is playing.
///
/// iOS lowers other apps' audio for as long as the app's audio session is active
/// with `duckOthers`, and audioplayers leaves the session active once something
/// has played, so it would stay lowered until the app closes.
///
/// Swapping `duckOthers` for `mixWithOthers` ends the lowering without
/// interrupting other apps' audio. The context is applied again before the next
/// `Audio` plays, because iOS applies a context to the whole app and an `Audio`
/// without its own context plays under the last one applied.
class IosDucking {
  static final _playing = <Object>{};
  static AudioContext? _context;
  static bool _released = false;

  /// Records the context last applied to the audio session.
  static Future<void> contextApplied(AudioContext context) async {
    _context = context;
    _released = false;
    await _releaseIfIdle();
  }

  /// Restores the applied context before [player] starts playing.
  ///
  /// [player] counts as playing from here on, so that another player stopping
  /// before its state changes doesn't end the lowering. If restoring fails, the
  /// next player to start tries again.
  static Future<void> startPlaying(Object player) async {
    _playing.add(player);
    if (!_released) return;
    _released = false;
    try {
      await AudioPlayer.global.setAudioContext(_context!);
    } catch (_) {
      _released = true;
      rethrow;
    }
  }

  /// Ends the lowering if [player] was the last one playing.
  ///
  /// A failure leaves the lowering in place until the next player stops, as no
  /// caller could act on it.
  static Future<void> stopPlaying(Object player) async {
    _playing.remove(player);
    await _releaseIfIdle();
  }

  static Future<void> _releaseIfIdle() async {
    final context = _context;
    if (_released ||
        _playing.isNotEmpty ||
        context == null ||
        !context.iOS.options.contains(AVAudioSessionOptions.duckOthers)) {
      return;
    }
    _released = true;
    try {
      await AudioPlayer.global.setAudioContext(context.copy(
          iOS: AudioContextIOS(
              category: context.iOS.category,
              options: const {AVAudioSessionOptions.mixWithOthers})));
    } catch (error) {
      _released = false;
      debugPrint("Audio context could not stop lowering other audio: $error");
    }
  }

  /// Forgets all state, between tests.
  @visibleForTesting
  static void reset() {
    _playing.clear();
    _context = null;
    _released = false;
  }
}
