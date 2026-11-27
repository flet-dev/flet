import 'package:flet/flet.dart';
import 'package:flutter/foundation.dart';
import 'package:webview_all/webview_all.dart';
import 'package:webview_platform_interface/webview_platform_interface.dart'
    show JavaScriptChannelParams;

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

final _channelCallbackHolder = JavaScriptChannelParams(
  name: "flet",
  onMessageReceived: (_) {},
);

/// Keeps `JavaScriptChannelParams.onMessageReceived` in AOT (release) builds.
///
/// On iOS and macOS, `webview_all` stores the handler behind
/// `setOnConsoleMessage` only in that field, and the native script message
/// handler reaches it through a weak reference. An app that never reads the
/// field lets the AOT compiler drop it as write-only, so the handler is
/// garbage collected and console messages stop arriving after the next
/// collection. Reading the field once keeps it.
void retainJavaScriptChannelCallbacks() {
  if (identityHashCode(_channelCallbackHolder.onMessageReceived) == 0) {
    debugPrint("JavaScriptChannelParams.onMessageReceived is retained.");
  }
}
