import 'dart:convert';

import '../models/control.dart';
import 'numbers.dart';

Duration? parseDuration(Control control, String propName,
    [Duration? defaultValue]) {
  var v = control.attrString(propName, null);
  if (v == null) {
    return defaultValue;
  }

  final j1 = json.decode(v);
  return durationFromJSON(j1);
}

Duration? durationFromJSON(dynamic json, [Duration? defaultValue]) {
  if (json == null) {
    return defaultValue;
  }
  if (json is int || json is double) {
    return Duration(milliseconds: parseInt(json, 0)!);
  }
  return Duration(
      days: parseInt(json["days"], 0)!,
      hours: parseInt(json["hours"], 0)!,
      minutes: parseInt(json["minutes"], 0)!,
      seconds: parseInt(json["seconds"], 0)!,
      milliseconds: parseInt(json["milliseconds"], 0)!,
      microseconds: parseInt(json["microseconds"], 0)!);
}

Duration? durationFromString(String? duration, [Duration? defaultValue]) {
  return duration != null
      ? durationFromJSON(json.decode(duration), defaultValue)
      : defaultValue;
}