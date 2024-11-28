import 'package:collection/collection.dart';
import 'package:webview_flutter/webview_flutter.dart';

LoadRequestMethod? parseLoadRequestMethod(String? value,
    [LoadRequestMethod? defValue]) {
  if (value == null) {
    return defValue;
  }
  return LoadRequestMethod.values.firstWhereOrNull(
          (e) => e.name.toLowerCase() == value.toLowerCase()) ??
      defValue;
}
