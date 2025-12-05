import 'package:url_launcher/url_launcher.dart';

import '../models/control.dart';
import 'platform_utils_web.dart'
    if (dart.library.io) "platform_utils_non_web.dart";

/// A simple class representing a URL and an optional target.
///
/// The [url] is the full string representation of the link.
/// The [target] specifies how the link should be opened (e.g., "_blank" for a new tab).
class Url {
  /// The full URL to be opened.
  final String url;

  /// The optional target for opening the URL (e.g., "_blank", "_self").
  final String? target;

  /// Creates a [Url] object with a required [url] and an optional [target].
  Url(this.url, [this.target]);
}

/// Opens a web browser or popup window to a given [Url].
///
/// Example usage:
/// ```dart
/// final url = Url("https://example.com", "_blank");
/// await openWebBrowser(url);
/// ```
Future<void> openWebBrowser(
  Url urlObj, {
  LaunchMode mode = LaunchMode.platformDefault,
  WebViewConfiguration? webViewConfiguration,
  BrowserConfiguration? browserConfiguration,
  String? webOnlyWindowName,
}) async {
  // Open the URL in the default browser or app
  var target = urlObj.target ?? webOnlyWindowName;
  var resolvedMode = (target == "_blank" && mode == LaunchMode.platformDefault)
      ? LaunchMode.externalApplication
      : mode;
  await launchUrl(
    Uri.parse(urlObj.url),
    mode: resolvedMode,
    webViewConfiguration: webViewConfiguration ?? const WebViewConfiguration(),
    browserConfiguration:
        browserConfiguration ?? const BrowserConfiguration(),
    webOnlyWindowName: target,
  );
}

Future<void> openWindow(
  Url urlObj, {
  String? title,
  double? width,
  double? height,
}) async {
  openPopupBrowserWindow(urlObj.url, title ?? "Flet", (width ?? 1200).round(),
      (height ?? 800).round());
}

Url? parseUrl(dynamic value, [Url? defaultValue]) {
  if (value is String) {
    return Url(value);
  } else if (value is Map) {
    return Url(value["url"], value["target"]);
  } else {
    return defaultValue;
  }
}

extension UrlParsers on Control {
  Url? getUrl(String propertyName, [Url? defaultValue]) {
    return parseUrl(get(propertyName), defaultValue);
  }
}
