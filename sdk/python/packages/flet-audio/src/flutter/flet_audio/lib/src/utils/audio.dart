import 'package:audioplayers/audioplayers.dart';
import 'package:collection/collection.dart';

ReleaseMode? parseReleaseMode(String? value, [ReleaseMode? defaultValue]) {
  if (value == null) return defaultValue;
  return ReleaseMode.values.firstWhereOrNull(
          (e) => e.name.toLowerCase() == value.toLowerCase()) ??
      defaultValue;
}
