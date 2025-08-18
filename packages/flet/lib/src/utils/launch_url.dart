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
  bool webPopupWindow = false,
  String? webPopupWindowName,
  int? webPopupWindowWidth,
  int? webPopupWindowHeight,
}) async {
  if (webPopupWindow == true) {
    // Open a popup browser window (web only)
    openPopupBrowserWindow(
      urlObj.url,
      webPopupWindowName ?? "Flet",
      webPopupWindowWidth ?? 1200,
      webPopupWindowHeight ?? 800,
    );
  } else {
    // Open the URL in the default browser or app
    var target = urlObj.target ?? webPopupWindowName;
    await launchUrl(
      Uri.parse(urlObj.url),
      webOnlyWindowName: target,
      mode: (target == "_blank")
          ? LaunchMode.externalApplication
          : LaunchMode.platformDefault,
    );
  }
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
