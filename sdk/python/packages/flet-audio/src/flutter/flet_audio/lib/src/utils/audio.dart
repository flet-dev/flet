import 'package:audioplayers/audioplayers.dart';
import 'package:collection/collection.dart';
import 'package:flet/flet.dart';

ReleaseMode? parseReleaseMode(String? value, [ReleaseMode? defaultValue]) {
  if (value == null) return defaultValue;
  return ReleaseMode.values.firstWhereOrNull(
          (e) => e.name.toLowerCase() == value.toLowerCase()) ??
      defaultValue;
}

AudioContext? parseAudioContext(dynamic value) {
  if (value is! Map) return null;

  final config = AudioContextConfig(
    route: parseEnum(AudioContextConfigRoute.values, value["route"]?.toString(),
        AudioContextConfigRoute.system)!,
    focus: parseEnum(AudioContextConfigFocus.values, value["focus"]?.toString(),
        AudioContextConfigFocus.gain)!,
    respectSilence: parseBool(value["respect_silence"], false)!,
    stayAwake: parseBool(value["stay_awake"], false)!,
  );

  return config.build();
}
