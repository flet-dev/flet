import '../utils/numbers.dart';

Map<String, double> parseResponsiveNumber(dynamic value, double defaultValue) {
  Map<String, double> result = {};
  if (value != null) {
    if (value is! Map<String, dynamic>) {
      value = {"": value};
    }
    result = value.map((key, value) => MapEntry(key, parseDouble(value, 0)!));
  }
  if (result[""] == null) {
    result[""] = defaultValue;
  }
  return result;
}

double getBreakpointNumber(Map<String, double> responsiveNumber, double width,
    Map<String, double> breakpoints) {
  // default value
  double? result = responsiveNumber[""];

  double maxBpWidth = 0;
  responsiveNumber.forEach((bpName, respValue) {
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
    throw Exception(
        "Responsive number not found for width=$width: $responsiveNumber");
  }
  return result!;
}
