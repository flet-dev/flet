import '../models/control.dart';
import '../utils/numbers.dart';

Map<String, double>? parseResponsiveNumber(dynamic value, double defaultValue) {
  Map<String, double> result = {};

  if (value != null) {
    if (value is Map) {
      result = value.map<String, double>(
        (key, val) => MapEntry(key.toString(), parseDouble(val, 0)!),
      );
    } else {
      result[""] = value;
    }
  }

  if (result[""] == null) {
    result[""] = defaultValue;
  }

  return result;
}

double getBreakpointNumber(
    Map<String, double> value, double width, Map<String, double> breakpoints) {
  // Defaults
  double? selectedValue = value[""];
  double highestMatchedBreakpoint = 0;

  for (final entry in value.entries) {
    final bpName = entry.key;
    final v = entry.value;

    if (bpName.isEmpty) continue;

    final bpWidth = breakpoints[bpName];
    if (bpWidth == null) continue;

    if (width >= bpWidth && bpWidth >= highestMatchedBreakpoint) {
      highestMatchedBreakpoint = bpWidth;
      selectedValue = v;
    }
  }

  if (selectedValue == null) {
    throw Exception("Responsive number not found for width=$width: $value");
  }
  return selectedValue;
}

extension ResponsiveParsers on Control {
  Map<String, double>? getResponsiveNumber(
      String propertyName, double defaultValue) {
    return parseResponsiveNumber(get(propertyName), defaultValue);
  }
}
