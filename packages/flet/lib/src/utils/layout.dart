import '../models/control.dart';
import 'numbers.dart';

int? parseExpand(dynamic value, [int? defaultValue]) {
  return value == true
      ? 1
      : value == false
          ? 0
          : parseInt(value) ?? defaultValue;
}

extension LayoutParsers on Control {
  int? getExpand(String propertyName, [int? defaultValue]) {
    return parseExpand(get(propertyName), defaultValue);
  }
}
