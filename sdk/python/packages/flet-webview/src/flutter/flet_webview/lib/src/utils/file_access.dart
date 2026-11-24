import 'package:webview_flutter/webview_flutter.dart';
import 'package:webview_flutter_android/webview_flutter_android.dart';

/// Grants the underlying webview permission to read `file://` URLs.
///
/// Only Android needs this: `WebSettings.allowFileAccess` defaults to `false`
/// when the app targets API 30 or above, so local pages fail to load with
/// `net::ERR_ACCESS_DENIED`. A no-op on every other platform, where the
/// webview already has access to the app's own container.
Future<void> allowFileAccess(WebViewController controller) async {
  final platformController = controller.platform;
  if (platformController is AndroidWebViewController) {
    await platformController.setAllowFileAccess(true);
  }
}
