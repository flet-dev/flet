import '../models/control.dart';
import 'numbers.dart';

Duration? parseDuration(dynamic value, [Duration? defaultValue]) {
  if (value == null) return defaultValue;
  if (value is int || value is double) {
    return Duration(milliseconds: parseInt(value, 0)!);
  }
  return Duration(
      days: parseInt(value["days"], 0)!,
      hours: parseInt(value["hours"], 0)!,
      minutes: parseInt(value["minutes"], 0)!,
      seconds: parseInt(value["seconds"], 0)!,
      milliseconds: parseInt(value["milliseconds"], 0)!,
      microseconds: parseInt(value["microseconds"], 0)!);
}
extension DurationParsers on Control {
  Duration? getDuration(String propertyName, [Duration? defaultValue]) {
    return parseDuration(get(propertyName), defaultValue);
  }
}