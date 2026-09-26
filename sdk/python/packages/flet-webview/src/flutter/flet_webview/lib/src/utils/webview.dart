import 'package:flet/flet.dart';
import 'package:webview_all/webview_all.dart';

LoadRequestMethod? parseLoadRequestMethod(
  String? value, [
  LoadRequestMethod? defaultValue,
]) {
  return parseEnum(LoadRequestMethod.values, value, defaultValue);
}

JavaScriptMode? parseJavaScriptMode(
  String? value, [
  JavaScriptMode? defaultValue,
]) {
  return parseEnum(JavaScriptMode.values, value, defaultValue);
}
