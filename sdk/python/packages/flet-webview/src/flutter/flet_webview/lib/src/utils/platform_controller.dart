import 'package:webview_all/webview_all.dart';
import 'package:webview_all_android/webview_all_android.dart';
import 'package:webview_all_linux/webview_all_linux.dart';
import 'package:webview_all_windows/webview_all_windows.dart';

/// Creation params for the registered platform implementation.
///
/// WebKitGTK reads `allowFileAccessFromFileUrls` once, when a document's
/// security context is created, so it has to be set before the first load.
/// Without it a local page still resolves sibling images, stylesheets and
/// classic scripts, but `fetch`, XHR, ES modules, `@font-face` and
/// `localStorage` fail because its origin serialises as "null".
/// `allowUniversalAccessFromFileUrls` stays off: it would give local pages
/// access to every origin.
PlatformWebViewControllerCreationParams createPlatformCreationParams() {
  if (WebViewPlatform.instance is LinuxWebViewPlatform) {
    return const LinuxWebViewControllerCreationParams(
      allowFileAccessFromFileUrls: true,
      allowUniversalAccessFromFileUrls: false,
    );
  }
  return const PlatformWebViewControllerCreationParams();
}

/// Grants the underlying webview permission to read `file://` URLs.
///
/// Only Android needs this: `WebSettings.allowFileAccess` defaults to `false`
/// when the app targets API 30 or above, and `loadDataWithBaseURL` does not
/// enable it, so local sub-resources of HTML loaded with a `file://` base URL
/// fail with `net::ERR_ACCESS_DENIED`.
Future<void> allowFileAccess(WebViewController controller) async {
  final platform = controller.platform;
  if (platform is AndroidWebViewController) {
    await platform.setAllowFileAccess(true);
  }
}

/// Releases the native webview behind [controller].
///
/// Windows and Linux keep a WebView2 browser process set or a WebKitGTK web
/// process alive per controller until it is disposed, and `dispose()` is not
/// part of the app-facing `WebViewController`.
Future<void> disposePlatformController(WebViewController controller) async {
  final platform = controller.platform;
  if (platform is WindowsWebViewController) {
    await platform.dispose();
  } else if (platform is LinuxWebViewController) {
    await platform.dispose();
  }
}
