import '../models/control.dart';
import '../utils/numbers.dart';

Map<String, double>? parseResponsiveNumber(dynamic value, double defaultDouble,
    [Map<String, double>? defaultValue]) {
  if (value == null) return defaultValue;

  if (value is! Map<String, dynamic>) {
    value = {"": value};
  }

  final result = value.map<String, double>(
    (key, val) => MapEntry(key, parseDouble(val, 0)!),
  );

  if (!result.containsKey("")) {
    result[""] = defaultDouble;
  }

  return result;
}

double getBreakpointNumber(
    Map<String, double> value, double width, Map<String, double> breakpoints) {
  // default value
  double? result = value[""];

  double maxBpWidth = 0;
  value.forEach((bpName, respValue) {
    if (bpName == "") {
      return;
    }
    var bpWidth = breakpoints[bpName];
    if (bpWidth == null) {
      throw Exception("Unknown breakpoint: $bpName");
    }
    if (width >= bpWidth && bpWidth >= maxBpWidth) {
      maxBpWidth = bpWidth;
      result = respValue;
    }
  });

  if (result == null) {
    throw Exception("Responsive number not found for width=$width: $value");
  }
  return result!;
}

extension ResponsiveParsers on Control {
  Map<String, double>? getResponsiveNumber(
      String propertyName, double defaultDouble,
      [Map<String, double>? defaultValue]) {
    return parseResponsiveNumber(
        get(propertyName), defaultDouble, defaultValue);
  }
}
