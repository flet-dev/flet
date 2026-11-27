import 'package:flutter/foundation.dart';
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
///
/// On web, a URL [isOpenableWebUrl] rejects is not opened, and an [embedded]
/// app (one shown inside another with `FletApp`) can't replace the page it's
/// embedded in: a `_self`, `_parent` or `_top` target opens a new tab instead.
/// Returns whether the URL was opened.
Future<bool> openWebBrowser(
  Url urlObj, {
  LaunchMode mode = LaunchMode.platformDefault,
  WebViewConfiguration? webViewConfiguration,
  BrowserConfiguration? browserConfiguration,
  String? webOnlyWindowName,
  bool embedded = false,
}) async {
  if (!isOpenableWebUrl(urlObj.url)) {
    debugPrint("Not opening ${urlObj.url}: its scheme can't be opened on web.");
    return false;
  }
  var target = launchTarget(urlObj.target ?? webOnlyWindowName, embedded);
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
  return true;
}

/// Opens [urlObj] in a popup window of the given size (web).
///
/// [title] names the popup window, so a link or another `openWindow()` with
/// the same name reuses it. A name the browser reads as a target - `_self`,
/// `_parent`, `_top`, `_blank` - is used as a plain name, so the popup never
/// replaces the page. A URL [isOpenableWebUrl] rejects is not opened. Returns
/// whether the URL was opened.
Future<bool> openWindow(
  Url urlObj, {
  String? title,
  double? width,
  double? height,
}) async {
  if (!isOpenableWebUrl(urlObj.url)) {
    debugPrint("Not opening ${urlObj.url}: its scheme can't be opened on web.");
    return false;
  }
  openPopupBrowserWindow(urlObj.url, popupWindowName(title),
      (width ?? 1200).round(), (height ?? 800).round());
  return true;
}

const _pageTargets = {"_self", "_parent", "_top"};

/// The browser target for a URL opened by an app: on web, an [embedded] app's
/// `_self`, `_parent` or `_top` becomes `_blank`, so it can't replace the page
/// it's embedded in.
@visibleForTesting
String? launchTarget(String? target, bool embedded) {
  if (kIsWeb && embedded && _pageTargets.contains(target)) return "_blank";
  return target;
}

/// The window name `openWindow()` gives its popup: [title], or "Flet". A name
/// starting with `_` is a target keyword to the browser (`_self` would load
/// the URL in the page itself), so it gets a `flet` prefix.
@visibleForTesting
String popupWindowName(String? title) {
  var name = title ?? "Flet";
  return name.startsWith("_") ? "flet$name" : name;
}

/// URL schemes a Flet app doesn't open, or load in a `WebView`, on web: a
/// `javascript:` URL runs script in the page, and a `blob:` or `filesystem:`
/// URL the app made itself is a document with the page's own origin. (A
/// `data:` document gets an opaque origin, and browsers block top-level
/// `data:` navigation.)
const blockedWebUrlSchemes = {"javascript", "blob", "filesystem"};

/// The scheme of [url] in lower case, read the way a browser reads it: tabs
/// and newlines anywhere, and leading spaces and control characters, are
/// ignored (`" java\tscript:"` is a `javascript:` URL). `null` for a relative
/// URL, which has none.
String? webUrlScheme(String url) {
  var normalized = url
      .replaceAll(RegExp(r"[\t\n\r]"), "")
      .replaceFirst(RegExp(r"^[\x00-\x20]+"), "");
  var match = RegExp(r"^([a-zA-Z][a-zA-Z0-9+.\-]*):").firstMatch(normalized);
  return match?.group(1)!.toLowerCase();
}

/// Whether [url] may be opened on this platform: off the web, always; on the
/// web, unless its scheme is one of [blockedWebUrlSchemes].
bool isOpenableWebUrl(String url) {
  if (!kIsWeb) return true;
  return !blockedWebUrlSchemes.contains(webUrlScheme(url));
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
