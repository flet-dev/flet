import '../models/control.dart';
import 'numbers.dart';

Duration? parseDuration(Control control, String propName,
    [Duration? defaultValue]) {
  var v = control.get(propName);
  if (v == null) {
    return defaultValue;
  }
  return durationFromJSON(v);
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
