import 'package:audioplayers/audioplayers.dart';
import 'package:flet/flet.dart';

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
