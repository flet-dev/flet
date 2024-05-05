import 'dart:ui';

import 'package:collection/collection.dart';

Clip? parseClip(String? clip, [Clip? defaultValue]) {
  if (clip == null) {
    return defaultValue;
  }
  return Clip.values.firstWhereOrNull(
          (e) => e.name.toLowerCase() == clip.toLowerCase()) ??
      defaultValue;
}
