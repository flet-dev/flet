import 'package:flet/flet.dart';
import 'package:webview_platform_interface/webview_platform_interface.dart';

/// Parse helpers bound to `webview_platform_interface`, the interface behind
/// the Windows and Linux implementations.
///
/// These deliberately duplicate the helpers in `utils/webview.dart`: the enums
/// there come from `webview_flutter_platform_interface` and are distinct Dart
/// types that happen to share these names, so the two libraries must never be
/// imported together.
LoadRequestMethod? parseDesktopLoadRequestMethod(String? value,
    [LoadRequestMethod? defaultValue]) {
  return parseEnum(LoadRequestMethod.values, value, defaultValue);
}

JavaScriptMode? parseDesktopJavaScriptMode(String? value,
    [JavaScriptMode? defaultValue]) {
  return parseEnum(JavaScriptMode.values, value, defaultValue);
}
