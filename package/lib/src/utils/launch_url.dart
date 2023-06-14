import 'package:collection/collection.dart';
import 'package:url_launcher/url_launcher.dart';

import 'platform_utils_non_web.dart'
    if (dart.library.js) "platform_utils_web.dart";

Future openWebBrowser(String url,
    {String? webWindowName,
    bool? webPopupWindow,
    int? windowWidth,
    int? windowHeight}) async {
  if (webPopupWindow == true) {
    openPopupBrowserWindow(
        url, webWindowName ?? "Flet", windowWidth ?? 1200, windowHeight ?? 800);
  } else {
    LaunchMode? mode = LaunchMode.values.firstWhereOrNull(
        (t) => t.name.toLowerCase() == (webWindowName ?? "").toLowerCase());
    await launchUrl(Uri.parse(url),
        webOnlyWindowName: mode == null ? webWindowName : null,
        mode: mode ?? LaunchMode.platformDefault);
  }
}
