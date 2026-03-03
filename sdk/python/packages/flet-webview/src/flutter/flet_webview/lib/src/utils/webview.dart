import 'package:flet/flet.dart';
import 'package:webview_flutter/webview_flutter.dart';

LoadRequestMethod? parseLoadRequestMethod(String? value,
    [LoadRequestMethod? defaultValue]) {
  return parseEnum(LoadRequestMethod.values, value, defaultValue);
}

JavaScriptMode? parseJavaScriptMode(String? value,
    [JavaScriptMode? defaultValue]) {
  return parseEnum(JavaScriptMode.values, value, defaultValue);
}
